package sa.fakkerwakammel.fakker_wakammel.guard

import android.accessibilityservice.AccessibilityService
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.content.pm.PackageManager
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.os.PowerManager
import android.provider.Settings
import android.view.accessibility.AccessibilityEvent
import android.widget.Toast
import org.json.JSONObject
import sa.fakkerwakammel.fakker_wakammel.MainActivity

/**
 * The guard. Android delivers window changes and taps to this accessibility
 * service, so it knows which app is in front without reading any screen
 * content. Every active second it advances the [NativeScheduler]; when a break
 * is due it pauses media and brings the question screen to the front, and it
 * keeps bringing it back until the child answers.
 */
class GuardService : AccessibilityService() {

    companion object {
        @Volatile var instance: GuardService? = null

        private val SYSTEM_IGNORE = setOf("com.android.systemui", "android", "com.google.android.inputmethod.latin", "com.samsung.android.honeyboard")
        /** Always allowed, even during a break: calls and emergencies. */
        private val ALWAYS_ALLOWED = setOf(
            "com.android.dialer", "com.google.android.dialer", "com.samsung.android.dialer", "com.android.phone",
            "com.android.server.telecom", "com.samsung.android.incallui", "com.android.emergency", "com.google.android.apps.safetyhub",
        )
        private val SETTINGS = setOf(
            "com.android.settings", "com.samsung.android.settings", "com.google.android.packageinstaller",
            "com.android.packageinstaller", "com.samsung.android.packageinstaller", "com.google.android.permissioncontroller",
        )
    }

    private val handler = Handler(Looper.getMainLooper())
    private lateinit var cfg: GuardConfig
    private lateinit var store: NativeStore
    private lateinit var notifier: Notifier
    private var media: MediaWatcher? = null

    private var scheduler: NativeScheduler? = null
    private var schedulerKey = ""
    private var currentPkg = ""
    private var currentClass = ""
    private var homes: Set<String> = emptySet()
    private var unflushed = 0
    private var lastLaunch = 0L
    private var lastWarnShown = -1
    private val alertThrottle = mutableMapOf<String, Long>()

    private val ticker = object : Runnable {
        override fun run() {
            try { tick() } catch (_: Exception) { }
            handler.postDelayed(this, 1000)
        }
    }

    override fun onServiceConnected() {
        instance = this
        cfg = GuardConfig(this)
        store = NativeStore(this)
        notifier = Notifier(this, cfg, store)
        Notifier.ensureChannels(this)
        homes = packageManager.queryIntentActivities(Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_HOME), 0)
            .map { it.activityInfo.packageName }.toSet()
        media = MediaWatcher(this) { sig, pkg -> if (pkg == currentPkg) scheduler?.signal(sig) }.also { it.start() }
        if (store.lastReportAt == 0L) store.lastReportAt = System.currentTimeMillis()
        handler.post(ticker)
    }

    override fun onDestroy() {
        instance = null
        handler.removeCallbacks(ticker)
        media?.stop()
        super.onDestroy()
    }

    override fun onInterrupt() {}

    // ---------------------------------------------------------------- events

    override fun onAccessibilityEvent(e: AccessibilityEvent?) {
        val pkg = e?.packageName?.toString() ?: return
        when (e.eventType) {
            AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED -> onWindow(pkg, e.className?.toString() ?: "")
            AccessibilityEvent.TYPE_VIEW_CLICKED, AccessibilityEvent.TYPE_VIEW_LONG_CLICKED,
            AccessibilityEvent.TYPE_VIEW_SCROLLED -> if (pkg == currentPkg) scheduler?.signal(Signal.TOUCH)
        }
    }

    private fun onWindow(pkg: String, cls: String) {
        if (pkg in SYSTEM_IGNORE || isKeyboard(pkg)) return
        if (pkg != currentPkg) {
            val wasContent = isContent(currentPkg)
            flushUsage()
            currentPkg = pkg
            currentClass = cls
            scheduler?.kind = kindOf(pkg)
            if (wasContent && isContent(pkg)) scheduler?.signal(Signal.APP_SWITCH)
        } else if (cls != currentClass) {
            // A new screen inside a game (menu, level end, loading) is a natural pause point.
            if (scheduler?.kind == ContentKind.GAME && !cls.startsWith("android.widget")) scheduler?.signal(Signal.MENU_SCREEN)
            currentClass = cls
        }
        enforce(System.currentTimeMillis(), fromWindow = true)
        checkDue()
    }

    // ------------------------------------------------------------------ tick

    private fun tick() {
        val now = System.currentTimeMillis()
        val childId = cfg.activeChildId(now)
        if (childId == null || !cfg.hasAccess(now)) {
            scheduler = null
            return
        }
        if (cfg.handoffExpired(now)) {
            if (store.pendingRoute != "handoff_over") {
                flushUsage()
                store.pendingRoute = "handoff_over"
                notifier.handoffEnded(childId)
                launch("handoff_over")
            }
            enforce(now)
            return
        }
        val screenOn = (getSystemService(POWER_SERVICE) as PowerManager).isInteractive
        if (!screenOn) return
        ensureScheduler(childId)
        if (store.pendingRoute != null) {
            enforce(now)
            return
        }
        if (isContent(currentPkg)) {
            val s = scheduler ?: return
            media?.checkNearEnd(currentPkg)
            s.tick()
            unflushed++
            if (unflushed >= 15) flushUsage()
            store.elapsed = s.elapsed

            val limit = cfg.dailyLimitMinutes
            if (limit > 0 && store.todaySeconds(childId) + unflushed >= (limit + cfg.limitBonusToday) * cfg.unit) {
                flushUsage()
                store.pendingRoute = "limit"
                val day = java.time.LocalDate.now().toString()
                if (store.limitAlertDay != day) {
                    store.limitAlertDay = day
                    notifier.dailyLimit(childId)
                }
                media?.pauseAll()
                launch("limit")
                return
            }
            if (s.phase == Phase.WARNING && s.warnRemaining == s.warnSeconds && lastWarnShown != s.elapsed) {
                lastWarnShown = s.elapsed
                warnChild(s.warnSeconds)
            }
            checkDue()
        }
        maybeReport(childId, now)
    }

    private fun checkDue() {
        val s = scheduler ?: return
        if (s.phase != Phase.DUE || store.pendingRoute != null) return
        val childId = cfg.activeChildId(System.currentTimeMillis()) ?: return
        flushUsage()
        store.pendingRoute = "quiz"
        store.escapeCount = 0
        store.setFlutterPendingBreak(childId)
        store.pushEvent(
            JSONObject().put("t", "break").put("c", childId).put("r", (s.reason ?: BreakReason.FIXED_TIME).dartName).put("w", s.elapsed)
        )
        media?.pauseAll()
        launch("quiz")
    }

    private fun ensureScheduler(childId: String) {
        val key = "$childId|${cfg.breakMode}|${cfg.intervalMinutes}|${cfg.graceMinutes}|${cfg.unit}|${cfg.childAge(childId)}"
        if (key == schedulerKey && scheduler != null) return
        schedulerKey = key
        scheduler = NativeScheduler.fromConfig(cfg.breakMode, cfg.intervalMinutes, cfg.graceMinutes, cfg.childAge(childId), cfg.unit, kindOf(currentPkg))
            .also { it.restore(store.elapsed) }
    }

    /** Called by the app after the questions are solved. */
    fun resetAfterBreak() {
        scheduler?.reset()
        store.elapsed = 0
    }

    /** Live state for the parent's "Protection status" panel. */
    fun diag(): Map<String, Any?> {
        val now = System.currentTimeMillis()
        val child = cfg.activeChildId(now)
        val s = scheduler
        return mapOf(
            "running" to true,
            "mode" to cfg.deviceMode,
            "child" to child,
            "childName" to cfg.childName(child),
            "hasAccess" to cfg.hasAccess(now),
            "currentApp" to if (currentPkg.isEmpty()) "" else label(currentPkg),
            "counting" to (child != null && isContent(currentPkg)),
            "elapsed" to (s?.elapsed ?: store.elapsed),
            "target" to (s?.targetSeconds ?: 0),
            "limit" to (s?.hardLimit ?: 0),
            "phase" to (s?.phase?.name ?: "-"),
            "pending" to store.pendingRoute,
            "unit" to cfg.unit,
            "kind" to (s?.kind?.name ?: "-"),
        )
    }

    /** "Test now": the next break comes ~6 s after the child is in a video or game. */
    fun testSoon() {
        val child = cfg.activeChildId(System.currentTimeMillis()) ?: return
        ensureScheduler(child)
        val s = scheduler ?: return
        s.reset()
        s.restore((s.hardLimit - s.warnSeconds - 1).coerceAtLeast(0))
        store.elapsed = s.elapsed
    }

    fun reloadConfig() {
        schedulerKey = ""
    }

    // ------------------------------------------------------------ enforcement

    /** [fromWindow] = the child actively switched app (counts as an escape attempt). */
    private fun enforce(now: Long, fromWindow: Boolean = false) {
        val childId = cfg.activeChildId(now) ?: return
        val route = store.pendingRoute
        val pkg = currentPkg
        if (pkg.isEmpty() || pkg == packageName || pkg in ALWAYS_ALLOWED) return

        if (route != null) {
            // A break / lock is open: anything else goes straight back to it.
            if (now - lastLaunch < 900) return
            if (route == "quiz" && fromWindow) {
                store.escapeCount = store.escapeCount + 1
                if (store.escapeCount == 3) notifier.escapeAttempts(childId, 3)
            }
            launch(route)
            return
        }
        // Settings / uninstall protection.
        if (cfg.protectSettings && pkg in SETTINGS && now > store.settingsPassUntil) {
            if (throttle("settings", 60_000)) notifier.settingsAttempt(childId)
            launch("pin_guard")
            return
        }
        // Parent's private apps during a hand-off session.
        if (cfg.deviceMode == "parent" && isContent(pkg) && pkg !in cfg.allowedApps) {
            if (throttle("blocked:$pkg", 120_000)) notifier.blockedApp(childId, label(pkg))
            launch("blocked", label(pkg))
        }
    }

    private fun launch(route: String, extra: String? = null) {
        lastLaunch = System.currentTimeMillis()
        val i = Intent(this, MainActivity::class.java)
            .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_REORDER_TO_FRONT or Intent.FLAG_ACTIVITY_SINGLE_TOP)
            .putExtra("fw_route", route)
        if (extra != null) i.putExtra("fw_extra", extra)
        try { startActivity(i) } catch (_: Exception) { }
    }

    private fun warnChild(seconds: Int) {
        val ar = cfg.uiLanguage != "en"
        val msg = if (ar) "⏳ سيتوقف بعد $seconds ثوانٍ لسؤال سريع — احفظ لعبتك 💾" else "⏳ Pausing in $seconds s for a quick question — save your game 💾"
        Toast.makeText(this, msg, Toast.LENGTH_LONG).show()
    }

    private fun maybeReport(childId: String, now: Long) {
        val every = cfg.reportEveryMinutes.toLong() * cfg.unit * 1000
        if (every <= 0 || now - store.lastReportAt < every) return
        flushUsage()
        notifier.periodicReport(childId, store.takeReportWindow(), ::label)
        store.lastReportAt = now
    }

    private fun throttle(key: String, ms: Long): Boolean {
        val now = System.currentTimeMillis()
        if (now - (alertThrottle[key] ?: 0) < ms) return false
        alertThrottle[key] = now
        return true
    }

    // ------------------------------------------------------------- helpers

    private fun flushUsage() {
        if (unflushed <= 0) return
        val childId = cfg.activeChildId(System.currentTimeMillis())
        if (childId != null && isContent(currentPkg)) {
            store.addUsage(childId, currentPkg, unflushed)
            store.pushEvent(JSONObject().put("t", "usage").put("c", childId).put("app", label(currentPkg)).put("pkg", currentPkg).put("s", unflushed))
        }
        unflushed = 0
    }

    fun isContent(pkg: String): Boolean =
        pkg.isNotEmpty() && pkg != packageName && pkg !in homes && pkg !in SYSTEM_IGNORE && pkg !in ALWAYS_ALLOWED &&
            pkg !in SETTINGS && pkg !in cfg.exemptApps && !isKeyboard(pkg)

    private fun isKeyboard(pkg: String): Boolean {
        val ime = Settings.Secure.getString(contentResolver, Settings.Secure.DEFAULT_INPUT_METHOD) ?: return false
        return ime.startsWith("$pkg/")
    }

    private fun kindOf(pkg: String): ContentKind = try {
        val ai = packageManager.getApplicationInfo(pkg, 0)
        @Suppress("DEPRECATION")
        val game = (Build.VERSION.SDK_INT >= 26 && ai.category == ApplicationInfo.CATEGORY_GAME) || (ai.flags and ApplicationInfo.FLAG_IS_GAME) != 0
        if (game) ContentKind.GAME else ContentKind.VIDEO
    } catch (_: PackageManager.NameNotFoundException) { ContentKind.VIDEO }

    fun label(pkg: String): String = try {
        packageManager.getApplicationLabel(packageManager.getApplicationInfo(pkg, 0)).toString()
    } catch (_: Exception) { pkg }
}

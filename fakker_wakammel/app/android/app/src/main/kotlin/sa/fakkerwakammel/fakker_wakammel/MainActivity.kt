package sa.fakkerwakammel.fakker_wakammel

import android.Manifest
import android.app.admin.DevicePolicyManager
import android.content.ComponentName
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationManagerCompat
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import sa.fakkerwakammel.fakker_wakammel.guard.AdminReceiver
import sa.fakkerwakammel.fakker_wakammel.guard.GuardConfig
import sa.fakkerwakammel.fakker_wakammel.guard.GuardService
import sa.fakkerwakammel.fakker_wakammel.guard.MediaListener
import sa.fakkerwakammel.fakker_wakammel.guard.NativeStore
import sa.fakkerwakammel.fakker_wakammel.guard.Notifier

/**
 * Hosts the Flutter UI and exposes the guard to Dart over the "fw/native"
 * channel. The guard opens this activity with an `fw_route` extra
 * (quiz / limit / handoff_over / pin_guard / blocked / parent).
 */
class MainActivity : FlutterActivity() {
    private var channel: MethodChannel? = null
    private var launchRoute: String? = null
    private var launchExtra: String? = null

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        readRoute(intent)
        val store = NativeStore(this)
        channel = MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "fw/native").apply {
            setMethodCallHandler { call, result ->
                when (call.method) {
                    "status" -> result.success(status())
                    "takeLaunchRoute" -> {
                        // An explicit route from the guard wins; otherwise an unresolved lock.
                        val r = launchRoute ?: store.pendingRoute
                        result.success(mapOf("route" to r, "extra" to launchExtra))
                        launchRoute = null
                        launchExtra = null
                    }
                    "openAccessibility" -> { open(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)); result.success(null) }
                    "openOverlay" -> {
                        open(Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:$packageName"))); result.success(null)
                    }
                    "openNotificationAccess" -> { open(Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS)); result.success(null) }
                    "requestNotifications" -> {
                        if (Build.VERSION.SDK_INT >= 33) {
                            ActivityCompat.requestPermissions(this@MainActivity, arrayOf(Manifest.permission.POST_NOTIFICATIONS), 7)
                        }
                        result.success(null)
                    }
                    "requestAdmin" -> {
                        val ar = GuardConfig(this@MainActivity).uiLanguage != "en"
                        open(
                            Intent(DevicePolicyManager.ACTION_ADD_DEVICE_ADMIN)
                                .putExtra(DevicePolicyManager.EXTRA_DEVICE_ADMIN, ComponentName(this@MainActivity, AdminReceiver::class.java))
                                .putExtra(
                                    DevicePolicyManager.EXTRA_ADD_EXPLANATION,
                                    if (ar) "يمنع حذف التطبيق دون علم ولي الأمر." else "Prevents the app being removed without a parent.",
                                )
                        )
                        result.success(null)
                    }
                    "listApps" -> result.success(listApps())
                    "configChanged" -> { GuardService.instance?.reloadConfig(); result.success(null) }
                    "breakDone" -> {
                        store.pendingRoute = null
                        store.escapeCount = 0
                        store.setFlutterPendingBreak(null)
                        GuardService.instance?.resetAfterBreak()
                        moveTaskToBack(true)
                        result.success(null)
                    }
                    "clearRoute" -> {
                        // Parent entered the PIN (hand-off over / limit / settings) or the child left a blocked app.
                        val route = call.argument<String>("route")
                        if (route == "pin_guard") store.settingsPassUntil = System.currentTimeMillis() + 3 * 60_000
                        if (store.pendingRoute == route) store.pendingRoute = null
                        if (call.argument<Boolean>("toBack") == true) moveTaskToBack(true)
                        result.success(null)
                    }
                    "takeEvents" -> result.success(store.takeEvents())
                    "notify" -> {
                        Notifier(this@MainActivity, GuardConfig(this@MainActivity), store).custom(
                            call.argument<String>("kind") ?: "info",
                            call.argument<String>("title") ?: "",
                            call.argument<String>("body") ?: "",
                            call.argument<String>("childId"),
                            call.argument<Boolean>("important") ?: false,
                        )
                        result.success(null)
                    }
                    "moveToBack" -> { moveTaskToBack(true); result.success(null) }
                    "goHome" -> {
                        startActivity(Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_HOME).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
                        result.success(null)
                    }
                    "openApp" -> {
                        val pkg = call.argument<String>("pkg")
                        val i = pkg?.let { packageManager.getLaunchIntentForPackage(it) }
                        if (i != null) startActivity(i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
                        result.success(i != null)
                    }
                    else -> result.notImplemented()
                }
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        val route = intent.getStringExtra("fw_route") ?: return
        channel?.invokeMethod("route", mapOf("route" to route, "extra" to intent.getStringExtra("fw_extra")))
    }

    private fun readRoute(i: Intent?) {
        launchRoute = i?.getStringExtra("fw_route")
        launchExtra = i?.getStringExtra("fw_extra")
    }

    private fun open(i: Intent) {
        try { startActivity(i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)) } catch (_: Exception) {
            startActivity(Intent(Settings.ACTION_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
        }
    }

    private fun status(): Map<String, Any> {
        val listeners = Settings.Secure.getString(contentResolver, "enabled_notification_listeners") ?: ""
        val enabledServices = Settings.Secure.getString(contentResolver, Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES) ?: ""
        val dpm = getSystemService(DEVICE_POLICY_SERVICE) as DevicePolicyManager
        return mapOf(
            "accessibility" to (GuardService.instance != null || enabledServices.contains("$packageName/")),
            "overlay" to Settings.canDrawOverlays(this),
            "notifications" to NotificationManagerCompat.from(this).areNotificationsEnabled(),
            "mediaAccess" to listeners.contains(ComponentName(this, MediaListener::class.java).flattenToString()),
            "admin" to dpm.isAdminActive(ComponentName(this, AdminReceiver::class.java)),
            "sdk" to Build.VERSION.SDK_INT,
            "manufacturer" to Build.MANUFACTURER,
        )
    }

    private fun listApps(): List<Map<String, Any>> {
        val pm = packageManager
        val launcher = Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
        return pm.queryIntentActivities(launcher, 0)
            .map { it.activityInfo.applicationInfo }
            .distinctBy { it.packageName }
            .filter { it.packageName != packageName }
            .map {
                @Suppress("DEPRECATION")
                val game = (Build.VERSION.SDK_INT >= 26 && it.category == android.content.pm.ApplicationInfo.CATEGORY_GAME) ||
                    (it.flags and android.content.pm.ApplicationInfo.FLAG_IS_GAME) != 0
                mapOf("pkg" to it.packageName, "label" to pm.getApplicationLabel(it).toString(), "game" to game)
            }
            .sortedBy { it["label"] as String }
    }
}

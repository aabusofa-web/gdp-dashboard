package sa.fakkerwakammel.fakker_wakammel.guard

import android.content.Context
import android.content.SharedPreferences
import org.json.JSONArray
import org.json.JSONObject
import java.time.LocalDate
import java.time.ZonedDateTime

/**
 * Read-only view of what the Flutter app saved (shared_preferences stores
 * everything in "FlutterSharedPreferences" with a "flutter." prefix; our values
 * are JSON strings). Native-only runtime state lives in [NativeStore].
 */
class GuardConfig(private val prefs: SharedPreferences) {

    constructor(ctx: Context) : this(ctx.getSharedPreferences("FlutterSharedPreferences", Context.MODE_PRIVATE))

    private fun obj(key: String): JSONObject? = try {
        prefs.getString("flutter.$key", null)?.let { JSONObject(it) }
    } catch (_: Exception) { null }

    private fun arr(key: String): JSONArray? = try {
        prefs.getString("flutter.$key", null)?.let { JSONArray(it) }
    } catch (_: Exception) { null }

    private val settings get() = obj("settings") ?: JSONObject()
    private val device get() = obj("device") ?: JSONObject()
    private val sub get() = obj("subscription") ?: JSONObject()

    /** child = the child's own device (always guarded) · parent = only during a hand-off session · off */
    val deviceMode: String get() = device.optString("mode", "off")
    val deviceChildId: String? get() = device.optString("childId", "").ifEmpty { null }
    val protectSettings: Boolean get() = device.optBoolean("protectSettings", true)
    val allowedApps: Set<String> get() = device.optJSONArray("allowedApps").toSet()
    val exemptApps: Set<String> get() = device.optJSONArray("exemptApps").toSet()

    val handoff: JSONObject? get() = obj("handoff")
    val handoffChildId: String? get() = handoff?.optString("childId", "")?.ifEmpty { null }
    /** Epoch ms when the hand-off session ends; 0 = no limit. */
    val handoffUntil: Long get() = handoff?.optLong("until", 0L) ?: 0L

    fun handoffActive(now: Long): Boolean = deviceMode == "parent" && handoffChildId != null

    fun handoffExpired(now: Long): Boolean = handoffActive(now) && handoffUntil > 0 && now >= handoffUntil

    /** The child currently using this device, or null when nothing should be guarded. */
    fun activeChildId(now: Long): String? = when (deviceMode) {
        "child" -> deviceChildId
        "parent" -> handoffChildId
        else -> null
    }

    fun childName(id: String?): String = child(id)?.optString("name", "") ?: ""
    fun childIsFemale(id: String?): Boolean = child(id)?.optString("gender") == "female"

    fun childAge(id: String?): Int {
        val bd = child(id)?.optString("birthDate") ?: return 8
        return try {
            val b = LocalDate.parse(bd.substring(0, 10))
            val n = LocalDate.now()
            var age = n.year - b.year
            if (n.monthValue < b.monthValue || (n.monthValue == b.monthValue && n.dayOfMonth < b.dayOfMonth)) age--
            age.coerceIn(0, 99)
        } catch (_: Exception) { 8 }
    }

    private fun child(id: String?): JSONObject? {
        if (id == null) return null
        val list = arr("children") ?: return null
        for (i in 0 until list.length()) {
            val c = list.optJSONObject(i) ?: continue
            if (c.optString("id") == id) return c
        }
        return null
    }

    val breakMode: BreakMode get() = when (settings.optString("breakMode", "smart")) {
        "fixed" -> BreakMode.FIXED
        "auto" -> BreakMode.AUTO
        else -> BreakMode.SMART
    }
    val intervalMinutes: Int get() = settings.optInt("intervalMinutes", 15)
    val graceMinutes: Int get() = settings.optInt("graceMinutes", 3)
    val dailyLimitMinutes: Int get() = settings.optInt("dailyLimitMinutes", 0)
    val uiLanguage: String get() = settings.optString("uiLanguage", "ar")

    // Parent notifications
    val reportEveryMinutes: Int get() = settings.optInt("reportEveryMinutes", 60)
    val quietStart: Int get() = settings.optInt("quietStart", 23)
    val quietEnd: Int get() = settings.optInt("quietEnd", 7)
    fun alertEnabled(kind: String): Boolean {
        val off = settings.optJSONArray("alertsOff").toSet()
        return kind !in off
    }

    /** Fast demo mode counts seconds instead of minutes (for trying the app). */
    val unit: Int get() = if (sub.optBoolean("demoSpeed", false)) 1 else 60

    /** Trial or paid subscription still valid. */
    fun hasAccess(now: Long): Boolean {
        if (sub.optBoolean("subscribed", false)) return true
        val start = sub.optString("trialStart", "")
        if (start.isEmpty()) return true
        return try {
            val startMs = java.time.LocalDateTime.parse(start.substring(0, 19))
                .atZone(ZonedDateTime.now().zone).toInstant().toEpochMilli()
            now < startMs + 3L * 24 * 3600 * 1000
        } catch (_: Exception) { true }
    }

    /** Extra minutes a parent granted today from the limit screen. */
    val limitBonusToday: Int get() {
        val b = obj("limit_bonus") ?: return 0
        return if (b.optString("day") == java.time.LocalDate.now().toString()) b.optInt("minutes", 0) else 0
    }

    val parentPin: String get() = settings.optString("parentPin", "1234")

    /** Attempts since [sinceMs] for the child: (answered, firstTry). */
    fun attemptStats(childId: String, sinceMs: Long): Pair<Int, Int> {
        val list = arr("attempts") ?: return 0 to 0
        var answered = 0
        var first = 0
        for (i in list.length() - 1 downTo 0) {
            val a = list.optJSONObject(i) ?: continue
            if (a.optString("c") != childId) continue
            val at = try {
                java.time.LocalDateTime.parse(a.optString("at").substring(0, 19)).atZone(ZonedDateTime.now().zone).toInstant().toEpochMilli()
            } catch (_: Exception) { continue }
            if (at < sinceMs) break
            answered++
            if (a.optBoolean("s") && a.optInt("a") <= 1) first++
        }
        return answered to first
    }

    companion object {
        fun JSONArray?.toSet(): Set<String> {
            if (this == null) return emptySet()
            return (0 until length()).mapNotNull { optString(it, null) }.toSet()
        }
    }
}

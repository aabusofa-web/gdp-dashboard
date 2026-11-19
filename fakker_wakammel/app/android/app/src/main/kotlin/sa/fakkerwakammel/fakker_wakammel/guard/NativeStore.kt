package sa.fakkerwakammel.fakker_wakammel.guard

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.time.LocalDate
import java.time.LocalDateTime

/**
 * Native runtime state (survives process death) and the queue of events the
 * Flutter app merges into its analytics the next time it opens.
 */
class NativeStore(ctx: Context) {
    private val p = ctx.getSharedPreferences("fw_native", Context.MODE_PRIVATE)
    private val flutter = ctx.getSharedPreferences("FlutterSharedPreferences", Context.MODE_PRIVATE)

    /** Active seconds since the last break (restored after a reboot / service restart). */
    var elapsed: Int
        get() = p.getInt("elapsed", 0)
        set(v) = p.edit().putInt("elapsed", v).apply()

    /** What the lock screen must show: quiz | handoff_over | limit | pin_guard | blocked — or null. */
    var pendingRoute: String?
        get() = p.getString("pendingRoute", null)
        set(v) = p.edit().putString("pendingRoute", v).apply()

    var escapeCount: Int
        get() = p.getInt("escapes", 0)
        set(v) = p.edit().putInt("escapes", v).apply()

    var settingsPassUntil: Long
        get() = p.getLong("settingsPass", 0)
        set(v) = p.edit().putLong("settingsPass", v).apply()

    var lastReportAt: Long
        get() = p.getLong("lastReport", 0)
        set(v) = p.edit().putLong("lastReport", v).apply()

    var limitAlertDay: String
        get() = p.getString("limitAlertDay", "") ?: ""
        set(v) = p.edit().putString("limitAlertDay", v).apply()

    /** The quiz must survive the app being killed: Flutter reads this key on start. */
    fun setFlutterPendingBreak(childId: String?) {
        val e = flutter.edit()
        if (childId == null) e.remove("flutter.pending_break") else e.putString("flutter.pending_break", childId)
        e.apply()
    }

    // ----- usage today / since last report -----
    private fun today() = LocalDate.now().toString()

    fun todaySeconds(childId: String): Int =
        if (p.getString("day", "") == today()) p.getInt("today_$childId", 0) else 0

    fun addUsage(childId: String, pkg: String, seconds: Int) {
        val e = p.edit()
        if (p.getString("day", "") != today()) {
            p.all.keys.filter { it.startsWith("today_") }.forEach { e.remove(it) }
            e.putString("day", today())
        }
        e.putInt("today_$childId", todaySeconds(childId) + seconds)
        val window = JSONObject(p.getString("window", "{}") ?: "{}")
        window.put(pkg, window.optInt(pkg, 0) + seconds)
        e.putString("window", window.toString())
        e.apply()
    }

    /** Usage per package since the last parent report; clears it. */
    fun takeReportWindow(): Map<String, Int> {
        val w = JSONObject(p.getString("window", "{}") ?: "{}")
        p.edit().putString("window", "{}").apply()
        return w.keys().asSequence().associateWith { w.optInt(it) }
    }

    // ----- event queue for Flutter -----
    @Synchronized
    fun pushEvent(e: JSONObject) {
        val arr = JSONArray(p.getString("events", "[]") ?: "[]")
        e.put("at", LocalDateTime.now().toString())
        arr.put(e)
        // Keep the queue bounded if the app is not opened for a long time.
        val trimmed = if (arr.length() > 2000) JSONArray((arr.length() - 2000 until arr.length()).map { arr.get(it) }) else arr
        p.edit().putString("events", trimmed.toString()).apply()
    }

    @Synchronized
    fun takeEvents(): String {
        val s = p.getString("events", "[]") ?: "[]"
        p.edit().putString("events", "[]").apply()
        return s
    }
}

package sa.fakkerwakammel.fakker_wakammel.guard

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import org.json.JSONObject
import sa.fakkerwakammel.fakker_wakammel.MainActivity
import sa.fakkerwakammel.fakker_wakammel.R
import java.time.LocalTime

/**
 * Parent notifications: periodic reports and instant alerts. Shown on this
 * device and queued as events so the Flutter side can relay them to the
 * parents' phones (Firebase) when family linking is set up.
 */
class Notifier(private val ctx: Context, private val cfg: GuardConfig, private val store: NativeStore) {

    companion object {
        const val CH_REPORTS = "fw_reports"
        const val CH_ALERTS = "fw_alerts"
        private var nextId = 2000

        fun ensureChannels(ctx: Context) {
            if (Build.VERSION.SDK_INT < 26) return
            val nm = ctx.getSystemService(NotificationManager::class.java)
            val ar = GuardConfig(ctx).uiLanguage != "en"
            nm.createNotificationChannel(
                NotificationChannel(CH_REPORTS, if (ar) "تقارير دورية للأبوين" else "Parent reports", NotificationManager.IMPORTANCE_DEFAULT)
            )
            nm.createNotificationChannel(
                NotificationChannel(CH_ALERTS, if (ar) "تنبيهات مهمة" else "Important alerts", NotificationManager.IMPORTANCE_HIGH)
            )
        }
    }

    private val ar get() = cfg.uiLanguage != "en"

    private fun quiet(): Boolean {
        val h = LocalTime.now().hour
        val s = cfg.quietStart
        val e = cfg.quietEnd
        if (s == e) return false
        return if (s < e) h in s until e else (h >= s || h < e)
    }

    private fun post(channel: String, title: String, body: String, kind: String, childId: String?) {
        if (!cfg.alertEnabled(kind)) return
        // Queued so the app can relay it to the parents' phones when family linking is on.
        store.pushEvent(JSONObject().put("t", "alert").put("k", kind).put("c", childId ?: "").put("title", title).put("body", body))
        if (channel == CH_REPORTS && quiet()) return
        if (Build.VERSION.SDK_INT >= 33 &&
            ctx.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
        ) return
        ensureChannels(ctx)
        val open = PendingIntent.getActivity(
            ctx, 0,
            Intent(ctx, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK).putExtra("fw_route", "parent"),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
        )
        val n = NotificationCompat.Builder(ctx, channel)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentTitle(title)
            .setContentText(body)
            .setStyle(NotificationCompat.BigTextStyle().bigText(body))
            .setContentIntent(open)
            .setAutoCancel(true)
            .setPriority(if (channel == CH_ALERTS) NotificationCompat.PRIORITY_HIGH else NotificationCompat.PRIORITY_DEFAULT)
            .build()
        try {
            NotificationManagerCompat.from(ctx).notify(nextId++, n)
        } catch (_: SecurityException) {
        }
    }

    private fun minutes(sec: Int): String {
        val m = sec / 60
        val h = m / 60
        val r = m % 60
        return if (ar) {
            if (h > 0) "$h س ${r} د" else "$m د"
        } else {
            if (h > 0) "${h}h ${r}m" else "${m}m"
        }
    }

    /** Periodic report: what the child watched/played and how they answered since the last report. */
    fun periodicReport(childId: String, usage: Map<String, Int>, appLabel: (String) -> String) {
        val name = cfg.childName(childId)
        val total = usage.values.sum()
        if (total < 60) return
        val top = usage.entries.sortedByDescending { it.value }.take(3)
            .joinToString(if (ar) "، " else ", ") { "${appLabel(it.key)} ${minutes(it.value)}" }
        val (answered, first) = cfg.attemptStats(childId, store.lastReportAt)
        val title = if (ar) "📊 تقرير $name" else "📊 $name's report"
        val body = if (ar) {
            "استخدم الجهاز ${minutes(total)} ($top) • أجاب $answered سؤال، منها $first من أول محاولة"
        } else {
            "Used the device ${minutes(total)} ($top) • answered $answered questions, $first first try"
        }
        post(CH_REPORTS, title, body, "report", childId)
    }

    fun escapeAttempts(childId: String, count: Int) {
        val name = cfg.childName(childId)
        post(
            CH_ALERTS,
            if (ar) "⚠️ محاولة تجاوز السؤال" else "⚠️ Tried to skip the question",
            if (ar) "$name حاول إغلاق شاشة السؤال $count مرات" else "$name tried to close the question screen $count times",
            "escape", childId,
        )
    }

    fun settingsAttempt(childId: String) {
        val name = cfg.childName(childId)
        post(
            CH_ALERTS,
            if (ar) "🛡️ محاولة دخول الإعدادات" else "🛡️ Settings access attempt",
            if (ar) "$name حاول فتح الإعدادات أو إيقاف الحماية" else "$name tried to open Settings or disable protection",
            "settings", childId,
        )
    }

    fun dailyLimit(childId: String) {
        val name = cfg.childName(childId)
        post(
            CH_ALERTS,
            if (ar) "🌙 انتهى وقت اليوم" else "🌙 Daily limit reached",
            if (ar) "انتهى وقت الشاشة المسموح لـ $name اليوم" else "$name has used today's screen time",
            "limit", childId,
        )
    }

    fun handoffEnded(childId: String) {
        val name = cfg.childName(childId)
        post(
            CH_ALERTS,
            if (ar) "⏰ انتهت جلسة $name" else "⏰ $name's session ended",
            if (ar) "انتهت مدة الجلسة. الجهاز مقفل حتى تُدخل رمزك السري." else "The session time is over. The device is locked until you enter your PIN.",
            "handoff", childId,
        )
    }

    fun blockedApp(childId: String, label: String) {
        val name = cfg.childName(childId)
        post(
            CH_ALERTS,
            if (ar) "🔒 تطبيق خاص" else "🔒 Private app",
            if (ar) "$name حاول فتح «$label» أثناء الجلسة" else "$name tried to open “$label” during the session",
            "blocked", childId,
        )
    }

    /** Free-form alert raised from Flutter (repeated mistakes, rushed answers, level up…). */
    fun custom(kind: String, title: String, body: String, childId: String?, important: Boolean) =
        post(if (important) CH_ALERTS else CH_REPORTS, title, body, kind, childId)
}

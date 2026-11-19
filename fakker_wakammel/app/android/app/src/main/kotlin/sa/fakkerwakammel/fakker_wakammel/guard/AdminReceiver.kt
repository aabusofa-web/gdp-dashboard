package sa.fakkerwakammel.fakker_wakammel.guard

import android.app.admin.DeviceAdminReceiver
import android.content.Context
import android.content.Intent

/**
 * Device admin: while active, Android won't uninstall the app until a parent
 * deactivates it — and the guard sends the child to the PIN screen whenever
 * Settings is opened, so only a parent can get there.
 */
class AdminReceiver : DeviceAdminReceiver() {
    override fun onDisableRequested(context: Context, intent: Intent): CharSequence {
        val ar = GuardConfig(context).uiLanguage != "en"
        return if (ar) "سيتم إيقاف حماية «فكّر وكمّل» وإبلاغ ولي الأمر." else "Fakker Wakammel protection will be turned off and the parent notified."
    }

    override fun onDisabled(context: Context, intent: Intent) {
        val cfg = GuardConfig(context)
        val store = NativeStore(context)
        val child = cfg.activeChildId(System.currentTimeMillis())
        val ar = cfg.uiLanguage != "en"
        Notifier(context, cfg, store).custom(
            "settings",
            if (ar) "🛡️ تم إيقاف حماية الحذف" else "🛡️ Uninstall protection turned off",
            if (ar) "تم تعطيل صلاحية مدير الجهاز لتطبيق فكّر وكمّل." else "Device-admin protection for Fakker Wakammel was disabled.",
            child, true,
        )
    }
}

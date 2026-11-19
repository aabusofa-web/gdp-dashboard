package sa.fakkerwakammel.fakker_wakammel.guard

import android.content.ComponentName
import android.content.Context
import android.media.AudioAttributes
import android.media.AudioFocusRequest
import android.media.AudioManager
import android.media.MediaMetadata
import android.media.session.MediaController
import android.media.session.MediaSessionManager
import android.media.session.PlaybackState
import android.os.Build
import android.service.notification.NotificationListenerService

/** Empty listener whose only job is to grant access to active media sessions. */
class MediaListener : NotificationListenerService()

/**
 * Watches media sessions (YouTube, YouTube Kids, Netflix, Shahid…) to find
 * natural break points: a video ended, a new one started, or playback paused.
 * Works only after the parent grants notification access; without it the
 * scheduler still works using time and app switches.
 */
class MediaWatcher(private val ctx: Context, private val onSignal: (Signal, String) -> Unit) {
    private val msm = ctx.getSystemService(Context.MEDIA_SESSION_SERVICE) as MediaSessionManager
    private val component = ComponentName(ctx, MediaListener::class.java)
    private val callbacks = mutableMapOf<MediaController, MediaController.Callback>()
    private val lastTitle = mutableMapOf<String, String>()
    private val nearEndFired = mutableSetOf<String>()

    private val sessionsListener = MediaSessionManager.OnActiveSessionsChangedListener { list -> attach(list ?: emptyList()) }

    fun start() {
        try {
            msm.addOnActiveSessionsChangedListener(sessionsListener, component)
            attach(msm.getActiveSessions(component))
        } catch (_: SecurityException) {
            // Notification access not granted yet.
        }
    }

    fun stop() {
        try { msm.removeOnActiveSessionsChangedListener(sessionsListener) } catch (_: Exception) { }
        callbacks.forEach { (c, cb) -> c.unregisterCallback(cb) }
        callbacks.clear()
    }

    private fun attach(list: List<MediaController>) {
        callbacks.forEach { (c, cb) -> c.unregisterCallback(cb) }
        callbacks.clear()
        for (c in list) {
            val pkg = c.packageName
            val cb = object : MediaController.Callback() {
                override fun onPlaybackStateChanged(state: PlaybackState?) {
                    when (state?.state) {
                        PlaybackState.STATE_PAUSED -> onSignal(Signal.MEDIA_PAUSED, pkg)
                        PlaybackState.STATE_STOPPED, PlaybackState.STATE_NONE -> onSignal(Signal.MEDIA_ENDED, pkg)
                        PlaybackState.STATE_PLAYING -> onSignal(Signal.MEDIA_PLAYING, pkg)
                    }
                }

                override fun onMetadataChanged(metadata: MediaMetadata?) {
                    val title = metadata?.getString(MediaMetadata.METADATA_KEY_TITLE) ?: return
                    val prev = lastTitle[pkg]
                    lastTitle[pkg] = title
                    nearEndFired.remove(pkg)
                    // A different video started: the previous one just ended.
                    if (prev != null && prev != title) onSignal(Signal.MEDIA_ENDED, pkg)
                }
            }
            c.registerCallback(cb)
            callbacks[c] = cb
        }
    }

    /** Fires MEDIA_ENDED in the last 2 seconds of a video (before autoplay jumps on). */
    fun checkNearEnd(pkg: String) {
        val c = callbacks.keys.firstOrNull { it.packageName == pkg } ?: return
        val st = c.playbackState ?: return
        if (st.state != PlaybackState.STATE_PLAYING) return
        val dur = c.metadata?.getLong(MediaMetadata.METADATA_KEY_DURATION) ?: return
        if (dur <= 0) return
        val pos = st.position + ((android.os.SystemClock.elapsedRealtime() - st.lastPositionUpdateTime) * st.playbackSpeed).toLong()
        if (dur - pos in 0..2000 && nearEndFired.add(pkg)) onSignal(Signal.MEDIA_ENDED, pkg)
    }

    /** Pause whatever is playing before the question appears. */
    fun pauseAll() {
        callbacks.keys.forEach { c ->
            try { if (c.playbackState?.state == PlaybackState.STATE_PLAYING) c.transportControls.pause() } catch (_: Exception) { }
        }
        // Players without a media session usually pause when they lose audio focus.
        val am = ctx.getSystemService(Context.AUDIO_SERVICE) as AudioManager
        if (Build.VERSION.SDK_INT >= 26) {
            am.requestAudioFocus(
                AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT)
                    .setAudioAttributes(AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_GAME).build())
                    .build()
            )
        }
    }
}

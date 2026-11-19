package sa.fakkerwakammel.fakker_wakammel.guard

/**
 * Kotlin twin of lib/core/break_scheduler.dart (keep the two in sync; both are
 * covered by unit tests). Runs inside the AccessibilityService so breaks happen
 * even when the Flutter UI is not running.
 */
enum class BreakMode { FIXED, SMART, AUTO }
enum class ContentKind { VIDEO, GAME }
enum class Signal { TOUCH, MEDIA_PLAYING, MEDIA_PAUSED, MEDIA_ENDED, LEVEL_COMPLETE, MENU_SCREEN, APP_SWITCH }
enum class Phase { WATCHING, SEEKING, WARNING, DUE }

/** Names match the Dart BreakReason enum so logs can be merged directly. */
enum class BreakReason(val dartName: String) {
    VIDEO_ENDED("videoEnded"), LEVEL_COMPLETE("levelComplete"), PAUSED("paused"), IDLE("idle"),
    APP_SWITCH("appSwitch"), FIXED_TIME("fixedTime"), GRACE_TIMEOUT("graceTimeout")
}

class NativeScheduler(
    val mode: BreakMode,
    val targetSeconds: Int,
    val graceSeconds: Int,
    val warnSeconds: Int = 10,
    val idleSeconds: Int = 8,
    var kind: ContentKind = ContentKind.VIDEO,
) {
    var elapsed = 0
        private set
    private var idle = 0
    var warnRemaining = 0
        private set
    var phase = Phase.WATCHING
        private set
    var reason: BreakReason? = null
        private set

    val isSmart get() = mode != BreakMode.FIXED
    val seekFrom get() = if (isSmart) (targetSeconds * 0.85).toInt() else targetSeconds
    val hardLimit get() = if (isSmart) targetSeconds + graceSeconds else targetSeconds

    fun restore(elapsedSeconds: Int) {
        elapsed = elapsedSeconds
        if (isSmart && elapsed >= seekFrom) phase = Phase.SEEKING
    }

    fun reset() {
        elapsed = 0; idle = 0; warnRemaining = 0; phase = Phase.WATCHING; reason = null
    }

    fun tick() {
        if (phase == Phase.DUE) return
        elapsed++
        idle++
        if (phase == Phase.WARNING) {
            warnRemaining--
            if (warnRemaining <= 0) fire(if (isSmart) BreakReason.GRACE_TIMEOUT else BreakReason.FIXED_TIME)
            return
        }
        if (!isSmart) {
            if (elapsed >= targetSeconds - warnSeconds) warn()
            return
        }
        if (elapsed >= seekFrom && phase == Phase.WATCHING) phase = Phase.SEEKING
        if (phase == Phase.SEEKING && kind == ContentKind.GAME && idle >= idleSeconds) {
            fire(BreakReason.IDLE); return
        }
        if (elapsed >= hardLimit - warnSeconds) warn()
    }

    fun signal(s: Signal) {
        if (s == Signal.TOUCH) idle = 0
        if (phase == Phase.DUE) return
        val canTakeNatural = isSmart && (phase == Phase.SEEKING || phase == Phase.WARNING)
        if (!canTakeNatural) return
        val natural = when (s) {
            Signal.MEDIA_ENDED -> BreakReason.VIDEO_ENDED
            Signal.LEVEL_COMPLETE, Signal.MENU_SCREEN -> BreakReason.LEVEL_COMPLETE
            Signal.MEDIA_PAUSED -> BreakReason.PAUSED
            Signal.APP_SWITCH -> BreakReason.APP_SWITCH
            else -> null
        }
        if (natural != null) fire(natural)
    }

    private fun warn() {
        if (phase == Phase.WARNING) return
        phase = Phase.WARNING
        warnRemaining = warnSeconds
    }

    private fun fire(r: BreakReason) {
        phase = Phase.DUE
        reason = r
    }

    companion object {
        /** Auto-mode interval (minutes) by age band index A..E — mirrors AgeBand.autoIntervalMinutes. */
        val AUTO_INTERVAL = intArrayOf(10, 15, 20, 25, 30)

        fun bandIndexForAge(age: Int) = when {
            age <= 5 -> 0
            age <= 8 -> 1
            age <= 12 -> 2
            age <= 15 -> 3
            else -> 4
        }

        fun fromConfig(mode: BreakMode, intervalMinutes: Int, graceMinutes: Int, age: Int, unit: Int, kind: ContentKind): NativeScheduler {
            val minutes = if (mode == BreakMode.AUTO) AUTO_INTERVAL[bandIndexForAge(age)] else intervalMinutes
            val grace = if (mode == BreakMode.AUTO) 3 else graceMinutes
            return NativeScheduler(
                mode = mode,
                targetSeconds = minutes * unit,
                graceSeconds = grace * unit,
                warnSeconds = if (unit == 1) 5 else 10,
                idleSeconds = if (unit == 1) 4 else 8,
                kind = kind,
            )
        }
    }
}

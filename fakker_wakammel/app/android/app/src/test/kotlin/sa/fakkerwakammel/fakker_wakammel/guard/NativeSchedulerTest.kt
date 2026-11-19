package sa.fakkerwakammel.fakker_wakammel.guard

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotEquals
import org.junit.Test

/** Mirrors test/smart_features_test.dart so the Dart and Kotlin schedulers behave identically. */
class NativeSchedulerTest {
    private fun run(s: NativeScheduler, seconds: Int) {
        repeat(seconds) { if (s.phase != Phase.DUE) s.tick() }
    }

    @Test fun fixedModePausesExactlyAtIntervalWithWarning() {
        val s = NativeScheduler(BreakMode.FIXED, targetSeconds = 100, graceSeconds = 30, warnSeconds = 10)
        run(s, 89)
        assertEquals(Phase.WATCHING, s.phase)
        s.tick()
        assertEquals(Phase.WARNING, s.phase)
        s.signal(Signal.MEDIA_ENDED)
        assertEquals(Phase.WARNING, s.phase)
        run(s, 20)
        assertEquals(Phase.DUE, s.phase)
        assertEquals(100, s.elapsed)
        assertEquals(BreakReason.FIXED_TIME, s.reason)
    }

    @Test fun smartModeIgnoresNaturalMomentsBefore85Percent() {
        val s = NativeScheduler(BreakMode.SMART, 100, 60)
        run(s, 50)
        s.signal(Signal.MEDIA_ENDED)
        assertEquals(Phase.WATCHING, s.phase)
    }

    @Test fun smartModeTakesEndOfVideo() {
        val s = NativeScheduler(BreakMode.SMART, 100, 60)
        run(s, 90)
        assertEquals(Phase.SEEKING, s.phase)
        s.signal(Signal.MEDIA_ENDED)
        assertEquals(BreakReason.VIDEO_ENDED, s.reason)
    }

    @Test fun smartModeNeverCutsActiveGame() {
        val s = NativeScheduler(BreakMode.SMART, 100, 60, kind = ContentKind.GAME)
        repeat(120) { s.signal(Signal.TOUCH); s.tick() }
        assertEquals(Phase.SEEKING, s.phase)
        s.signal(Signal.LEVEL_COMPLETE)
        assertEquals(BreakReason.LEVEL_COMPLETE, s.reason)
    }

    @Test fun idleCountsForGamesOnly() {
        val game = NativeScheduler(BreakMode.SMART, 100, 60, idleSeconds = 8, kind = ContentKind.GAME)
        repeat(86) { game.signal(Signal.TOUCH); game.tick() }
        run(game, 8)
        assertEquals(BreakReason.IDLE, game.reason)
        val video = NativeScheduler(BreakMode.SMART, 100, 60, idleSeconds = 8)
        run(video, 120)
        assertNotEquals(Phase.DUE, video.phase)
    }

    @Test fun graceTimeoutWarnsThenPauses() {
        val s = NativeScheduler(BreakMode.SMART, 100, 60, warnSeconds = 10)
        run(s, 150)
        assertEquals(Phase.WARNING, s.phase)
        run(s, 20)
        assertEquals(BreakReason.GRACE_TIMEOUT, s.reason)
        assertEquals(160, s.elapsed)
    }

    @Test fun autoModeUsesAgeBand() {
        assertEquals(600, NativeScheduler.fromConfig(BreakMode.AUTO, 15, 3, age = 4, unit = 60, kind = ContentKind.VIDEO).targetSeconds)
        assertEquals(1800, NativeScheduler.fromConfig(BreakMode.AUTO, 15, 3, age = 17, unit = 60, kind = ContentKind.VIDEO).targetSeconds)
    }

    @Test fun restoreAfterServiceRestartKeepsProgress() {
        val s = NativeScheduler(BreakMode.SMART, 100, 60)
        s.restore(90)
        assertEquals(Phase.SEEKING, s.phase)
        s.signal(Signal.MEDIA_PAUSED)
        assertEquals(BreakReason.PAUSED, s.reason)
    }

    @Test fun swipingToNextReelIsANaturalBreakInFeeds() {
        val feed = NativeScheduler(BreakMode.SMART, 100, 60)
        run(feed, 50)
        feed.signal(Signal.CONTENT_SWIPE)
        assertEquals("not before 85%", Phase.WATCHING, feed.phase)
        run(feed, 40)
        feed.signal(Signal.CONTENT_SWIPE)
        assertEquals(BreakReason.VIDEO_ENDED, feed.reason)

        val game = NativeScheduler(BreakMode.SMART, 100, 60, kind = ContentKind.GAME)
        repeat(95) { game.signal(Signal.TOUCH); game.tick() }
        game.signal(Signal.CONTENT_SWIPE)
        assertNotEquals("a scroll inside a game is play, not a pause", Phase.DUE, game.phase)
    }

    @Test fun reasonNamesMatchDart() {
        assertEquals("videoEnded", BreakReason.VIDEO_ENDED.dartName)
        assertEquals("graceTimeout", BreakReason.GRACE_TIMEOUT.dartName)
    }
}

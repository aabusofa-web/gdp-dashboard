import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:fakker_wakammel/core/adaptive_engine.dart';
import 'package:fakker_wakammel/core/anti_cheat.dart';
import 'package:fakker_wakammel/core/break_scheduler.dart';
import 'package:fakker_wakammel/core/models.dart';
import 'package:flutter_test/flutter_test.dart';

List<Question> loadBank() {
  final j = jsonDecode(File('assets/questions/seed_questions.json').readAsStringSync()) as Map<String, dynamic>;
  return (j['questions'] as List).map((q) => Question.fromJson(Map<String, dynamic>.from(q as Map))).toList();
}

final now = DateTime(2026, 11, 19);
ChildProfile kid({int age = 10, Gender g = Gender.male}) =>
    ChildProfile(id: 'k', name: 'Sara', birthDate: DateTime(2026 - age, 1, 1), gender: g);

void runFor(BreakScheduler s, int seconds) {
  for (var i = 0; i < seconds && s.phase != SchedulerPhase.due; i++) {
    s.tick();
  }
}

void main() {
  final bank = loadBank();

  group('break scheduler', () {
    test('fixed mode pauses exactly at the interval, with a warning first', () {
      final s = BreakScheduler(mode: BreakMode.fixed, targetSeconds: 100, graceSeconds: 30, warnSeconds: 10);
      runFor(s, 89);
      expect(s.phase, SchedulerPhase.watching);
      s.tick();
      expect(s.phase, SchedulerPhase.warning);
      s.signal(ActivitySignal.mediaEnded); // natural moments are ignored in fixed mode
      expect(s.phase, SchedulerPhase.warning);
      runFor(s, 20);
      expect(s.phase, SchedulerPhase.due);
      expect(s.elapsed, 100);
      expect(s.reason, BreakReason.fixedTime);
    });

    test('smart mode does not interrupt before 85% of the interval', () {
      final s = BreakScheduler(mode: BreakMode.smart, targetSeconds: 100, graceSeconds: 60);
      runFor(s, 50);
      s.signal(ActivitySignal.mediaEnded);
      expect(s.phase, SchedulerPhase.watching);
    });

    test('smart mode takes the end of a video as the break', () {
      final s = BreakScheduler(mode: BreakMode.smart, targetSeconds: 100, graceSeconds: 60);
      runFor(s, 90);
      expect(s.phase, SchedulerPhase.seeking);
      s.signal(ActivitySignal.mediaEnded);
      expect(s.phase, SchedulerPhase.due);
      expect(s.reason, BreakReason.videoEnded);
    });

    test('smart mode in a game waits for level end, not mid-play', () {
      final s = BreakScheduler(mode: BreakMode.smart, targetSeconds: 100, graceSeconds: 60, kind: ContentKind.game);
      for (var i = 0; i < 120; i++) {
        s.signal(ActivitySignal.touch); // actively playing
        s.tick();
      }
      expect(s.phase, SchedulerPhase.seeking, reason: 'must not cut an active game');
      s.signal(ActivitySignal.levelComplete);
      expect(s.reason, BreakReason.levelComplete);
    });

    test('smart mode treats idle play as a good moment, but not idle video', () {
      final game = BreakScheduler(mode: BreakMode.smart, targetSeconds: 100, graceSeconds: 60, idleSeconds: 8, kind: ContentKind.game);
      for (var i = 0; i < 86; i++) {
        game.signal(ActivitySignal.touch);
        game.tick();
      }
      runFor(game, 8);
      expect(game.reason, BreakReason.idle);

      final video = BreakScheduler(mode: BreakMode.smart, targetSeconds: 100, graceSeconds: 60, idleSeconds: 8);
      runFor(video, 120);
      expect(video.phase, isNot(SchedulerPhase.due));
    });

    test('smart mode warns then pauses if no good moment comes within the grace period', () {
      final s = BreakScheduler(mode: BreakMode.smart, targetSeconds: 100, graceSeconds: 60, warnSeconds: 10);
      runFor(s, 150);
      expect(s.phase, SchedulerPhase.warning);
      runFor(s, 20);
      expect(s.reason, BreakReason.graceTimeout);
      expect(s.elapsed, 160);
    });

    test('auto mode picks the interval from the age band', () {
      final st = AppSettings(breakMode: BreakMode.auto);
      expect(BreakScheduler.fromSettings(st, AgeBand.a).targetSeconds, 10 * 60);
      expect(BreakScheduler.fromSettings(st, AgeBand.e).targetSeconds, 30 * 60);
    });
  });

  group('parent choices', () {
    test('only the chosen domains are asked (e.g. geography + religion)', () {
      final e = AdaptiveEngine(random: Random(5));
      final k = kid()..domains = {Domain.geography, Domain.religion};
      for (var i = 0; i < 200; i++) {
        final q = e.nextQuestion(child: k, bank: bank, history: const [], now: now)!;
        expect({Domain.geography, Domain.religion}, contains(q.domain));
      }
    });

    test('language to improve gets a large share of questions', () {
      final e = AdaptiveEngine(random: Random(9));
      final k = kid(age: 10)..learnLanguage = 'fr';
      var fr = 0;
      for (var i = 0; i < 400; i++) {
        if (e.nextQuestion(child: k, bank: bank, history: const [], now: now)!.domain == Domain.french) fr++;
      }
      expect(fr / 400, greaterThan(0.3));
    });

    test('national questions only appear for that country', () {
      final e = AdaptiveEngine(random: Random(2));
      final k = kid(age: 4);
      final seenAbroad = <String?>{};
      for (var i = 0; i < 300; i++) {
        seenAbroad.add(e.nextQuestion(child: k, bank: bank, history: const [], now: now, country: 'GB')!.region);
      }
      expect(seenAbroad, {null});
      var saudi = 0;
      for (var i = 0; i < 600; i++) {
        if (e.nextQuestion(child: k, bank: bank, history: const [], now: now, country: 'SA')!.region == 'SA') saudi++;
      }
      expect(saudi, greaterThan(0));
    });
  });

  group('anti-cheat', () {
    test('a lightning-fast first answer is not rewarded like real knowledge', () {
      final e = AdaptiveEngine();
      final q = bank.firstWhere((q) => q.domain == Domain.math && q.type == QuestionType.mcq);
      final honest = kid(), guesser = kid();
      e.applyResult(child: honest, question: q, attempts: 1, solved: true, secondsTaken: 6, now: now);
      final log = e.applyResult(child: guesser, question: q, attempts: 1, solved: true, secondsTaken: 0, now: now, fastGuess: true);
      expect(log.fastGuess, isTrue);
      expect(guesser.levelFor(Domain.math, now), lessThan(honest.levelFor(Domain.math, now)));
      expect(guesser.fastGuessStreak, 1);
    });

    test('options stay locked long enough to read, longer for longer text', () {
      final short = bank.firstWhere((q) => q.type == QuestionType.mcq && q.text.ar.length < 25);
      final long = bank.firstWhere((q) => q.type == QuestionType.mcq && q.text.ar.length > 60);
      expect(AntiCheat.readSeconds(short, 'ar', AgeBand.c), greaterThanOrEqualTo(2));
      expect(AntiCheat.readSeconds(long, 'ar', AgeBand.c), greaterThan(AntiCheat.readSeconds(short, 'ar', AgeBand.c)));
      expect(AntiCheat.cooldownSeconds(1), lessThan(AntiCheat.cooldownSeconds(3)));
    });

    test('trace scoring accepts a faithful trace and rejects scribbles', () {
      // Glyph: a vertical bar x=100, y 20..180.
      final mask = [for (var y = 20.0; y <= 180; y += 6) Point(100.0, y)];
      final good = [for (var y = 22.0; y <= 178; y += 3) Point(102.0, y)];
      final partial = [for (var y = 22.0; y <= 60; y += 3) Point(102.0, y)];
      final scribble = [for (var x = 0.0; x <= 200; x += 3) Point(x, 100 + 60 * sin(x / 10))];
      expect(TraceScore.compute(mask, good).passed, isTrue);
      expect(TraceScore.compute(mask, partial).passed, isFalse);
      expect(TraceScore.compute(mask, scribble).passed, isFalse);
    });
  });

  test('localized text falls back gracefully', () {
    const t = LocalizedText('مرحبا', 'Hello', {'fr': 'Bonjour'});
    expect(t.of('fr'), 'Bonjour');
    expect(t.of('tr'), 'مرحبا');
    expect(const LocalizedText('', 'Hi').of('ar'), 'Hi');
  });
}

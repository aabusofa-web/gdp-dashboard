import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:fakker_wakammel/core/adaptive_engine.dart';
import 'package:fakker_wakammel/core/models.dart';
import 'package:flutter_test/flutter_test.dart';

List<Question> loadBank() {
  final j = jsonDecode(File('assets/questions/seed_questions.json').readAsStringSync()) as Map<String, dynamic>;
  return (j['questions'] as List).map((q) => Question.fromJson(Map<String, dynamic>.from(q as Map))).toList();
}

ChildProfile child({int age = 7, Gender g = Gender.male}) =>
    ChildProfile(id: 'k1', name: 'Test', birthDate: DateTime(2026 - age, 1, 1), gender: g);

final now = DateTime(2026, 11, 19);

void main() {
  final bank = loadBank();

  test('seed bank is valid and covers every domain and band', () {
    expect(bank.length, greaterThan(100));
    expect(bank.map((q) => q.id).toSet().length, bank.length, reason: 'ids must be unique');
    for (final d in Domain.values) {
      expect(bank.any((q) => q.domain == d), isTrue, reason: '$d missing');
    }
    for (final b in AgeBand.values) {
      expect(bank.where((q) => q.ageBands.contains(b)).length, greaterThan(20), reason: '$b thin');
    }
    for (final q in bank) {
      expect(q.answer, inInclusiveRange(0, q.options.length - 1));
      expect(q.text.ar.isNotEmpty && q.text.en.isNotEmpty, isTrue, reason: q.id);
    }
  });

  test('age bands map correctly', () {
    expect(AgeBand.forAge(3), AgeBand.a);
    expect(AgeBand.forAge(8), AgeBand.b);
    expect(AgeBand.forAge(12), AgeBand.c);
    expect(AgeBand.forAge(15), AgeBand.d);
    expect(AgeBand.forAge(20), AgeBand.e);
  });

  test('level deltas follow the number of attempts', () {
    expect(AdaptiveEngine.delta(attempts: 1, solved: true), 0.5);
    expect(AdaptiveEngine.delta(attempts: 2, solved: true), 0.15);
    expect(AdaptiveEngine.delta(attempts: 3, solved: true), -0.1);
    expect(AdaptiveEngine.delta(attempts: 3, solved: false), -0.3);
    expect(AdaptiveEngine.stars(attempts: 1, solved: true), 3);
    expect(AdaptiveEngine.stars(attempts: 3, solved: false), 0);
  });

  test('three first-try answers in a row give a promotion bonus', () {
    final e = AdaptiveEngine(random: Random(1));
    final k = child(age: 10); // band C, starts at 6
    final q = bank.firstWhere((q) => q.domain == Domain.math);
    e.applyResult(child: k, question: q, attempts: 1, solved: true, secondsTaken: 5, now: now);
    e.applyResult(child: k, question: q, attempts: 1, solved: true, secondsTaken: 5, now: now);
    final log = e.applyResult(child: k, question: q, attempts: 1, solved: true, secondsTaken: 5, now: now);
    expect(log.levelAfter, closeTo(6 + 0.5 * 3 + 0.5, 1e-9));
    expect(k.streaks[Domain.math], 0);
  });

  test('levels stay within band floor and band ceiling + 2', () {
    final e = AdaptiveEngine(random: Random(1));
    final k = child(age: 4); // band A: 1..4 (+2)
    final q = bank.firstWhere((q) => q.ageBands.contains(AgeBand.a));
    for (var i = 0; i < 50; i++) {
      e.applyResult(child: k, question: q, attempts: 1, solved: true, secondsTaken: 1, now: now);
    }
    expect(k.levelFor(q.domain, now), 6);
    for (var i = 0; i < 50; i++) {
      e.applyResult(child: k, question: q, attempts: 3, solved: false, secondsTaken: 1, now: now);
    }
    expect(k.levelFor(q.domain, now), 1);
  });

  test('moving to an older band lifts the level to the new floor', () {
    final k = child(age: 8)..levels[Domain.science] = 4;
    expect(k.levelFor(Domain.science, now), 4); // band B floor 3
    expect(k.levelFor(Domain.science, DateTime(2027, 1, 2)), 6); // now 9 → band C floor 6
  });

  test('selection respects gender audience and age band', () {
    final e = AdaptiveEngine(random: Random(42));
    final girl = child(age: 14, g: Gender.female);
    for (var i = 0; i < 300; i++) {
      final q = e.nextQuestion(child: girl, bank: bank, history: const [], now: now)!;
      expect(q.audience.fits(Gender.female), isTrue, reason: q.id);
      expect(q.ageBands.any((b) => {AgeBand.c, AgeBand.d, AgeBand.e}.contains(b)), isTrue, reason: q.id);
    }
  });

  test('a mastered question does not come back for 30 days', () {
    final e = AdaptiveEngine(random: Random(7));
    final k = child(age: 7);
    final history = <AttemptLog>[];
    final seen = <String>{};
    // Answer everything correctly first try; no repeats should occur while unseen ones remain.
    for (var i = 0; i < 20; i++) {
      final q = e.nextQuestion(child: k, bank: bank, history: history, now: now, enabledDomains: {Domain.math})!;
      if (q.domain == Domain.math && q.ageBands.contains(AgeBand.b)) {
        expect(seen.contains(q.id), isFalse, reason: 'repeated ${q.id} too early');
      }
      seen.add(q.id);
      history.add(e.applyResult(child: k, question: q, attempts: 1, solved: true, secondsTaken: 3, now: now));
    }
  });

  test('stronger children get harder questions', () {
    final e = AdaptiveEngine(random: Random(3));
    final weak = child(age: 14);
    final strong = child(age: 14);
    for (final d in Domain.values) {
      weak.levels[d] = 10;
      strong.levels[d] = 16;
    }
    double avg(ChildProfile k) {
      var sum = 0;
      for (var i = 0; i < 200; i++) {
        sum += e.nextQuestion(child: k, bank: bank, history: const [], now: now)!.difficulty;
      }
      return sum / 200;
    }

    expect(avg(strong), greaterThan(avg(weak) + 2));
  });
}

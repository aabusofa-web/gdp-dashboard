# فكّر وكمّل – التصميم التقني

## 1. مكونات النظام

```
┌────────────────────────────┐      ┌──────────────────────────┐
│  تطبيق فكّر وكمّل (Flutter)  │      │  لوحة الأدمن (Next.js)   │
│  ─ وضع ولي الأمر            │      │  ─ بنك الأسئلة            │
│  ─ وضع الطفل + شاشة السؤال  │      │  ─ المراجعة والاعتماد     │
│  ─ المحرك التكيّفي (محلي)    │      │  ─ الإحصائيات             │
│  ─ طبقة أصلية:              │      └────────────┬─────────────┘
│    Android: Accessibility  │                   │
│    + Overlay + DeviceAdmin │                   │
│    iOS: FamilyControls +   │                   │
│    DeviceActivity + Shield │                   │
└─────────────┬──────────────┘                   │
              │  مزامنة (عند توفر الإنترنت)        │
              ▼                                  ▼
       ┌──────────────────────────────────────────────┐
       │ Firebase: Auth · Firestore · Cloud Functions │
       │ Storage (صور/صوت) · FCM (إشعارات)            │
       │ RevenueCat (إدارة الاشتراكات للمتجرين)        │
       └──────────────────────────────────────────────┘
```

| الطبقة | التقنية | ملاحظة |
|---|---|---|
| التطبيق | Flutter 3.x (Dart) | كود واحد لأندرويد وأندرويد TV وiOS |
| الإيقاف على أندرويد | Kotlin: `AccessibilityService` + `SYSTEM_ALERT_WINDOW` + `ForegroundService` + `DeviceAdminReceiver` | يكتشف التطبيق الظاهر ويعدّ الوقت ويعرض شاشة السؤال |
| الإيقاف على iOS | Swift: `FamilyControls` + `DeviceActivityMonitor` + `ManagedSettings` (Shield) | يحتاج موافقة Apple |
| التخزين المحلي | Hive/SharedPreferences (الإصدار الأول) ← Drift/SQLite | يعمل بدون إنترنت |
| الخادم | Firebase | تكلفته مجانية إلى قرابة 50 دولاراً شهرياً حتى 10 آلاف مستخدم |
| الاشتراكات | RevenueCat فوق Google Play Billing وStoreKit | مجاني حتى إيراد شهري قدره 2,500 دولار |
| لوحة الأدمن | Next.js + Firebase Admin | |

---

## 2. نموذج البيانات

### Question (سؤال)
```json
{
  "id": "rel-a-001",
  "domain": "religion",
  "ageBands": ["A", "B"],
  "difficulty": 2,
  "gender": "all",
  "type": "mcq",
  "text": { "ar": "كم عدد الصلوات المفروضة في اليوم؟", "en": "How many obligatory prayers are there each day?" },
  "options": [ { "ar": "3", "en": "3" }, { "ar": "5", "en": "5" }, { "ar": "7", "en": "7" } ],
  "answer": 1,
  "explanation": { "ar": "...", "en": "..." },
  "image": null,
  "status": "published",
  "source": "system"
}
```
- `gender` يأخذ إحدى القيم `all` أو `male` أو `female`.
- `source` يأخذ القيمة `system` لبنك المنصة، أو `family` لسؤال أضافه ولي الأمر.

### ChildProfile (ملف الطفل)
`id, name, birthDate, gender, language, avatar, domainLevels{domain: double}, streaks{domain: int}`

### Settings (الإعدادات)
`intervalMinutes, questionsPerBreak, maxAttempts, onFail(alternate|lock), lockMinutes, dailyLimitMinutes?, bedtime?, includedApps[], excludedApps[]`

### AttemptLog (سجل المحاولات)
`id, childId, questionId, domain, difficulty, attempts, solved, levelBefore, levelAfter, secondsTaken, timestamp`

### UsageLog (سجل الاستخدام)
`childId, appPackage, startedAt, endedAt, seconds`

### هيكل Firestore
```
families/{familyId}
  ├─ settings
  ├─ children/{childId}
  │    ├─ attempts/{attemptId}
  │    └─ usage/{day}
  └─ customQuestions/{questionId}
questions/{questionId}          ← البنك العام (يكتبه الأدمن فقط)
admins/{uid}
```

---

## 3. المحرك التكيّفي (Adaptive Engine)

### 3.1 تحديث المستوى
```
level_new = clamp(level + Δ(attempts, solved) + bonus, bandMin, bandMax + 2)

Δ: المحاولة الأولى +0.5 | الثانية +0.15 | الثالثة فما بعد −0.1 | لم يحلّ −0.3
bonus: +0.5 عند 3 إجابات صحيحة متتالية من المحاولة الأولى في نفس المجال
```
يُسمح للطفل المتفوق بتجاوز الحد الأعلى لفئته العمرية بمستويين، فيرى أسئلة الفئة التالية.

### 3.2 اختيار السؤال التالي
1. **اختيار المجال:** 60% أضعف مجال (أقل مستوى)، و40% تناوب عشوائي مرجَّح بين المجالات المفعّلة.
2. **تصفية المرشحين:** فئة الطفل العمرية، والجنس المناسب (`all` أو جنس الطفل)، واللغة، والحالة `published`.
3. **استبعاد:** الأسئلة التي ما زالت ضمن فترة التكرار المتباعد.
4. **الترتيب:** حسب الفرق المطلق بين صعوبة السؤال ومستوى الطفل، ثم الأقل ظهوراً.
5. إن لم يوجد سؤال مناسب: توسيع البحث للفئة المجاورة، ثم لأي مجال.

### 3.3 التكرار المتباعد
| النتيجة السابقة | يعود السؤال بعد |
|---|---|
| صحيح من أول محاولة | 30 يوماً |
| صحيح من المحاولة الثانية | 7 أيام |
| صحيح من المحاولة الثالثة فما بعد | 3 أيام |
| لم يحل | يوم واحد |

---

## 4. آلية الإيقاف على أندرويد
1. تستقبل `AccessibilityService` حدث `TYPE_WINDOW_STATE_CHANGED`، فتعرف اسم التطبيق الظاهر.
2. إن كان التطبيق مشمولاً يبدأ عدّاد يعتمد على `SystemClock.elapsedRealtime()`، ويتوقف العدّاد عند إغلاق الشاشة أو الخروج من التطبيق.
3. عند بلوغ المدة: تُفتح `QuizActivity` (Flutter) فوق كل شيء، وتُرسل للتطبيق المفتوح أمر إيقاف الوسائط عبر `AudioManager` لطلب التركيز الصوتي (audio focus).
4. بعد الحل: تُغلق `QuizActivity` فيعود الطفل للتطبيق، ويُصفَّر العدّاد.
5. محاولة إغلاق شاشة السؤال بزر الرجوع أو الرئيسية: تكتشفها الخدمة وتعيد فتح الشاشة فوراً.

## 5. آلية الإيقاف على iOS
1. يختار ولي الأمر التطبيقات عبر `FamilyActivityPicker`.
2. يضبط `DeviceActivityMonitor` حدثاً عند بلوغ X دقيقة من الاستخدام.
3. عند الحدث: يُطبق `ManagedSettingsStore.shield` على التطبيقات، وتظهر شاشة مخصصة: "افتح فكّر وكمّل وأجب".
4. يجيب الطفل في التطبيق، فيُرفع الحجب ويُعاد ضبط الحدث.

---

## 6. خارطة الطريق
| المرحلة | المخرجات | المدة | الحالة |
|---|---|---|---|
| 1 | وثائق المتطلبات والتصميم وبنك الأسئلة الأولي | أسبوع | ✅ |
| 2 | المحرك التكيّفي، وشاشة السؤال، والإعدادات، والتحليلات (Flutter) | 2 إلى 3 أسابيع | 🟡 بدأ العمل عليها |
| 3 | طبقة الإيقاف الأصلية على أندرويد (Kotlin)، وبناء ملف التثبيت APK | 2 إلى 3 أسابيع | ⏳ |
| 4 | Firebase (الحسابات والمزامنة) والاشتراك عبر RevenueCat | أسبوعان | ⏳ |
| 5 | لوحة الأدمن (ويب) | أسبوعان إلى 3 | ⏳ |
| 6 | أندرويد TV | أسبوع إلى أسبوعين | ⏳ |
| 7 | iOS وiPadOS (يُقدَّم طلب Family Controls لـ Apple من الآن) | 3 إلى 5 أسابيع | ⏳ |
| 8 | تجربة مغلقة مع 20 إلى 30 عائلة، ثم النشر | أسبوعان إلى 3 | ⏳ |

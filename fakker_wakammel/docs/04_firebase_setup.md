# ربط جوالي الأب والأم – إعداد Firebase (مرة واحدة)

## لماذا؟
لكي يصل تنبيه مثل "سارة حاولت تجاوز السؤال" أو التقرير الدوري إلى **جوال الأب وجوال الأم معاً** وهما في العمل أو خارج البيت، يحتاج التطبيق خادماً وسيطاً. نستخدم **Firebase** من Google لسببين:
- مجاني للاستخدام العادي: آلاف الأسر ضمن الحد المجاني تقريباً.
- موثوق، ويعمل في السعودية.

## كيف يعمل
```
جهاز الطفل ──(تنبيه)──► Firestore: families/{id}/alerts
                                  │
                          دالة relayAlert (Cloud Functions)
                                  │
              ┌───────────────────┴───────────────────┐
         جوال الأب (إشعار)                      جوال الأم (إشعار)
```
- **الربط بين الأجهزة:** يكون برمز من 6 أرقام صالح لمدة 24 ساعة، فلا حاجة لبريد أو كلمة مرور.
- **الخصوصية:** قواعد الأمان (`backend/firestore.rules`) لا تسمح بقراءة بيانات العائلة إلا للأجهزة المرتبطة بها.

## الخطوات (قرابة 20 دقيقة)
1. ادخل إلى https://console.firebase.google.com بحساب Google الخاص بالمشروع، واضغط **Add project** ← الاسم: `fakker-wakammel`.
2. من **Build ← Firestore Database ← Create database**، واختر الموقع `me-central2 (Dammam)` إن توفر، ثم ابدأ بوضع **Production**.
3. من **Build ← Authentication ← Get started ← Sign-in method**، فعّل **Anonymous**.
4. من **Project settings ← Add app ← Android**:
   - Package name: `sa.fakkerwakammel.app`
   - انسخ القيم التالية من صفحة الإعدادات:
     - `apiKey`: Web API Key
     - `appId`: يبدأ بـ `1:...:android:...`
     - `messagingSenderId`: Project number
     - `projectId`
5. **ترقية الخطة إلى Blaze (الدفع حسب الاستخدام):** ضرورية لتشغيل الدالة التي ترسل الإشعارات.
   - التكلفة الفعلية للاستخدام المتوقع في البداية: **0 – 5 دولارات شهرياً**.
   - **ضع تنبيه ميزانية** (مثلاً 10 دولارات) من Google Cloud Billing.
6. أرسل لي القيم الأربع من الخطوة 4، أو ضعها في ملف `app/firebase.env.json` بهذا الشكل:
   ```json
   {
     "FW_FIREBASE_API_KEY": "...",
     "FW_FIREBASE_APP_ID": "...",
     "FW_FIREBASE_SENDER_ID": "...",
     "FW_FIREBASE_PROJECT_ID": "fakker-wakammel"
   }
   ```
   هذا الملف لا يُرفع إلى GitHub.
7. النشر (أتولاه عنك إن أعطيتني صلاحية، أو من جهازك):
   ```bash
   npm i -g firebase-tools && firebase login
   cd fakker_wakammel/backend && firebase use fakker-wakammel
   (cd functions && npm install) && firebase deploy --only firestore:rules,functions
   ```
8. بناء التطبيق بالربط:
   ```bash
   cd fakker_wakammel/app
   flutter build apk --release --split-per-abi --dart-define-from-file=firebase.env.json
   ```

## الاستخدام
1. **جوال الأب:** الإعدادات ← ربط العائلة ← **إنشاء عائلة**، فيظهر رمز من 6 أرقام.
2. **جوال الأم:** الإعدادات ← ربط العائلة ← **الانضمام برمز** ← اختر "جوال ولي أمر".
3. **جهاز الطفل:** الانضمام بالرمز نفسه أو برمز جديد، واختر "جهاز الطفل".
4. انتهى. كل تنبيه يحدث على جهاز الطفل، أو على جوال أحد الأبوين أثناء جلسة طفل، يصل للأب والأم معاً.

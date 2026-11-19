"""Builds the seed question bank JSON for Fakker Wakammel."""
import json, sys
from collections import Counter

# (domain, bands, difficulty, gender, q_ar, q_en, [(opt_ar,opt_en)...], answer, exp_ar, exp_en)
Q = []
def q(domain, bands, diff, gender, qar, qen, opts, ans, ear, een, **kw):
    Q.append((domain, bands, diff, gender, qar, qen, opts, ans, ear, een, kw))

# ---------------- RELIGION ----------------
q("religion","AB",1,"all","كم عدد الصلوات المفروضة في اليوم؟","How many obligatory prayers are there each day?",
  [("ثلاث","Three"),("خمس","Five"),("سبع","Seven")],1,"الصلوات المفروضة خمس: الفجر والظهر والعصر والمغرب والعشاء.","There are five: Fajr, Dhuhr, Asr, Maghrib and Isha.")
q("religion","AB",2,"all","ماذا نقول قبل أن نأكل؟","What do we say before eating?",
  [("بسم الله","Bismillah"),("مع السلامة","Goodbye"),("صباح الخير","Good morning")],0,"نقول: بسم الله قبل الطعام، والحمد لله بعده.","We say Bismillah before eating and Alhamdulillah after.")
q("religion","A",1,"all","في أي مدينة توجد الكعبة؟","In which city is the Kaaba?",
  [("مكة المكرمة","Makkah"),("الرياض","Riyadh"),("جدة","Jeddah")],0,"الكعبة المشرفة في المسجد الحرام بمكة المكرمة.","The Kaaba is in Al-Masjid Al-Haram in Makkah.")
q("religion","BC",5,"all","في أي شهر يصوم المسلمون؟","In which month do Muslims fast?",
  [("شعبان","Sha'ban"),("رمضان","Ramadan"),("محرم","Muharram"),("رجب","Rajab")],1,"صيام شهر رمضان هو الركن الرابع من أركان الإسلام.","Fasting Ramadan is the fourth pillar of Islam.")
q("religion","BC",6,"all","ما أول ركن من أركان الإسلام؟","What is the first pillar of Islam?",
  [("الصلاة","Prayer"),("الشهادتان","The Shahada"),("الزكاة","Zakat"),("الحج","Hajj")],1,"أركان الإسلام: الشهادتان، الصلاة، الزكاة، الصوم، الحج.","Pillars: Shahada, prayer, zakat, fasting, Hajj.")
q("religion","C",8,"all","كم عدد سور القرآن الكريم؟","How many surahs are in the Quran?",
  [("100","100"),("114","114"),("120","120"),("99","99")],1,"القرآن الكريم 114 سورة، أولها الفاتحة وآخرها الناس.","The Quran has 114 surahs, from Al-Fatiha to An-Nas.")
q("religion","CD",9,"all","ما أول كلمة نزلت من القرآن؟","What was the first word of the Quran revealed?",
  [("اقرأ","Iqra (Read)"),("الحمد","Al-Hamd"),("قل","Qul (Say)"),("يا أيها","O you")],0,"أول ما نزل: \"اقرأ باسم ربك الذي خلق\" في غار حراء.","The first revelation was \"Read in the name of your Lord\" in the cave of Hira.")
q("religion","CD",10,"all","إلى أي مدينة هاجر النبي ﷺ؟","To which city did the Prophet ﷺ migrate?",
  [("الطائف","Taif"),("المدينة المنورة","Madinah"),("القدس","Jerusalem"),("دمشق","Damascus")],1,"هاجر النبي ﷺ من مكة إلى المدينة المنورة، وبها بدأ التقويم الهجري.","He migrated from Makkah to Madinah; the Hijri calendar starts from it.")
q("religion","DE",13,"all","ما نسبة زكاة المال (النقود) إذا بلغت النصاب وحال عليها الحول؟","What is the zakat rate on money that reaches nisab for a full year?",
  [("1%","1%"),("2.5%","2.5%"),("5%","5%"),("10%","10%")],1,"زكاة النقود ربع العُشر أي 2.5%.","Zakat on money is one quarter of a tenth: 2.5%.")
q("religion","DE",14,"all","ما أطول سورة في القرآن الكريم؟","What is the longest surah in the Quran?",
  [("آل عمران","Al-Imran"),("البقرة","Al-Baqarah"),("النساء","An-Nisa"),("الكهف","Al-Kahf")],1,"سورة البقرة أطول السور، وعدد آياتها 286 آية.","Al-Baqarah is the longest, with 286 verses.")
q("religion","E",16,"all","في أي شهر هجري يؤدَّى الحج؟","In which Hijri month is Hajj performed?",
  [("رمضان","Ramadan"),("شوال","Shawwal"),("ذو الحجة","Dhul-Hijjah"),("محرم","Muharram")],2,"مناسك الحج في أيام من شهر ذي الحجة، ويوم عرفة هو التاسع منه.","Hajj rites take place in Dhul-Hijjah; the Day of Arafah is the 9th.")
q("religion","BCD",8,"male","صلاة الجمعة تجب جماعةً في المسجد على من؟","Friday prayer in congregation is obligatory upon whom?",
  [("الرجال البالغين","Adult men"),("الأطفال فقط","Children only"),("لا أحد","No one")],0,"صلاة الجمعة واجبة على الرجل البالغ المقيم، وتُصلى ركعتين بعد الخطبة.","Jumu'ah is obligatory on adult resident men: two rak'ahs after the sermon.")
q("religion","CDE",11,"female","السيدة خديجة رضي الله عنها كانت تعمل في:","Khadijah (may Allah be pleased with her) worked in:",
  [("التجارة","Trade"),("الزراعة","Farming"),("الطب","Medicine"),("التعليم","Teaching")],0,"كانت سيدة أعمال ناجحة تُدير قوافل تجارية، وهي أول من آمن بالنبي ﷺ.","She was a successful businesswoman running trade caravans, and the first to believe in the Prophet ﷺ.")

# ---------------- ECONOMY ----------------
q("economy","A",2,"all","أين نشتري الخبز؟","Where do we buy bread?",
  [("من المخبز","From the bakery"),("من المستشفى","From the hospital"),("من المدرسة","From the school")],0,"المخبز يصنع الخبز ويبيعه.","The bakery makes and sells bread.")
q("economy","AB",3,"all","لماذا نذهب إلى العمل؟","Why do people go to work?",
  [("لنكسب المال ونفيد الناس","To earn money and help others"),("لننام","To sleep"),("للعب فقط","Only to play")],0,"العمل يوفر دخلاً للأسرة ويقدّم خدمة للمجتمع.","Work earns income and provides services to society.")
q("economy","B",6,"all","إذا كثر الطلب على لعبة وقلّت الكمية في المتاجر، ماذا يحدث لسعرها غالباً؟","If many people want a toy but stores have few, what usually happens to its price?",
  [("يرتفع","It goes up"),("ينخفض","It goes down"),("لا يتغير","It stays the same")],0,"قانون العرض والطلب: كثرة الطلب مع قلة المعروض ترفع السعر.","Supply and demand: high demand with low supply raises prices.")
q("economy","C",9,"all","ما معنى \"التضخم\"؟","What does \"inflation\" mean?",
  [("ارتفاع عام في الأسعار","A general rise in prices"),("زيادة عدد السكان","Population growth"),("انخفاض الأسعار","Falling prices"),("زيادة الرواتب فقط","Only salaries rising")],0,"التضخم يعني أن المال نفسه يشتري أشياء أقل مع الوقت.","Inflation means the same money buys less over time.")
q("economy","C",10,"all","ما العملة الرسمية للمملكة العربية السعودية؟","What is the official currency of Saudi Arabia?",
  [("الدرهم","Dirham"),("الريال","Riyal"),("الدينار","Dinar"),("الجنيه","Pound")],1,"الريال السعودي هو العملة الرسمية، ويصدره البنك المركزي السعودي (ساما).","The Saudi riyal, issued by the Saudi Central Bank (SAMA).", region="SA")
q("economy","DE",13,"all","ماذا يقيس \"الناتج المحلي الإجمالي\"؟","What does GDP measure?",
  [("قيمة السلع والخدمات المنتجة في الدولة خلال سنة","Value of goods and services produced in a country in a year"),("عدد السكان","Population"),("مساحة الدولة","Country area"),("حجم الديون","Total debt")],0,"الناتج المحلي الإجمالي أهم مقياس لحجم اقتصاد الدولة.","GDP is the main measure of an economy's size.")
q("economy","D",14,"all","ما هي \"رؤية السعودية 2030\"؟","What is Saudi Vision 2030?",
  [("خطة لتنويع الاقتصاد وتقليل الاعتماد على النفط","A plan to diversify the economy beyond oil"),("مسابقة رياضية","A sports competition"),("اسم قمر صناعي","A satellite name"),("نظام مروري","A traffic law")],0,"رؤية 2030 تهدف لتنويع مصادر الدخل وتنمية السياحة والصناعة والتقنية.","Vision 2030 aims to diversify income through tourism, industry and tech.", region="SA")
q("economy","E",17,"all","عندما يرفع البنك المركزي سعر الفائدة، فالهدف غالباً:","When a central bank raises interest rates, the goal is usually to:",
  [("خفض التضخم","Reduce inflation"),("زيادة الاقتراض","Increase borrowing"),("طباعة نقود أكثر","Print more money"),("رفع الأسعار","Raise prices")],0,"رفع الفائدة يقلل الاقتراض والإنفاق فيخفّ ارتفاع الأسعار.","Higher rates reduce borrowing and spending, cooling inflation.")
q("economy","E",18,"all","\"تكلفة الفرصة البديلة\" تعني:","\"Opportunity cost\" means:",
  [("قيمة أفضل بديل تخليت عنه عند اتخاذ قرار","The value of the best alternative you gave up"),("سعر السلعة","The price of a product"),("الضريبة","A tax"),("ربح الشركة","Company profit")],0,"مثال: إن قضيت ساعتين في اللعب فتكلفتهما هي ما كنت ستنجزه في المذاكرة.","E.g. two hours of gaming cost you the studying you could have done.")

# ---------------- COMMERCE ----------------
q("commerce","A",2,"all","اشتريت حلوى بريال وأعطيت البائع ريالين. كم يرجع لك؟","Candy costs 1 riyal and you pay 2. How much change do you get?",
  [("ريال واحد","1 riyal"),("ريالان","2 riyals"),("لا شيء","Nothing")],0,"2 − 1 = 1 ريال.","2 − 1 = 1 riyal.")
q("commerce","B",5,"all","اشترى أحمد قلماً بـ 3 ريال وباعه بـ 5 ريال. كم ربح؟","Ahmed bought a pen for 3 and sold it for 5 riyals. What was his profit?",
  [("ريالان","2 riyals"),("8 ريال","8 riyals"),("3 ريال","3 riyals")],0,"الربح = سعر البيع − سعر الشراء = 5 − 3 = 2.","Profit = selling price − cost = 5 − 3 = 2.")
q("commerce","BC",7,"all","ما أهم شيء يجعل الزبون يعود للمتجر؟","What most makes a customer come back to a shop?",
  [("الأمانة والخدمة الجيدة","Honesty and good service"),("رفع الأسعار","Raising prices"),("إغلاق المتجر مبكراً","Closing early"),("عدم الرد على الأسئلة","Ignoring questions")],0,"الثقة والخدمة الممتازة أساس نجاح أي تجارة.","Trust and great service are the basis of any successful business.")
q("commerce","C",10,"all","متجر باع 20 قطعة بسعر 10 ريال، وتكاليفه 120 ريال. كم صافي الربح؟","A shop sold 20 items at 10 riyals; costs were 120. What is the net profit?",
  [("80 ريال","80"),("200 ريال","200"),("120 ريال","120"),("320 ريال","320")],0,"الإيراد 200 − التكاليف 120 = 80 ريال.","Revenue 200 − costs 120 = 80.")
q("commerce","D",13,"all","ما المقصود بـ \"رأس المال\" في المشروع؟","What is \"capital\" in a business?",
  [("المال والأصول المستخدمة لبدء المشروع وتشغيله","Money and assets used to start and run it"),("الأرباح الشهرية","Monthly profits"),("اسم الشركة","Company name"),("عدد الموظفين","Number of employees")],0,"رأس المال هو ما يُستثمر في المشروع من نقود ومعدات.","Capital is the money and equipment invested.")
q("commerce","D",14,"all","ما الفرق بين \"الإيراد\" و\"الربح\"؟","What's the difference between revenue and profit?",
  [("الربح = الإيراد − التكاليف","Profit = revenue − costs"),("لا فرق","No difference"),("الإيراد = الربح − التكاليف","Revenue = profit − costs"),("الربح دائماً أكبر","Profit is always bigger")],0,"قد يكون الإيراد كبيراً لكن الربح صغيراً إذا ارتفعت التكاليف.","Revenue can be large while profit is small if costs are high.")
q("commerce","E",16,"all","\"نقطة التعادل\" في المشروع هي:","A business's \"break-even point\" is when:",
  [("تتساوى الإيرادات مع التكاليف","Revenue equals costs"),("تتضاعف الأرباح","Profits double"),("يُغلق المشروع","It closes"),("يُوظَّف موظف جديد","A new hire joins")],0,"بعد نقطة التعادل يبدأ المشروع بتحقيق الربح.","After break-even, the business starts making profit.")
q("commerce","E",18,"all","تكلفة المنتج 40 ريال، وتريد هامش ربح 25% من سعر البيع. كم يكون سعر البيع؟","Cost is 40 SAR and you want a 25% margin on the selling price. What's the price?",
  [("50 ريال","50"),("53.3 ريال","53.3"),("45 ريال","45"),("60 ريال","60")],1,"السعر = التكلفة ÷ (1 − 0.25) = 40 ÷ 0.75 ≈ 53.3 ريال. (50 تعطي هامشاً 20% فقط).","Price = cost ÷ (1 − 0.25) = 53.3. (50 gives only a 20% margin.)")
q("commerce","CDE",12,"female","ما الذي يساعد صاحبة مشروع منزلي (مثل الحلويات) على زيادة مبيعاتها؟","What helps a home-business owner (e.g. desserts) increase sales?",
  [("جودة ثابتة وتصوير جيد وتسويق عبر التواصل","Consistent quality, good photos, social marketing"),("رفع السعر دون سبب","Raising prices for no reason"),("تغيير الوصفة كل يوم","Changing the recipe daily"),("عدم تحديد سعر","No fixed price")],0,"الجودة الثابتة والعرض الجذاب والتسويق الذكي أساس نمو المشاريع المنزلية.","Consistent quality, attractive presentation and smart marketing drive growth.")
q("commerce","CDE",12,"male","ما أول خطوة قبل فتح مشروع (مثل مغسلة سيارات)؟","What's the first step before opening a business (e.g. a car wash)?",
  [("دراسة السوق والمنافسين","Study the market and competitors"),("شراء أغلى المعدات","Buy the most expensive equipment"),("الاقتراض فوراً","Borrow immediately"),("اختيار لون الشعار","Pick a logo colour")],0,"دراسة السوق تبيّن هل يوجد طلب كافٍ وما السعر المناسب.","Market research shows whether demand exists and what price fits.")

# ---------------- FINANCE ----------------
q("finance","A",2,"all","أين نضع النقود لنوفرها؟","Where do we put money to save it?",
  [("في الحصالة","In a piggy bank"),("في سلة المهملات","In the bin"),("تحت المطر","Out in the rain")],0,"الحصالة تساعدنا على الادخار شيئاً فشيئاً.","A piggy bank helps us save little by little.")
q("finance","AB",4,"all","معك 10 ريال. ما التصرف الذكي؟","You have 10 riyals. What is the smart choice?",
  [("أصرف جزءاً وأدّخر جزءاً","Spend some, save some"),("أصرفها كلها فوراً","Spend it all now"),("أرميها","Throw it away")],0,"قاعدة بسيطة: ادّخر جزءاً من كل مبلغ تحصل عليه.","Simple rule: save part of every amount you get.")
q("finance","BC",7,"all","ادخرت 5 ريال كل أسبوع. كم تجمع في 4 أسابيع؟","You save 5 riyals a week. How much after 4 weeks?",
  [("20 ريال","20"),("9 ريال","9"),("15 ريال","15")],0,"5 × 4 = 20 ريال.","5 × 4 = 20.")
q("finance","C",10,"all","ما الفرق بين \"الحاجة\" و\"الرغبة\"؟","What's the difference between a need and a want?",
  [("الحاجة ضرورية للحياة والرغبة شيء نحبه وليس ضرورياً","A need is essential; a want is nice but not essential"),("لا فرق","No difference"),("الرغبة أهم دائماً","Wants always matter more"),("الحاجة غالية دائماً","Needs are always expensive")],0,"الطعام حاجة، أما اللعبة الجديدة فرغبة؛ نقدّم الحاجات أولاً.","Food is a need, a new toy is a want; needs come first.")
q("finance","D",13,"all","ما فائدة إعداد \"ميزانية\" شهرية؟","Why make a monthly budget?",
  [("لمعرفة الدخل والمصروفات والتحكم فيها","To know and control income and spending"),("لزيادة المصروفات","To spend more"),("لا فائدة","No benefit"),("لإخفاء المال","To hide money")],0,"الميزانية تمنع الإسراف وتساعدك على الادخار لأهدافك.","A budget prevents overspending and helps you save for goals.")
q("finance","DE",15,"all","قاعدة 50/30/20 في الميزانية تعني:","The 50/30/20 budgeting rule means:",
  [("50% للضروريات و30% للرغبات و20% للادخار","50% needs, 30% wants, 20% savings"),("50% ادخار","50% savings"),("20% للضروريات","20% needs"),("30% ضرائب","30% taxes")],0,"تقسيم بسيط يضمن تغطية الضروريات وبناء مدخرات.","A simple split that covers needs and builds savings.")
q("finance","E",17,"all","ما \"صندوق الطوارئ\"؟","What is an emergency fund?",
  [("مدخرات تغطي مصاريف 3–6 أشهر للظروف المفاجئة","Savings covering 3–6 months of expenses"),("قرض بنكي","A bank loan"),("بطاقة ائتمان","A credit card"),("استثمار في الأسهم","Stock investment")],0,"يحميك من الاقتراض عند فقدان عمل أو مصروف مفاجئ.","It protects you from debt when surprises happen.")
q("finance","E",19,"all","استثمرت 1000 ريال بعائد 10% سنوياً مع إعادة استثمار الأرباح. كم تصبح بعد سنتين؟","You invest 1000 SAR at 10% a year, reinvesting gains. Value after 2 years?",
  [("1200","1200"),("1210","1210"),("1100","1100"),("1020","1020")],1,"السنة الأولى 1100، والثانية 1100 × 1.1 = 1210؛ هذا هو \"العائد المركب\".","Year 1: 1100; year 2: 1100 × 1.1 = 1210 — compound growth.")

# ---------------- ENGINEERING ----------------
q("engineering","A",2,"all","أي شكل يتدحرج بسهولة؟","Which shape rolls easily?",
  [("الدائرة (العجلة)","Circle (wheel)"),("المربع","Square"),("المثلث","Triangle")],0,"العجلات دائرية لأنها تتدحرج بسهولة.","Wheels are round because circles roll easily.")
q("engineering","AB",4,"all","ماذا نستخدم لتثبيت مسمار في الخشب؟","What tool do we use to drive a nail into wood?",
  [("المطرقة","Hammer"),("الملعقة","Spoon"),("المقص","Scissors")],0,"المطرقة أداة لدق المسامير.","A hammer drives nails.")
q("engineering","B",6,"all","ما الذي يجعل المصباح يضيء؟","What makes a light bulb glow?",
  [("الكهرباء","Electricity"),("الماء","Water"),("الهواء","Air")],0,"يمر التيار الكهربائي في المصباح فيُنتج ضوءاً.","Electric current passes through the bulb and produces light.")
q("engineering","C",9,"all","ما الآلة البسيطة المستخدمة في المنحدر لرفع الأشياء بجهد أقل؟","Which simple machine lets you lift loads with less effort using a slope?",
  [("المستوى المائل","Inclined plane"),("البكرة","Pulley"),("المسمار","Nail"),("الحبل","Rope")],0,"المستوى المائل يقلل القوة المطلوبة مقابل مسافة أطول.","An inclined plane reduces force needed over a longer distance.")
q("engineering","C",11,"all","لماذا تُصنع الأسلاك الكهربائية من النحاس؟","Why are electric wires made of copper?",
  [("لأنه موصل جيد للكهرباء","It conducts electricity well"),("لأنه خفيف جداً","It's very light"),("لأنه عازل","It's an insulator"),("لأنه رخيص فقط","Only because it's cheap")],0,"النحاس من أفضل الموصلات، ويُغلف بالبلاستيك العازل للأمان.","Copper is an excellent conductor, wrapped in plastic for safety.")
q("engineering","D",13,"all","حسب قانون أوم، إذا كان الجهد 12 فولت والمقاومة 4 أوم، فالتيار:","By Ohm's law, with 12 V and 4 Ω, the current is:",
  [("3 أمبير","3 A"),("48 أمبير","48 A"),("8 أمبير","8 A"),("16 أمبير","16 A")],0,"التيار = الجهد ÷ المقاومة = 12 ÷ 4 = 3 أمبير.","I = V ÷ R = 12 ÷ 4 = 3 A.")
q("engineering","D",15,"all","في البرمجة، ما \"الحلقة\" (Loop)؟","In programming, what is a loop?",
  [("تكرار مجموعة أوامر عدة مرات","Repeating instructions several times"),("خطأ في البرنامج","A bug"),("نوع من الشاشات","A type of screen"),("كلمة مرور","A password")],0,"الحلقات توفّر كتابة الكود نفسه مرات كثيرة.","Loops save writing the same code repeatedly.")
q("engineering","E",17,"all","لماذا تُبنى الجسور غالباً على شكل مثلثات (الجملونات)؟","Why do many bridges use triangle trusses?",
  [("المثلث شكل ثابت يوزّع الأحمال ولا يتشوه","Triangles are rigid and spread loads"),("لأنه أجمل فقط","Only for looks"),("لأنه أرخص دائماً","Always cheaper"),("لتقليل الطول","To shorten length")],0,"المثلث لا يتغير شكله تحت الضغط دون تغيير طول أضلاعه.","A triangle can't deform without changing a side length.")
q("engineering","E",19,"all","ما مصدر الطاقة في الألواح الشمسية الكهروضوئية؟","What do photovoltaic solar panels convert into electricity?",
  [("ضوء الشمس مباشرة","Sunlight directly"),("حرارة الأرض","Earth's heat"),("الرياح","Wind"),("الماء","Water")],0,"الخلايا الكهروضوئية تحول الضوء إلى كهرباء مباشرة عبر أشباه الموصلات.","PV cells turn light directly into electricity via semiconductors.")

# ---------------- CRAFTS ----------------
q("crafts","A",1,"all","ماذا نستخدم لقص الورق؟","What do we use to cut paper?",
  [("المقص","Scissors"),("الملعقة","Spoon"),("الفرشاة","Brush")],0,"المقص أداة القص، ونستخدمه بحذر.","Scissors cut paper; use them carefully.")
q("crafts","AB",3,"all","ماذا يحتاج النبات لينمو؟","What does a plant need to grow?",
  [("الماء والشمس","Water and sunlight"),("الحلوى","Candy"),("الظلام فقط","Only darkness")],0,"النبات يحتاج الماء والضوء والتربة والهواء.","Plants need water, light, soil and air.")
q("crafts","B",6,"all","ما الأداة التي يستخدمها النجار لقطع الخشب؟","What tool does a carpenter use to cut wood?",
  [("المنشار","Saw"),("المكنسة","Broom"),("المسطرة","Ruler")],0,"المنشار أداة النجار الأساسية للقطع.","The saw is the carpenter's main cutting tool.")
q("crafts","BC",8,"all","لماذا نقيس مرتين قبل القص؟","Why measure twice before cutting?",
  [("لتجنب الخطأ وهدر المواد","To avoid mistakes and waste"),("لإضاعة الوقت","To waste time"),("لأن القياس ممتع فقط","Only for fun")],0,"\"قِس مرتين واقطع مرة\" قاعدة ذهبية في كل الحرف.","\"Measure twice, cut once\" is a golden rule.")
q("crafts","C",10,"all","ما الحرفة السعودية التقليدية المعروفة بنسج سعف النخيل؟","Which traditional Saudi craft weaves palm fronds?",
  [("الخوص (السفافة)","Khoos (palm weaving)"),("الحدادة","Blacksmithing"),("الزجاج","Glassmaking"),("الخزف","Pottery")],0,"الخوص حرفة تراثية تُصنع بها السلال والحُصر من سعف النخيل.","Khoos makes baskets and mats from palm fronds.", region="SA")
q("crafts","D",13,"all","ما فائدة \"السماد العضوي\" (الكمبوست)؟","What is compost used for?",
  [("تغذية التربة من بقايا الطعام والنباتات","Enriching soil from food and plant waste"),("تنظيف الملابس","Cleaning clothes"),("وقود للسيارات","Car fuel"),("طلاء الجدران","Painting walls")],0,"الكمبوست يحوّل النفايات العضوية إلى سماد طبيعي ويقلل النفايات.","Compost turns organic waste into natural fertiliser.")
q("crafts","DE",15,"all","عند استخدام المثقاب الكهربائي، ما أهم إجراء سلامة؟","What's the key safety step when using a power drill?",
  [("لبس النظارة الواقية وتثبيت القطعة","Wear goggles and clamp the piece"),("الإمساك بالقطعة باليد فقط","Hold the piece by hand"),("العمل بسرعة دون تركيز","Work fast without focus"),("لبس ملابس واسعة","Wear loose clothes")],0,"النظارة تحمي العين، والتثبيت يمنع دوران القطعة.","Goggles protect eyes; clamping stops the piece spinning.")
q("crafts","E",17,"all","لماذا يُعدّ تعلم حرفة يدوية مفيداً اقتصادياً؟","Why is learning a craft economically valuable?",
  [("يمكن أن تتحول لمصدر دخل أو مشروع صغير","It can become income or a small business"),("لا قيمة لها اليوم","It has no value today"),("تمنع التعلم","It prevents learning"),("مكلفة دائماً","Always costly")],0,"الحرف المتقنة مطلوبة وتفتح باب العمل الحر والمشاريع.","Skilled crafts are in demand and open freelance paths.")
q("crafts","BCD",8,"female","في الخياطة، ما الأداة التي تحمي الإصبع عند دفع الإبرة؟","In sewing, which tool protects your finger when pushing the needle?",
  [("الكشتبان","Thimble"),("البكرة","Spool"),("الدبوس","Pin")],0,"الكشتبان غطاء معدني يوضع على الإصبع.","A thimble is a metal cap worn on the finger.")
q("crafts","BCD",8,"male","ما الأداة المستخدمة لشد البراغي وفكها؟","Which tool tightens and loosens screws?",
  [("المفك","Screwdriver"),("المقص","Scissors"),("الفرشاة","Brush")],0,"المفك يناسب رأس البرغي، سواء مسطحاً أو صليبياً.","Screwdrivers fit flat or cross-head screws.")

# ---------------- SCIENCE ----------------
q("science","A",1,"all","ما لون السماء في النهار الصافي؟","What colour is a clear daytime sky?",
  [("أزرق","Blue"),("أخضر","Green"),("أحمر","Red")],0,"تبدو السماء زرقاء بسبب تشتت ضوء الشمس.","The sky looks blue because sunlight scatters.")
q("science","A",2,"all","أي حيوان يعيش في الماء؟","Which animal lives in water?",
  [("السمكة","Fish"),("الجمل","Camel"),("القطة","Cat")],0,"السمك يتنفس في الماء بالخياشيم.","Fish breathe in water using gills.")
q("science","B",5,"all","ما أقرب نجم إلى الأرض؟","What is the closest star to Earth?",
  [("الشمس","The Sun"),("القمر","The Moon"),("المريخ","Mars")],0,"الشمس نجم، أما القمر فتابع للأرض والمريخ كوكب.","The Sun is a star; the Moon is a satellite, Mars a planet.")
q("science","B",6,"all","ما حالة الماء عندما يتجمد؟","What does water become when it freezes?",
  [("ثلج (صلب)","Ice (solid)"),("بخار","Steam"),("يبقى سائلاً","Stays liquid")],0,"يتجمد الماء عند صفر درجة مئوية.","Water freezes at 0 °C.")
q("science","C",9,"all","ما الغاز الذي نحتاجه للتنفس؟","Which gas do we need to breathe?",
  [("الأكسجين","Oxygen"),("ثاني أكسيد الكربون","Carbon dioxide"),("الهيليوم","Helium"),("النيتروجين","Nitrogen")],0,"نستنشق الأكسجين ونزفر ثاني أكسيد الكربون.","We inhale oxygen and exhale carbon dioxide.")
q("science","C",11,"all","كم عدد كواكب المجموعة الشمسية؟","How many planets are in the Solar System?",
  [("8","8"),("9","9"),("7","7"),("10","10")],0,"ثمانية كواكب؛ صُنّف بلوتو كوكباً قزماً عام 2006.","Eight; Pluto was reclassified as a dwarf planet in 2006.")
q("science","D",13,"all","ما العضو المسؤول عن ضخ الدم في الجسم؟","Which organ pumps blood around the body?",
  [("القلب","Heart"),("الرئة","Lung"),("الكبد","Liver"),("المعدة","Stomach")],0,"القلب عضلة تضخ الدم عبر الأوعية الدموية.","The heart is a muscle pumping blood through vessels.")
q("science","D",14,"all","ما الرمز الكيميائي للماء؟","What is the chemical formula of water?",
  [("H₂O","H₂O"),("CO₂","CO₂"),("O₂","O₂"),("NaCl","NaCl")],0,"جزيء الماء: ذرتا هيدروجين وذرة أكسجين.","Two hydrogen atoms and one oxygen atom.")
q("science","E",16,"all","ما وحدة قياس القوة في النظام الدولي؟","What is the SI unit of force?",
  [("النيوتن","Newton"),("الجول","Joule"),("الواط","Watt"),("الباسكال","Pascal")],0,"النيوتن = كيلوجرام × متر/ثانية².","1 N = 1 kg·m/s².")
q("science","E",18,"all","ما وظيفة الميتوكوندريا في الخلية؟","What is the role of mitochondria in a cell?",
  [("إنتاج الطاقة","Producing energy"),("تخزين المعلومات الوراثية فقط","Only storing DNA"),("صنع البروتين","Making protein"),("حماية الخلية","Protecting the cell")],0,"تُسمى \"مصنع الطاقة\" لأنها تنتج جزيئات ATP.","Called the powerhouse: they produce ATP.")
q("science","CDE",12,"female","من أول امرأة سعودية وعربية تصل إلى الفضاء (2023)؟","Who was the first Saudi and Arab woman in space (2023)?",
  [("ريانة برناوي","Rayyanah Barnawi"),("حياة سندي","Hayat Sindi"),("غادة المطيري","Ghada Al-Mutairi"),("سارة الأميري","Sarah Al Amiri")],0,"ريانة برناوي عالمة أبحاث الخلايا الجذعية، شاركت في مهمة إلى محطة الفضاء الدولية.","Rayyanah Barnawi, a stem-cell researcher, flew to the ISS.")
q("science","CDE",12,"male","من أول رائد فضاء عربي ومسلم (1985)؟","Who was the first Arab and Muslim astronaut (1985)?",
  [("الأمير سلطان بن سلمان","Prince Sultan bin Salman"),("هزاع المنصوري","Hazza Al Mansouri"),("علي القرني","Ali AlQarni"),("محمد فارس","Muhammed Faris")],0,"شارك الأمير سلطان بن سلمان في رحلة المكوك ديسكفري عام 1985.","He flew on Space Shuttle Discovery in 1985.")

# ---------------- MATH ----------------
q("math","A",1,"all","كم إصبعاً في اليد الواحدة؟","How many fingers are on one hand?",
  [("5","5"),("3","3"),("10","10")],0,"في اليد الواحدة خمسة أصابع.","One hand has five fingers.")
q("math","A",2,"all","معك تفاحتان وأخذت واحدة أخرى. كم أصبح معك؟","You have 2 apples and get 1 more. How many now?",
  [("3","3"),("2","2"),("4","4")],0,"2 + 1 = 3.","2 + 1 = 3.")
q("math","A",3,"all","أي عدد أكبر؟","Which number is bigger?",
  [("7","7"),("4","4"),("2","2")],0,"7 أكبر من 4 ومن 2.","7 is bigger than 4 and 2.")
q("math","B",5,"all","كم يساوي 6 × 3؟","What is 6 × 3?",
  [("18","18"),("9","9"),("15","15")],0,"6 × 3 = 6 + 6 + 6 = 18.","6 × 3 = 6 + 6 + 6 = 18.")
q("math","B",7,"all","نصف 20 يساوي:","Half of 20 is:",
  [("10","10"),("5","5"),("15","15")],0,"20 ÷ 2 = 10.","20 ÷ 2 = 10.")
q("math","C",9,"all","كم يساوي 25% من 80؟","What is 25% of 80?",
  [("20","20"),("25","25"),("40","40"),("16","16")],0,"25% = ربع، و80 ÷ 4 = 20.","25% is a quarter: 80 ÷ 4 = 20.")
q("math","C",11,"all","مساحة مستطيل طوله 8 سم وعرضه 5 سم:","Area of a rectangle 8 cm by 5 cm:",
  [("40 سم²","40 cm²"),("26 سم²","26 cm²"),("13 سم²","13 cm²"),("45 سم²","45 cm²")],0,"المساحة = الطول × العرض = 8 × 5 = 40.","Area = length × width = 40.")
q("math","D",13,"all","حل المعادلة: 3س + 5 = 20","Solve: 3x + 5 = 20",
  [("س = 5","x = 5"),("س = 15","x = 15"),("س = 25/3","x = 25/3"),("س = 3","x = 3")],0,"3س = 15 ← س = 5.","3x = 15 → x = 5.")
q("math","D",15,"all","مجموع زوايا المثلث يساوي:","The angles of a triangle add up to:",
  [("180°","180°"),("360°","360°"),("90°","90°"),("270°","270°")],0,"مجموع زوايا أي مثلث 180 درجة.","Any triangle's angles sum to 180°.")
q("math","E",17,"all","ما احتمال ظهور عدد زوجي عند رمي حجر نرد؟","Probability of rolling an even number on a die?",
  [("1/2","1/2"),("1/3","1/3"),("1/6","1/6"),("2/3","2/3")],0,"الأعداد الزوجية 2 و4 و6، أي 3 من 6 = 1/2.","Evens: 2, 4, 6 → 3 of 6 = 1/2.")
q("math","E",19,"all","ما قيمة 2¹⁰؟","What is 2¹⁰?",
  [("1024","1024"),("512","512"),("2048","2048"),("100","100")],0,"2¹⁰ = 1024، ولهذا الكيلوبايت ≈ 1024 بايت.","2¹⁰ = 1024 — why a kilobyte ≈ 1024 bytes.")

# ---------------- ARABIC ----------------
q("arabic","A",1,"all","ما أول حرف في كلمة \"أسد\"؟","What is the first letter of the word \"أسد\" (lion)?",
  [("أ","أ"),("س","س"),("د","د")],0,"أسد تبدأ بحرف الألف.","أسد starts with Alif.")
q("arabic","A",3,"all","ما عكس كلمة \"كبير\"؟","What is the opposite of \"كبير\" (big)?",
  [("صغير","صغير (small)"),("طويل","طويل (tall)"),("سريع","سريع (fast)")],0,"عكس كبير: صغير.","The opposite of كبير is صغير.")
q("arabic","B",5,"all","ما جمع كلمة \"كتاب\"؟","What is the plural of \"كتاب\" (book)?",
  [("كُتُب","كُتُب"),("كاتب","كاتب"),("مكتبة","مكتبة")],0,"جمع كتاب: كُتُب (جمع تكسير).","The plural of كتاب is كُتُب.")
q("arabic","BC",7,"all","ما مرادف كلمة \"سعيد\"؟","What is a synonym of \"سعيد\" (happy)?",
  [("فرحان","فرحان"),("حزين","حزين"),("غاضب","غاضب")],0,"سعيد وفرحان بمعنى واحد.","سعيد and فرحان have the same meaning.")
q("arabic","C",10,"all","في جملة \"قرأ الطالبُ الدرسَ\"، ما الفاعل؟","In \"قرأ الطالبُ الدرسَ\", which word is the subject (فاعل)?",
  [("الطالبُ","الطالبُ"),("قرأ","قرأ"),("الدرسَ","الدرسَ"),("لا يوجد","None")],0,"الطالب هو من قام بالفعل، وهو مرفوع.","الطالب performed the action, so it is the فاعل (nominative).")
q("arabic","D",13,"all","ما نوع الهمزة في كلمة \"استخدام\"؟","What type of hamza is at the start of \"استخدام\"?",
  [("همزة وصل","همزة وصل"),("همزة قطع","همزة قطع"),("همزة متوسطة","همزة متوسطة"),("لا يوجد همزة","None")],0,"مصدر الفعل السداسي تبدأ بهمزة وصل.","Verbal nouns of six-letter verbs start with همزة وصل.")
q("arabic","E",16,"all","من الملقب بـ \"أمير الشعراء\"؟","Who is known as the \"Prince of Poets\"?",
  [("أحمد شوقي","Ahmed Shawqi"),("المتنبي","Al-Mutanabbi"),("حافظ إبراهيم","Hafez Ibrahim"),("نزار قباني","Nizar Qabbani")],0,"بويع أحمد شوقي أميراً للشعراء عام 1927.","Ahmed Shawqi was crowned Prince of Poets in 1927.")
q("arabic","E",18,"all","ما إعراب \"مجتهداً\" في: \"كان الطالبُ مجتهداً\"؟","What is the case role of \"مجتهداً\" in \"كان الطالبُ مجتهداً\"?",
  [("خبر كان منصوب","خبر كان (accusative)"),("اسم كان مرفوع","اسم كان (nominative)"),("مفعول به","Direct object"),("حال","حال")],0,"كان ترفع الاسم وتنصب الخبر.","كان makes its subject nominative and its predicate accusative.")

# ---------------- ENGLISH ----------------
q("english","A",2,"all","What colour is a banana? / ما لون الموز بالإنجليزية؟","What colour is a banana?",
  [("Yellow","Yellow"),("Blue","Blue"),("Black","Black")],0,"الموز لونه أصفر = Yellow.","A banana is yellow.")
q("english","A",3,"all","ما معنى كلمة \"Cat\"؟","What does \"Cat\" mean?",
  [("قطة","قطة (cat)"),("كلب","كلب (dog)"),("طائر","طائر (bird)")],0,"Cat تعني قطة.","Cat = قطة.")
q("english","B",5,"all","ما معنى \"Apple\"؟","What is \"Apple\" in Arabic?",
  [("تفاحة","تفاحة"),("برتقالة","برتقالة"),("موزة","موزة")],0,"Apple = تفاحة.","Apple = تفاحة.")
q("english","B",7,"all","اختر الصحيح: I ___ a student.","Choose the correct word: I ___ a student.",
  [("am","am"),("is","is"),("are","are")],0,"مع I نستخدم am.","With I we use am.")
q("english","C",9,"all","What is the plural of \"child\"?","What is the plural of \"child\"?",
  [("children","children"),("childs","childs"),("childes","childes"),("childrens","childrens")],0,"جمع child شاذ: children.","Child has an irregular plural: children.")
q("english","C",11,"all","Choose the past tense of \"go\":","Choose the past tense of \"go\":",
  [("went","went"),("goed","goed"),("gone","gone"),("goes","goes")],0,"go فعل شاذ، ماضيه went.","Go is irregular: went.")
q("english","D",13,"all","Choose the correct sentence:","Choose the correct sentence:",
  [("She doesn't like coffee.","She doesn't like coffee."),("She don't like coffee.","She don't like coffee."),("She not like coffee.","She not like coffee."),("She doesn't likes coffee.","She doesn't likes coffee.")],0,"مع she نستخدم doesn't ثم الفعل بدون s.","With she: doesn't + base verb.")
q("english","DE",15,"all","\"Sustainable\" means:","\"Sustainable\" means:",
  [("مستدام","مستدام"),("مؤقت","مؤقت"),("مكلف","مكلف"),("سريع","سريع")],0,"Sustainable = يمكن الاستمرار فيه دون استنزاف الموارد.","Able to continue without depleting resources.")
q("english","E",17,"all","If I ___ rich, I would travel the world.","If I ___ rich, I would travel the world.",
  [("were","were"),("am","am"),("will be","will be"),("be","be")],0,"الشرط الثاني (غير الواقعي): If + were + would.","Second conditional: If + were, would + verb.")

# ---------------- HEALTH ----------------
q("health","A",1,"all","متى نغسل أيدينا؟","When should we wash our hands?",
  [("قبل الأكل وبعده","Before and after eating"),("لا نغسلها أبداً","Never"),("مرة في الأسبوع","Once a week")],0,"غسل اليدين يحمينا من الجراثيم.","Handwashing protects us from germs.")
q("health","A",2,"all","كم مرة نفرش أسناننا في اليوم؟","How many times a day should we brush our teeth?",
  [("مرتين على الأقل","At least twice"),("لا داعي","No need"),("مرة في الشهر","Once a month")],0,"نفرش الأسنان صباحاً وقبل النوم.","Brush in the morning and before bed.")
q("health","B",5,"all","أي طعام صحي أكثر؟","Which food is healthier?",
  [("الخضار والفواكه","Vegetables and fruit"),("الحلوى","Candy"),("المشروبات الغازية","Soda")],0,"الخضار والفواكه غنية بالفيتامينات.","Fruit and vegetables are rich in vitamins.")
q("health","BC",7,"all","عند عبور الشارع نعبر من:","We cross the street at:",
  [("ممر المشاة","The pedestrian crossing"),("أي مكان","Anywhere"),("بين السيارات","Between cars")],0,"ممر المشاة والإشارة يحمياننا من الحوادث.","Crossings and signals keep us safe.")
q("health","C",9,"all","ما رقم الهلال الأحمر (الإسعاف) في السعودية؟","What is the ambulance (Red Crescent) number in Saudi Arabia?",
  [("997","997"),("998","998"),("999","999"),("911","911")],0,"997 للإسعاف، 998 للدفاع المدني، 999 للشرطة، و911 موحّد في بعض المناطق.","997 ambulance, 998 civil defence, 999 police; 911 unified in some regions.", region="SA")
q("health","C",11,"all","كم ساعة نوم يحتاجها طفل في عمر 10 سنوات تقريباً؟","About how much sleep does a 10-year-old need?",
  [("9–12 ساعة","9–12 hours"),("4 ساعات","4 hours"),("6 ساعات","6 hours"),("15 ساعة","15 hours")],0,"توصي الجمعيات الطبية بـ 9–12 ساعة للأعمار 6–12.","Medical guidance: 9–12 hours for ages 6–12.")
q("health","D",13,"all","ما أول ما تفعله عند جرح بسيط ينزف؟","First thing to do for a small bleeding cut?",
  [("الضغط عليه بقطعة نظيفة","Press with a clean cloth"),("وضع التراب","Put dirt on it"),("تجاهله","Ignore it"),("فركه بقوة","Rub it hard")],0,"الضغط المباشر يوقف النزيف، ثم التنظيف والتغطية.","Direct pressure stops bleeding; then clean and cover.")
q("health","DE",15,"all","ما الفيتامين الذي يُنتجه الجسم عند التعرض للشمس؟","Which vitamin does the body make in sunlight?",
  [("فيتامين د","Vitamin D"),("فيتامين ج","Vitamin C"),("فيتامين أ","Vitamin A"),("فيتامين ب12","Vitamin B12")],0,"فيتامين د مهم لصحة العظام.","Vitamin D is important for bones.")
q("health","E",17,"all","ما المعدل الطبيعي لنبض القلب للبالغ أثناء الراحة؟","What is a normal resting heart rate for an adult?",
  [("60–100 نبضة/دقيقة","60–100 bpm"),("20–40","20–40"),("120–160","120–160"),("200+","200+")],0,"المعدل الطبيعي 60–100، والرياضيون قد يكون أقل.","Normal is 60–100 bpm; athletes may be lower.")
q("health","DE",14,"female","ما المعدن الذي تحتاجه الفتيات بشكل خاص في سن البلوغ لتجنب فقر الدم؟","Which mineral do girls especially need in puberty to avoid anaemia?",
  [("الحديد","Iron"),("الصوديوم","Sodium"),("الرصاص","Lead"),("الزئبق","Mercury")],0,"الحديد موجود في اللحوم والعدس والسبانخ، ويُمتص أفضل مع فيتامين ج.","Iron is in meat, lentils and spinach; vitamin C helps absorption.")
q("health","DE",14,"male","قبل رفع الأوزان في النادي، ما الأهم لتجنب الإصابة؟","Before lifting weights, what matters most to avoid injury?",
  [("الإحماء وتعلّم الطريقة الصحيحة","Warm-up and correct technique"),("رفع أثقل وزن فوراً","Lift the heaviest weight at once"),("عدم شرب الماء","Avoid water"),("التمرين يومياً بلا راحة","Train daily with no rest")],0,"الإحماء والأسلوب الصحيح والتدرج تحمي العضلات والمفاصل.","Warm-up, form and gradual progress protect muscles and joints.")

# ---------------- ENVIRONMENT ----------------
q("environment","A",1,"all","أين نرمي النفايات؟","Where do we throw rubbish?",
  [("في سلة المهملات","In the bin"),("في الشارع","On the street"),("في البحر","In the sea")],0,"رمي النفايات في مكانها يحافظ على نظافة البيئة.","Binning rubbish keeps the environment clean.")
q("environment","AB",3,"all","ماذا نفعل بالصنبور بعد غسل اليدين؟","What do we do with the tap after washing hands?",
  [("نغلقه","Turn it off"),("نتركه مفتوحاً","Leave it running"),("نكسره","Break it")],0,"إغلاق الصنبور يوفر الماء.","Turning off the tap saves water.")
q("environment","B",5,"all","أي هذه المواد يمكن إعادة تدويرها؟","Which of these can be recycled?",
  [("علبة الألمنيوم","Aluminium can"),("قشر الموز","Banana peel"),("المنديل المستعمل","Used tissue")],0,"علب الألمنيوم تُعاد تدويرها بلا حدود تقريباً.","Aluminium cans can be recycled almost endlessly.")
q("environment","B",7,"all","ماذا تعني الأسهم الثلاثة على شكل مثلث على العبوات؟","What do three arrows in a triangle on packaging mean?",
  [("قابل لإعادة التدوير","Recyclable"),("خطر","Danger"),("ممنوع اللمس","Do not touch")],0,"رمز إعادة التدوير، وقد يحتوي رقماً يدل على نوع البلاستيك.","The recycling symbol; a number may show the plastic type.")
q("environment","C",9,"all","ما المقصود بالقاعدة 3R؟","What is the 3R rule?",
  [("التقليل، إعادة الاستخدام، إعادة التدوير","Reduce, Reuse, Recycle"),("اقرأ، اكتب، ارسم","Read, Write, Draw"),("اجرِ، اقفز، ارتح","Run, Jump, Rest"),("لا شيء مما سبق","None")],0,"الأولوية للتقليل ثم إعادة الاستخدام ثم التدوير.","Reduce first, then reuse, then recycle.")
q("environment","C",11,"all","كم سنة تقريباً تحتاج قارورة بلاستيكية لتتحلل؟","Roughly how long does a plastic bottle take to break down?",
  [("حوالي 450 سنة","About 450 years"),("سنة واحدة","1 year"),("10 سنوات","10 years"),("أسبوع","A week")],0,"تقديرات شائعة تصل إلى مئات السنين، ولذلك نقلل البلاستيك أحادي الاستخدام.","Estimates run to hundreds of years — so cut single-use plastic.")
q("environment","D",13,"all","ما هي \"مبادرة السعودية الخضراء\"؟","What is the Saudi Green Initiative?",
  [("مبادرة تشمل زراعة 10 مليارات شجرة وخفض الانبعاثات","Planting 10 billion trees and cutting emissions"),("ملعب كرة قدم","A football stadium"),("نوع سيارة","A car model"),("تطبيق ألعاب","A gaming app")],0,"أُطلقت عام 2021 للتشجير وحماية البيئة ومواجهة التغير المناخي.","Launched in 2021 for afforestation and climate action.", region="SA")
q("environment","D",15,"all","ما الغاز الرئيسي المسبب للاحتباس الحراري من حرق الوقود؟","Which main greenhouse gas comes from burning fuel?",
  [("ثاني أكسيد الكربون","Carbon dioxide"),("الأكسجين","Oxygen"),("الهيليوم","Helium"),("الأرغون","Argon")],0,"CO₂ يحبس الحرارة في الغلاف الجوي.","CO₂ traps heat in the atmosphere.")
q("environment","E",17,"all","ما مفهوم \"الاقتصاد الدائري\"؟","What is the \"circular economy\"?",
  [("إبقاء المواد قيد الاستخدام عبر إعادة الاستخدام والتدوير بدل رميها","Keeping materials in use via reuse and recycling"),("اقتصاد يعتمد على النفط","An oil-based economy"),("شراء أكثر","Buying more"),("نظام ضرائب","A tax system")],0,"بديل لنموذج \"خُذ – اصنع – ارمِ\"، ويقلل النفايات والتكلفة.","An alternative to take–make–dispose that cuts waste and cost.")
q("environment","E",19,"all","ما الطريقة الأفضل بيئياً للتعامل مع النفايات العضوية (بقايا الطعام)؟","What is the most eco-friendly way to handle food waste?",
  [("التسميد أو الهضم اللاهوائي لإنتاج سماد وغاز حيوي","Composting or anaerobic digestion for compost and biogas"),("الحرق المكشوف","Open burning"),("الدفن في المرادم دائماً","Always landfill"),("رميها في البحر","Dumping at sea")],0,"تحويلها لسماد أو طاقة يقلل غاز الميثان من المرادم.","Turning it into compost or energy reduces landfill methane.")

# ---------------- CITIZENSHIP ----------------
q("citizenship","A",2,"all","ما لون علم المملكة العربية السعودية؟","What colour is the flag of Saudi Arabia?",
  [("أخضر","Green"),("أحمر","Red"),("أزرق","Blue")],0,"العلم أخضر وعليه الشهادتان وسيف.","The flag is green with the Shahada and a sword.", region="SA")
q("citizenship","AB",4,"all","ما عاصمة المملكة العربية السعودية؟","What is the capital of Saudi Arabia?",
  [("الرياض","Riyadh"),("جدة","Jeddah"),("الدمام","Dammam")],0,"الرياض هي العاصمة.","Riyadh is the capital.", region="SA")
q("citizenship","B",6,"all","متى يكون اليوم الوطني السعودي؟","When is Saudi National Day?",
  [("23 سبتمبر","23 September"),("1 يناير","1 January"),("22 فبراير","22 February")],0,"23 سبتمبر ذكرى توحيد المملكة عام 1932، و22 فبراير يوم التأسيس.","23 Sept marks unification (1932); 22 Feb is Founding Day.", region="SA")
q("geography","C",9,"all","ما أكبر قارة في العالم مساحةً؟","Which is the largest continent by area?",
  [("آسيا","Asia"),("أفريقيا","Africa"),("أوروبا","Europe"),("أستراليا","Australia")],0,"آسيا أكبر القارات مساحة وسكاناً.","Asia is largest in area and population.")
q("citizenship","C",11,"all","من مؤسس المملكة العربية السعودية الحديثة؟","Who founded the modern Kingdom of Saudi Arabia?",
  [("الملك عبدالعزيز آل سعود","King Abdulaziz Al Saud"),("الملك فيصل","King Faisal"),("الملك فهد","King Fahd"),("الملك خالد","King Khalid")],0,"وحّد الملك عبدالعزيز المملكة وأعلن قيامها عام 1932.","King Abdulaziz unified and declared the Kingdom in 1932.", region="SA")
q("geography","D",13,"all","ما أطول نهر في العالم (حسب أغلب المصادر)؟","What is the longest river in the world (per most sources)?",
  [("النيل","The Nile"),("الأمازون","The Amazon"),("الفرات","The Euphrates"),("الدانوب","The Danube")],0,"النيل حوالي 6650 كم، مع جدل علمي حول الأمازون.","The Nile ~6,650 km, though some argue for the Amazon.")
q("citizenship","DE",15,"all","ما أهمية التصويت والمشاركة المجتمعية؟","Why does civic participation matter?",
  [("تساعد على تطوير المجتمع واتخاذ قرارات أفضل","It helps improve society and decisions"),("لا أهمية لها","It doesn't matter"),("مضيعة للوقت","A waste of time"),("للكبار فقط","Only for elders")],0,"المشاركة والتطوع يعززان الانتماء والتنمية.","Participation and volunteering build belonging and development.")
q("citizenship","E",17,"all","أي منظمة دولية مقرها الرئيسي في نيويورك وتضم معظم دول العالم؟","Which global organisation is headquartered in New York with almost all countries as members?",
  [("الأمم المتحدة","United Nations"),("جامعة الدول العربية","Arab League"),("الاتحاد الأوروبي","European Union"),("منظمة أوبك","OPEC")],0,"تأسست الأمم المتحدة عام 1945 وتضم 193 دولة.","Founded 1945; 193 member states.")

# ---------------- LIFE SKILLS ----------------
q("life_skills","A",1,"all","ماذا نقول عندما يساعدنا أحد؟","What do we say when someone helps us?",
  [("شكراً","Thank you"),("لا شيء","Nothing"),("اذهب","Go away")],0,"الشكر من الأخلاق الجميلة.","Saying thank you is good manners.")
q("life_skills","A",3,"all","إذا ضعت في السوق، لمن تذهب؟","If you get lost in a mall, who should you go to?",
  [("موظف الأمن أو موظف المتجر","A security guard or shop staff"),("أي شخص غريب في الخارج","Any stranger outside"),("أخرج وحدي للشارع","Walk out to the street alone")],0,"اطلب المساعدة من موظف رسمي وابقَ داخل المكان.","Ask an official staff member and stay inside.")
q("life_skills","B",5,"all","شخص غريب على الإنترنت يطلب صورتك أو عنوانك. ماذا تفعل؟","A stranger online asks for your photo or address. What do you do?",
  [("أرفض وأخبر والديّ","Refuse and tell my parents"),("أرسلها فوراً","Send it right away"),("أطلب منه هدية","Ask for a gift")],0,"لا نشارك معلوماتنا الشخصية أبداً، ونخبر الوالدين.","Never share personal info; tell your parents.")
q("life_skills","BC",8,"all","لديك واجب ولعب. ما الترتيب الأفضل؟","You have homework and playtime. What's the best order?",
  [("الواجب أولاً ثم اللعب","Homework first, then play"),("اللعب طوال اليوم","Play all day"),("لا أعمل الواجب","Skip homework")],0,"إنجاز المهم أولاً يجعل وقت اللعب ممتعاً بلا قلق.","Doing important tasks first makes play stress-free.")
q("life_skills","C",10,"all","ما أفضل كلمة مرور؟","Which is the best password?",
  [("Sa#7kLm!29q","Sa#7kLm!29q"),("123456","123456"),("password","password"),("اسمي","My name")],0,"كلمة المرور القوية طويلة وتجمع حروفاً وأرقاماً ورموزاً.","Strong passwords are long and mix letters, numbers and symbols.")
q("life_skills","D",13,"all","اختلفت مع صديقك. ما أفضل تصرف؟","You disagree with a friend. What's best?",
  [("أستمع له وأعبّر عن رأيي بهدوء","Listen and calmly share my view"),("أصرخ","Shout"),("أقاطعه للأبد","Cut him off forever"),("أنشر الخلاف على الإنترنت","Post it online")],0,"الحوار الهادئ والاستماع يحلان معظم الخلافات.","Calm dialogue and listening resolve most conflicts.")
q("life_skills","DE",15,"all","وصلتك رسالة: \"ربحت جائزة، أرسل رمز التحقق\". ماذا تفعل؟","A message says \"You won a prize, send the verification code\". What do you do?",
  [("أتجاهلها ولا أشارك الرمز أبداً","Ignore it and never share the code"),("أرسل الرمز","Send the code"),("أتصل وأعطيهم بياناتي البنكية","Call and give bank details"),("أنشرها لأصدقائي","Forward to friends")],0,"هذا احتيال شائع؛ الجهات الرسمية لا تطلب رمز التحقق.","A common scam; legitimate bodies never ask for OTP codes.")
q("life_skills","E",17,"all","ما أهم عنصر في سيرة ذاتية ناجحة للتقديم على وظيفة؟","What matters most in a successful CV?",
  [("إنجازات واضحة ومهارات مرتبطة بالوظيفة","Clear achievements and relevant skills"),("صفحات كثيرة","Many pages"),("ألوان كثيرة","Lots of colours"),("صورة كبيرة فقط","Just a big photo")],0,"السيرة القوية مختصرة وتُبرز إنجازات قابلة للقياس.","A strong CV is concise with measurable achievements.")
q("life_skills","E",18,"all","أسلوب \"بومودورو\" لإدارة الوقت يعني:","The Pomodoro technique means:",
  [("العمل 25 دقيقة بتركيز ثم استراحة قصيرة","25 focused minutes, then a short break"),("العمل بلا توقف","Working non-stop"),("النوم 25 دقيقة","Sleeping 25 minutes"),("تأجيل المهام","Postponing tasks")],0,"يرفع التركيز ويقلل الإرهاق.","Boosts focus and reduces fatigue.")

# ================= v1.1 additions =================
GOOD = [("سلوك سليم ✅","Good behaviour ✅"),("سلوك خاطئ ❌","Wrong behaviour ❌")]
TRUE = [("صح ✅","True ✅"),("خطأ ❌","False ❌")]
def tf(domain, bands, diff, qar, qen, good, ear, een, labels=GOOD, **kw):
    q(domain, bands, diff, "all", qar, qen, labels, 0 if good else 1, ear, een, type="trueFalse", **kw)
def match(domain, bands, diff, qar, qen, pairs, ear="", een="", **kw):
    q(domain, bands, diff, "all", qar, qen, [], None, ear, een, type="match", pairs=pairs, **kw)
def trace(domain, bands, diff, glyph, what_ar, what_en):
    q(domain, bands, diff, "all", f"تتبّع {what_ar} «{glyph}» بإصبعك", f"Trace the {what_en} “{glyph}” with your finger", [], None,
      "أحسنت! الكتابة باليد تقوّي الذاكرة.", "Great! Writing by hand strengthens memory.", type="trace", trace=glyph)

# ---------------- BEHAVIOR (التربية والسلوك) ----------------
tf("behavior","A",1,"يا {name}، قلنا «شكراً» لمن ساعدنا.","{name}, we said “thank you” to someone who helped us.",True,"الشكر خُلق جميل يفرح الآخرين.","Saying thanks makes others happy.", emoji="🙏")
tf("behavior","A",2,"رمي الألعاب على الأرض عند الغضب.","Throwing toys on the floor when angry.",False,"عند الغضب نتنفس بهدوء ونخبر ماما أو بابا.","When angry, breathe slowly and tell a parent.", emoji="🧸")
tf("behavior","A",2,"مشاركة الألعاب مع الإخوة والأصدقاء.","Sharing toys with siblings and friends.",True,"المشاركة تجعل اللعب أمتع.","Sharing makes play more fun.", emoji="🤝")
tf("behavior","AB",3,"ترتيب السرير والألعاب بعد اللعب.","Tidying the bed and toys after playing.",True,"النظام يجعل البيت جميلاً ويساعد الأسرة.","Tidying keeps home nice and helps the family.", emoji="🛏️")
tf("behavior","B",4,"يا {name}، صديقك نسي قلمه فأعطيته قلمك.","{name}, your friend forgot a pen and you lent yours.",True,"مساعدة الآخرين من أجمل الأخلاق.","Helping others is a beautiful habit.", emoji="✏️")
tf("behavior","B",5,"الكذب على الأم حتى لا تغضب.","Lying to mum so she won't be upset.",False,"الصدق دائماً أفضل، والاعتراف بالخطأ شجاعة.","Honesty is always better; admitting mistakes is brave.", emoji="🤥")
tf("behavior","B",6,"السخرية من زميل لأن ملابسه مختلفة.","Mocking a classmate because his clothes are different.",False,"نحترم الجميع ولا نسخر من أحد.","We respect everyone and mock no one.", emoji="🚫")
q("behavior","AB",3,"all","ماذا نقول عندما ندخل البيت؟","What do we say when entering the house?",[("السلام عليكم","Assalamu alaikum"),("لا شيء","Nothing"),("وداعاً","Goodbye")],0,"نُلقي السلام على أهل البيت.","We greet the family with salam.", emoji="🏠")
tf("behavior","C",7,"مساعدة كبير السن في حمل أغراضه.","Helping an elderly person carry their bags.",True,"احترام الكبير وتوقيره من قيمنا.","Respecting elders is one of our values.", emoji="👴")
tf("behavior","C",8,"الاعتذار عند الخطأ حتى لو لم يرك أحد.","Apologising for a mistake even if no one saw it.",True,"الأمانة مع النفس تبني شخصية قوية.","Being honest with yourself builds strong character.")
tf("behavior","C",9,"أخذ شيء من البقالة دون دفع لأنه شيء صغير.","Taking something small from a shop without paying.",False,"هذه سرقة مهما كان الشيء صغيراً.","That is stealing, however small.", emoji="🛒")
tf("behavior","D",11,"الصبر على الأخ الصغير وتعليمه بهدوء.","Being patient with a younger sibling and teaching calmly.",True,"القدوة الهادئة تعلّم أكثر من الصراخ.","Calm example teaches more than shouting.")
tf("behavior","D",12,"نشر صورة زميل على الإنترنت دون إذنه للضحك.","Posting a classmate's photo online without permission for laughs.",False,"هذا تنمّر إلكتروني ويؤذي مشاعره.","That's cyberbullying and hurts them.", emoji="📱")
tf("behavior","E",14,"الغش في الاختبار مقبول إذا كان الجميع يغش.","Cheating in exams is fine if everyone does it.",False,"الخطأ لا يصبح صواباً بكثرة فاعليه، و«من غشّنا فليس منا».","Wrong doesn't become right because many do it.")
tf("behavior","E",15,"الالتزام بالموعد واحترام وقت الآخرين.","Being on time and respecting others' time.",True,"احترام الوقت علامة احتراف ومسؤولية.","Punctuality signals professionalism and responsibility.", emoji="⏰")

# ---------------- GEOGRAPHY ----------------
q("geography","A",2,"all","أين تعيش الجمال غالباً؟","Where do camels usually live?",[("في الصحراء","In the desert"),("في البحر","In the sea"),("في القطب","At the pole")],0,"الجمل يتحمّل الحر والعطش في الصحراء.","Camels handle heat and thirst in the desert.", emoji="🐪")
q("geography","A",3,"all","ما شكل كوكب الأرض؟","What shape is planet Earth?",[("كرة","A ball"),("مربع","A square"),("مثلث","A triangle")],0,"الأرض كروية الشكل تقريباً.","Earth is almost a sphere.", emoji="🌍")
tf("geography","AB",4,"الأرض تدور حول الشمس.","The Earth goes around the Sun.",True,"تكمل الأرض دورة حول الشمس كل سنة.","Earth completes one orbit every year.", labels=TRUE, emoji="☀️")
q("geography","B",5,"all","كم عدد قارات العالم؟","How many continents are there?",[("7","7"),("5","5"),("10","10")],0,"آسيا، أفريقيا، أوروبا، أمريكا الشمالية، أمريكا الجنوبية، أستراليا، أنتاركتيكا.","Asia, Africa, Europe, N. America, S. America, Australia, Antarctica.")
q("geography","B",6,"all","ما أكبر محيط في العالم؟","What is the largest ocean?",[("المحيط الهادئ","Pacific"),("المحيط الأطلسي","Atlantic"),("المحيط الهندي","Indian")],0,"المحيط الهادئ يغطي نحو ثلث سطح الأرض.","The Pacific covers about a third of Earth's surface.", emoji="🌊")
q("geography","C",8,"all","في أي قارة تقع شبه الجزيرة العربية؟","On which continent is the Arabian Peninsula?",[("آسيا","Asia"),("أفريقيا","Africa"),("أوروبا","Europe"),("أستراليا","Australia")],0,"تقع في جنوب غرب آسيا.","It lies in south-west Asia.")
q("geography","C",10,"all","ما أعلى جبل في العالم؟","What is the highest mountain in the world?",[("إيفرست","Everest"),("كليمنجارو","Kilimanjaro"),("الألب","Alps"),("طويق","Tuwaiq")],0,"ارتفاع قمة إيفرست نحو 8849 متراً.","Everest is about 8,849 m high.", emoji="🏔️")
match("geography","C",9,"صِل كل دولة بعاصمتها","Match each country with its capital",[("السعودية","Saudi Arabia","الرياض","Riyadh"),("مصر","Egypt","القاهرة","Cairo"),("فرنسا","France","باريس","Paris"),("اليابان","Japan","طوكيو","Tokyo")])
q("geography","D",13,"all","ما أكبر صحراء حارة في العالم؟","What is the largest hot desert?",[("الصحراء الكبرى","Sahara"),("الربع الخالي","Rub' al Khali"),("صحراء غوبي","Gobi"),("صحراء أتاكاما","Atacama")],0,"الصحراء الكبرى في شمال أفريقيا، والربع الخالي أكبر صحراء رملية متصلة.","The Sahara; the Empty Quarter is the largest continuous sand desert.")
q("geography","D",14,"all","خط الاستواء يقسم الأرض إلى:","The equator divides Earth into:",[("نصف شمالي ونصف جنوبي","Northern and southern halves"),("شرقي وغربي","Eastern and western halves"),("قارات","Continents"),("محيطات","Oceans")],0,"خط الطول صفر (غرينتش) هو الذي يقسمها شرقاً وغرباً.","The prime meridian divides east and west.")
q("geography","E",16,"all","ما سبب تعاقب الليل والنهار؟","What causes day and night?",[("دوران الأرض حول محورها","Earth spinning on its axis"),("دوران الأرض حول الشمس","Earth orbiting the Sun"),("دوران القمر","The Moon's orbit"),("السحب","Clouds")],0,"دورة كاملة حول المحور كل 24 ساعة تقريباً.","One full spin about every 24 hours.")
q("geography","E",18,"all","ما المضيق الذي يصل البحر الأحمر بخليج عدن؟","Which strait links the Red Sea to the Gulf of Aden?",[("باب المندب","Bab el-Mandeb"),("هرمز","Hormuz"),("جبل طارق","Gibraltar"),("البوسفور","Bosphorus")],0,"من أهم الممرات الملاحية لتجارة العالم.","One of the world's key shipping lanes.")

# ---------------- HISTORY ----------------
q("history","B",7,"all","من بنى الأهرامات في الجيزة؟","Who built the pyramids of Giza?",[("المصريون القدماء","Ancient Egyptians"),("الرومان","Romans"),("الإنجليز","The English")],0,"بُنيت قبل أكثر من 4500 سنة.","Built over 4,500 years ago.", emoji="🔺")
q("history","C",11,"all","مَن العالم المسلم الملقب بـ«أبو الجبر»؟","Which Muslim scholar is called the “father of algebra”?",[("الخوارزمي","Al-Khwarizmi"),("ابن بطوطة","Ibn Battuta"),("الفارابي","Al-Farabi"),("ابن خلدون","Ibn Khaldun")],0,"ومن اسمه جاءت كلمة «خوارزمية» (Algorithm).","The word “algorithm” comes from his name.")
q("history","C",11,"all","متى طارت أول طائرة بمحرك (الأخوان رايت)؟","When did the first powered aeroplane fly (Wright brothers)?",[("1903","1903"),("1803","1803"),("1953","1953"),("2003","2003")],0,"كانت الرحلة الأولى 12 ثانية فقط.","The first flight lasted just 12 seconds.", emoji="✈️")
q("history","D",13,"all","ابن سينا اشتهر بكتابه:","Ibn Sina is famous for his book:",[("القانون في الطب","The Canon of Medicine"),("المقدمة","The Muqaddimah"),("رحلة ابن بطوطة","The Travels"),("كليلة ودمنة","Kalila wa Dimna")],0,"دُرّس كتابه في جامعات أوروبا قروناً.","It was taught in European universities for centuries.")
q("history","D",14,"all","في أي عام هبط الإنسان على القمر أول مرة؟","When did humans first land on the Moon?",[("1969","1969"),("1959","1959"),("1979","1979"),("1989","1989")],0,"مهمة أبولو 11.","The Apollo 11 mission.", emoji="🌕")
q("history","D",14,"all","ما «طريق الحرير»؟","What was the Silk Road?",[("طرق تجارية قديمة بين الصين والعالم","Ancient trade routes linking China to the world"),("نهر في الهند","A river in India"),("مصنع حرير","A silk factory"),("سور عظيم","A great wall")],0,"نقل البضائع والأفكار بين الشرق والغرب.","It carried goods and ideas between East and West.")
q("history","E",16,"all","في أي عام انتهت الحرب العالمية الثانية؟","When did World War II end?",[("1945","1945"),("1918","1918"),("1939","1939"),("1950","1950")],0,"بدأت 1939 وانتهت 1945.","It ran from 1939 to 1945.")
q("history","E",18,"all","ما «الثورة الصناعية»؟","What was the Industrial Revolution?",[("التحول إلى الإنتاج بالآلات في القرنين 18–19","The shift to machine production in the 18th–19th c."),("ثورة سياسية","A political revolt"),("اختراع الإنترنت","The invention of the internet"),("حرب عالمية","A world war")],0,"بدأت في بريطانيا وغيّرت الاقتصاد والمدن.","It began in Britain and transformed economies and cities.", emoji="🏭")
match("history","E",15,"صِل كل عالِم بمجاله","Match each scholar with his field",[("ابن الهيثم","Ibn al-Haytham","البصريات","Optics"),("الخوارزمي","Al-Khwarizmi","الجبر","Algebra"),("ابن سينا","Ibn Sina","الطب","Medicine"),("نيوتن","Newton","الجاذبية","Gravity")])

# ---------------- FRENCH ----------------
q("french","B",5,"all","ما معنى كلمة «Bonjour»؟","What does “Bonjour” mean?",[("مرحباً / صباح الخير","Hello / Good morning"),("شكراً","Thank you"),("مع السلامة","Goodbye")],0,"Bonjour تحية فرنسية في الصباح والنهار.","Bonjour is the daytime French greeting.", fr="Que signifie « Bonjour » ?", emoji="👋")
q("french","B",6,"all","ما معنى كلمة «Merci»؟","What does “Merci” mean?",[("شكراً","Thank you"),("نعم","Yes"),("لا","No")],0,"Merci = شكراً، وMerci beaucoup = شكراً جزيلاً.","Merci = thank you; merci beaucoup = thanks a lot.", fr="Que signifie « Merci » ?")
q("french","BC",7,"all","كيف نقول «نعم» بالفرنسية؟","How do you say “yes” in French?",[("Oui","Oui"),("Non","Non"),("Merci","Merci")],0,"Oui = نعم، Non = لا.","Oui = yes, Non = no.", fr="Comment dit-on « oui » ?")
match("french","C",8,"صِل الكلمة الفرنسية بمعناها","Match the French word to its meaning",[("Bonjour","Bonjour","مرحباً","Hello"),("Merci","Merci","شكراً","Thank you"),("Au revoir","Au revoir","مع السلامة","Goodbye"),("Oui","Oui","نعم","Yes")], fr="Associe chaque mot à son sens")
q("french","C",9,"all","ما الرقم «deux»؟","Which number is “deux”?",[("2","2"),("3","3"),("10","10"),("1","1")],0,"un = 1، deux = 2، trois = 3.","un = 1, deux = 2, trois = 3.", fr="Quel nombre est « deux » ?")
q("french","C",10,"all","ما معنى «Le chat»؟","What does “le chat” mean?",[("القطة","The cat"),("الكلب","The dog"),("البيت","The house"),("الشجرة","The tree")],0,"le chat = القطة، le chien = الكلب.","le chat = cat, le chien = dog.", fr="Que signifie « le chat » ?", emoji="🐱")
q("french","D",12,"all","ما معنى «Je m'appelle Sara»؟","What does “Je m'appelle Sara” mean?",[("اسمي سارة","My name is Sara"),("أنا جائعة","I am hungry"),("أين سارة؟","Where is Sara?"),("سارة في المدرسة","Sara is at school")],0,"Je m'appelle … = اسمي …","Je m'appelle … = my name is …", fr="Que veut dire « Je m'appelle Sara » ?")
q("french","D",13,"all","ما معنى «L'école»؟","What does “l'école” mean?",[("المدرسة","School"),("المستشفى","Hospital"),("السوق","Market"),("الملعب","Stadium")],0,"l'école = المدرسة.","l'école = school.", fr="Que signifie « l'école » ?", emoji="🏫")
q("french","E",15,"all","اختر الترجمة الفرنسية لـ «أنا طالب»","Choose the French for “I am a student”",[("Je suis étudiant","Je suis étudiant"),("J'ai étudiant","J'ai étudiant"),("Je étudiant suis","Je étudiant suis"),("Tu es étudiant","Tu es étudiant")],0,"être (يكون): je suis، tu es، il est.","être: je suis, tu es, il est.", fr="Traduis « I am a student »")
q("french","E",16,"all","ما معنى «Le recyclage»؟","What does “le recyclage” mean?",[("إعادة التدوير","Recycling"),("النفايات","Waste"),("الطاقة","Energy"),("الماء","Water")],0,"كلمة مهمة في مجال الاستدامة.","A key word in sustainability.", fr="Que signifie « le recyclage » ?", emoji="♻️")

# ---------------- YOUNG-AGE ACTIVITIES ----------------
q("math","A",1,"all","كم تفاحة ترى؟","How many apples do you see?",[("3","3"),("2","2"),("4","4")],0,"واحد، اثنان، ثلاثة — 3 تفاحات!","One, two, three — 3 apples!", emoji="🍎🍎🍎")
q("science","A",2,"all","أي حيوان يقول «مياو»؟","Which animal says “meow”?",[("🐱 القطة","🐱 Cat"),("🐶 الكلب","🐶 Dog"),("🐮 البقرة","🐮 Cow")],0,"القطة تقول مياو، والكلب يقول هاو.","Cats meow, dogs woof.")
tf("science","A",1,"الشمس تطلع في النهار.","The Sun comes out in the daytime.",True,"في النهار نرى الشمس، وفي الليل نرى القمر والنجوم.","By day we see the Sun; at night the Moon and stars.", labels=TRUE, emoji="☀️")
tf("science","A",2,"السمكة تطير في السماء.","Fish fly in the sky.",False,"السمكة تسبح في الماء، والطيور تطير.","Fish swim; birds fly.", labels=TRUE, emoji="🐟")
tf("science","B",4,"النبات يحتاج إلى الماء ليعيش.","Plants need water to live.",True,"بدون ماء يذبل النبات.","Without water plants wilt.", labels=TRUE, emoji="🌱")
match("science","A",2,"صِل كل حيوان ببيته","Match each animal to its home",[("🐦","🐦","عُش","Nest"),("🐝","🐝","خلية","Hive"),("🐟","🐟","ماء","Water"),("🐄","🐄","حظيرة","Barn")])
match("math","A",1,"صِل كل رقم بعدد التفاحات","Match each number with the apples",[("1","1","🍎","🍎"),("2","2","🍎🍎","🍎🍎"),("3","3","🍎🍎🍎","🍎🍎🍎")])
match("english","AB",3,"صِل الكلمة بالصورة","Match the word to the picture",[("Cat","Cat","🐱","🐱"),("Dog","Dog","🐶","🐶"),("Sun","Sun","☀️","☀️")])
match("crafts","B",5,"صِل كل أداة بصاحب المهنة","Match each tool with the job",[("🪚 منشار","🪚 Saw","نجّار","Carpenter"),("✂️ مقص","✂️ Scissors","خيّاط","Tailor"),("🩺 سماعة","🩺 Stethoscope","طبيب","Doctor"),("🌱 مجرفة","🌱 Shovel","مزارع","Farmer")])
match("arabic","B",6,"صِل كل كلمة بعكسها","Match each word with its opposite",[("كبير","كبير","صغير","صغير"),("طويل","طويل","قصير","قصير"),("ساخن","ساخن","بارد","بارد")])
match("economy","D",12,"صِل كل مصطلح بمعناه","Match each term to its meaning",[("الإيراد","Revenue","المال الداخل من المبيعات","Money in from sales"),("التكلفة","Cost","المال المصروف للإنتاج","Money spent to produce"),("الربح","Profit","الإيراد ناقص التكلفة","Revenue minus cost")])
match("english","D",13,"صِل كل كلمة بمرادفها","Match each word with its synonym",[("big","big","large","large"),("fast","fast","quick","quick"),("happy","happy","glad","glad")])
match("environment","B",6,"صِل كل نفاية بالحاوية الصحيحة","Match each item to the right bin",[("🥫 علبة","🥫 Can","معادن","Metal"),("📰 جريدة","📰 Newspaper","ورق","Paper"),("🍌 قشر موز","🍌 Peel","عضوي","Organic"),("🍾 قارورة زجاج","🍾 Glass bottle","زجاج","Glass")])

trace("arabic","A",1,"أ","حرف","letter")
trace("arabic","A",2,"ب","حرف","letter")
trace("arabic","AB",3,"م","حرف","letter")
trace("arabic","B",4,"ج","حرف","letter")
trace("math","A",1,"1","رقم","number")
trace("math","A",2,"2","رقم","number")
trace("math","A",3,"3","رقم","number")
trace("math","B",4,"5","رقم","number")
trace("english","A",3,"A","حرف","letter")
trace("english","B",4,"B","حرف","letter")


def main(out):
    bank = []
    counters = Counter()
    prefix = {"religion":"rel","economy":"eco","commerce":"com","finance":"fin","engineering":"eng",
              "crafts":"crf","science":"sci","math":"mat","arabic":"ara","english":"enl","health":"hlt",
              "environment":"env","citizenship":"cit","life_skills":"lif",
              "behavior":"beh","geography":"geo","history":"his","french":"frn"}
    for (d, bands, diff, g, qar, qen, opts, ans, ear, een, kw) in Q:
        counters[d] += 1
        t = kw.get("type", "mcq")
        text = {"ar": qar, "en": qen}
        if kw.get("fr"): text["fr"] = kw["fr"]
        item = {"id": f"{prefix[d]}-{counters[d]:03d}", "domain": d, "ageBands": list(bands), "difficulty": diff,
                "gender": g, "type": t, "text": text}
        if t in ("mcq", "trueFalse"):
            assert 0 <= ans < len(opts), qen
            item["options"] = [{"ar": a, "en": e} for a, e in opts]
            item["answer"] = ans
        if t == "match":
            assert len(kw["pairs"]) >= 3, qen
            item["pairs"] = [{"l": {"ar": la, "en": le}, "r": {"ar": ra, "en": re}} for la, le, ra, re in kw["pairs"]]
        if t == "trace": item["trace"] = kw["trace"]
        for k in ("emoji", "region"):
            if kw.get(k): item[k] = kw[k]
        item["explanation"] = {"ar": ear, "en": een}
        item.update({"status": "published", "source": "system"})
        bank.append(item)
    json.dump({"version": 1, "questions": bank}, open(out, "w"), ensure_ascii=False, indent=1)
    by_band = Counter(b for x in bank for b in x["ageBands"])
    print(len(bank), "questions;", dict(Counter(x["domain"] for x in bank)))
    print("bands:", dict(sorted(by_band.items())), "gender:", dict(Counter(x["gender"] for x in bank)))
    print("types:", dict(Counter(x["type"] for x in bank)), "regional:", sum(1 for x in bank if "region" in x))

if __name__ == "__main__":
    main(sys.argv[1])

# 📚 فهرس قاعدة البيانات القرآنية الهرمية
## Quran Hierarchical Database Index

---

## 🎯 نظرة عامة سريعة

هذا المجلد يحتوي على **قاعدة بيانات PostgreSQL احترافية وشاملة** للقرآن الكريم مع:

✨ **19 جدول** عبر 5 مستويات هرمية
✨ **400+ عمود** مصمم بدقة
✨ **Vector Embeddings** للبحث الدلالي
✨ **Full-Text Search** للبحث السريع
✨ **Morphological Analysis** للتحليل الصرفي
✨ **أدوات استيراد متقدمة** من SQLite

---

## 📂 هيكل الملفات

```
database/
├─ 📖 الوثائق الرئيسية
│  ├─ INDEX.md                          ← أنت هنا! 🎯
│  ├─ README.md                         ← مقدمة شاملة
│  ├─ QUICK_START.md                    ← دليل البدء السريع
│  ├─ IMPORT_GUIDE.md                   ← دليل الاستيراد التفصيلي
│  ├─ 00_DATABASE_ANALYSIS.md           ← تحليل معماري كامل
│  └─ SMART_QUERIES.md                  ← 50+ استعلام جاهز
│
├─ 🗄️ سكريبتات SQL
│  ├─ sql/01_setup.sql                  ← إعداد القاعدة والامتدادات
│  ├─ sql/02_level0_core_tables.sql     ← الجداول الأساسية
│  ├─ sql/03_remaining_levels.sql       ← المستويات 1-5
│  └─ sql/04_views_and_functions.sql    ← Views ودوال
│
├─ 🔧 أدوات التثبيت
│  ├─ install_linux.sh                  ← تثبيت تلقائي على Linux
│  └─ install_windows.bat               ← تثبيت تلقائي على Windows
│
├─ 📥 أدوات الاستيراد
│  ├─ explore_sqlite.py                 ← استكشاف قواعد SQLite
│  ├─ import_from_sqlite.py             ← استيراد بسيط
│  ├─ import_advanced.py                ← استيراد متقدم مع تكوين
│  └─ import_config.template.json       ← قالب ملف التكوين
│
└─ 📝 ملفات العمل
   └─ import_config.json                ← (أنشئه بنفسك)
```

---

## 🚀 البدء السريع (5 دقائق)

### للمبتدئين 🔰

```bash
# 1. اقرأ المقدمة
cat README.md

# 2. اتبع دليل البدء السريع
cat QUICK_START.md

# 3. ثبّت القاعدة
./install_linux.sh

# 4. استورد بياناتك
python3 import_from_sqlite.py
```

### للمحترفين 🎓

```bash
# 1. راجع التحليل المعماري
cat 00_DATABASE_ANALYSIS.md

# 2. استكشف قاعدتك الموجودة
./explore_sqlite.py /path/to/your/quran.db --export

# 3. أنشئ تكوين مخصص
cp import_config.template.json import_config.json
nano import_config.json

# 4. نفّذ الاستيراد المتقدم
./import_advanced.py --config import_config.json

# 5. استعرض الاستعلامات الذكية
cat SMART_QUERIES.md
```

---

## 📖 الوثائق حسب الحالة

### 🆕 "أريد فهم المشروع"
1. `README.md` - ابدأ هنا
2. `00_DATABASE_ANALYSIS.md` - فهم معماري عميق
3. `SMART_QUERIES.md` - أمثلة عملية

### ⚡ "أريد تثبيت سريع"
1. `QUICK_START.md` - 5 دقائق فقط
2. `install_linux.sh` أو `install_windows.bat`

### 📥 "أريد استيراد بياناتي"
1. `IMPORT_GUIDE.md` - دليل شامل خطوة بخطوة
2. `explore_sqlite.py` - اكتشف بنية قاعدتك
3. `import_from_sqlite.py` - للحالات البسيطة
4. `import_advanced.py` - للحالات المعقدة

### 💻 "أريد برمجة تطبيق"
1. `00_DATABASE_ANALYSIS.md` - فهم الجداول والعلاقات
2. `SMART_QUERIES.md` - استعلامات جاهزة
3. `sql/04_views_and_functions.sql` - دوال مساعدة

### 🔧 "لدي مشكلة"
1. `QUICK_START.md` - استكشاف الأخطاء
2. `IMPORT_GUIDE.md` - حل مشاكل الاستيراد
3. Email: duhatv@gmail.com

---

## 🗂️ دليل الملفات التفصيلي

### 📘 README.md
**الغرض:** مقدمة شاملة للمشروع
**يحتوي على:**
- نظرة عامة على المزايا
- إحصائيات القاعدة (114 سورة، 6236 آية، إلخ)
- البنية الهرمية المصورة
- خطوات التثبيت
- أمثلة استخدام أساسية
- معلومات الترخيص والتواصل

**متى تقرأه:** عند البدء بالمشروع لأول مرة

---

### 📗 QUICK_START.md
**الغرض:** دليل سريع للتثبيت والتشغيل
**يحتوي على:**
- تثبيت PostgreSQL وpgvector
- تنفيذ السكريبتات خطوة بخطوة
- اختبارات سريعة
- سكريبت تثبيت شامل
- أمثلة اتصال (Python, Node.js, PHP)
- إعدادات الأداء
- نصائح الصيانة

**متى تقرأه:** عندما تريد تثبيت سريع (5-10 دقائق)

---

### 📕 IMPORT_GUIDE.md
**الغرض:** دليل شامل لاستيراد البيانات
**يحتوي على:**
- شرح الأدوات الثلاثة (explore, import_simple, import_advanced)
- سيناريوهات استخدام متنوعة
- جداول تعيين الأعمدة
- قواعد التحقق والتحويل
- نصائح الأداء
- استكشاف الأخطاء
- أمثلة كاملة لقواعد شهيرة

**متى تقرأه:** قبل البدء باستيراد بياناتك

---

### 📙 00_DATABASE_ANALYSIS.md
**الغرض:** تحليل معماري تقني عميق
**يحتوي على:**
- ERD (Entity Relationship Diagram)
- تفاصيل كل جدول من الـ19 جدول
- شرح العلاقات (Foreign Keys)
- تحليل الأداء والفهارس
- توصيات التحسين
- استراتيجيات التقسيم (Partitioning)

**متى تقرأه:** عند تطوير تطبيقات معقدة أو دراسة معمارية

---

### 📓 SMART_QUERIES.md
**الغرض:** مكتبة استعلامات جاهزة
**يحتوي على:** 50+ استعلام في 7 فئات:
1. استعلامات أساسية
2. بحث متقدم (Full-Text)
3. تحليل صرفي
4. استعلامات موضوعية
5. إحصائيات
6. بحث دلالي (Vector)
7. استعلامات معقدة

**متى تقرأه:** عند كتابة استعلامات أو البحث عن أمثلة

---

### 🛠️ install_linux.sh
**الغرض:** تثبيت تلقائي كامل على Linux
**يقوم بـ:**
- ✅ التحقق من PostgreSQL
- ✅ تثبيت pgvector إذا لزم
- ✅ تنفيذ السكريبتات الأربعة بالترتيب
- ✅ عرض تقارير مفصلة

**الاستخدام:**
```bash
chmod +x install_linux.sh
./install_linux.sh
```

---

### 🛠️ install_windows.bat
**الغرض:** تثبيت تلقائي كامل على Windows
**يقوم بـ:**
- ✅ التحقق من PostgreSQL
- ✅ طلب بيانات الاتصال
- ✅ تنفيذ السكريبتات بالترتيب
- ✅ عرض النتائج

**الاستخدام:**
```cmd
install_windows.bat
```

---

### 🔍 explore_sqlite.py
**الغرض:** استكشاف قواعد SQLite الموجودة
**المميزات:**
- 📊 عرض جميع الجداول والأعمدة
- 🔍 كشف تلقائي لجداول القرآن
- 📈 إحصائيات تفصيلية
- 💾 تصدير البنية إلى JSON

**الاستخدام:**
```bash
# استكشاف بسيط
./explore_sqlite.py /path/to/quran.db

# مع عينة بيانات
./explore_sqlite.py /path/to/quran.db --sample

# جدول محدد
./explore_sqlite.py /path/to/quran.db --table quran

# تصدير
./explore_sqlite.py /path/to/quran.db --export schema.json
```

---

### 📥 import_from_sqlite.py
**الغرض:** استيراد بسيط وسريع
**مناسب لـ:**
- قواعد بيانات بسيطة
- استيراد السور والآيات فقط
- حالات الاستخدام السريعة

**التعديل المطلوب:**
```python
# في بداية الملف
SQLITE_DB_PATH = r"/path/to/your/quran.db"

PG_CONFIG = {
    'password': 'your_password'  # أدخل كلمة المرور
}
```

**الاستخدام:**
```bash
./import_from_sqlite.py
```

---

### 📥 import_advanced.py
**الغرض:** استيراد متقدم مع تكوين شامل
**مناسب لـ:**
- قواعد بيانات معقدة
- استيراد جداول متعددة
- تعيين أعمدة مخصص
- قواعد تحقق معقدة

**الاستخدام:**
```bash
# إنشاء التكوين
cp import_config.template.json import_config.json
nano import_config.json

# التشغيل
./import_advanced.py --config import_config.json
```

---

### ⚙️ import_config.template.json
**الغرض:** قالب لملف تكوين الاستيراد المتقدم
**يحتوي على:**
- إعدادات الاتصال (SQLite & PostgreSQL)
- خيارات الاستيراد
- تعيين الجداول والأعمدة
- قواعد التحويل
- قواعد التحقق

**الاستخدام:**
```bash
# انسخه وعدّله
cp import_config.template.json import_config.json
```

---

### 🗃️ sql/01_setup.sql
**الغرض:** إعداد القاعدة الأولي
**ينشئ:**
- قاعدة البيانات `quran_hierarchical_db`
- الامتدادات (vector, pg_trgm, unaccent)
- المخططات (schemas): quran, analytics, community
- 15 نوع مخصص (ENUM types)
- دوال مساعدة للبحث

---

### 🗃️ sql/02_level0_core_tables.sql
**الغرض:** الجداول الأساسية (المستوى 0)
**ينشئ:**
- `quran.surahs` - السور (114 سورة)
- `quran.ayahs` - الآيات (6236+ آية)
- `quran.words` - الكلمات (77,430+ كلمة)
- الفهارس الأساسية
- فهارس البحث (Full-Text, Vector)

---

### 🗃️ sql/03_remaining_levels.sql
**الغرض:** المستويات 1-5
**ينشئ:**
- **Level 1:** roots, patterns (التحليل الصرفي)
- **Level 2:** mufassireen, tafsir, translators, translations
- **Level 3:** revelation_contexts, topics, ayah_topics, qiraat, sources
- **Level 4:** reciters, recitations
- **Level 5:** users, bookmarks, annotations
- جميع Foreign Keys والعلاقات

---

### 🗃️ sql/04_views_and_functions.sql
**الغرض:** Views ودوال للأداء والسهولة
**ينشئ:**
- 5 Materialized Views
- 7 دوال (Functions)
- 1 Stored Procedure
- فهارس على Views

---

## 🎓 مسارات التعلم

### المسار السريع (30 دقيقة) ⚡
```
1. README.md (5 دقائق)
2. QUICK_START.md (5 دقائق)
3. install_linux.sh (10 دقائق)
4. SMART_QUERIES.md - جرب 5 استعلامات (10 دقائق)
```

### المسار الشامل (3 ساعات) 📚
```
1. README.md (10 دقائق)
2. 00_DATABASE_ANALYSIS.md (60 دقيقة)
3. QUICK_START.md + التثبيت (20 دقيقة)
4. IMPORT_GUIDE.md (30 دقيقة)
5. استيراد بياناتك (40 دقيقة)
6. SMART_QUERIES.md - تجريب (20 دقيقة)
```

### المسار الاحترافي (يومين) 🎯
```
اليوم 1:
- دراسة جميع الوثائق بتمعن
- فهم البنية المعمارية
- تخطيط استراتيجية الاستيراد
- تجهيز البيانات

اليوم 2:
- تنفيذ التثبيت الكامل
- استيراد جميع الجداول
- التحقق من البيانات
- اختبار الاستعلامات
- تحسين الأداء
```

---

## 💡 نصائح مهمة

### ✅ قبل البدء
- [ ] تأكد من تثبيت PostgreSQL 15+
- [ ] احصل على قواعد البيانات المصدرية جاهزة
- [ ] راجع `QUICK_START.md` أولاً
- [ ] جهّز مساحة تخزين كافية (5GB+)

### ✅ أثناء الاستيراد
- [ ] استخدم `explore_sqlite.py` قبل الاستيراد
- [ ] احتفظ بنسخة احتياطية من بياناتك
- [ ] راقب رسائل الأخطاء
- [ ] تحقق من البيانات بعد كل جدول

### ✅ بعد التثبيت
- [ ] نفّذ اختبارات التحقق في `QUICK_START.md`
- [ ] جرّب الاستعلامات في `SMART_QUERIES.md`
- [ ] اقرأ نصائح الأداء
- [ ] إعداد النسخ الاحتياطي الدوري

---

## 📞 الدعم والمساعدة

| المشكلة | الحل |
|---------|------|
| خطأ في التثبيت | `QUICK_START.md` → استكشاف الأخطاء |
| مشكلة استيراد | `IMPORT_GUIDE.md` → حل المشاكل |
| سؤال تقني | `00_DATABASE_ANALYSIS.md` |
| مساعدة عامة | duhatv@gmail.com |

---

## 🏆 الخطوات التالية

بعد إتمام التثبيت والاستيراد:

1. ✅ تطوير تطبيق القرآن الخاص بك
2. ✅ إضافة مزايا البحث المتقدم
3. ✅ تطبيق الذكاء الاصطناعي للتحليل
4. ✅ بناء واجهات برمجية (APIs)
5. ✅ المساهمة في المشروع

---

## 📊 الإحصائيات

| العنصر | العدد |
|--------|-------|
| 📄 ملفات الوثائق | 7 |
| 🗃️ سكريبتات SQL | 4 |
| 🔧 أدوات Python | 3 |
| 📋 الجداول | 19 |
| 🔍 Views | 5 |
| ⚙️ الدوال | 7 |
| 📊 الاستعلامات الجاهزة | 50+ |

---

<div align="center">

## 🌟 استمتع ببناء تطبيقك! 🌟

**صُنع بـ ❤️ للمسلمين في كل مكان**

**Built with ❤️ for Muslims everywhere**

---

**آخر تحديث:** 2025-10-30
**الإصدار:** 1.0.0
**البريد الإلكتروني:** duhatv@gmail.com
**الموقع:** duhatv.net

</div>

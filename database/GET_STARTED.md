# 🚀 ابدأ الآن - دليل التشغيل السريع
## Get Started - Quick Launch Guide

---

<div align="center">

## ✅ تم تجهيز كل شيء لك!

**قاعدة بيانات PostgreSQL احترافية + أدوات استيراد متقدمة**

</div>

---

## 📍 أنت هنا الآن

لديك الآن نظام متكامل لقاعدة بيانات قرآنية هرمية ذكية تحتوي على:

✨ **19 جدول** عبر 5 مستويات هرمية
✨ **400+ عمود** مصمم بدقة
✨ **أدوات استيراد ذكية** من SQLite إلى PostgreSQL
✨ **سكريبتات تثبيت تلقائية** لـ Linux و Windows
✨ **وثائق شاملة** بالعربية والإنجليزية

---

## ⚡ البدء في 3 خطوات

### الخطوة 1️⃣: راجع الفهرس

```bash
cd /home/user/duhatv/database
cat INDEX.md
```

هذا الملف يعطيك خريطة كاملة لجميع الملفات والأدوات المتاحة.

---

### الخطوة 2️⃣: اختر مسارك

#### 🔰 للمبتدئين (30 دقيقة)

```bash
# اقرأ دليل البدء السريع
cat QUICK_START.md

# ثبّت القاعدة
chmod +x install_linux.sh
./install_linux.sh

# جرّب استعلامات جاهزة
cat SMART_QUERIES.md
```

#### 🎓 للمحترفين (3 ساعات)

```bash
# افهم البنية المعمارية
cat 00_DATABASE_ANALYSIS.md

# استكشف قاعدتك الموجودة
./explore_sqlite.py /path/to/your/quran.db --sample

# أنشئ تكوين استيراد مخصص
cp import_config.template.json import_config.json
nano import_config.json

# نفّذ الاستيراد
./import_advanced.py --config import_config.json
```

---

### الخطوة 3️⃣: استورد بياناتك

#### أ) إذا كانت لديك قاعدة SQLite بسيطة

```bash
# 1. استكشف قاعدتك أولاً
./explore_sqlite.py /path/to/quran.db

# 2. عدّل المسار في import_from_sqlite.py
nano import_from_sqlite.py
# غيّر السطر: SQLITE_DB_PATH = r"/path/to/your/quran.db"

# 3. نفّذ الاستيراد
./import_from_sqlite.py
```

#### ب) إذا كانت لديك قاعدة معقدة

```bash
# 1. استكشف وصدّر البنية
./explore_sqlite.py /path/to/quran.db --export schema.json

# 2. أنشئ ملف تكوين
cp import_config.template.json import_config.json

# 3. عدّل التكوين حسب بنية قاعدتك
nano import_config.json

# 4. نفّذ الاستيراد المتقدم
./import_advanced.py --config import_config.json
```

---

## 📂 الملفات الأساسية

### 📖 للقراءة أولاً

| الملف | الوصف | متى تقرأه |
|------|-------|-----------|
| `INDEX.md` | خريطة كاملة للمشروع | الآن! |
| `README.md` | مقدمة شاملة | عند البدء |
| `QUICK_START.md` | تثبيت سريع | قبل التثبيت |
| `IMPORT_GUIDE.md` | دليل الاستيراد | قبل الاستيراد |

### 🔧 للتنفيذ

| الأداة | الغرض | الاستخدام |
|-------|-------|----------|
| `install_linux.sh` | تثبيت تلقائي | `./install_linux.sh` |
| `explore_sqlite.py` | استكشاف SQLite | `./explore_sqlite.py db.db` |
| `import_from_sqlite.py` | استيراد بسيط | `./import_from_sqlite.py` |
| `import_advanced.py` | استيراد متقدم | `./import_advanced.py -c config.json` |

---

## 💡 سيناريوهات عملية

### 🎯 السيناريو 1: "لدي ملف quran.db وأريد استخدامه"

```bash
# الخطوة 1: اكتشف ما بداخله
./explore_sqlite.py ~/Desktop/quran.db --sample

# الخطوة 2: ثبّت قاعدة PostgreSQL
./install_linux.sh

# الخطوة 3: عدّل المسار في import_from_sqlite.py
nano import_from_sqlite.py
# غيّر: SQLITE_DB_PATH = r"/home/user/Desktop/quran.db"

# الخطوة 4: نفّذ الاستيراد
./import_from_sqlite.py

# الخطوة 5: تحقق من النتيجة
psql -U postgres -d quran_hierarchical_db -c "SELECT COUNT(*) FROM quran.ayahs;"
```

---

### 🎯 السيناريو 2: "لدي عدة قواعد بيانات (قرآن + ترجمات + تفاسير)"

```bash
# الخطوة 1: استكشف كل قاعدة
./explore_sqlite.py ~/quran.db --export quran_schema.json
./explore_sqlite.py ~/translations.db --export trans_schema.json
./explore_sqlite.py ~/tafsir.db --export tafsir_schema.json

# الخطوة 2: ثبّت PostgreSQL
./install_linux.sh

# الخطوة 3: أنشئ تكوينات منفصلة
cp import_config.template.json config_quran.json
cp import_config.template.json config_translations.json
cp import_config.template.json config_tafsir.json

# الخطوة 4: عدّل كل تكوين حسب القاعدة المناسبة
nano config_quran.json
nano config_translations.json
nano config_tafsir.json

# الخطوة 5: نفّذ الاستيراد بالترتيب
./import_advanced.py --config config_quran.json
./import_advanced.py --config config_translations.json
./import_advanced.py --config config_tafsir.json
```

---

### 🎯 السيناريو 3: "أريد فهم البنية قبل البدء"

```bash
# الخطوة 1: اقرأ التحليل المعماري
cat 00_DATABASE_ANALYSIS.md

# الخطوة 2: راجع الاستعلامات الذكية
cat SMART_QUERIES.md

# الخطوة 3: افحص سكريبتات SQL
cat sql/01_setup.sql
cat sql/02_level0_core_tables.sql
cat sql/03_remaining_levels.sql
cat sql/04_views_and_functions.sql

# الخطوة 4: الآن أنت جاهز للتثبيت!
./install_linux.sh
```

---

## 🔍 التحقق بعد التثبيت

بعد تثبيت القاعدة، تحقق من نجاح العملية:

```bash
# اتصل بالقاعدة
psql -U postgres -d quran_hierarchical_db

# في psql، نفّذ:
```

```sql
-- عرض المخططات
\dn

-- عرض جميع الجداول
\dt quran.*
\dt analytics.*
\dt community.*

-- عد الجداول
SELECT COUNT(*)
FROM information_schema.tables
WHERE table_schema IN ('quran', 'analytics', 'community');

-- التحقق من الامتدادات
\dx

-- إذا استوردت بيانات، تحقق:
SELECT COUNT(*) FROM quran.surahs;   -- يجب أن يكون 114
SELECT COUNT(*) FROM quran.ayahs;    -- يجب أن يكون 6236+

-- جرّب استعلام بحث
SELECT * FROM quran.search_ayahs_fulltext('الله', 'arabic', 5);
```

---

## 📊 ماذا بعد التثبيت؟

### 1️⃣ تطوير التطبيق

```python
# مثال Python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="quran_hierarchical_db",
    user="quran_readonly",
    password="your_password"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM quran.ayahs WHERE aya_sur_id = 1 ORDER BY aya_number")

for row in cursor.fetchall():
    print(row)
```

### 2️⃣ استعلامات ذكية

راجع `SMART_QUERIES.md` للحصول على 50+ استعلام جاهز:

- بحث نصي متقدم
- تحليل صرفي
- بحث دلالي
- إحصائيات
- استعلامات معقدة

### 3️⃣ تحسين الأداء

راجع `QUICK_START.md` لـ:

- إعدادات PostgreSQL الموصى بها
- استراتيجيات الفهرسة
- تحديث Materialized Views
- النسخ الاحتياطي والاستعادة

---

## 🛠️ استكشاف الأخطاء

### المشكلة: "PostgreSQL غير مثبت"

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql-15 postgresql-contrib

# تشغيل الخدمة
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### المشكلة: "pgvector غير موجود"

```bash
# سيثبته install_linux.sh تلقائياً
# أو يمكنك تثبيته يدوياً:
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

### المشكلة: "no such table"

```bash
# استخدم أداة الاستكشاف لمعرفة الأسماء الحقيقية
./explore_sqlite.py /path/to/db.db --sample
```

### المشكلة: "permission denied"

```sql
-- منح الصلاحيات في PostgreSQL
GRANT USAGE ON SCHEMA quran TO your_user;
GRANT SELECT ON ALL TABLES IN SCHEMA quran TO your_user;
```

---

## 📞 هل تحتاج مساعدة؟

| نوع المساعدة | المصدر |
|--------------|--------|
| 📖 فهم المشروع | `README.md` |
| ⚡ تثبيت سريع | `QUICK_START.md` |
| 📥 استيراد البيانات | `IMPORT_GUIDE.md` |
| 🏗️ فهم البنية | `00_DATABASE_ANALYSIS.md` |
| 🔍 استعلامات | `SMART_QUERIES.md` |
| 🗺️ الفهرس الشامل | `INDEX.md` |
| 📧 دعم فني | duhatv@gmail.com |

---

## ✅ قائمة التحقق

### قبل البدء
- [ ] PostgreSQL 15+ مثبت
- [ ] لديك قواعد بيانات SQLite جاهزة
- [ ] مساحة تخزين كافية (5GB+)
- [ ] قرأت `INDEX.md` و `README.md`

### التثبيت
- [ ] نفّذت `install_linux.sh` بنجاح
- [ ] تحققت من إنشاء الجداول
- [ ] تحققت من الامتدادات

### الاستيراد
- [ ] استكشفت قواعد SQLite الموجودة
- [ ] أنشأت ملف تكوين مناسب
- [ ] نفّذت عملية الاستيراد
- [ ] تحققت من البيانات المستوردة

### الاختبار
- [ ] جرّبت استعلامات من `SMART_QUERIES.md`
- [ ] تحققت من الأداء
- [ ] أعددت النسخ الاحتياطي

---

## 🎯 الخلاصة

الآن لديك:

✅ قاعدة بيانات PostgreSQL احترافية جاهزة
✅ 19 جدول منظم في 5 مستويات هرمية
✅ أدوات استيراد ذكية ومرنة
✅ وثائق شاملة بالعربية
✅ 50+ استعلام جاهز للاستخدام
✅ سكريبتات تثبيت تلقائية
✅ أمثلة عملية متنوعة

---

<div align="center">

## 🌟 استمتع ببناء تطبيقك القرآني! 🌟

**جميع الأدوات جاهزة - ابدأ الآن!**

**All tools are ready - Start now!**

---

**📧 Email:** duhatv@gmail.com
**🌐 Website:** duhatv.net
**📱 Phone:** +905342390000

---

**آخر تحديث:** 2025-10-30
**الإصدار:** 1.0.0

</div>

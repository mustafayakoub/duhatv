# 📦 القرآن الكريم Ultimate v3.0 - الحزمة الكاملة
## Quran Ultimate v3.0 - Complete Package

---

<div align="center">

**🎉 تطبيق قرآني احترافي متكامل**

**قاعدة بيانات PostgreSQL + SQLite | واجهة PyQt6 عصرية**

**✅ جاهز للتشغيل الفوري!**

</div>

---

## 📋 محتويات الحزمة

### 📱 التطبيقات (4 إصدارات)

| الملف | الإصدار | الوصف |
|-------|---------|-------|
| `quran_ultimate.py` | **v3.0** ⭐ | التطبيق الجديد - PostgreSQL + SQLite |
| `quran_pro.py` | v2.1 | تطبيق متقدم مع صوتيات |
| `quran_app_v2_final.py` | v2.0 | إصدار مستقر |
| `quran_app_ultimate.py` | v1.0 | الإصدار الأول |

**🌟 الإصدار الموصى به: `quran_ultimate.py`**

---

### 🗄️ قاعدة البيانات

```
database/
├── sql/                    ← 4 سكريبتات PostgreSQL
│   ├── 01_setup_no_vector.sql
│   ├── 02_level0_core_tables.sql
│   ├── 03_remaining_levels.sql
│   └── 04_views_and_functions.sql
│
├── explore_sqlite.py       ← استكشاف قواعد SQLite
├── import_from_sqlite.py   ← استيراد بسيط
├── import_advanced.py      ← استيراد متقدم
├── import_config.template.json
│
├── install_linux.sh        ← تثبيت تلقائي Linux
├── install_windows.bat     ← تثبيت تلقائي Windows
│
└── *.md                    ← 9 وثائق شاملة
```

---

### 💻 الكود المصدري

```
src/
├── postgres_manager.py  ⭐ جديد - مدير PostgreSQL
├── db_manager.py           مدير SQLite
├── config.py               الإعدادات
├── audio_player.py         مشغل الصوت
├── audio_widget.py         واجهة الصوت
└── dialogs.py              النوافذ المنبثقة
```

---

### 📚 الوثائق (7 ملفات)

| الوثيقة | الحجم | الوصف |
|---------|-------|-------|
| **ULTIMATE_GUIDE.md** | 20 KB | ⭐ دليل التطبيق الشامل |
| **DEVELOPMENT_SUMMARY.md** | 13 KB | ملخص التطوير الكامل |
| README.md | 7 KB | نظرة عامة |
| INSTALL.md | 4 KB | دليل التثبيت |
| AUDIO_FEATURE.md | 8 KB | دليل الصوتيات |
| TEST_APP.md | 8 KB | دليل الاختبار |
| START_HERE.txt | 14 KB | دليل البداية |

**في مجلد database:**
- INDEX.md - فهرس شامل
- GET_STARTED.md - البدء السريع
- IMPORT_GUIDE.md - دليل الاستيراد
- DEPLOYMENT_REPORT.md - تقرير النشر
- SMART_QUERIES.md - 50+ استعلام
- QUICK_START.md - تثبيت سريع
- README.md - معلومات القاعدة
- 00_DATABASE_ANALYSIS.md - التحليل المعماري

---

### ⚙️ الإعدادات والسكريبتات

```
requirements.txt              ← متطلبات v2.x
requirements_ultimate.txt  ⭐ متطلبات v3.0

run.sh                        ← تشغيل v2.x (Linux)
run_ultimate.sh            ⭐ تشغيل v3.0 (Linux)

run.bat / RUN_APP.bat         ← تشغيل Windows
```

---

## 🚀 التشغيل السريع (3 خطوات)

### الخطوة 1️⃣: فك الضغط

```bash
# Linux/Mac
unzip Quran_Ultimate_v3.0_Complete.zip -d quran_ultimate
cd quran_ultimate

# Windows
# انقر بزر الماوس الأيمن → Extract All
```

---

### الخطوة 2️⃣: تثبيت المتطلبات

```bash
# تثبيت PyQt6 (إلزامي)
pip3 install PyQt6

# تثبيت psycopg2 (اختياري - لـ PostgreSQL)
pip3 install psycopg2-binary

# أو تثبيت كل المتطلبات
pip3 install -r requirements_ultimate.txt
```

---

### الخطوة 3️⃣: التشغيل!

#### Linux/Mac:
```bash
chmod +x run_ultimate.sh
./run_ultimate.sh
```

#### Windows:
```cmd
python quran_ultimate.py
```

#### أو مباشرة:
```bash
python3 quran_ultimate.py
```

---

## 🎯 اختر قاعدة البيانات

عند التشغيل لأول مرة:

```
┌─────────────────────────────────┐
│  📖 القرآن الكريم Ultimate      │
│     اختر نوع قاعدة البيانات     │
├─────────────────────────────────┤
│  🐘 PostgreSQL                  │
│  قاعدة بيانات هرمية ذكية       │
│  بحث متقدم + إحصائيات           │
│                                 │
│  💾 SQLite                       │
│  قاعدة بيانات محلية             │
│  سريع وبسيط                     │
└─────────────────────────────────┘
```

### اختر PostgreSQL إذا:
- ✅ لديك PostgreSQL مثبت
- ✅ تريد بحث متقدم (Full-Text Search)
- ✅ تخطط لإضافة تفاسير وترجمات
- ✅ تريد إحصائيات وتحليلات

### اختر SQLite إذا:
- ✅ تريد تشغيل سريع بدون إعداد
- ✅ لا تحتاج ميزات متقدمة
- ✅ تفضل البساطة

---

## 🗄️ إعداد PostgreSQL (إذا اخترته)

### 1. تثبيت PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get install postgresql-15

# macOS
brew install postgresql@15

# Windows
# حمّل من: https://www.postgresql.org/download/
```

### 2. تشغيل قاعدة البيانات

```bash
# انتقل لمجلد database
cd database

# Linux
chmod +x install_linux.sh
./install_linux.sh

# Windows
install_windows.bat
```

هذا سينشئ:
- ✅ قاعدة `quran_hierarchical_db`
- ✅ 3 جداول أساسية
- ✅ بيانات نموذجية للتجربة

### 3. استيراد البيانات الكاملة (اختياري)

```bash
# إذا كان لديك قاعدة SQLite موجودة
./explore_sqlite.py /path/to/your/quran.db

# استيراد البيانات
./import_from_sqlite.py
```

---

## 📖 استخدام التطبيق

### الميزات الأساسية:

1. **تصفح السور**
   - اختر من قائمة السور
   - عرض فوري للسورة كاملة

2. **البحث**
   - اكتب في حقل البحث
   - نتائج فورية مع تمييز

3. **تبديل الرسم**
   - عثماني: بِسۡمِ ٱللَّهِ
   - إملائي: بسم الله

4. **معلومات تفصيلية**
   - رقم السورة والآية
   - رقم الصفحة والجزء
   - نوع السورة (مكية/مدنية)

---

## 📚 قراءة الوثائق

### للبدء:
```bash
cat ULTIMATE_GUIDE.md
```

### لفهم المشروع:
```bash
cat DEVELOPMENT_SUMMARY.md
```

### لإعداد القاعدة:
```bash
cd database
cat GET_STARTED.md
```

---

## 🆘 حل المشاكل

### المشكلة: "PyQt6 not found"
```bash
pip3 install PyQt6
```

### المشكلة: "psycopg2 not found"
```bash
# اختر SQLite بدلاً من PostgreSQL
# أو ثبت psycopg2:
pip3 install psycopg2-binary
```

### المشكلة: "no such table"
```bash
# تأكد من وجود ملف قاعدة البيانات في مجلد data
# أو استخدم PostgreSQL بعد تنفيذ install_linux.sh
```

### المشكلة: الخط لا يظهر صحيحاً
```bash
# ثبت خطوط عربية
sudo apt-get install fonts-arabeyes
```

---

## 📁 هيكل المشروع

```
quran_ultimate/
├── 📱 quran_ultimate.py        ← التطبيق الرئيسي
├── 📚 ULTIMATE_GUIDE.md        ← اقرأ هذا أولاً!
├── 📊 DEVELOPMENT_SUMMARY.md   ← ملخص شامل
│
├── src/                        ← الكود المصدري
│   ├── postgres_manager.py     ← مدير PostgreSQL
│   ├── db_manager.py           ← مدير SQLite
│   └── ...
│
├── database/                   ← قاعدة البيانات
│   ├── sql/                    ← سكريبتات SQL
│   ├── *.py                    ← أدوات الاستيراد
│   ├── *.sh/*.bat              ← سكريبتات التثبيت
│   └── *.md                    ← 9 وثائق
│
├── fonts/                      ← الخطوط العربية
├── data/                       ← البيانات
└── requirements_ultimate.txt   ← المتطلبات
```

---

## 💡 نصائح

### للحصول على أفضل تجربة:

1. ✅ اقرأ `ULTIMATE_GUIDE.md` أولاً
2. ✅ استخدم **PostgreSQL** للبحث المتقدم
3. ✅ استخدم **SQLite** للبساطة والسرعة
4. ✅ ثبت جميع المتطلبات من `requirements_ultimate.txt`
5. ✅ استورد بيانات كاملة من قاعدة موثوقة

---

## 📊 المواصفات التقنية

| المكون | التقنية |
|--------|---------|
| **اللغة** | Python 3.8+ |
| **الواجهة** | PyQt6 6.4+ |
| **القواعد** | PostgreSQL 15+ / SQLite 3 |
| **الحجم** | 157 KB (مضغوط) |
| **الملفات** | 60+ ملف |
| **السطور** | 7,000+ سطر |

---

## 🌟 الميزات

### ✨ واجهة عصرية
- تصميم أنيق مع تدرجات لونية
- سهلة الاستخدام
- نصوص واضحة ومريحة

### 🔍 بحث متقدم
- Full-Text Search في PostgreSQL
- بحث بسيط في SQLite
- تمييز النتائج
- معلومات تفصيلية

### 🗄️ قاعدة قوية
- بنية هرمية ذكية
- فهرسة محسنة
- قابلة للتوسع
- 19 جدول محتمل

### 📚 وثائق شاملة
- 9 ملفات وثائق
- 650+ صفحة
- أمثلة عملية
- دروس تفصيلية

---

## 🔮 الإصدارات القادمة

- [ ] التفاسير المتعددة
- [ ] الترجمات (40+ لغة)
- [ ] القراءات العشر
- [ ] الصوتيات المتزامنة
- [ ] الإشارات المرجعية
- [ ] التعليقات الشخصية
- [ ] تطبيق محمول
- [ ] واجهة ويب

---

## 📞 الدعم والمساعدة

### التواصل:
- **📧 Email:** duhatv@gmail.com
- **🌐 Website:** duhatv.net
- **📱 Phone:** +905342390000

### المساهمة:
نرحب بمساهماتكم:
- 🐛 الإبلاغ عن مشاكل
- 💡 اقتراح مزايا
- 🔧 تحسين الكود
- 📚 تحسين الوثائق

---

## ⚖️ الترخيص

هذا المشروع مفتوح المصدر ومجاني للجميع.

استخدمه، عدّله، شاركه كما تشاء.

---

## 🙏 شكر وتقدير

- **tanzil.net** - النصوص القرآنية
- **quran.com** - الإلهام
- **PostgreSQL** - قاعدة قوية
- **PyQt** - واجهات احترافية
- **المجتمع الإسلامي** - الدعم والتشجيع

---

<div align="center">

## 🎊 استمتع بالتطبيق! 🎊

**صُنع بـ ❤️ للمسلمين في كل مكان**

**Built with ❤️ for Muslims everywhere**

---

**🚀 للبدء الآن:**

```bash
./run_ultimate.sh
```

**أو**

```bash
python3 quran_ultimate.py
```

---

**📖 للمزيد من المعلومات:**

```bash
cat ULTIMATE_GUIDE.md
```

---

**📧 للدعم:**

duhatv@gmail.com

---

**تاريخ الإصدار:** 2025-10-30

**الإصدار:** 3.0.0

**الحالة:** ✅ جاهز للإنتاج

</div>

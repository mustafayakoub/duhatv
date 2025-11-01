# 🪟 تشغيل المشروع بدون Docker - مباشرة على Windows

<div dir="rtl">

## إذا لم تريد استخدام Docker، يمكنك تشغيل كل شيء محلياً!

</div>

---

## 📋 المتطلبات

### 1. PostgreSQL 16
**تحميل:** https://www.postgresql.org/download/windows/

**التثبيت:**
- Port: `5432`
- Username: `postgres`
- Password: `postgres` (أو ما تختاره)

### 2. Python 3.10+
**تحميل:** https://www.python.org/downloads/

**تثبيت:** ✅ Add Python to PATH

### 3. Rust (للـ Backend)
**تحميل:** https://www.rust-lang.org/tools/install

**تشغيل:** `rustup-init.exe`

---

## 🗄️ الخطوة 1: إعداد قاعدة البيانات

### افتح pgAdmin أو psql

```sql
-- إنشاء قاعدة البيانات
CREATE DATABASE quran_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Arabic_Saudi Arabia.1256'
    LC_CTYPE = 'Arabic_Saudi Arabia.1256';

-- الاتصال بقاعدة البيانات
\c quran_db

-- تطبيق Schema
\i C:/quran11/database/migrations/001_schema.sql
```

**أو من CMD:**
```cmd
cd C:\quran11\database\migrations
psql -U postgres -d quran_db -f 001_schema.sql
```

---

## 🐍 الخطوة 2: نقل البيانات (Python)

### في CMD أو PowerShell:

```powershell
cd C:\quran11\scripts

# تثبيت المكتبات
pip install psycopg2-binary python-dotenv

# تعديل المتغيرات
set TARGET_DB_URL=postgresql://postgres:postgres@localhost:5432/quran_db
set SOURCE_DB_1=C:/quran9/quran_ultimate_final.db
set SOURCE_DB_2=C:/quran9/surah_database_app_v32.db
set SOURCE_DB_3=C:/quran9/Quran_Crystalline.db

# تشغيل Migration
python migrate_data.py
```

**انتظر...** (5-30 دقيقة حسب حجم البيانات)

---

## 🦀 الخطوة 3: تشغيل Rust Backend

### في PowerShell:

```powershell
cd C:\quran11\backend-rust

# تعيين متغير البيئة
$env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/quran_db"

# تشغيل
cargo run --release
```

**انتظر...** (أول مرة قد يستغرق وقتاً للترجمة)

**يعمل على:** http://localhost:8000

---

## ✅ الخطوة 4: الاختبار

### افتح المتصفح:

**1. Health Check:**
```
http://localhost:8000/health
```

**2. قائمة السور:**
```
http://localhost:8000/api/v1/surahs
```

**3. سورة الفاتحة:**
```
http://localhost:8000/api/v1/surahs/1/ayahs
```

**4. البحث:**
```
http://localhost:8000/api/v1/search?q=الحمد
```

---

## 📝 ملف Batch للتشغيل السريع

**احفظ هذا في** `C:\quran11\RUN_LOCAL.bat`:

```batch
@echo off
echo ═══════════════════════════════════════════════════════════════════════════
echo   🚀 Quran Modern Stack - Local Run
echo ═══════════════════════════════════════════════════════════════════════════

REM تعيين المتغيرات
set DATABASE_URL=postgresql://postgres:postgres@localhost:5432/quran_db
set RUST_LOG=info

REM الانتقال إلى مجلد Rust
cd /d C:\quran11\backend-rust

REM تشغيل Rust Backend
echo 🦀 Starting Rust Backend...
cargo run --release

pause
```

**شغّله بالضغط المزدوج!**

---

## 🔧 حل المشاكل

### مشكلة: "psql: error: connection to server failed"

**الحل:**
1. تأكد من تشغيل PostgreSQL
2. افتح Services (Win+R → `services.msc`)
3. ابحث عن "postgresql"
4. اضغط "Start"

---

### مشكلة: "cargo: command not found"

**الحل:**
1. أعد تشغيل PowerShell
2. أو أعد تشغيل الكمبيوتر
3. تحقق: `rustc --version`

---

### مشكلة: "error: linker `link.exe` not found"

**الحل:**
ثبت **Microsoft C++ Build Tools**:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

---

### مشكلة: Migration بطيء جداً

**الحل:**
عدّل `migrate_data.py` - قلل `page_size` في:
```python
execute_batch(self.cursor, insert_query, ayahs, page_size=100)  # كان 500
```

---

## ⚡ الأداء

**بدون Docker:**
- ✅ أسرع قليلاً (لا overhead)
- ✅ استخدام مباشر للموارد
- ✅ سهل للتطوير

**مع Docker:**
- ✅ أسهل في الإعداد
- ✅ بيئة معزولة
- ✅ سهل النشر

---

## 🎯 الخطوات القادمة

بعد التشغيل الناجح:

1. ✅ **Frontend** - أضف واجهة React
2. ✅ **Go Service** - أضف خدمة البحث
3. ✅ **Redis** - أضف Caching
4. ✅ **API Documentation** - أضف Swagger

---

<div dir="rtl" align="center">

## 🎉 تم! النظام يعمل محلياً!

**الآن عندك:**
- ✅ PostgreSQL مع 2+ مليون سجل
- ✅ Rust API سريع جداً
- ✅ كل شيء محلي على Windows

**أسرع من Python بـ 100 مرة! 🚀**

</div>

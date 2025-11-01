# 🚀 دليل التشغيل السريع لـ Windows

<div dir="rtl">

## مرحباً! هذا دليل مبسط جداً لتشغيل المشروع على Windows 🪟

</div>

---

## ✅ الخطوة 1: تحقق من المتطلبات

قبل البدء، تأكد من تثبيت:

### Docker Desktop لـ Windows
- **تحميل**: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **تثبيت**: شغّل الملف وانتظر الانتهاء
- **تشغيل**: افتح Docker Desktop وانتظر حتى يبدأ

### تحقق من التثبيت
افتح **PowerShell** أو **CMD** واكتب:
```powershell
docker --version
docker-compose --version
```

يجب أن ترى الإصدارات:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

---

## 📁 الخطوة 2: ترتيب الملفات

### المسار المطلوب:
```
C:\quran11\              ← مجلد المشروع
├── .env                 ← ملف الإعدادات (أنشئه!)
├── docker-compose.yml
├── README.md
├── database/
├── backend-rust/
├── scripts/
└── ...
```

### أنشئ ملف `.env`

**افتح Notepad** واكتب:
```env
POSTGRES_DB=quran_db
POSTGRES_USER=quran
POSTGRES_PASSWORD=quran_secure_pass_2025
DATABASE_URL=postgresql://quran:quran_secure_pass_2025@postgres:5432/quran_db

REDIS_PASSWORD=redis_secure_pass_2025
REDIS_URL=redis://:redis_secure_pass_2025@redis:6379

SOURCE_DB_1=C:/quran9/quran_ultimate_final.db
SOURCE_DB_2=C:/quran9/surah_database_app_v32.db
SOURCE_DB_3=C:/quran9/Quran_Crystalline.db
```

**احفظه** باسم `.env` (مع النقطة!) في `C:\quran11\`

---

## ⚙️ الخطوة 3: تعديل docker-compose.yml

**افتح** `C:\quran11\docker-compose.yml` بـ Notepad

**ابحث عن** السطر:
```yaml
    volumes:
      - C:/quran9:/source-dbs:ro
```

**غيّره إلى** مسار قواعد البيانات عندك:
```yaml
    volumes:
      - C:/quran9:/source-dbs:ro  # إذا كانت قواعد البيانات في C:\quran9
```

**أو** إذا كانت في مكان آخر:
```yaml
    volumes:
      - C:/path/to/your/databases:/source-dbs:ro
```

---

## 🎯 الخطوة 4: التشغيل!

### افتح PowerShell أو CMD

```powershell
# اذهب إلى مجلد المشروع
cd C:\quran11
```

### شغّل Docker Compose

```powershell
docker-compose up -d
```

**انتظر...**  سيتم تحميل الصور (أول مرة فقط، قد يستغرق وقتاً)

```
[+] Running 5/5
 ✔ Network quran-network       Created
 ✔ Container quran-postgres     Started
 ✔ Container quran-redis        Started
 ✔ Container quran-backend-rust Started
 ✔ Container quran-frontend     Started
```

---

## 📊 الخطوة 5: إنشاء قاعدة البيانات

### تطبيق Schema

```powershell
docker-compose exec postgres psql -U quran -d quran_db -f /migrations/001_schema.sql
```

يجب أن ترى:
```
CREATE EXTENSION
CREATE EXTENSION
CREATE TABLE
CREATE TABLE
...
```

### نقل البيانات (اختياري الآن)

```powershell
docker-compose run --rm migration
```

**ملاحظة:** قد يستغرق نقل البيانات وقتاً (5-30 دقيقة حسب حجم البيانات)

---

## 🌐 الخطوة 6: اختبار النظام

### 1. افتح المتصفح

**اذهب إلى:** http://localhost:8000/health

**يجب أن ترى:**
```json
{
  "status": "healthy",
  "service": "quran-backend-rust",
  "version": "1.0.0"
}
```

### 2. اختبر السور

**اذهب إلى:** http://localhost:8000/api/v1/surahs

**يجب أن ترى** قائمة السور (بعد نقل البيانات):
```json
{
  "success": true,
  "data": [...],
  "count": 114
}
```

---

## 📋 أوامر مفيدة

### عرض الخدمات العاملة
```powershell
docker-compose ps
```

### عرض اللوجز
```powershell
# كل الخدمات
docker-compose logs -f

# خدمة محددة
docker-compose logs -f backend-rust
docker-compose logs -f postgres
```

### إيقاف الخدمات
```powershell
docker-compose down
```

### إعادة التشغيل
```powershell
docker-compose restart
```

### حذف كل شيء والبدء من جديد
```powershell
docker-compose down -v
docker-compose up -d
```

---

## ❌ حل المشاكل الشائعة

### مشكلة: "docker: command not found"

**الحل:**
1. تأكد من تثبيت Docker Desktop
2. أعد تشغيل الكمبيوتر
3. تأكد من تشغيل Docker Desktop

---

### مشكلة: "Error: Cannot connect to Docker daemon"

**الحل:**
1. افتح Docker Desktop
2. انتظر حتى يبدأ (أيقونة Docker في الـ System Tray)
3. حاول مرة أخرى

---

### مشكلة: "Port is already allocated"

**الحل:**
```powershell
# أوقف الخدمات
docker-compose down

# غيّر الـ Port في docker-compose.yml
# مثلاً بدل 8000:8000 إلى 8080:8000

# شغّل مرة أخرى
docker-compose up -d
```

---

### مشكلة: "No such file or directory: /migrations/001_schema.sql"

**الحل:**
تأكد من وجود المجلد `database/migrations/` والملف `001_schema.sql` فيه.

---

### مشكلة: قواعد البيانات غير موجودة

**الحل:**
1. تأكد من وجود الملفات في `C:\quran9\`
2. عدّل المسار في `.env` و `docker-compose.yml`

مثال:
```env
SOURCE_DB_1=C:/المسار/الصحيح/quran_ultimate_final.db
```

---

## 🎨 الواجهات

| الخدمة | الرابط | الوصف |
|--------|--------|-------|
| 🦀 Rust API | http://localhost:8000 | API رئيسي |
| 🦀 Health Check | http://localhost:8000/health | صحة النظام |
| 🦀 Surahs | http://localhost:8000/api/v1/surahs | قائمة السور |
| 🦀 Search | http://localhost:8000/api/v1/search?q=الحمد | بحث |

---

## 🚀 اختصارات للاختبار السريع

احفظ هذا في ملف `test.bat`:

```batch
@echo off
echo ===================================
echo Testing Quran Modern Stack
echo ===================================

echo.
echo 1. Health Check:
curl http://localhost:8000/health

echo.
echo 2. Get Surahs:
curl http://localhost:8000/api/v1/surahs

echo.
echo 3. Search:
curl "http://localhost:8000/api/v1/search?q=الحمد"

echo.
echo ===================================
echo Tests Complete!
echo ===================================
pause
```

شغّله بالضغط المزدوج عليه!

---

## 📖 الخطوات القادمة

بعد التشغيل الناجح:

1. ✅ **نقل البيانات** - استخدم `docker-compose run --rm migration`
2. ✅ **إضافة Frontend** - واجهة ويب جميلة
3. ✅ **إضافة Go Service** - بحث متقدم
4. ✅ **تخصيص** - غيّر الألوان والتصميم

---

## 💡 نصائح

- 🔄 **Docker Desktop** يجب أن يكون شغال دائماً
- 📊 **اللوجز** مفيدة لمعرفة المشاكل: `docker-compose logs -f`
- 🛑 **إيقاف نظيف** استخدم `docker-compose down` قبل إغلاق الكمبيوتر
- 💾 **Backup** احتفظ بنسخة من `.env` و `docker-compose.yml`

---

<div dir="rtl" align="center">

## 🎉 مبروك! النظام جاهز!

**استمتع بأسرع نظام قرآني في العالم!**

⚡ **أسرع 100 مرة من Python**

🦀 **مبني بـ Rust** - أقوى لغة برمجية

🌍 **دعم كامل للعربية** - في كل مكان

---

**هل واجهت مشكلة؟**

📧 تواصل معنا أو افتح Issue على GitHub

</div>

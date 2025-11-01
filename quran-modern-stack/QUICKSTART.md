# 🚀 دليل التشغيل السريع - Quran Modern Stack

<div dir="rtl">

## مرحباً بك في نظام القرآن الحديث المتكامل! 🌟

هذا الدليل سيساعدك في تشغيل النظام الكامل في **أقل من 5 دقائق**!

</div>

---

## 📋 المتطلبات الأساسية

قبل البدء، تأكد من تثبيت:

✅ **Docker Desktop** (Windows/Mac) أو Docker + Docker Compose (Linux)
✅ **قواعد البيانات الثلاث** في المسار: `C:\quran9\`

---

## 🎯 التشغيل السريع (3 خطوات فقط!)

### 1️⃣ استنساخ المشروع

```bash
# Clone the repository
git clone <repository-url>
cd quran-modern-stack
```

### 2️⃣ تشغيل كل الخدمات

```bash
# ابدأ كل الخدمات بأمر واحد!
docker-compose up -d
```

سيتم تشغيل:
- ✅ PostgreSQL (قاعدة البيانات)
- ✅ Redis (الكاش)
- ✅ Rust Backend API
- ✅ Go Search Service
- ✅ React Frontend

### 3️⃣ نقل البيانات

```bash
# تطبيق Schema
docker-compose exec postgres psql -U quran -d quran_db -f /migrations/001_schema.sql

# نقل البيانات من القواعد الثلاث
docker-compose run --rm migration
```

**🎉 تم! النظام جاهز الآن!**

---

## 🌐 الوصول للتطبيق

| الخدمة | الرابط | الوصف |
|--------|--------|-------|
| 🎨 **Frontend** | http://localhost:3000 | الواجهة الرئيسية |
| ⚡ **Rust API** | http://localhost:8000 | API رئيسي |
| 🐹 **Go Search** | http://localhost:8001 | خدمة البحث |
| 📊 **PostgreSQL** | localhost:5432 | قاعدة البيانات |
| 🔴 **Redis** | localhost:6379 | الكاش |

---

## 🧪 اختبار النظام

### اختبار Rust API

```bash
# Health check
curl http://localhost:8000/health

# Get all surahs
curl http://localhost:8000/api/v1/surahs

# Get specific surah
curl http://localhost:8000/api/v1/surahs/1

# Get ayahs of Al-Fatiha
curl http://localhost:8000/api/v1/surahs/1/ayahs

# Search in Quran
curl "http://localhost:8000/api/v1/search?q=الحمد"
```

### اختبار من المتصفح

افتح: http://localhost:3000

---

## 📊 مراقبة النظام

### عرض اللوجز (Logs)

```bash
# كل الخدمات
docker-compose logs -f

# خدمة محددة
docker-compose logs -f backend-rust
docker-compose logs -f search-service-go
docker-compose logs -f frontend
```

### حالة الخدمات

```bash
docker-compose ps
```

---

## 🛠️ التطوير

<div dir="rtl">

### تطوير Rust Backend

</div>

```bash
cd backend-rust

# Install Rust (if needed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Run locally
cargo run

# Build release
cargo build --release

# Test
cargo test
```

<div dir="rtl">

### تطوير Go Service

</div>

```bash
cd services-go/search-service

# Install Go (if needed)
# Download from: https://go.dev/dl/

# Run locally
go run main.go

# Build
go build -o search-service

# Test
go test ./...
```

<div dir="rtl">

### تطوير Frontend

</div>

```bash
cd frontend-ts

# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Test
npm test
```

---

## 🔧 استكشاف الأخطاء

### المشكلة: PostgreSQL لا يعمل

```bash
# إعادة تشغيل
docker-compose restart postgres

# عرض اللوج
docker-compose logs postgres

# الدخول للـ Container
docker-compose exec postgres psql -U quran -d quran_db
```

### المشكلة: قواعد البيانات المصدر غير موجودة

تأكد من:
1. وجود الملفات في `C:\quran9\`
2. تعديل المسار في `docker-compose.yml` إذا كان مختلفاً

```yaml
# في docker-compose.yml تحت migration service
volumes:
  - /your/actual/path:/source-dbs:ro  # غيّر هذا السطر
```

### المشكلة: Rust build بطيء جداً

```bash
# استخدم cache للتسريع
docker-compose build --no-cache backend-rust
```

### المشكلة: Frontend لا يتصل بـ API

تأكد من:
1. Backend يعمل: `curl http://localhost:8000/health`
2. CORS مفعّل في Backend
3. المتغيرات في `.env` صحيحة

---

## 📦 الأوامر المفيدة

### إيقاف وبدء

```bash
# إيقاف كل الخدمات
docker-compose down

# بدء كل الخدمات
docker-compose up -d

# إعادة تشغيل خدمة محددة
docker-compose restart backend-rust
```

### تنظيف النظام

```bash
# إيقاف وحذف الـ containers
docker-compose down

# إيقاف وحذف كل شيء (بما فيه البيانات!)
docker-compose down -v

# حذف الصور
docker-compose down --rmi all
```

### إعادة البناء

```bash
# إعادة بناء كل الصور
docker-compose build

# إعادة بناء بدون cache
docker-compose build --no-cache

# إعادة بناء خدمة محددة
docker-compose build backend-rust
```

---

## 🎨 التخصيص

### تغيير الـ Port

في `docker-compose.yml`:

```yaml
services:
  backend-rust:
    ports:
      - "8080:8000"  # غيّر 8080 للـ port الذي تريده
```

### تغيير قاعدة البيانات

في `.env`:

```env
POSTGRES_DB=my_quran_db
POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_secure_password
```

---

## 📈 الإنتاج (Production)

### بناء للإنتاج

```bash
# Build all services
docker-compose -f docker-compose.prod.yml build

# Run in production mode
docker-compose -f docker-compose.prod.yml up -d
```

### النشر (Deployment)

الخيارات:
- ☁️ **AWS ECS** - Elastic Container Service
- ☁️ **Google Cloud Run** - Serverless containers
- ☁️ **DigitalOcean App Platform** - Simple deployment
- 🐳 **Kubernetes** - للمشاريع الكبيرة

---

## 🔒 الأمان

### تغيير كلمات المرور

❗ **مهم جداً للإنتاج:**

1. غيّر `POSTGRES_PASSWORD` في `.env`
2. غيّر `REDIS_PASSWORD` في `.env`
3. غيّر `JWT_SECRET` في `.env`

```env
POSTGRES_PASSWORD=your-super-secure-password-here
REDIS_PASSWORD=another-secure-password
JWT_SECRET=very-long-and-random-jwt-secret-key
```

---

## 📚 الموارد الإضافية

- 📖 [الوثائق الكاملة](./README.md)
- 🏗️ [تحليل قواعد البيانات](./DATABASE_ANALYSIS.md)
- 🎯 [البنية المعمارية](./ARCHITECTURE.md)
- 🐛 [الإبلاغ عن الأخطاء](https://github.com/your-repo/issues)

---

## 🆘 الحصول على المساعدة

إذا واجهت أي مشاكل:

1. 📖 اقرأ [قسم استكشاف الأخطاء](#-استكشاف-الأخطاء) أعلاه
2. 🔍 ابحث في [القضايا المفتوحة](https://github.com/your-repo/issues)
3. 💬 افتح [قضية جديدة](https://github.com/your-repo/issues/new)
4. 📧 راسلنا على: support@example.com

---

<div dir="rtl" align="center">

## 🎉 تهانينا! النظام جاهز للاستخدام!

**نتمنى لك تجربة رائعة مع Quran Modern Stack**

بُني بـ ❤️ باستخدام **Rust 🦀 + Go 🐹 + TypeScript 💙**

</div>

---

## 🌟 النسخة القادمة

قريباً:
- [ ] Go Microservice للبحث المتقدم
- [ ] TypeScript Frontend الكامل
- [ ] دعم GraphQL
- [ ] تطبيق Mobile (React Native)
- [ ] AI-powered Search
- [ ] Audio recitation support

**ابقَ على اتصال! 🚀**

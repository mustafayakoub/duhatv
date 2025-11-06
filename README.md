# 🌟 مشروع بصائر القرآن الكريم
# Basaer Quran Insights Project

<div align="center">

![Status](https://img.shields.io/badge/status-in--development-yellow)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**موسوعة قرآنية شاملة مفتوحة المصدر**
**Comprehensive Open-Source Quranic Encyclopedia**

[الوثائق](#-الوثائق) • [البدء السريع](#-البدء-السريع) • [المميزات](#-المميزات) • [المساهمة](#-المساهمة)

</div>

---

## 📖 نظرة عامة

**بصائر القرآن الكريم** هو مشروع موسوعي طموح يهدف إلى بناء أذكى وأشمل منصة قرآنية رقمية في العالم، تجمع بين:

- 🕌 **1400 سنة** من التفاسير والعلوم القرآنية
- 🤖 **أحدث التقنيات** (Rust, Go, TypeScript, PostgreSQL, AI)
- 🌍 **الانفتاح والشفافية** (Open Source & Community-Driven)
- ⚡ **الأداء والدقة** (قاعدة بيانات محسّنة + بحث ذكي)

### الأرقام الرئيسية

```
📚 114 سورة          |  6,236 آية          |  77,432 كلمة
🔤 1,775 جذر لغوي    |  102+ تفسير         |  81,068+ ترجمة
📖 293 مصدر موثق     |  6,145 تصنيف موضوعي |  2M+ سجل بيانات
```

---

## ✨ المميزات

### 🎯 النص القرآني الكامل
- ✅ النص العثماني (بالتشكيل الكامل)
- ✅ النص الإملائي (الرسم الحديث)
- ✅ 7 قراءات متواترة (حفص، ورش، قالون، شعبة، السوسي، الدوري)
- ✅ مصحف التجويد المرمز بالألوان
- ✅ 72+ لغة ترجمة

### 🔬 التحليل اللغوي المتقدم
- ✅ إعراب كامل لكل كلمة (77,432 إعراب)
- ✅ تحليل صرفي شامل (الأوزان، الجذور، الاشتقاقات)
- ✅ معاني الكلمات بالعربية والإنجليزية
- ✅ 1,775 جذر لغوي فريد
- ✅ 2,006 فعل قرآني مع تصريفاته

### 📚 التفاسير والشروح
- ✅ 102+ تفسير عبر التاريخ
- ✅ مرتبة تاريخياً (من الطبري 310 هـ حتى اليوم)
- ✅ منقحة من التكرار والزوائد
- ✅ موثقة بالمصادر (293 مصدر)
- ✅ قابلة للبحث والمقارنة

### 🔍 البحث الذكي
- ✅ بحث نصي كامل (Full-text Search)
- ✅ بحث بالجذور اللغوية
- ✅ بحث بالموضوعات (6,145 تصنيف)
- ✅ بحث في التفاسير
- ✅ بحث دلالي (Semantic Search) بالذكاء الاصطناعي

### 🎨 الواجهات
- 🖥️ **Desktop App** (Tauri) - أوفلاين كامل لـ Windows/Mac/Linux
- 🌐 **Web App** (React) - متاح عالمياً على الإنترنت
- 📱 **Mobile Apps** (React Native) - iOS و Android

### 🚀 الأداء والتقنيات
- **Backend API:** Rust (Axum + SQLx + Tokio) - سرعة فائقة
- **Microservices:** Go (Fiber + GORM) - معالجة متزامنة
- **Database:** PostgreSQL 16 - محسّنة للعربية
- **Search Engine:** Meilisearch - بحث فوري
- **Cache:** Redis - استجابة سريعة
- **AI:** Python (Transformers, BERT) - ذكاء اصطناعي

---

## 🚀 البدء السريع

### المتطلبات

- **Docker** 24+ & **Docker Compose** 2.23+
- **Git** 2.40+
- (اختياري) **Rust** 1.75+, **Go** 1.21+, **Node.js** 20+

### التثبيت والتشغيل

```bash
# 1. استنساخ المشروع
git clone https://github.com/your-org/basaer-quran.git
cd basaer-quran

# 2. نسخ ملف البيئة
cp .env.example .env

# 3. تشغيل كل الخدمات (PostgreSQL + Redis + Meilisearch + API)
docker-compose up -d

# 4. تطبيق Schema
docker-compose exec postgres psql -U quran -d quran_db -f /migrations/001_schema.sql

# 5. استيراد البيانات
cd quran-modern-stack/scripts
python import_hafs_data.py --input /path/to/hafs_smart_v8.json

# 6. الوصول إلى API
curl http://localhost:8000/api/v1/surahs
```

**🎉 تهانينا! النظام يعمل الآن.**

### الوصول إلى الخدمات

| الخدمة | العنوان | الوصف |
|--------|---------|-------|
| API Gateway | http://localhost:8000 | Rust API |
| Meilisearch | http://localhost:7700 | محرك البحث |
| PostgreSQL | localhost:5432 | قاعدة البيانات |
| Redis | localhost:6379 | Cache |

---

## 📂 هيكل المشروع

```
basaer-quran/
├── 📄 README.md                        # هذا الملف
├── 📄 BASAER_PROJECT_PLAN.md          # خطة المشروع الشاملة
├── 📄 DATABASE_ANALYSIS.md            # تحليل قواعد البيانات
├── 📄 ARCHITECTURE.md                 # المعمارية التقنية
│
├── 📁 quran-modern-stack/             # المشروع الرئيسي
│   ├── 📁 database/
│   │   └── migrations/
│   │       └── 001_schema.sql         # PostgreSQL Schema
│   │
│   ├── 📁 backend-rust/               # Rust API
│   │   ├── Cargo.toml
│   │   ├── Dockerfile
│   │   └── src/
│   │       ├── main.rs
│   │       ├── routes/
│   │       ├── models/
│   │       └── db/
│   │
│   ├── 📁 services-go/                # Go Microservices
│   │   └── search-service/
│   │       ├── main.go
│   │       ├── handlers/
│   │       └── Dockerfile
│   │
│   ├── 📁 frontend-desktop/           # Tauri Desktop App
│   │   ├── package.json
│   │   ├── src-tauri/
│   │   └── src/
│   │
│   ├── 📁 scripts/                    # Python Scripts
│   │   ├── import_hafs_data.py       # استيراد البيانات
│   │   ├── migrate_data.py
│   │   └── requirements.txt
│   │
│   └── 📄 docker-compose.yml
│
└── 📁 data/                           # البيانات الخام
    ├── hafs_smart_v8.json
    ├── *.db (SQLite databases)
    └── fonts/
```

---

## 🛠️ التطوير

### إعداد بيئة التطوير

#### Backend (Rust)

```bash
cd quran-modern-stack/backend-rust

# تثبيت المكتبات
cargo build

# تشغيل الخادم
cargo run --release

# الاختبارات
cargo test
```

#### Microservices (Go)

```bash
cd quran-modern-stack/services-go/search-service

# تثبيت المكتبات
go mod download

# تشغيل الخدمة
go run main.go

# الاختبارات
go test ./...
```

#### Frontend (Tauri)

```bash
cd quran-modern-stack/frontend-desktop

# تثبيت المكتبات
npm install

# التطوير
npm run tauri dev

# البناء
npm run tauri build
```

---

## 📚 الوثائق

- 📖 [خطة المشروع الشاملة](./BASAER_PROJECT_PLAN.md)
- 🏗️ [المعمارية التقنية](./ARCHITECTURE.md)
- 💾 [تحليل قواعد البيانات](./DATABASE_ANALYSIS.md)
- 🚀 [دليل البدء السريع](./quran-modern-stack/QUICKSTART.md)
- 📡 [توثيق API](./quran-modern-stack/API_DOCS.md) (قريباً)
- 🤝 [دليل المساهمة](./CONTRIBUTING.md) (قريباً)

---

## 🗺️ خارطة الطريق

### ✅ المرحلة 0: التخطيط (مكتملة)
- [x] كتابة الوثائق الشاملة
- [x] تصميم قاعدة البيانات
- [x] تحديد المعمارية
- [x] كتابة سكريبتات الاستيراد

### 🔄 المرحلة 1: البنية الأساسية (قيد التنفيذ)
- [x] PostgreSQL Schema
- [ ] استيراد البيانات من JSON
- [ ] Rust API الأساسية
- [ ] Docker Compose

### 📅 المرحلة 2: المحتوى (Q1 2025)
- [ ] استيراد جميع التفاسير
- [ ] استيراد جميع الترجمات
- [ ] التحليل اللغوي الكامل
- [ ] القراءات المتعددة

### 📅 المرحلة 3: الواجهة (Q2 2025)
- [ ] Desktop App (Tauri)
- [ ] البحث المتقدم
- [ ] مصحف التجويد
- [ ] الفلاتر الذكية

### 📅 المرحلة 4: الذكاء الاصطناعي (Q3 2025)
- [ ] البحث الدلالي
- [ ] التلخيص الآلي
- [ ] Q&A Engine
- [ ] Knowledge Graph

### 📅 المرحلة 5: التوسع (Q4 2025+)
- [ ] Web App
- [ ] Mobile Apps
- [ ] منصة تعليمية
- [ ] Quran ChatGPT

---

## 🤝 المساهمة

نرحب بأي مساهمات! سواء كنت:
- 💻 **مطور:** ساهم في الكود
- 📚 **باحث:** دقق البيانات والتفاسير
- 🌍 **مترجم:** أضف ترجمات جديدة
- 🎨 **مصمم:** حسّن الواجهات
- 📝 **كاتب:** حسّن الوثائق

### كيف تساهم؟

1. **Fork** المشروع
2. أنشئ **Branch** جديد (`git checkout -b feature/amazing-feature`)
3. **Commit** تغييراتك (`git commit -m 'Add amazing feature'`)
4. **Push** إلى Branch (`git push origin feature/amazing-feature`)
5. افتح **Pull Request**

---

## 📜 الترخيص

هذا المشروع مفتوح المصدر تحت رخصة [MIT](LICENSE).

**يُسمح بـ:**
- ✅ الاستخدام التجاري
- ✅ التعديل والتوزيع
- ✅ الاستخدام الخاص
- ✅ البناء عليه

**بشرط:**
- 📄 الاحتفاظ بإشعار الترخيص
- 📄 الإشارة إلى المشروع الأصلي

---

## 🙏 شكر وتقدير

### المصادر والبيانات
- **Tanzil.net** - نص القرآن الكريم الموثوق
- **Quran.com** - API والبيانات المفتوحة
- **المدونة العربية القرآنية** - التحليل اللغوي
- **مجمع الملك فهد** - المصاحف والقراءات

### التقنيات المستخدمة
- **Rust** 🦀 - لغة برمجة آمنة وسريعة
- **Go** 🐹 - لغة برمجة بسيطة وفعالة
- **PostgreSQL** 🐘 - قاعدة بيانات قوية
- **React** ⚛️ - مكتبة واجهات حديثة

---

## 📞 التواصل

- **Email:** info@basaer-quran.org (قريباً)
- **Discord:** [Join our server](https://discord.gg/basaer) (قريباً)
- **Twitter:** [@BasaerQuran](https://twitter.com/BasaerQuran) (قريباً)
- **GitHub:** [Issues & Discussions](https://github.com/your-org/basaer-quran/issues)

---

## 💝 ادعمنا

إذا أعجبك المشروع:
- ⭐ أعط **نجمة** للمشروع على GitHub
- 🔄 **شارك** المشروع مع الآخرين
- 💰 **تبرع** لدعم التطوير (قريباً)
- 🤲 **ادعُ** لنا بالتوفيق والقبول

---

<div align="center">

### "إِنَّ هَٰذَا الْقُرْآنَ يَهْدِي لِلَّتِي هِيَ أَقْوَمُ" (الإسراء: 9)

**بُني بـ ❤️ لخدمة كتاب الله العزيز**

---

**آخر تحديث:** 2025-01-05 | **الإصدار:** 0.1.0 | **الحالة:** 🚧 قيد التطوير

[⬆️ العودة للأعلى](#-مشروع-بصائر-القرآن-الكريم)

</div>

# 🔍 Quran Search Service - خدمة البحث في القرآن الكريم

خدمة بحث سريعة ومتقدمة في القرآن الكريم مكتوبة بلغة Go، تستخدم PostgreSQL Full-Text Search و Redis للكاش.

A fast and advanced Quran search microservice written in Go, utilizing PostgreSQL Full-Text Search and Redis caching.

## ✨ المميزات - Features

### 🔎 بحث نصي كامل - Full-Text Search
- بحث سريع في نصوص القرآن الكريم باستخدام PostgreSQL FTS
- تطبيع تلقائي للنص العربي (إزالة التشكيل، توحيد الأحرف)
- دعم البحث بالفلاتر (السورة، الجزء، الصفحة)
- ترتيب النتائج حسب الصلة (Relevance Ranking)

### 🔄 بحث عن الآيات المتشابهة - Similar Verse Search
- البحث عن آيات مشابهة باستخدام Trigram Matching
- قابل للتخصيص عبر معامل التشابه (Threshold)
- مفيد لإيجاد آيات ذات معنى مشابه

### 💡 اقتراحات تلقائية - Auto-complete Suggestions
- اقتراحات فورية أثناء الكتابة
- دعم البحث في أسماء السور
- كاش طويل الأمد للأداء العالي

### ⚡ أداء عالي - High Performance
- استخدام Redis للكاش
- Connection pooling لقاعدة البيانات
- Graceful shutdown
- صور Docker صغيرة الحجم (Multi-stage builds)

## 🚀 التشغيل السريع - Quick Start

### المتطلبات - Prerequisites
- Go 1.21 أو أحدث
- PostgreSQL 16+
- Redis 7+ (اختياري)

### التثبيت - Installation

```bash
# استنساخ المشروع - Clone repository
cd /path/to/quran-modern-stack/services-go/search-service

# تحميل المكتبات - Download dependencies
go mod download

# تشغيل الخدمة - Run service
go run .
```

### التشغيل باستخدام Docker

```bash
# بناء الصورة - Build image
docker build -t quran-search-service .

# تشغيل الحاوية - Run container
docker run -p 8001:8001 \
  -e DATABASE_URL=postgresql://quran:pass@postgres:5432/quran_db \
  -e REDIS_URL=redis://:pass@redis:6379/0 \
  quran-search-service
```

### التشغيل باستخدام Docker Compose

```bash
# من المجلد الرئيسي للمشروع
docker-compose up -d search-service-go
```

## 📡 نقاط النهاية - API Endpoints

### 1. فحص الصحة - Health Check
```http
GET /health
```

**استجابة - Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-01T12:00:00Z",
  "service": "quran-search-service",
  "version": "1.0.0",
  "checks": {
    "database": true,
    "redis": true
  }
}
```

### 2. البحث في القرآن - Search Quran

```http
GET /api/search?q={query}&surah={number}&limit={count}
```

**المعاملات - Parameters:**
- `q` (مطلوب): نص البحث
- `surah` (اختياري): رقم السورة (1-114)
- `juz` (اختياري): رقم الجزء (1-30)
- `page` (اختياري): رقم الصفحة (1-604)
- `language` (اختياري): اللغة (ar, en) - افتراضياً: ar
- `limit` (اختياري): عدد النتائج (افتراضياً: 20، الحد الأقصى: 100)
- `offset` (اختياري): الإزاحة للترقيم (افتراضياً: 0)

**مثال - Example:**
```bash
curl "http://localhost:8001/api/search?q=الله&surah=1&limit=10"
```

**استجابة - Response:**
```json
{
  "results": [
    {
      "ayah_id": 1,
      "surah_number": 1,
      "ayah_number": 1,
      "surah_name_arabic": "الفاتحة",
      "surah_name_en": "Al-Fatihah",
      "text_uthmani": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
      "text_simple": "بسم الله الرحمن الرحيم",
      "juz_number": 1,
      "page_number": 1,
      "rank": 0.987,
      "matched_text": "بسم <mark>الله</mark> الرحمن الرحيم"
    }
  ],
  "total": 2699,
  "query": "الله",
  "limit": 10,
  "offset": 0,
  "execution_time_ms": 15.3
}
```

### 3. البحث عن الآيات المتشابهة - Find Similar Verses

```http
GET /api/similar?text={text}&threshold={value}
```

**المعاملات - Parameters:**
- `text` (مطلوب): النص المراد البحث عن مشابهات له
- `threshold` (اختياري): حد التشابه 0-1 (افتراضياً: 0.3)
- `limit` (اختياري): عدد النتائج (افتراضياً: 10، الحد الأقصى: 50)

**مثال - Example:**
```bash
curl "http://localhost:8001/api/similar?text=بسم الله الرحمن الرحيم&threshold=0.5"
```

**استجابة - Response:**
```json
{
  "results": [
    {
      "ayah_id": 1,
      "surah_number": 1,
      "ayah_number": 1,
      "text_uthmani": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
      "text_simple": "بسم الله الرحمن الرحيم",
      "rank": 1.0
    }
  ],
  "total": 5,
  "text": "بسم الله الرحمن الرحيم",
  "threshold": 0.5,
  "execution_time_ms": 8.2
}
```

### 4. الاقتراحات التلقائية - Auto-complete Suggestions

```http
GET /api/suggest?q={partial_query}
```

**المعاملات - Parameters:**
- `q` (مطلوب): الاستعلام الجزئي (2 أحرف على الأقل)
- `limit` (اختياري): عدد الاقتراحات (افتراضياً: 5، الحد الأقصى: 20)

**مثال - Example:**
```bash
curl "http://localhost:8001/api/suggest?q=الفات"
```

**استجابة - Response:**
```json
{
  "suggestions": [
    {
      "text": "الفاتحة",
      "type": "surah",
      "score": 0.95
    }
  ],
  "query": "الفات"
}
```

### 5. الإحصائيات - Metrics

```http
GET /metrics
```

**استجابة - Response:**
```json
{
  "timestamp": "2025-11-01T12:00:00Z",
  "service": "quran-search-service",
  "database": {
    "max_connections": 25,
    "acquired_connections": 3,
    "idle_connections": 5,
    "total_connections": 8
  },
  "cache": {
    "status": "available",
    "hits": 1523,
    "misses": 87,
    "total_conns": 10,
    "idle_conns": 8
  }
}
```

## 🔧 التكوين - Configuration

يتم التكوين عبر متغيرات البيئة:

| المتغير | الوصف | القيمة الافتراضية |
|---------|--------|-------------------|
| `PORT` | منفذ الخدمة | `8001` |
| `DATABASE_URL` | عنوان PostgreSQL | `postgresql://quran:pass@localhost:5432/quran_db` |
| `REDIS_URL` | عنوان Redis | `redis://:pass@localhost:6379/0` |
| `GO_ENV` | البيئة | `development` |
| `LOG_LEVEL` | مستوى السجلات | `info` |

## 🏗️ البنية المعمارية - Architecture

```
search-service/
├── main.go           # نقطة الدخول الرئيسية
├── handlers.go       # معالجات HTTP
├── search.go         # منطق البحث
├── cache.go          # طبقة الكاش
├── database.go       # اتصال قاعدة البيانات
├── Dockerfile        # صورة Docker
├── go.mod            # ملف المكتبات
├── go.sum            # ملف التحقق
└── README.md         # التوثيق
```

## 🎯 خوارزميات البحث - Search Algorithms

### 1. تطبيع النص العربي - Arabic Text Normalization

```go
// تطبيع تلقائي للنص العربي
// - إزالة التشكيل (الفتحة، الضمة، الكسرة، إلخ)
// - توحيد الأحرف المتشابهة (أ، إ، آ → ا)
// - إزالة التطويل (ـ)
```

### 2. البحث النصي الكامل - Full-Text Search

```sql
-- استخدام PostgreSQL tsvector و tsquery
-- للبحث السريع والمرتب
SELECT * FROM ayahs
WHERE search_vector @@ plainto_tsquery('arabic', 'الله')
ORDER BY ts_rank(search_vector, plainto_tsquery('arabic', 'الله')) DESC;
```

### 3. البحث بالتشابه - Trigram Similarity

```sql
-- استخدام pg_trgm لإيجاد النصوص المتشابهة
SELECT *, similarity(text_simple, 'بسم الله') as rank
FROM ayahs
WHERE similarity(text_simple, 'بسم الله') > 0.3
ORDER BY rank DESC;
```

## 📊 الأداء - Performance

### Benchmarks

- **البحث البسيط**: ~10-20ms
- **البحث مع فلاتر**: ~15-30ms
- **البحث عن المتشابهات**: ~20-40ms
- **الاقتراحات**: ~5-10ms (مع الكاش)

### التحسينات - Optimizations

- ✅ Connection pooling
- ✅ Redis caching
- ✅ GIN indexes على search_vector
- ✅ Trigram indexes على text_simple
- ✅ Prepared statements
- ✅ Context timeouts

## 🧪 الاختبار - Testing

```bash
# تشغيل الاختبارات
go test -v ./...

# اختبار مع التغطية
go test -cover ./...

# اختبار الأداء
go test -bench=. ./...
```

## 📝 التطوير - Development

### إضافة نقطة نهاية جديدة - Adding New Endpoint

1. أضف المعالج في `handlers.go`
2. أضف المنطق في `search.go` إذا لزم الأمر
3. سجل المسار في `setupRoutes()` في `main.go`
4. حدث التوثيق في `README.md`

### إضافة فلتر جديد - Adding New Filter

1. أضف الحقل إلى `SearchParams` في `search.go`
2. أضف شرط WHERE في دالة `Search()`
3. أضف معامل الاستعلام في `handleSearch()`

## 🐛 استكشاف الأخطاء - Troubleshooting

### الخدمة لا تبدأ
```bash
# تحقق من الاتصال بقاعدة البيانات
psql $DATABASE_URL -c "SELECT 1"

# تحقق من Redis
redis-cli -u $REDIS_URL ping
```

### بطء في البحث
```bash
# تحقق من الفهارس
psql $DATABASE_URL -c "SELECT * FROM pg_indexes WHERE tablename = 'ayahs'"

# شغل ANALYZE
psql $DATABASE_URL -c "ANALYZE ayahs"
```

### نتائج غير دقيقة
- تحقق من تطبيع النص
- جرب تقليل/زيادة threshold في البحث المتشابه
- راجع إعدادات FTS

## 📄 الترخيص - License

هذا المشروع جزء من Quran Modern Stack ومفتوح المصدر.

This project is part of Quran Modern Stack and is open source.

## 🤝 المساهمة - Contributing

نرحب بالمساهمات! الرجاء:
1. Fork المشروع
2. إنشاء branch للميزة الجديدة
3. Commit التغييرات
4. Push إلى branch
5. فتح Pull Request

---

**تم بحمد الله**
Quran Modern Stack Team 🌙

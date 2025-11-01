# Architecture - البنية المعمارية

## Overview - نظرة عامة

The Quran Search Service is a high-performance microservice built with Go that provides fast, accurate search capabilities for the Quran. It leverages PostgreSQL's full-text search capabilities and Redis caching for optimal performance.

خدمة البحث في القرآن هي خدمة صغيرة عالية الأداء مبنية بلغة Go توفر إمكانيات بحث سريعة ودقيقة للقرآن الكريم. تستفيد من قدرات البحث النصي الكامل في PostgreSQL وكاش Redis للأداء الأمثل.

## System Architecture - البنية المعمارية للنظام

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│                      (Frontend / API Consumer)                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP/JSON
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   Go Search Microservice                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    HTTP Router (chi)                     │   │
│  │  ┌──────────┬──────────┬──────────┬──────────────────┐ │   │
│  │  │ /health  │ /metrics │ /search  │ /similar /suggest│ │   │
│  │  └──────────┴──────────┴──────────┴──────────────────┘ │   │
│  └───────────────────┬─────────────────────────────────────┘   │
│                      │                                           │
│  ┌───────────────────▼─────────────────────────────────────┐   │
│  │              Middleware Layer                            │   │
│  │  • Request ID   • Logging   • Recovery  • Timeout       │   │
│  │  • Compression  • CORS                                   │   │
│  └───────────────────┬─────────────────────────────────────┘   │
│                      │                                           │
│  ┌───────────────────▼─────────────────────────────────────┐   │
│  │              Business Logic Layer                        │   │
│  │  ┌────────────┬────────────┬────────────────────────┐   │   │
│  │  │  Search    │  Similar   │  Suggestions           │   │   │
│  │  │  Engine    │  Matcher   │  Generator             │   │   │
│  │  └────────────┴────────────┴────────────────────────┘   │   │
│  └───────────────────┬─────────────────────────────────────┘   │
│                      │                                           │
│  ┌───────────────────▼─────────────────────────────────────┐   │
│  │              Data Access Layer                           │   │
│  │  ┌────────────────────┬──────────────────────────────┐  │   │
│  │  │  PostgreSQL Pool   │     Redis Client             │  │   │
│  │  │  (pgx/v5)          │     (go-redis/v9)            │  │   │
│  │  └────────────────────┴──────────────────────────────┘  │   │
│  └───────────────────┬──────────┬──────────────────────────┘   │
└────────────────────────┼──────────┼──────────────────────────────┘
                        │          │
              ┌─────────▼─┐    ┌──▼───────┐
              │ PostgreSQL │    │  Redis   │
              │  Database  │    │  Cache   │
              └────────────┘    └──────────┘
```

## Components - المكونات

### 1. HTTP Router Layer - طبقة التوجيه

**File**: `main.go`

The router handles incoming HTTP requests and routes them to appropriate handlers.

```go
// Key responsibilities:
- Route registration
- Middleware chain setup
- CORS configuration
- Server lifecycle management
```

**Features**:
- Chi v5 router (lightweight, fast)
- RESTful endpoint design
- Middleware composition
- Graceful shutdown

### 2. Middleware Layer - طبقة Middleware

**File**: `main.go` (LoggerMiddleware)

Middleware functions that process requests before they reach handlers.

**Middleware Stack**:
1. **RequestID**: Unique ID for request tracking
2. **RealIP**: Extract real client IP
3. **Logger**: Request/response logging
4. **Recoverer**: Panic recovery
5. **Compress**: gzip compression (level 5)
6. **Timeout**: 30-second timeout
7. **CORS**: Cross-Origin Resource Sharing

### 3. Handler Layer - طبقة المعالجات

**File**: `handlers.go`

HTTP handlers that process requests and return responses.

**Handlers**:
```go
- handleHealth()      // GET /health
- handleMetrics()     // GET /metrics
- handleSearch()      // GET /api/search
- handleSimilar()     // GET /api/similar
- handleSuggest()     // GET /api/suggest
```

**Responsibilities**:
- Parameter extraction and validation
- Cache lookup
- Business logic delegation
- Response formatting
- Error handling

### 4. Business Logic Layer - طبقة المنطق

**File**: `search.go`

Core search functionality and text processing.

**Components**:
- **Search Engine**: Full-text search implementation
- **Text Normalizer**: Arabic text normalization
- **Similarity Matcher**: Trigram-based matching
- **Suggestion Generator**: Auto-complete logic

**Key Functions**:
```go
Search()               // Full-text search with filters
FindSimilar()         // Similarity search
GetSuggestions()      // Auto-complete
NormalizeArabicText() // Text normalization
```

### 5. Data Access Layer - طبقة الوصول للبيانات

**Files**: `database.go`, `cache.go`

Database and cache management.

**Database** (`database.go`):
- Connection pool management
- Query execution
- Transaction handling
- Health monitoring

**Cache** (`cache.go`):
- Redis operations
- Cache key generation
- TTL management
- Graceful fallback

## Data Flow - تدفق البيانات

### Search Request Flow - تدفق طلب البحث

```
1. Client Request
   │
   ├─→ HTTP GET /api/search?q=الله&surah=1
   │
2. Router + Middleware
   │
   ├─→ Request validation
   ├─→ Logging
   ├─→ Timeout setup
   │
3. Handler (handleSearch)
   │
   ├─→ Extract parameters
   ├─→ Generate cache key
   │
4. Cache Layer
   │
   ├─→ Check Redis
   ├───→ HIT: Return cached result ─────┐
   │                                      │
   └───→ MISS: Continue                  │
                                         │
5. Business Logic                        │
   │                                      │
   ├─→ Normalize query text             │
   ├─→ Build SQL query                  │
   │                                      │
6. Database                              │
   │                                      │
   ├─→ Execute FTS query                │
   ├─→ Return results                   │
   │                                      │
7. Cache Update                          │
   │                                      │
   ├─→ Store in Redis (5 min TTL)       │
   │                                      │
8. Response                              │
   │                                      │
   └─→ Format JSON ◄────────────────────┘
   │
   └─→ Return to client
```

## Database Schema - مخطط قاعدة البيانات

### Key Tables - الجداول الرئيسية

```sql
-- Ayahs (Verses)
ayahs (
    id SERIAL PRIMARY KEY,
    surah_id INTEGER,
    ayah_number INTEGER,
    text_uthmani TEXT,        -- With diacritics
    text_simple TEXT,          -- Without diacritics
    search_vector tsvector,    -- Full-text search
    juz_number INTEGER,
    page_number INTEGER
)

-- Surahs (Chapters)
surahs (
    id SERIAL PRIMARY KEY,
    number INTEGER,
    name_arabic TEXT,
    name_transliteration TEXT,
    revelation_type TEXT,
    ayah_count INTEGER
)
```

### Indexes - الفهارس

```sql
-- Full-text search index
CREATE INDEX idx_ayahs_search ON ayahs USING GIN(search_vector);

-- Trigram similarity index
CREATE INDEX idx_ayahs_text_simple ON ayahs USING GIN(text_simple gin_trgm_ops);

-- Foreign key indexes
CREATE INDEX idx_ayahs_surah ON ayahs(surah_id);
CREATE INDEX idx_ayahs_juz ON ayahs(juz_number);
CREATE INDEX idx_ayahs_page ON ayahs(page_number);
```

## Caching Strategy - استراتيجية الكاش

### Cache Keys - مفاتيح الكاش

```
Format: {prefix}{hash}

Examples:
- search:a3c7e9f2... (search results)
- similar:b4d8f1e3... (similar verses)
- suggest:c5e9g2h4... (suggestions)
```

### TTL Configuration - إعدادات TTL

```go
CacheTTLShort  = 5 minutes   // Search results
CacheTTLMedium = 15 minutes  // Similar verses
CacheTTLLong   = 1 hour      // Suggestions
```

### Cache Hit Ratio - نسبة إصابة الكاش

Expected performance:
- Initial requests: ~20% hit ratio
- After warmup: ~70-80% hit ratio
- Popular queries: ~95% hit ratio

## Text Processing - معالجة النصوص

### Arabic Normalization - تطبيع النص العربي

```go
Input:  "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"

Steps:
1. Remove diacritics (تشكيل)
   → "بسم الله الرحمن الرحيم"

2. Normalize alif variants
   → أ، إ، آ، ٱ → ا

3. Normalize ta marbuta
   → ة → ه

4. Normalize alif maqsura
   → ى → ي

5. Remove tatweel
   → ـ → (removed)

6. Trim whitespace

Output: "بسم الله الرحمن الرحيم"
```

## Performance Optimization - تحسين الأداء

### 1. Connection Pooling - مجموعة الاتصالات

```go
PostgreSQL Pool:
- Min connections: 5
- Max connections: 25
- Max lifetime: 1 hour
- Idle timeout: 30 minutes
- Health check: 1 minute

Redis Pool:
- Pool size: 10
- Min idle: 5
- Dial timeout: 5 seconds
```

### 2. Query Optimization - تحسين الاستعلامات

- Prepared statements (avoided N+1 queries)
- Index-optimized queries
- Selective field retrieval
- Pagination support

### 3. Response Optimization - تحسين الاستجابة

- gzip compression (level 5)
- Streaming JSON responses
- Minimal object allocation
- Connection reuse

## Error Handling - معالجة الأخطاء

### Error Types - أنواع الأخطاء

```go
1. Client Errors (4xx)
   - 400 Bad Request: Invalid parameters
   - 404 Not Found: Route not found

2. Server Errors (5xx)
   - 500 Internal Server Error: Unexpected errors
   - 503 Service Unavailable: Database down

3. Timeout Errors
   - 30-second request timeout
   - Context cancellation
```

### Error Response Format - صيغة استجابة الخطأ

```json
{
  "error": "Query parameter 'q' is required",
  "status": 400,
  "timestamp": "2025-11-01T12:00:00Z"
}
```

## Logging - السجلات

### Log Levels - مستويات السجلات

```go
DEBUG  - Detailed debugging information
INFO   - General information (default)
WARN   - Warning messages
ERROR  - Error messages
```

### Log Format - صيغة السجلات

```json
{
  "level": "info",
  "method": "GET",
  "path": "/api/search",
  "status": 200,
  "duration": 15.3,
  "remote_addr": "127.0.0.1",
  "message": "HTTP request",
  "timestamp": "2025-11-01T12:00:00Z"
}
```

## Security Considerations - اعتبارات الأمان

1. **SQL Injection Prevention**: Parameterized queries
2. **Input Validation**: All user inputs validated
3. **CORS**: Configured for allowed origins
4. **Rate Limiting**: (Planned feature)
5. **Non-root Container**: Docker runs as user 1000
6. **No Sensitive Logs**: Credentials never logged

## Scalability - قابلية التوسع

### Horizontal Scaling - التوسع الأفقي

```
Load Balancer
     │
     ├─→ Service Instance 1 ─→ PostgreSQL (shared)
     ├─→ Service Instance 2 ─→ Redis (shared)
     └─→ Service Instance N
```

### Vertical Scaling - التوسع العمودي

- Increase connection pool size
- Increase Redis pool size
- Optimize cache TTL
- Add read replicas

## Monitoring - المراقبة

### Health Check - فحص الصحة

```bash
curl http://localhost:8001/health
```

### Metrics - الإحصائيات

```bash
curl http://localhost:8001/metrics
```

**Available Metrics**:
- Database connection stats
- Cache hit/miss ratio
- Request duration
- Active connections

---

**تم بحمد الله**
Quran Modern Stack Team 🌙

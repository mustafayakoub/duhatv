# Quick Start Guide - دليل البدء السريع

Get the Quran Search Service running in 5 minutes!

## 🚀 Development Setup - إعداد التطوير

### Prerequisites - المتطلبات
```bash
# Check Go version (need 1.21+)
go version

# Check Docker (optional but recommended)
docker --version
```

### Option 1: Local Development - التطوير المحلي

```bash
# 1. Navigate to the service directory
cd /home/user/duhatv/quran-modern-stack/services-go/search-service

# 2. Install dependencies
make install

# 3. Copy environment file
cp .env.example .env

# 4. Edit .env with your database credentials
# DATABASE_URL=postgresql://quran:password@localhost:5432/quran_db
# REDIS_URL=redis://:password@localhost:6379/0

# 5. Run the service
make dev
```

Service will be available at: http://localhost:8001

### Option 2: Docker Development - التطوير باستخدام Docker

```bash
# 1. Build Docker image
make docker-build

# 2. Run with docker-compose (recommended)
cd /home/user/duhatv/quran-modern-stack
docker-compose up -d search-service-go

# Or run standalone
make docker-run
```

## ✅ Verify Installation - التحقق من التثبيت

```bash
# Check service health
curl http://localhost:8001/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "quran-search-service",
#   "version": "1.0.0",
#   "checks": {
#     "database": true,
#     "redis": true
#   }
# }
```

## 🧪 Test the Service - اختبار الخدمة

### Manual Testing - اختبار يدوي

```bash
# 1. Search for "الله" (Allah)
curl "http://localhost:8001/api/search?q=الله&limit=5" | jq

# 2. Search in specific surah
curl "http://localhost:8001/api/search?q=الرحمن&surah=1" | jq

# 3. Find similar verses
curl "http://localhost:8001/api/similar?text=بسم الله الرحمن الرحيم&threshold=0.5" | jq

# 4. Get suggestions
curl "http://localhost:8001/api/suggest?q=الفات" | jq
```

### Automated Testing - اختبار تلقائي

```bash
# Run test script
./test-api.sh

# Run with verbose output
VERBOSE=true ./test-api.sh

# Run unit tests
make test

# Run with coverage
make test-cover
```

## 📊 View Metrics - عرض الإحصائيات

```bash
# Service metrics
curl http://localhost:8001/metrics | jq

# Database stats
curl http://localhost:8001/metrics | jq '.database'

# Cache stats
curl http://localhost:8001/metrics | jq '.cache'
```

## 🔧 Common Tasks - المهام الشائعة

### Build for Production - بناء للإنتاج
```bash
make build-prod
```

### Run Tests - تشغيل الاختبارات
```bash
# All tests
make test

# With coverage
make test-cover

# Benchmarks
make bench
```

### Code Quality - جودة الكود
```bash
# Format code
make fmt

# Run linter
make lint

# Run vet
make vet
```

### Clean Build - تنظيف البناء
```bash
make clean
```

## 🐛 Troubleshooting - استكشاف الأخطاء

### Service won't start - الخدمة لا تبدأ

```bash
# Check database connection
psql "postgresql://quran:pass@localhost:5432/quran_db" -c "SELECT 1"

# Check Redis connection
redis-cli -u "redis://:pass@localhost:6379/0" ping

# Check logs
docker-compose logs -f search-service-go
```

### Slow queries - استعلامات بطيئة

```bash
# Check database indexes
psql "postgresql://..." -c "SELECT * FROM pg_indexes WHERE tablename = 'ayahs'"

# Run ANALYZE
psql "postgresql://..." -c "ANALYZE ayahs"
```

### Port already in use - المنفذ مستخدم بالفعل

```bash
# Find process using port 8001
lsof -i :8001

# Kill process
kill -9 <PID>

# Or use different port
PORT=8002 make dev
```

## 📚 Next Steps - الخطوات التالية

1. **Read Documentation**
   - [README.md](README.md) - Full documentation
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
   - [CHANGELOG.md](CHANGELOG.md) - Version history

2. **Explore API**
   - Try different search queries
   - Test with different filters
   - Experiment with similarity threshold

3. **Customize Configuration**
   - Adjust cache TTL
   - Configure connection pools
   - Set up monitoring

4. **Integrate with Frontend**
   - Use TypeScript frontend
   - Build custom UI
   - Create mobile app

## 🎯 Example Use Cases - حالات الاستخدام

### Search for a word - البحث عن كلمة
```bash
curl "http://localhost:8001/api/search?q=رحمة&limit=10"
```

### Search in specific Juz - البحث في جزء معين
```bash
curl "http://localhost:8001/api/search?q=الله&juz=30"
```

### Search on specific page - البحث في صفحة معينة
```bash
curl "http://localhost:8001/api/search?q=الحمد&page=1"
```

### Find verses similar to Ayatul Kursi - آيات مشابهة لآية الكرسي
```bash
curl "http://localhost:8001/api/similar?text=اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ"
```

### Auto-complete for "البقرة" - إكمال تلقائي لـ "البقرة"
```bash
curl "http://localhost:8001/api/suggest?q=البق"
```

## 🔗 Useful Links - روابط مفيدة

- **GitHub**: [Quran Modern Stack](https://github.com/...)
- **Docker Hub**: [Search Service Image](https://hub.docker.com/...)
- **API Documentation**: See [README.md](README.md)
- **Issue Tracker**: Report bugs on GitHub

## 💬 Getting Help - الحصول على المساعدة

- Check [README.md](README.md) for detailed documentation
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Run `make help` for available commands
- Check logs for error messages

---

**تم بحمد الله**

Happy Coding! 🌙

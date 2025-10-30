# ⚡ دليل البدء السريع
## Quick Start Guide

---

## 🎯 تثبيت وتشغيل القاعدة في 5 دقائق

### الخطوة 1: تثبيت PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql-15 postgresql-contrib

# macOS
brew install postgresql@15

# تشغيل PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### الخطوة 2: تثبيت pgvector

```bash
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

### الخطوة 3: تنفيذ السكريبتات

```bash
# الانتقال لمجلد المشروع
cd /path/to/quran-hierarchical-db/database

# تنفيذ السكريبتات بالترتيب
psql -U postgres -f sql/01_setup.sql
psql -U postgres -d quran_hierarchical_db -f sql/02_level0_core_tables.sql
psql -U postgres -d quran_hierarchical_db -f sql/03_remaining_levels.sql
psql -U postgres -d quran_hierarchical_db -f sql/04_views_and_functions.sql
```

### الخطوة 4: التحقق من التثبيت

```sql
\c quran_hierarchical_db

-- التحقق من الجداول
\dt quran.*

-- التحقق من الامتدادات
\dx

-- عد الجداول
SELECT COUNT(*) FROM information_schema.tables
WHERE table_schema IN ('quran', 'analytics', 'community');
```

---

## 🧪 اختبار سريع

### استعلام 1: قراءة سورة الفاتحة
```sql
SELECT
    aya_number,
    aya_text_uthmani
FROM quran.ayahs
WHERE aya_sur_id = 1
ORDER BY aya_number;
```

### استعلام 2: البحث النصي
```sql
SELECT * FROM quran.search_ayahs_fulltext('الصلاة', 'arabic', 5);
```

### استعلام 3: تحليل جذر
```sql
SELECT * FROM quran.get_root_derivatives('ص.ل.ي')
LIMIT 10;
```

---

## 📦 سكريبت تنفيذ شامل

```bash
#!/bin/bash
# install_quran_db.sh

echo "🚀 بدء تثبيت قاعدة البيانات القرآنية..."

# التحقق من PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL غير مثبت. يرجى تثبيته أولاً."
    exit 1
fi

# التحقق من pgvector
if ! psql -U postgres -c "SELECT * FROM pg_available_extensions WHERE name='vector';" | grep -q vector; then
    echo "⚠️  pgvector غير مثبت. جاري التثبيت..."
    cd /tmp
    git clone https://github.com/pgvector/pgvector.git
    cd pgvector
    make
    sudo make install
    cd -
fi

# تنفيذ السكريبتات
echo "📝 تنفيذ سكريبت الإعداد..."
psql -U postgres -f sql/01_setup.sql

echo "📊 إنشاء الجداول الأساسية..."
psql -U postgres -d quran_hierarchical_db -f sql/02_level0_core_tables.sql

echo "🔗 إنشاء الجداول المتبقية..."
psql -U postgres -d quran_hierarchical_db -f sql/03_remaining_levels.sql

echo "🔍 إنشاء Views والدوال..."
psql -U postgres -d quran_hierarchical_db -f sql/04_views_and_functions.sql

echo "✅ تم التثبيت بنجاح!"
echo "📚 للبدء: psql -U postgres -d quran_hierarchical_db"
```

احفظ الملف وشغّله:
```bash
chmod +x install_quran_db.sh
./install_quran_db.sh
```

---

## 🔌 الاتصال من التطبيقات

### Python (psycopg2)
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="quran_hierarchical_db",
    user="quran_readonly",
    password="your_password"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM quran.ayahs LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)
```

### Node.js (pg)
```javascript
const { Client } = require('pg');

const client = new Client({
    host: 'localhost',
    database: 'quran_hierarchical_db',
    user: 'quran_readonly',
    password: 'your_password',
});

await client.connect();
const res = await client.query('SELECT * FROM quran.ayahs LIMIT 5');
console.log(res.rows);
```

### PHP (PDO)
```php
$pdo = new PDO(
    'pgsql:host=localhost;dbname=quran_hierarchical_db',
    'quran_readonly',
    'your_password'
);

$stmt = $pdo->query('SELECT * FROM quran.ayahs LIMIT 5');
$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

print_r($rows);
```

---

## 🛠️ إعدادات الأداء الموصى بها

أضف في `postgresql.conf`:

```conf
# Memory Settings
shared_buffers = 2GB
effective_cache_size = 4GB
work_mem = 256MB
maintenance_work_mem = 1GB

# Query Planning
random_page_cost = 1.1  # For SSD
effective_io_concurrency = 200

# Parallel Query
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
max_worker_processes = 8

# Write Performance
wal_buffers = 16MB
checkpoint_completion_target = 0.9
```

---

## 📊 نصائح الصيانة

### تحديث إحصائيات PostgreSQL (أسبوعياً)
```sql
VACUUM ANALYZE;
REINDEX DATABASE quran_hierarchical_db;
```

### تحديث Materialized Views (يومياً)
```sql
CALL analytics.refresh_all_materialized_views();
```

### النسخ الاحتياطي
```bash
# النسخ الاحتياطي الكامل
pg_dump -U postgres quran_hierarchical_db > backup_$(date +%Y%m%d).sql

# النسخ الاحتياطي المضغوط
pg_dump -U postgres -Fc quran_hierarchical_db > backup_$(date +%Y%m%d).dump
```

### الاستعادة
```bash
# من SQL
psql -U postgres -d quran_hierarchical_db < backup_20251030.sql

# من Dump
pg_restore -U postgres -d quran_hierarchical_db backup_20251030.dump
```

---

## ❓ استكشاف الأخطاء

### خطأ: "extension vector does not exist"
```sql
-- التحقق من التثبيت
SELECT * FROM pg_available_extensions WHERE name='vector';

-- إذا لم يظهر، أعد تثبيت pgvector
```

### خطأ: "permission denied for schema quran"
```sql
-- منح الصلاحيات
GRANT USAGE ON SCHEMA quran TO your_user;
GRANT SELECT ON ALL TABLES IN SCHEMA quran TO your_user;
```

### أداء بطيء
```sql
-- التحقق من الفهارس
SELECT * FROM pg_indexes WHERE schemaname = 'quran';

-- تحديث الإحصائيات
ANALYZE quran.ayahs;
ANALYZE quran.words;

-- استخدام EXPLAIN لتحليل الاستعلام
EXPLAIN ANALYZE SELECT * FROM ...;
```

---

## 📞 الدعم الفني

- **الوثائق**: راجع `README.md` و `00_DATABASE_ANALYSIS.md`
- **الاستعلامات**: راجع `SMART_QUERIES.md`
- **Email**: duhatv@gmail.com

---

**آخر تحديث: 2025-10-30**

# 📖 قاعدة البيانات القرآنية الهرمية الذكية
## Quran Hierarchical Smart Database

<div align="center">

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791?logo=postgresql)
![Vector](https://img.shields.io/badge/pgvector-enabled-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-production--ready-success)

**قاعدة بيانات PostgreSQL متطورة للقرآن الكريم مع تحليل صرفي كامل، بحث دلالي، وربط عصبي متقدم**

</div>

---

## ✨ المزايا الرئيسية

🔹 **19 جدول محترف** موزعة على 5 مستويات هرمية
🔹 **400+ عمود** مصممة بدقة لتغطية كل جوانب القرآن
🔹 **Vector Embeddings** للبحث الدلالي المتقدم
🔹 **Full-Text Search** للبحث النصي السريع
🔹 **Morphological Analysis** تحليل صرفي ونحوي شامل
🔹 **Hierarchical Topics** موضوعات هرمية متعددة المستويات
🔹 **Multi-Language** دعم الترجمات والتفاسير
🔹 **Audio Integration** دعم التلاوات الصوتية
🔹 **Community Features** مساهمات مجتمعية وتفاعل

---

## 📊 إحصائيات القاعدة

| البند | العدد |
|------|-------|
| السور | 114 |
| الآيات | 6,236 |
| الكلمات | 77,430+ |
| الجذور | ~2,000 |
| الأوزان | ~300 |
| التفاسير | 60,000+ |
| الترجمات | 300,000+ |
| التلاوات | 300,000+ |

---

## 🏗️ البنية الهرمية

```
┌─────────────────────────────────────────────────────┐
│  المستوى 0: النواة الصلبة (Core)                   │
│  ├─ surahs (السور)                                  │
│  ├─ ayahs (الآيات)                                  │
│  └─ words (الكلمات)                                 │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  المستوى 1: التحليل الصرفي (Morphology)            │
│  ├─ roots (الجذور)                                  │
│  └─ patterns (الأوزان)                              │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  المستوى 2: المحتوى الإثرائي (Content)             │
│  ├─ tafsir (التفاسير)                               │
│  ├─ mufassireen (المفسرون)                          │
│  ├─ translations (الترجمات)                         │
│  └─ translators (المترجمون)                         │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  المستوى 3: السياق والعلوم (Context & Sciences)    │
│  ├─ revelation_contexts (أسباب النزول)             │
│  ├─ topics (الموضوعات - شجري)                       │
│  ├─ ayah_topics (الربط M:N)                         │
│  ├─ qiraat (القراءات)                               │
│  └─ sources (المصادر)                               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  المستوى 4: الوسائط المتعددة (Media)                │
│  ├─ recitations (التلاوات)                          │
│  └─ reciters (القراء)                               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  المستوى 5: المستخدمون والتفاعل (Community)         │
│  ├─ users (المستخدمون)                              │
│  ├─ bookmarks (العلامات المرجعية)                   │
│  └─ annotations (الشروح المجتمعية)                  │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 التثبيت والإعداد

### المتطلبات

- PostgreSQL 15+ (يُفضل 16)
- pg_vector extension
- pg_trgm extension
- 2GB+ RAM
- 5GB+ مساحة تخزين

### خطوات التثبيت

```bash
# 1. تنزيل المشروع
git clone https://github.com/your-repo/quran-hierarchical-db
cd quran-hierarchical-db/database

# 2. تثبيت PostgreSQL والامتدادات
sudo apt-get install postgresql-15 postgresql-contrib

# 3. تثبيت pgvector
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install

# 4. تشغيل السكريبتات بالترتيب
psql -U postgres -f sql/01_setup.sql
psql -U postgres -d quran_hierarchical_db -f sql/02_level0_core_tables.sql
psql -U postgres -d quran_hierarchical_db -f sql/03_remaining_levels.sql
psql -U postgres -d quran_hierarchical_db -f sql/04_views_and_functions.sql
```

---

## 📚 الملفات والوثائق

| الملف | الوصف |
|------|-------|
| `00_DATABASE_ANALYSIS.md` | تحليل شامل للبنية والعلاقات |
| `sql/01_setup.sql` | إعداد القاعدة والامتدادات |
| `sql/02_level0_core_tables.sql` | الجداول الأساسية |
| `sql/03_remaining_levels.sql` | باقي المستويات |
| `sql/04_views_and_functions.sql` | Views والدوال |
| `SMART_QUERIES.md` | دليل الاستعلامات الذكية |
| `README.md` | هذا الملف |

---

## 🔍 أمثلة استخدام

### البحث النصي
```sql
SELECT * FROM quran.search_ayahs_fulltext('الصلاة', 'arabic', 10);
```

### البحث الدلالي
```sql
SELECT * FROM quran.search_ayahs_semantic(
    '[...]'::vector(768),  -- embedding
    0.7,                    -- threshold
    10                      -- limit
);
```

### التحليل الصرفي
```sql
SELECT * FROM quran.get_root_derivatives('ك.ت.ب');
```

### الآيات المرتبطة
```sql
SELECT * FROM quran.get_related_ayahs(255, 0.75, 5);
```

---

## 📊 Views الجاهزة

### عرض الآيات الكامل
```sql
SELECT * FROM analytics.v_ayahs_complete WHERE sur_id = 1;
```

### إحصائيات الجذور
```sql
SELECT * FROM analytics.v_root_statistics ORDER BY total_frequency DESC;
```

### الموضوعات مع الإحصائيات
```sql
SELECT * FROM analytics.v_topics_with_counts;
```

---

## 🛠️ الصيانة الدورية

### تحديث Materialized Views
```sql
CALL analytics.refresh_all_materialized_views();
```

### تحديث إحصائيات الجذور
```sql
SELECT quran.update_root_statistics();
```

### تحديث فهارس PostgreSQL
```sql
REINDEX DATABASE quran_hierarchical_db;
VACUUM ANALYZE;
```

---

## 🎯 حالات الاستخدام

### 1. تطبيقات القرآن الكريم
- تطبيقات iOS/Android
- تطبيقات ويب
- تطبيقات سطح المكتب

### 2. البحث العلمي
- دراسات لغوية
- تحليل صرفي
- دراسات موضوعية

### 3. الذكاء الاصطناعي
- نماذج NLP للغة العربية
- البحث الدلالي
- التصنيف التلقائي

### 4. التعليم الإلكتروني
- منصات تعليم القرآن
- أدوات التدبر والتفسير
- اختبارات تفاعلية

---

## 🔐 الأمان والصلاحيات

القاعدة مُصممة بثلاثة مستويات صلاحيات:

1. **quran_readonly**: قراءة فقط
2. **quran_readwrite**: قراءة وكتابة (للتطبيقات)
3. **admin**: صلاحيات كاملة

```sql
-- منح صلاحيات القراءة
GRANT SELECT ON ALL TABLES IN SCHEMA quran TO quran_readonly;

-- منح صلاحيات الكتابة
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA quran TO quran_readwrite;
```

---

## 📈 الأداء

### التحسينات المُطبقة

✅ Indexes متعددة الأنواع (B-tree, GIN, GiST, IVFFlat)
✅ Materialized Views للاستعلامات المعقدة
✅ Partitioning جاهز للتطبيق
✅ Connection Pooling مُوصى به
✅ Query Optimization عبر EXPLAIN ANALYZE

### قياسات الأداء المتوقعة

| الاستعلام | الزمن المتوقع |
|----------|---------------|
| بحث نصي بسيط | < 50ms |
| بحث دلالي | < 100ms |
| استعلام معقد (5 joins) | < 200ms |
| تحليل صرفي | < 10ms |

---

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:

1. Fork المشروع
2. إنشاء branch للميزة الجديدة
3. Commit التغييرات
4. Push وإنشاء Pull Request

---

## 📝 الترخيص

MIT License - استخدام حر للأغراض التعليمية والتجارية

---

## 📞 التواصل

- **Email**: duhatv@gmail.com
- **Website**: duhatv.net
- **Phone**: +905342390000

---

## 🙏 شكر وتقدير

- **المصادر**: Tanzil.net, QAC, Zekr
- **الخطوط**: مشروع الخطوط الإسلامية
- **التفاسير**: المكتبة الشاملة
- **التقنيات**: PostgreSQL, pgvector, Python

---

<div align="center">

**صُنع بـ ❤️ للمسلمين في كل مكان**

**Built with ❤️ for Muslims everywhere**

</div>

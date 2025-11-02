# 📊 تحليل شامل لقاعدة البيانات القرآنية الهرمية الذكية

## 🎯 نظرة عامة

قاعدة بيانات PostgreSQL متقدمة تحتوي على **19 جدول** موزعة على **5 مستويات هرمية**.

---

## 🏗️ البنية الهرمية

### المستوى 0: النواة الصلبة (Core Tables)
```
┌─────────────────────────────────────────┐
│        1. surahs (السور)               │
│           114 سجل                       │
│        30+ عمود                         │
└─────────────────────────────────────────┘
              ↓ (1:N)
┌─────────────────────────────────────────┐
│        2. ayahs (الآيات)                │
│           6,236 سجل                     │
│        45+ عمود                         │
│        - Full-Text Search (TSVECTOR)    │
│        - Vector Embeddings              │
└─────────────────────────────────────────┘
              ↓ (1:N)
┌─────────────────────────────────────────┐
│        3. words (الكلمات)               │
│           77,430+ سجل                   │
│        55+ عمود                         │
│        - تحليل صرفي كامل                │
│        - CAMeL Tools Integration        │
└─────────────────────────────────────────┘
```

### المستوى 1: التحليل الصرفي
```
┌──────────────────────┐      ┌──────────────────────┐
│   4. roots           │      │   5. patterns        │
│   (الجذور)          │      │   (الأوزان)          │
│   ~2000 جذر          │      │   ~300 وزن           │
└──────────────────────┘      └──────────────────────┘
         ↑                             ↑
         └─────────── N:M ──────────────┘
                      │
                   words
```

### المستوى 2: المحتوى الإثرائي
```
┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐
│  6. tafsir      │  │  8. translations │  │  7. mufassireen │
│  (التفاسير)     │  │  (الترجمات)      │  │  (المفسرون)     │
└─────────────────┘  └──────────────────┘  └─────────────────┘
        ↓ N:1                ↓ N:1                  ↑ 1:N
        └────────── ayahs ───────────────────────────┘
```

### المستوى 3: السياق والعلوم
```
┌──────────────────────────────────────────────────────┐
│                    11. topics                        │
│                  (الموضوعات - شجرية)                │
│                  Self-Referencing Tree               │
└──────────────────────────────────────────────────────┘
                         ↕ N:M
┌──────────────────────────────────────────────────────┐
│              12. ayah_topics (جدول وسيط)            │
└──────────────────────────────────────────────────────┘
                         ↕ N:M
┌──────────────────────────────────────────────────────┐
│                    2. ayahs                          │
└──────────────────────────────────────────────────────┘
                         ↓ 1:N
┌──────────────────────────────────────────────────────┐
│          10. revelation_contexts                     │
│             (أسباب النزول)                           │
└──────────────────────────────────────────────────────┘
```

### المستوى 4: الوسائط المتعددة
```
┌─────────────────┐           ┌─────────────────┐
│  16. reciters   │ 1:N       │ 15. recitations │
│  (القراء)       │◄──────────│  (التلاوات)     │
└─────────────────┘           └─────────────────┘
                                      ↓ N:1
                              ┌─────────────────┐
                              │   2. ayahs      │
                              └─────────────────┘
```

### المستوى 5: المستخدمون والتفاعل
```
┌──────────────────┐
│   17. users      │
│   (المستخدمون)   │
└──────────────────┘
       ↓ 1:N
┌──────────────────┐    ┌──────────────────┐
│  18. bookmarks   │    │  19. annotations │
│  (العلامات)      │    │  (الشروح)        │
└──────────────────┘    └──────────────────┘
       ↓ N:1                   ↓ N:1
┌──────────────────┐    ┌──────────────────┐
│   2. ayahs       │    │  ayahs/words/etc │
└──────────────────┘    └──────────────────┘
```

---

## 🔗 العلاقات الرئيسية (Relationships)

### علاقات One-to-Many (1:N)
1. **surahs → ayahs**
   - كل سورة تحتوي على عدة آيات
   - `ayahs.aya_sur_id → surahs.sur_id`

2. **ayahs → words**
   - كل آية تحتوي على عدة كلمات
   - `words.wrd_aya_id → ayahs.aya_id`

3. **ayahs → tafsir**
   - كل آية لها عدة تفاسير (من مفسرين مختلفين)
   - `tafsir.taf_aya_id → ayahs.aya_id`

4. **mufassireen → tafsir**
   - كل مفسر له عدة تفاسير (لآيات مختلفة)
   - `tafsir.taf_mufassir_id → mufassireen.muf_id`

5. **ayahs → translations**
   - `translations.trl_aya_id → ayahs.aya_id`

6. **ayahs → recitations**
   - `recitations.rec_aya_id → ayahs.aya_id`

7. **reciters → recitations**
   - `recitations.rec_reciter_id → reciters.rct_id`

8. **users → bookmarks**
   - `bookmarks.bmk_usr_id → users.usr_id`

9. **users → annotations**
   - `annotations.note_usr_id → users.usr_id`

### علاقات Many-to-Many (N:M)
1. **ayahs ↔ topics** (عبر ayah_topics)
   - كل آية تتناول عدة مواضيع
   - كل موضوع له عدة آيات
   - جدول وسيط: `ayah_topics`

2. **words ↔ roots** (ضمني)
   - كل كلمة تنتمي لجذر
   - كل جذر له عدة كلمات مشتقة
   - `words.wrd_root → roots.root_text`

3. **words ↔ patterns** (ضمني)
   - كل كلمة على وزن صرفي
   - كل وزن عليه عدة كلمات
   - `words.wrd_pattern → patterns.pat_text`

### علاقات Self-Referencing (ذاتية)
1. **topics → topics** (شجرة هرمية)
   - كل موضوع قد يكون له موضوع أب
   - `topics.top_parent_id → topics.top_id`
   - يشكل هيكل شجري متعدد المستويات

---

## 🎯 الحقول الخاصة والمتقدمة

### 1. Full-Text Search (البحث النصي)
```sql
-- في جدول ayahs
aya_text_search TSVECTOR
-- يُحدّث تلقائياً من aya_text_simple
-- فهرس GIN للبحث السريع

-- في جدول tafsir
taf_search_vector TSVECTOR

-- في جدول translations
trl_search_vector TSVECTOR
```

### 2. Vector Embeddings (المتجهات النصية للبحث الدلالي)
```sql
-- في جدول ayahs
aya_embedding_v1 vector(768)    -- نموذج كبير
aya_embedding_v2 vector(384)    -- نموذج صغير

-- في جدول words
wrd_embedding vector(512)

-- في جدول tafsir
taf_embedding vector(768)
```

### 3. JSONB Fields (الحقول المرنة)
```sql
-- تخزين بيانات معقدة ومرنة
sur_main_themes JSONB
sur_stats JSONB
sur_metadata JSONB

aya_pos_summary JSONB        -- ملخص أنواع الكلمات
aya_analysis JSONB           -- تحليلات متقدمة

wrd_camel_analysis JSONB     -- تحليل CAMeL Tools
wrd_morphological_features JSONB

top_metadata JSONB
```

### 4. Array Fields (مصفوفات)
```sql
-- للفلترة السريعة والبحث المتعدد
sur_main_topics TEXT[]
sur_keywords TEXT[]

aya_roots TEXT[]
aya_patterns TEXT[]
aya_topics TEXT[]
aya_keywords TEXT[]

wrd_letters CHAR[]
wrd_syllables TEXT[]

root_patterns TEXT[]
root_synonyms TEXT[]
root_antonyms TEXT[]
```

---

## 📈 الإحصائيات التقديرية

| الجدول | عدد السجلات التقريبي | حجم البيانات التقديري |
|--------|----------------------|------------------------|
| surahs | 114 | ~50 KB |
| ayahs | 6,236 | ~15 MB |
| words | 77,430 | ~100 MB |
| roots | 2,000 | ~500 KB |
| patterns | 300 | ~100 KB |
| tafsir | 60,000+ | ~500 MB+ |
| mufassireen | 50 | ~50 KB |
| translations | 300,000+ | ~200 MB+ |
| revelation_contexts | 500 | ~2 MB |
| topics | 1,000+ | ~1 MB |
| ayah_topics | 20,000+ | ~5 MB |
| qiraat | 5,000+ | ~2 MB |
| recitations | 300,000+ | روابط فقط ~10 MB |
| reciters | 100 | ~100 KB |
| users | متغير | متغير |
| bookmarks | متغير | متغير |
| annotations | متغير | متغير |

**إجمالي تقديري:** ~1-2 GB (بدون الملفات الصوتية)

---

## 🔍 نقاط القوة في التصميم

### ✅ المرونة
- حقول JSONB للتوسع المستقبلي
- حقول metadata في كل جدول
- دعم أنواع بيانات متقدمة (vector, TSVECTOR)

### ✅ الأداء
- معرفات UUID لكل سجل
- فهارس متقدمة (GIN, GiST, B-tree)
- حقول محسوبة مسبقاً (word_count, letter_count)

### ✅ البحث المتقدم
- بحث نصي كامل (Full-Text Search)
- بحث دلالي (Semantic Search via Embeddings)
- بحث هيكلي (عبر العلاقات)

### ✅ قابلية التوسع
- بنية هرمية واضحة
- جداول وسيطة للعلاقات المعقدة
- دعم للمساهمات المجتمعية

---

## ⚠️ التحديات المحتملة

### 1. حجم البيانات
- جدول tafsir قد يصل لعدة GB
- Vector embeddings تستهلك مساحة كبيرة
- **الحل:** Partitioning حسب السورة أو الجزء

### 2. الأداء
- استعلامات معقدة عبر 5-6 جداول
- **الحل:** Materialized Views + EXPLAIN ANALYZE

### 3. التكامل
- دمج بيانات من مصادر متعددة
- **الحل:** ETL pipelines + Data validation

### 4. الصيانة
- تحديث الـ embeddings
- **الحل:** Async jobs + Triggers

---

## 🚀 الاستعلامات الذكية المقترحة

### 1. البحث الدلالي المتقدم
```sql
-- البحث عن آيات مشابهة دلالياً
SELECT * FROM ayahs
ORDER BY aya_embedding_v1 <-> '[...]'::vector
LIMIT 10;
```

### 2. التحليل الصرفي العميق
```sql
-- جميع الكلمات من جذر معين في موضوع معين
SELECT w.*, a.*, t.top_name_ar
FROM words w
JOIN ayahs a ON w.wrd_aya_id = a.aya_id
JOIN ayah_topics at ON a.aya_id = at.ayt_aya_id
JOIN topics t ON at.ayt_top_id = t.top_id
WHERE w.wrd_root = 'ك.ت.ب'
  AND t.top_name_ar = 'العلم';
```

### 3. الإحصائيات الموضوعية
```sql
-- أكثر الجذور تكراراً في موضوع معين
SELECT w.wrd_root, COUNT(*) as frequency
FROM words w
JOIN ayahs a ON w.wrd_aya_id = a.aya_id
WHERE 'عقيدة' = ANY(a.aya_topics)
GROUP BY w.wrd_root
ORDER BY frequency DESC
LIMIT 20;
```

### 4. الربط السياقي
```sql
-- جميع الآيات المرتبطة بحدث تاريخي معين
SELECT a.*, rc.ctx_reason_ar, s.sur_name_ar
FROM ayahs a
JOIN revelation_contexts rc ON a.aya_revelation_context_id = rc.ctx_id
JOIN surahs s ON a.aya_sur_id = s.sur_id
WHERE rc.ctx_event ILIKE '%غزوة بدر%';
```

---

## 📚 المراجع التقنية

- **PostgreSQL 15+** لدعم vector data type
- **pgvector extension** للبحث الدلالي
- **pg_trgm extension** للبحث الضبابي
- **PostGIS** (اختياري) لتخزين مواقع جغرافية

---

تم التحليل بتاريخ: **2025-10-30**

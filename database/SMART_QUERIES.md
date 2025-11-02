# 🧠 دليل الاستعلامات الذكية
## قاعدة البيانات القرآنية الهرمية

---

## 📋 جدول المحتويات

1. [استعلامات أساسية](#1-استعلامات-أساسية)
2. [البحث المتقدم](#2-البحث-المتقدم)
3. [التحليل الصرفي](#3-التحليل-الصرفي)
4. [الموضوعات والربط](#4-الموضوعات-والربط)
5. [التحليل الإحصائي](#5-التحليل-الإحصائي)
6. [البحث الدلالي](#6-البحث-الدلالي)
7. [استعلامات متقدمة](#7-استعلامات-متقدمة)

---

## 1. استعلامات أساسية

### 1.1 قراءة آيات سورة كاملة
```sql
SELECT
    aya_number,
    aya_text_uthmani AS نص_الآية,
    aya_word_count AS عدد_الكلمات,
    aya_juz AS الجزء,
    aya_page AS الصفحة
FROM quran.ayahs
WHERE aya_sur_id = 1  -- الفاتحة
ORDER BY aya_number;
```

### 1.2 البحث عن آية برقمها العالمي
```sql
SELECT
    s.sur_name_ar AS السورة,
    a.aya_number AS رقم_الآية,
    a.aya_text_uthmani AS النص
FROM quran.ayahs a
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
WHERE a.aya_global_id = 100;
```

### 1.3 الحصول على جميع السور المكية
```sql
SELECT
    sur_id,
    sur_name_ar,
    sur_ayah_count,
    sur_revelation_order
FROM quran.surahs
WHERE sur_revelation_type = 'meccan'
ORDER BY sur_revelation_order;
```

---

## 2. البحث المتقدم

### 2.1 البحث النصي الكامل (Full-Text Search)
```sql
-- البحث عن كلمة "الله"
SELECT
    s.sur_name_ar,
    a.aya_number,
    a.aya_text_uthmani,
    ts_rank(a.aya_text_search, query) AS relevance
FROM quran.ayahs a
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id,
     plainto_tsquery('quran.arabic_quran', 'الله') query
WHERE a.aya_text_search @@ query
ORDER BY relevance DESC
LIMIT 20;
```

### 2.2 البحث باستخدام الدالة المخصصة
```sql
SELECT * FROM quran.search_ayahs_fulltext('الصلاة والزكاة', 'arabic', 15);
```

### 2.3 البحث الضبابي (Fuzzy Search)
```sql
-- البحث عن كلمات مشابهة لـ "رحمن"
SELECT DISTINCT wrd_text_simple
FROM quran.words
WHERE wrd_text_simple % 'رحمن'  -- similarity operator
ORDER BY similarity(wrd_text_simple, 'رحمن') DESC
LIMIT 10;
```

### 2.4 البحث في عدة حقول
```sql
-- البحث في النص أو الترجمة أو التفسير
SELECT
    'ayah' AS source,
    a.aya_id AS id,
    a.aya_text_uthmani AS text
FROM quran.ayahs a
WHERE a.aya_text_simple ILIKE '%محمد%'

UNION ALL

SELECT
    'translation' AS source,
    t.trl_aya_id AS id,
    t.trl_text AS text
FROM quran.translations t
WHERE t.trl_text ILIKE '%Muhammad%'

UNION ALL

SELECT
    'tafsir' AS source,
    tf.taf_aya_id AS id,
    LEFT(tf.taf_text, 200) AS text
FROM quran.tafsir tf
WHERE tf.taf_text ILIKE '%النبي%'
LIMIT 50;
```

---

## 3. التحليل الصرفي

### 3.1 جميع الكلمات من جذر معين
```sql
-- جميع مشتقات جذر "ك.ت.ب"
SELECT
    wrd_text_simple AS الكلمة,
    wrd_pattern AS الوزن,
    wrd_pos AS النوع,
    wrd_frequency_quran AS التكرار,
    COUNT(*) AS عدد_المواضع
FROM quran.words
WHERE wrd_root = 'ك.ت.ب'
GROUP BY wrd_text_simple, wrd_pattern, wrd_pos, wrd_frequency_quran
ORDER BY wrd_frequency_quran DESC;
```

### 3.2 استخدام الدالة للحصول على المشتقات مع أمثلة
```sql
SELECT * FROM quran.get_root_derivatives('ع.ل.م');
```

### 3.3 الكلمات على وزن معين
```sql
-- جميع الكلمات على وزن "فاعل"
SELECT
    wrd_text_simple,
    wrd_root,
    wrd_gloss_ar,
    COUNT(*) OVER (PARTITION BY wrd_text_simple) AS frequency
FROM quran.words
WHERE wrd_pattern = 'فاعل'
GROUP BY wrd_text_simple, wrd_root, wrd_gloss_ar
ORDER BY frequency DESC;
```

### 3.4 تحليل أنواع الكلمات في آية
```sql
-- توزيع أنواع الكلمات في الفاتحة
SELECT
    wrd_pos AS نوع_الكلمة,
    COUNT(*) AS العدد,
    ARRAY_AGG(wrd_text_simple ORDER BY wrd_position) AS الكلمات
FROM quran.words
WHERE wrd_aya_id IN (
    SELECT aya_id FROM quran.ayahs WHERE aya_sur_id = 1
)
GROUP BY wrd_pos
ORDER BY COUNT(*) DESC;
```

### 3.5 إحصائيات الجذور في سورة معينة
```sql
-- أكثر الجذور تكراراً في سورة البقرة
SELECT
    wrd_root AS الجذر,
    r.root_meaning_ar AS المعنى,
    COUNT(*) AS التكرار,
    COUNT(DISTINCT wrd_text_simple) AS عدد_المشتقات
FROM quran.words w
LEFT JOIN quran.roots r ON w.wrd_root = r.root_text
WHERE wrd_aya_id IN (
    SELECT aya_id FROM quran.ayahs WHERE aya_sur_id = 2
)
GROUP BY wrd_root, r.root_meaning_ar
ORDER BY التكرار DESC
LIMIT 20;
```

---

## 4. الموضوعات والربط

### 4.1 الآيات حسب موضوع معين
```sql
-- جميع الآيات عن موضوع "التوحيد"
SELECT
    s.sur_name_ar,
    a.aya_number,
    a.aya_text_simple,
    at.ayt_relevance_score AS درجة_الارتباط
FROM quran.ayah_topics at
JOIN quran.ayahs a ON at.ayt_aya_id = a.aya_id
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
JOIN quran.topics t ON at.ayt_top_id = t.top_id
WHERE t.top_name_ar = 'التوحيد'
ORDER BY at.ayt_relevance_score DESC;
```

### 4.2 الموضوعات الهرمية (شجرية)
```sql
-- الموضوعات وفروعها
WITH RECURSIVE topic_tree AS (
    SELECT
        top_id,
        top_name_ar,
        top_parent_id,
        top_level,
        0 AS depth,
        top_name_ar AS full_path
    FROM quran.topics
    WHERE top_parent_id IS NULL

    UNION ALL

    SELECT
        t.top_id,
        t.top_name_ar,
        t.top_parent_id,
        t.top_level,
        tt.depth + 1,
        tt.full_path || ' > ' || t.top_name_ar
    FROM quran.topics t
    JOIN topic_tree tt ON t.top_parent_id = tt.top_id
)
SELECT
    REPEAT('  ', depth) || top_name_ar AS الموضوع_الهرمي,
    top_level AS المستوى,
    full_path AS المسار_الكامل
FROM topic_tree
ORDER BY full_path;
```

### 4.3 إحصائيات موضوع معين
```sql
-- استخدام الدالة المخصصة
SELECT * FROM quran.get_topic_statistics(5);
```

### 4.4 الموضوعات المشتركة بين آيتين
```sql
-- المواضيع المشتركة
SELECT DISTINCT t.top_name_ar
FROM quran.ayah_topics at1
JOIN quran.ayah_topics at2 ON at1.ayt_top_id = at2.ayt_top_id
JOIN quran.topics t ON at1.ayt_top_id = t.top_id
WHERE at1.ayt_aya_id = 100
  AND at2.ayt_aya_id = 200;
```

---

## 5. التحليل الإحصائي

### 5.1 إحصائيات السور
```sql
SELECT
    sur_name_ar AS السورة,
    sur_ayah_count AS عدد_الآيات,
    sur_word_count AS عدد_الكلمات,
    sur_letter_count AS عدد_الحروف,
    ROUND(sur_word_count::NUMERIC / sur_ayah_count, 2) AS متوسط_الكلمات_للآية,
    sur_revelation_type AS النوع
FROM quran.surahs
ORDER BY sur_word_count DESC;
```

### 5.2 توزيع الآيات حسب الأجزاء
```sql
SELECT
    aya_juz AS الجزء,
    COUNT(*) AS عدد_الآيات,
    SUM(aya_word_count) AS إجمالي_الكلمات,
    ROUND(AVG(aya_word_count), 2) AS متوسط_الكلمات
FROM quran.ayahs
GROUP BY aya_juz
ORDER BY aya_juz;
```

### 5.3 أطول وأقصر الآيات
```sql
-- أطول 10 آيات
SELECT
    s.sur_name_ar,
    a.aya_number,
    a.aya_word_count,
    LEFT(a.aya_text_simple, 100) || '...' AS بداية_النص
FROM quran.ayahs a
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
ORDER BY a.aya_word_count DESC
LIMIT 10;

-- أقصر 10 آيات
SELECT
    s.sur_name_ar,
    a.aya_number,
    a.aya_word_count,
    a.aya_text_simple AS النص_الكامل
FROM quran.ayahs a
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
WHERE a.aya_word_count > 0
ORDER BY a.aya_word_count ASC
LIMIT 10;
```

### 5.4 أكثر الكلمات تكراراً في القرآن
```sql
SELECT
    wrd_text_simple AS الكلمة,
    wrd_root AS الجذر,
    SUM(wrd_frequency_quran) AS إجمالي_التكرار,
    COUNT(DISTINCT wrd_aya_id) AS عدد_الآيات
FROM quran.words
GROUP BY wrd_text_simple, wrd_root
ORDER BY إجمالي_التكرار DESC
LIMIT 50;
```

### 5.5 تحليل تكرار الكلمات في سياق معين
```sql
-- استخدام الدالة المخصصة للبحث في سورة البقرة
SELECT * FROM quran.analyze_word_frequency_in_context('surah', 2)
LIMIT 20;

-- في جزء معين
SELECT * FROM quran.analyze_word_frequency_in_context('juz', 1)
LIMIT 20;

-- في موضوع معين
SELECT * FROM quran.analyze_word_frequency_in_context('topic', 5)
LIMIT 20;
```

---

## 6. البحث الدلالي (Semantic Search)

### 6.1 البحث عن آيات مشابهة دلالياً
```sql
-- البحث باستخدام embedding معين (يُحصل عليه من نموذج ML)
-- مثال: embedding لجملة "الإيمان بالله"
SELECT * FROM quran.search_ayahs_semantic(
    '[0.123, 0.456, 0.789, ...]'::vector(768),  -- embedding من النموذج
    0.7,  -- حد التشابه
    10    -- عدد النتائج
);
```

### 6.2 الآيات المرتبطة بآية معينة
```sql
-- آيات مشابهة لآية الكرسي
SELECT * FROM quran.get_related_ayahs(
    255,  -- aya_id لآية الكرسي
    0.75, -- حد التشابه
    5     -- عدد النتائج
);
```

### 6.3 تجميع الآيات حسب التشابه (Clustering)
```sql
-- استعلام متقدم لتجميع الآيات في سورة معينة
WITH aya_similarities AS (
    SELECT
        a1.aya_id AS aya1,
        a2.aya_id AS aya2,
        1 - (a1.aya_embedding_v1 <=> a2.aya_embedding_v1) AS similarity
    FROM quran.ayahs a1
    CROSS JOIN quran.ayahs a2
    WHERE a1.aya_sur_id = 2  -- البقرة
      AND a2.aya_sur_id = 2
      AND a1.aya_id < a2.aya_id
      AND a1.aya_embedding_v1 IS NOT NULL
      AND a2.aya_embedding_v1 IS NOT NULL
)
SELECT
    aya1,
    aya2,
    similarity,
    RANK() OVER (PARTITION BY aya1 ORDER BY similarity DESC) AS rank
FROM aya_similarities
WHERE similarity > 0.8
ORDER BY aya1, rank
LIMIT 100;
```

---

## 7. استعلامات متقدمة

### 7.1 الآيات التي تتكلم عن نفس الحدث التاريخي
```sql
-- آيات غزوة بدر
SELECT
    s.sur_name_ar,
    a.aya_number,
    a.aya_text_simple,
    rc.ctx_event,
    rc.ctx_date_hijri
FROM quran.revelation_contexts rc
JOIN quran.ayahs a ON a.aya_revelation_context_id = rc.ctx_id
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
WHERE rc.ctx_event ILIKE '%بدر%';
```

### 7.2 مقارنة تفاسير مختلفة لآية واحدة
```sql
-- تفاسير آية الكرسي من مفسرين مختلفين
SELECT
    m.muf_name_ar AS المفسر,
    m.muf_tafsir_name AS كتاب_التفسير,
    LEFT(t.taf_text, 200) || '...' AS بداية_التفسير,
    t.taf_type AS نوع_التفسير
FROM quran.tafsir t
JOIN quran.mufassireen m ON t.taf_mufassir_id = m.muf_id
WHERE t.taf_aya_id = 255  -- آية الكرسي
ORDER BY m.muf_death_year;
```

### 7.3 الآيات التي تحتوي على أكثر من جذر معين
```sql
-- آيات تحتوي على جذور: ع.ل.م، ق.ر.أ، ك.ت.ب
SELECT
    s.sur_name_ar,
    a.aya_number,
    a.aya_text_simple,
    ARRAY(
        SELECT DISTINCT wrd_root
        FROM quran.words w
        WHERE w.wrd_aya_id = a.aya_id
          AND wrd_root IN ('ع.ل.م', 'ق.ر.أ', 'ك.ت.ب')
    ) AS الجذور_الموجودة
FROM quran.ayahs a
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
WHERE a.aya_roots && ARRAY['ع.ل.م', 'ق.ر.أ', 'ك.ت.ب']
  AND ARRAY_LENGTH(
      ARRAY(SELECT unnest(a.aya_roots) INTERSECT SELECT unnest(ARRAY['ع.ل.م', 'ق.ر.أ', 'ك.ت.ب'])),
      1
  ) >= 2;
```

### 7.4 تتبع جذر عبر القرآن بالترتيب
```sql
-- تتبع استخدام جذر "ص.ل.ي" عبر المصحف
SELECT
    a.aya_global_id,
    s.sur_name_ar,
    a.aya_number,
    w.wrd_text_simple AS الكلمة,
    w.wrd_pattern AS الوزن,
    a.aya_text_simple
FROM quran.words w
JOIN quran.ayahs a ON w.wrd_aya_id = a.aya_id
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
WHERE w.wrd_root = 'ص.ل.ي'
ORDER BY a.aya_global_id;
```

### 7.5 تحليل الترابط بين الموضوعات
```sql
-- أزواج الموضوعات التي تظهر معاً كثيراً
SELECT
    t1.top_name_ar AS الموضوع_الأول,
    t2.top_name_ar AS الموضوع_الثاني,
    COUNT(*) AS عدد_الآيات_المشتركة
FROM quran.ayah_topics at1
JOIN quran.ayah_topics at2 ON at1.ayt_aya_id = at2.ayt_aya_id AND at1.ayt_top_id < at2.ayt_top_id
JOIN quran.topics t1 ON at1.ayt_top_id = t1.top_id
JOIN quran.topics t2 ON at2.ayt_top_id = t2.top_id
GROUP BY t1.top_name_ar, t2.top_name_ar
HAVING COUNT(*) >= 5
ORDER BY عدد_الآيات_المشتركة DESC
LIMIT 20;
```

### 7.6 استعلام شامل: بناء "صفحة آية"
```sql
-- جميع المعلومات المتعلقة بآية معينة
WITH aya_info AS (
    SELECT * FROM quran.ayahs WHERE aya_id = 255  -- آية الكرسي
)
SELECT
    -- معلومات أساسية
    json_build_object(
        'surah', (SELECT json_build_object(
            'id', s.sur_id,
            'name_ar', s.sur_name_ar,
            'name_en', s.sur_name_en,
            'type', s.sur_revelation_type
        ) FROM quran.surahs s WHERE s.sur_id = a.aya_sur_id),
        'ayah', json_build_object(
            'number', a.aya_number,
            'text_uthmani', a.aya_text_uthmani,
            'text_simple', a.aya_text_simple,
            'word_count', a.aya_word_count,
            'juz', a.aya_juz,
            'page', a.aya_page
        ),
        'words', (
            SELECT json_agg(json_build_object(
                'text', w.wrd_text_simple,
                'root', w.wrd_root,
                'pattern', w.wrd_pattern,
                'pos', w.wrd_pos,
                'meaning', w.wrd_gloss_ar
            ) ORDER BY w.wrd_position)
            FROM quran.words w WHERE w.wrd_aya_id = a.aya_id
        ),
        'topics', (
            SELECT json_agg(t.top_name_ar)
            FROM quran.ayah_topics at
            JOIN quran.topics t ON at.ayt_top_id = t.top_id
            WHERE at.ayt_aya_id = a.aya_id
        ),
        'tafsirs', (
            SELECT json_agg(json_build_object(
                'mufassir', m.muf_name_ar,
                'text', LEFT(tf.taf_text, 500)
            ))
            FROM quran.tafsir tf
            JOIN quran.mufassireen m ON tf.taf_mufassir_id = m.muf_id
            WHERE tf.taf_aya_id = a.aya_id
            LIMIT 3
        ),
        'recitations', (
            SELECT json_agg(json_build_object(
                'reciter', r.rct_name_ar,
                'url', rec.rec_file_url
            ))
            FROM quran.recitations rec
            JOIN quran.reciters r ON rec.rec_reciter_id = r.rct_id
            WHERE rec.rec_aya_id = a.aya_id
            LIMIT 5
        )
    ) AS complete_aya_data
FROM aya_info a;
```

---

## 🎯 أمثلة استعلامات ذكية إضافية

### البحث متعدد المعايير
```sql
-- آيات مكية، في الجزء الأول، تحتوي على جذر "ر.ح.م"، موضوع "رحمة الله"
SELECT
    s.sur_name_ar,
    a.aya_number,
    a.aya_text_simple
FROM quran.ayahs a
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
WHERE s.sur_revelation_type = 'meccan'
  AND a.aya_juz = 1
  AND 'ر.ح.م' = ANY(a.aya_roots)
  AND EXISTS (
      SELECT 1 FROM quran.ayah_topics at
      JOIN quran.topics t ON at.ayt_top_id = t.top_id
      WHERE at.ayt_aya_id = a.aya_id
        AND t.top_name_ar ILIKE '%رحمة%'
  );
```

### تحليل أسلوبي
```sql
-- متوسط طول الآيات في كل سورة
SELECT
    s.sur_name_ar,
    COUNT(*) AS عدد_الآيات,
    ROUND(AVG(a.aya_word_count), 2) AS متوسط_الكلمات,
    MIN(a.aya_word_count) AS أقصر_آية,
    MAX(a.aya_word_count) AS أطول_آية
FROM quran.ayahs a
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
GROUP BY s.sur_id, s.sur_name_ar
ORDER BY متوسط_الكلمات DESC;
```

---

## ⚡ تحسين الأداء

### استخدام EXPLAIN ANALYZE
```sql
EXPLAIN ANALYZE
SELECT * FROM quran.search_ayahs_fulltext('الله', 'arabic', 20);
```

### تحديث الإحصائيات
```sql
ANALYZE quran.ayahs;
ANALYZE quran.words;
ANALYZE quran.tafsir;
```

### تحديث Materialized Views
```sql
CALL analytics.refresh_all_materialized_views();
```

---

**تم إنشاء هذا الدليل: 2025-10-30**

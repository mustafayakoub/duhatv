-- ═══════════════════════════════════════════════════════════════
-- 🔍 Views المتقدمة والدوال الذكية
-- ═══════════════════════════════════════════════════════════════

\c quran_hierarchical_db
SET search_path TO quran, public;

BEGIN;

-- ═══════════════════════════════════════════════════════════════
-- MATERIALIZED VIEWS للأداء العالي
-- ═══════════════════════════════════════════════════════════════

-- View 1: عرض كامل للآيات مع معلومات السورة
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.v_ayahs_complete AS
SELECT
    a.aya_id,
    a.aya_uuid,
    a.aya_global_id,
    a.aya_number,
    a.aya_text_uthmani,
    a.aya_text_simple,
    a.aya_word_count,
    a.aya_letter_count,
    a.aya_juz,
    a.aya_hizb,
    a.aya_page,
    a.aya_topics,
    a.aya_roots,
    -- معلومات السورة
    s.sur_id,
    s.sur_name_ar,
    s.sur_name_en,
    s.sur_revelation_type,
    s.sur_ayah_count,
    -- حسابات إضافية
    a.aya_number || '/' || s.sur_ayah_count AS aya_position,
    ROUND((a.aya_number::NUMERIC / s.sur_ayah_count) * 100, 2) AS aya_percentage
FROM quran.ayahs a
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id;

CREATE UNIQUE INDEX idx_v_ayahs_complete_id ON analytics.v_ayahs_complete(aya_id);
CREATE INDEX idx_v_ayahs_complete_surah ON analytics.v_ayahs_complete(sur_id);

COMMENT ON MATERIALIZED VIEW analytics.v_ayahs_complete IS
'عرض شامل للآيات مع معلومات السور - يُحدث يومياً';

-- View 2: إحصائيات الجذور
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.v_root_statistics AS
SELECT
    r.root_id,
    r.root_text,
    r.root_meaning_ar,
    r.root_type,
    COUNT(DISTINCT w.wrd_id) AS total_words,
    COUNT(DISTINCT w.wrd_aya_id) AS total_ayahs,
    COUNT(DISTINCT a.aya_sur_id) AS total_surahs,
    ARRAY_AGG(DISTINCT w.wrd_pattern) AS used_patterns,
    SUM(w.wrd_frequency_quran) AS total_frequency
FROM quran.roots r
LEFT JOIN quran.words w ON w.wrd_root = r.root_text
LEFT JOIN quran.ayahs a ON w.wrd_aya_id = a.aya_id
GROUP BY r.root_id, r.root_text, r.root_meaning_ar, r.root_type
ORDER BY total_frequency DESC NULLS LAST;

CREATE UNIQUE INDEX idx_v_root_statistics_id ON analytics.v_root_statistics(root_id);
CREATE INDEX idx_v_root_statistics_freq ON analytics.v_root_statistics(total_frequency DESC);

COMMENT ON MATERIALIZED VIEW analytics.v_root_statistics IS
'إحصائيات شاملة لكل جذر لغوي';

-- View 3: الموضوعات مع عدد الآيات
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.v_topics_with_counts AS
WITH RECURSIVE topic_tree AS (
    -- المستوى الأول (الجذور)
    SELECT
        top_id,
        top_name_ar,
        top_parent_id,
        top_level,
        top_path,
        ARRAY[top_id] AS path_array
    FROM quran.topics
    WHERE top_parent_id IS NULL

    UNION ALL

    -- المستويات الفرعية
    SELECT
        t.top_id,
        t.top_name_ar,
        t.top_parent_id,
        t.top_level,
        t.top_path,
        tt.path_array || t.top_id
    FROM quran.topics t
    JOIN topic_tree tt ON t.top_parent_id = tt.top_id
)
SELECT
    tt.*,
    COUNT(DISTINCT at.ayt_aya_id) AS direct_ayahs,
    COALESCE(
        (SELECT STRING_AGG(top_name_ar, ' > ' ORDER BY level)
         FROM unnest(tt.path_array) WITH ORDINALITY AS x(id, level)
         JOIN quran.topics t ON t.top_id = x.id),
        tt.top_name_ar
    ) AS full_path_arabic
FROM topic_tree tt
LEFT JOIN quran.ayah_topics at ON tt.top_id = at.ayt_top_id
GROUP BY tt.top_id, tt.top_name_ar, tt.top_parent_id, tt.top_level, tt.top_path, tt.path_array
ORDER BY tt.path_array;

CREATE UNIQUE INDEX idx_v_topics_with_counts_id ON analytics.v_topics_with_counts(top_id);

COMMENT ON MATERIALIZED VIEW analytics.v_topics_with_counts IS
'الموضوعات الهرمية مع عدد الآيات المباشرة';

-- ═══════════════════════════════════════════════════════════════
-- REGULAR VIEWS (عروض عادية)
-- ═══════════════════════════════════════════════════════════════

-- View 4: عرض الكلمات مع سياقها الكامل
CREATE OR REPLACE VIEW quran.v_words_with_context AS
SELECT
    w.*,
    a.aya_text_uthmani,
    a.aya_number,
    s.sur_id,
    s.sur_name_ar,
    r.root_meaning_ar,
    p.pat_meaning_ar
FROM quran.words w
JOIN quran.ayahs a ON w.wrd_aya_id = a.aya_id
JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
LEFT JOIN quran.roots r ON w.wrd_root = r.root_text
LEFT JOIN quran.patterns p ON w.wrd_pattern = p.pat_text;

COMMENT ON VIEW quran.v_words_with_context IS
'عرض الكلمات مع السياق الكامل (الآية، السورة، المعاني)';

-- View 5: آخر نشاط المستخدمين
CREATE OR REPLACE VIEW community.v_users_activity AS
SELECT
    u.usr_id,
    u.usr_username,
    u.usr_display_name,
    u.usr_level,
    u.usr_contribution_points,
    u.usr_streak_days,
    u.last_login,
    COUNT(DISTINCT b.bmk_id) AS bookmarks_count,
    COUNT(DISTINCT n.note_id) AS notes_count,
    COALESCE(a.aya_number, 0) AS last_read_aya,
    COALESCE(s.sur_name_ar, '') AS last_read_surah
FROM community.users u
LEFT JOIN community.bookmarks b ON u.usr_id = b.bmk_usr_id
LEFT JOIN community.annotations n ON u.usr_id = n.note_usr_id
LEFT JOIN quran.ayahs a ON u.usr_last_read_aya = a.aya_id
LEFT JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
GROUP BY u.usr_id, a.aya_number, s.sur_name_ar;

COMMENT ON VIEW community.v_users_activity IS
'نظرة عامة على نشاط المستخدمين';

-- ═══════════════════════════════════════════════════════════════
-- FUNCTIONS المتقدمة
-- ═══════════════════════════════════════════════════════════════

-- Function 1: البحث الدلالي باستخدام Embeddings
CREATE OR REPLACE FUNCTION quran.search_ayahs_semantic(
    query_embedding vector(768),
    similarity_threshold REAL DEFAULT 0.7,
    limit_results INTEGER DEFAULT 10
)
RETURNS TABLE (
    aya_id INTEGER,
    aya_text_uthmani TEXT,
    sur_name_ar VARCHAR(50),
    aya_number SMALLINT,
    similarity_score REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.aya_id,
        a.aya_text_uthmani,
        s.sur_name_ar,
        a.aya_number,
        1 - (a.aya_embedding_v1 <=> query_embedding) AS similarity_score
    FROM quran.ayahs a
    JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
    WHERE a.aya_embedding_v1 IS NOT NULL
      AND (1 - (a.aya_embedding_v1 <=> query_embedding)) >= similarity_threshold
    ORDER BY similarity_score DESC
    LIMIT limit_results;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION quran.search_ayahs_semantic(vector, REAL, INTEGER) IS
'البحث الدلالي عن آيات مشابهة باستخدام Vector Embeddings';

-- Function 2: البحث النصي الكامل المتقدم
CREATE OR REPLACE FUNCTION quran.search_ayahs_fulltext(
    search_query TEXT,
    search_language TEXT DEFAULT 'arabic',
    limit_results INTEGER DEFAULT 20
)
RETURNS TABLE (
    aya_id INTEGER,
    aya_text_uthmani TEXT,
    sur_name_ar VARCHAR(50),
    aya_number SMALLINT,
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.aya_id,
        a.aya_text_uthmani,
        s.sur_name_ar,
        a.aya_number,
        ts_rank(a.aya_text_search, query) AS rank
    FROM quran.ayahs a
    JOIN quran.surahs s ON a.aya_sur_id = s.sur_id,
    plainto_tsquery('quran.arabic_quran', search_query) query
    WHERE a.aya_text_search @@ query
    ORDER BY rank DESC
    LIMIT limit_results;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION quran.search_ayahs_fulltext(TEXT, TEXT, INTEGER) IS
'البحث النصي الكامل مع ترتيب حسب الأهمية';

-- Function 3: الحصول على جميع مشتقات جذر معين
CREATE OR REPLACE FUNCTION quran.get_root_derivatives(
    root_text_param VARCHAR(20)
)
RETURNS TABLE (
    word_text VARCHAR(100),
    word_pattern VARCHAR(30),
    word_pos quran.word_pos,
    frequency INTEGER,
    example_ayah TEXT,
    example_surah VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        w.wrd_text_simple,
        w.wrd_pattern,
        w.wrd_pos,
        w.wrd_frequency_quran,
        a.aya_text_simple,
        s.sur_name_ar
    FROM quran.words w
    JOIN quran.ayahs a ON w.wrd_aya_id = a.aya_id
    JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
    WHERE w.wrd_root = root_text_param
    ORDER BY w.wrd_frequency_quran DESC;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION quran.get_root_derivatives(VARCHAR) IS
'الحصول على جميع المشتقات من جذر معين مع أمثلة';

-- Function 4: إحصائيات موضوع معين
CREATE OR REPLACE FUNCTION quran.get_topic_statistics(
    topic_id_param INTEGER
)
RETURNS TABLE (
    total_ayahs INTEGER,
    total_surahs INTEGER,
    meccan_ayahs INTEGER,
    medinan_ayahs INTEGER,
    most_common_roots TEXT[],
    average_aya_length NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(DISTINCT at.ayt_aya_id)::INTEGER,
        COUNT(DISTINCT a.aya_sur_id)::INTEGER,
        COUNT(DISTINCT a.aya_id) FILTER (WHERE s.sur_revelation_type = 'meccan')::INTEGER,
        COUNT(DISTINCT a.aya_id) FILTER (WHERE s.sur_revelation_type = 'medinan')::INTEGER,
        ARRAY(
            SELECT unnest(a.aya_roots)
            FROM quran.ayah_topics at2
            JOIN quran.ayahs a2 ON at2.ayt_aya_id = a2.aya_id
            WHERE at2.ayt_top_id = topic_id_param
            GROUP BY unnest
            ORDER BY COUNT(*) DESC
            LIMIT 10
        ),
        AVG(a.aya_word_count)
    FROM quran.ayah_topics at
    JOIN quran.ayahs a ON at.ayt_aya_id = a.aya_id
    JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
    WHERE at.ayt_top_id = topic_id_param;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION quran.get_topic_statistics(INTEGER) IS
'إحصائيات تفصيلية عن موضوع معين';

-- Function 5: الآيات المرتبطة (بناءً على التشابه الدلالي)
CREATE OR REPLACE FUNCTION quran.get_related_ayahs(
    aya_id_param INTEGER,
    similarity_threshold REAL DEFAULT 0.75,
    limit_results INTEGER DEFAULT 5
)
RETURNS TABLE (
    related_aya_id INTEGER,
    aya_text TEXT,
    sur_name VARCHAR(50),
    similarity REAL
) AS $$
DECLARE
    source_embedding vector(768);
BEGIN
    -- الحصول على embedding الآية المصدر
    SELECT aya_embedding_v1 INTO source_embedding
    FROM quran.ayahs
    WHERE aya_id = aya_id_param;

    IF source_embedding IS NULL THEN
        RAISE EXCEPTION 'Embedding not found for aya_id: %', aya_id_param;
    END IF;

    RETURN QUERY
    SELECT
        a.aya_id,
        a.aya_text_uthmani,
        s.sur_name_ar,
        1 - (a.aya_embedding_v1 <=> source_embedding) AS similarity
    FROM quran.ayahs a
    JOIN quran.surahs s ON a.aya_sur_id = s.sur_id
    WHERE a.aya_id != aya_id_param
      AND a.aya_embedding_v1 IS NOT NULL
      AND (1 - (a.aya_embedding_v1 <=> source_embedding)) >= similarity_threshold
    ORDER BY similarity DESC
    LIMIT limit_results;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION quran.get_related_ayahs(INTEGER, REAL, INTEGER) IS
'الحصول على آيات مرتبطة دلالياً بآية معينة';

-- Function 6: تحليل تكرار الكلمات في سياق معين
CREATE OR REPLACE FUNCTION quran.analyze_word_frequency_in_context(
    context_type VARCHAR(20), -- 'surah', 'juz', 'topic'
    context_id INTEGER
)
RETURNS TABLE (
    word_text VARCHAR(100),
    word_root VARCHAR(20),
    frequency BIGINT,
    unique_ayahs BIGINT
) AS $$
BEGIN
    IF context_type = 'surah' THEN
        RETURN QUERY
        SELECT
            w.wrd_text_simple,
            w.wrd_root,
            COUNT(*) AS frequency,
            COUNT(DISTINCT w.wrd_aya_id) AS unique_ayahs
        FROM quran.words w
        JOIN quran.ayahs a ON w.wrd_aya_id = a.aya_id
        WHERE a.aya_sur_id = context_id
        GROUP BY w.wrd_text_simple, w.wrd_root
        ORDER BY frequency DESC;

    ELSIF context_type = 'juz' THEN
        RETURN QUERY
        SELECT
            w.wrd_text_simple,
            w.wrd_root,
            COUNT(*) AS frequency,
            COUNT(DISTINCT w.wrd_aya_id) AS unique_ayahs
        FROM quran.words w
        JOIN quran.ayahs a ON w.wrd_aya_id = a.aya_id
        WHERE a.aya_juz = context_id
        GROUP BY w.wrd_text_simple, w.wrd_root
        ORDER BY frequency DESC;

    ELSIF context_type = 'topic' THEN
        RETURN QUERY
        SELECT
            w.wrd_text_simple,
            w.wrd_root,
            COUNT(*) AS frequency,
            COUNT(DISTINCT w.wrd_aya_id) AS unique_ayahs
        FROM quran.words w
        JOIN quran.ayah_topics at ON w.wrd_aya_id = at.ayt_aya_id
        WHERE at.ayt_top_id = context_id
        GROUP BY w.wrd_text_simple, w.wrd_root
        ORDER BY frequency DESC;
    END IF;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION quran.analyze_word_frequency_in_context(VARCHAR, INTEGER) IS
'تحليل تكرار الكلمات في سياق معين (سورة، جزء، موضوع)';

-- Function 7: تحديث إحصائيات الجذور
CREATE OR REPLACE FUNCTION quran.update_root_statistics()
RETURNS VOID AS $$
BEGIN
    UPDATE quran.roots r
    SET
        root_word_count = (
            SELECT COUNT(DISTINCT wrd_id)
            FROM quran.words w
            WHERE w.wrd_root = r.root_text
        ),
        root_ayah_count = (
            SELECT COUNT(DISTINCT wrd_aya_id)
            FROM quran.words w
            WHERE w.wrd_root = r.root_text
        ),
        root_frequency = (
            SELECT SUM(wrd_frequency_quran)
            FROM quran.words w
            WHERE w.wrd_root = r.root_text
        ),
        updated_at = CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION quran.update_root_statistics() IS
'تحديث إحصائيات جميع الجذور (يُشغل دورياً)';

-- ═══════════════════════════════════════════════════════════════
-- STORED PROCEDURES للعمليات المعقدة
-- ═══════════════════════════════════════════════════════════════

-- Procedure 1: تحديث جميع Materialized Views
CREATE OR REPLACE PROCEDURE analytics.refresh_all_materialized_views()
LANGUAGE plpgsql AS $$
BEGIN
    RAISE NOTICE 'Refreshing materialized views...';

    REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.v_ayahs_complete;
    RAISE NOTICE 'Refreshed: v_ayahs_complete';

    REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.v_root_statistics;
    RAISE NOTICE 'Refreshed: v_root_statistics';

    REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.v_topics_with_counts;
    RAISE NOTICE 'Refreshed: v_topics_with_counts';

    RAISE NOTICE 'All materialized views refreshed successfully!';
END;
$$;

COMMENT ON PROCEDURE analytics.refresh_all_materialized_views() IS
'تحديث جميع الـ Materialized Views (يُشغل يومياً عبر cron)';

COMMIT;

-- ═══════════════════════════════════════════════════════════════
-- ✅ تم إنشاء جميع Views والدوال بنجاح!
-- ═══════════════════════════════════════════════════════════════

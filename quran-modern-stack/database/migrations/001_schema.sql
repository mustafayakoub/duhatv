-- ═══════════════════════════════════════════════════════════════════════════
-- Quran Modern Stack - Unified Database Schema
-- نظام قاعدة بيانات قرآنية موحدة وحديثة
--
-- Version: 1.0
-- Database: PostgreSQL 16+
-- Encoding: UTF-8
-- Collation: ar_SA.UTF-8 (for Arabic support)
-- ═══════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════
-- Extensions (الإضافات)
-- ═══════════════════════════════════════════════════════════════════════════

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- Similar text search
CREATE EXTENSION IF NOT EXISTS "unaccent";       -- Remove accents
CREATE EXTENSION IF NOT EXISTS "btree_gin";      -- GIN indexes for better performance
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements"; -- Query performance monitoring

-- ═══════════════════════════════════════════════════════════════════════════
-- Core Tables (الجداول الأساسية)
-- ═══════════════════════════════════════════════════════════════════════════

-- السور (Surahs)
CREATE TABLE surahs (
    id SERIAL PRIMARY KEY,
    number INTEGER UNIQUE NOT NULL CHECK (number BETWEEN 1 AND 114),
    name_arabic TEXT NOT NULL,
    name_transliteration TEXT,
    name_translation_en TEXT,

    -- معلومات النزول
    revelation_type TEXT CHECK (revelation_type IN ('Meccan', 'Medinan', 'مكية', 'مدنية')),
    revelation_order INTEGER,

    -- الإحصائيات
    ayah_count INTEGER NOT NULL CHECK (ayah_count > 0),
    word_count INTEGER,
    letter_count INTEGER,

    -- معلومات إضافية
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE surahs IS 'السور - كل سور القرآن الكريم';
COMMENT ON COLUMN surahs.number IS 'رقم السورة في المصحف (1-114)';
COMMENT ON COLUMN surahs.revelation_type IS 'مكية أو مدنية';

-- الآيات (Ayahs)
CREATE TABLE ayahs (
    id SERIAL PRIMARY KEY,
    surah_id INTEGER NOT NULL REFERENCES surahs(id) ON DELETE CASCADE,
    ayah_number INTEGER NOT NULL CHECK (ayah_number > 0),
    global_ayah_number INTEGER UNIQUE CHECK (global_ayah_number BETWEEN 1 AND 6236),

    -- النصوص المختلفة
    text_uthmani TEXT NOT NULL,              -- النص العثماني (بالتشكيل)
    text_simple TEXT NOT NULL,               -- نص مبسط (بدون تشكيل)
    text_imlaei TEXT,                        -- النص الإملائي
    text_tajweed TEXT,                       -- نص مع علامات التجويد

    -- معلومات المصحف
    juz_number INTEGER CHECK (juz_number BETWEEN 1 AND 30),
    hizb_number INTEGER CHECK (hizb_number BETWEEN 1 AND 60),
    page_number INTEGER CHECK (page_number BETWEEN 1 AND 604),

    -- معلومات إضافية
    sajda_type TEXT CHECK (sajda_type IN ('recommended', 'obligatory', 'مستحبة', 'واجبة')),
    revelation_order_global INTEGER,

    -- للبحث السريع
    search_vector tsvector,

    -- معلومات إضافية
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(surah_id, ayah_number)
);

CREATE INDEX idx_ayahs_surah ON ayahs(surah_id);
CREATE INDEX idx_ayahs_juz ON ayahs(juz_number);
CREATE INDEX idx_ayahs_page ON ayahs(page_number);
CREATE INDEX idx_ayahs_search ON ayahs USING GIN(search_vector);
CREATE INDEX idx_ayahs_text_simple ON ayahs USING GIN(text_simple gin_trgm_ops);

COMMENT ON TABLE ayahs IS 'الآيات - كل آيات القرآن الكريم (6236 آية)';

-- الجذور (Roots)
CREATE TABLE roots (
    id SERIAL PRIMARY KEY,
    root_text TEXT UNIQUE NOT NULL,
    root_letters INTEGER CHECK (root_letters BETWEEN 2 AND 5),
    occurrence_count INTEGER DEFAULT 0,
    description TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_roots_text ON roots(root_text);

COMMENT ON TABLE roots IS 'الجذور - جذور الكلمات العربية في القرآن (1775 جذر)';

-- اللمّات (Lemmas)
CREATE TABLE lemmas (
    id SERIAL PRIMARY KEY,
    lemma_text TEXT UNIQUE NOT NULL,
    root_id INTEGER REFERENCES roots(id),
    occurrence_count INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_lemmas_root ON lemmas(root_id);
CREATE INDEX idx_lemmas_text ON lemmas(lemma_text);

COMMENT ON TABLE lemmas IS 'اللمّات - الأشكال الأساسية للكلمات';

-- الكلمات (Words)
CREATE TABLE words (
    id SERIAL PRIMARY KEY,
    ayah_id INTEGER NOT NULL REFERENCES ayahs(id) ON DELETE CASCADE,
    word_number INTEGER NOT NULL CHECK (word_number > 0),
    global_word_number INTEGER UNIQUE CHECK (global_word_number BETWEEN 1 AND 77430),

    -- النصوص
    text_uthmani TEXT NOT NULL,
    text_simple TEXT NOT NULL,
    text_imlaei TEXT,

    -- اللغويات
    root_id INTEGER REFERENCES roots(id),
    lemma_id INTEGER REFERENCES lemmas(id),

    -- الإحداثيات (للمصحف الإلكتروني)
    page_number INTEGER,
    line_number INTEGER,
    position_x REAL,
    position_y REAL,

    -- معلومات إضافية
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(ayah_id, word_number)
);

CREATE INDEX idx_words_ayah ON words(ayah_id);
CREATE INDEX idx_words_root ON words(root_id);
CREATE INDEX idx_words_lemma ON words(lemma_id);
CREATE INDEX idx_words_page ON words(page_number);
CREATE INDEX idx_words_text ON words USING GIN(text_simple gin_trgm_ops);

COMMENT ON TABLE words IS 'الكلمات - كل كلمات القرآن (77430 كلمة)';

-- ═══════════════════════════════════════════════════════════════════════════
-- Content Tables (جداول المحتوى)
-- ═══════════════════════════════════════════════════════════════════════════

-- المصادر (Sources)
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    year_hijri INTEGER,
    year_gregorian INTEGER,
    source_type TEXT NOT NULL CHECK (source_type IN ('tafseer', 'translation', 'analysis', 'irab', 'sarf')),
    language TEXT NOT NULL DEFAULT 'ar',
    description TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sources_type ON sources(source_type);
CREATE INDEX idx_sources_language ON sources(language);

COMMENT ON TABLE sources IS 'المصادر - كل مصادر التفاسير والترجمات (293 مصدر)';

-- التفاسير (Tafseer)
CREATE TABLE tafseer (
    id SERIAL PRIMARY KEY,
    ayah_id INTEGER NOT NULL REFERENCES ayahs(id) ON DELETE CASCADE,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    tafseer_text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(ayah_id, source_id)
);

CREATE INDEX idx_tafseer_ayah ON tafseer(ayah_id);
CREATE INDEX idx_tafseer_source ON tafseer(source_id);
CREATE INDEX idx_tafseer_text ON tafseer USING GIN(to_tsvector('arabic', tafseer_text));

COMMENT ON TABLE tafseer IS 'التفاسير - تفاسير الآيات من مصادر متعددة (10+ تفسير)';

-- الترجمات (Translations)
CREATE TABLE translations (
    id SERIAL PRIMARY KEY,
    ayah_id INTEGER NOT NULL REFERENCES ayahs(id) ON DELETE CASCADE,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    language TEXT NOT NULL,
    translation_text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(ayah_id, source_id)
);

CREATE INDEX idx_translations_ayah ON translations(ayah_id);
CREATE INDEX idx_translations_source ON translations(source_id);
CREATE INDEX idx_translations_language ON translations(language);

COMMENT ON TABLE translations IS 'الترجمات - ترجمات الآيات (81,068 ترجمة)';

-- ═══════════════════════════════════════════════════════════════════════════
-- Linguistic Analysis Tables (جداول التحليل اللغوي)
-- ═══════════════════════════════════════════════════════════════════════════

-- إعراب الكلمات (Word I'rab)
CREATE TABLE word_irab (
    id SERIAL PRIMARY KEY,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    irab_text TEXT NOT NULL,
    source_id INTEGER REFERENCES sources(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_word_irab_word ON word_irab(word_id);

COMMENT ON TABLE word_irab IS 'الإعراب - إعراب كلمات القرآن (77,432 إعراب)';

-- صرف الكلمات (Word Sarf)
CREATE TABLE word_sarf (
    id SERIAL PRIMARY KEY,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    sarf_text TEXT NOT NULL,
    pattern_id INTEGER,
    source_id INTEGER REFERENCES sources(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_word_sarf_word ON word_sarf(word_id);

COMMENT ON TABLE word_sarf IS 'الصرف - صرف كلمات القرآن (77,432 صرف)';

-- معاني الكلمات (Word Meanings)
CREATE TABLE word_meanings (
    id SERIAL PRIMARY KEY,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    meaning_text TEXT NOT NULL,
    language TEXT DEFAULT 'ar',
    source_id INTEGER REFERENCES sources(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_word_meanings_word ON word_meanings(word_id);
CREATE INDEX idx_word_meanings_language ON word_meanings(language);

COMMENT ON TABLE word_meanings IS 'المعاني - معاني كلمات القرآن (77,432 معنى)';

-- الأنماط الصرفية (Morphological Patterns)
CREATE TABLE patterns (
    id SERIAL PRIMARY KEY,
    nature TEXT,
    length INTEGER,
    root_text TEXT,
    pattern_base TEXT,
    pattern TEXT,
    pattern_wazan TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_patterns_root ON patterns(root_text);

COMMENT ON TABLE patterns IS 'الأنماط الصرفية - أنماط الصرف (27,228 نمط)';

-- الأفعال القرآنية (Quranic Verbs)
CREATE TABLE quranic_verbs (
    id SERIAL PRIMARY KEY,
    masdar TEXT,
    root TEXT,
    verb_type TEXT,
    verb_class TEXT,
    translation_en TEXT,
    translation_ar TEXT,
    past_form TEXT,
    present_form TEXT,
    imperative_form TEXT,
    subject TEXT,
    object TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_verbs_root ON quranic_verbs(root);
CREATE INDEX idx_verbs_masdar ON quranic_verbs(masdar);

COMMENT ON TABLE quranic_verbs IS 'الأفعال - الأفعال القرآنية (2,006 فعل)';

-- ═══════════════════════════════════════════════════════════════════════════
-- Quranic Features Tables (جداول الخصائص القرآنية)
-- ═══════════════════════════════════════════════════════════════════════════

-- القراءات (Qeraat)
CREATE TABLE qeraat (
    id SERIAL PRIMARY KEY,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    qeraa_text TEXT NOT NULL,
    note TEXT,
    source_id INTEGER REFERENCES sources(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_qeraat_word ON qeraat(word_id);

COMMENT ON TABLE qeraat IS 'القراءات - قراءات القرآن (77,432 قراءة)';

-- التجويد (Tajweed)
CREATE TABLE tajweed (
    id SERIAL PRIMARY KEY,
    ayah_id INTEGER NOT NULL REFERENCES ayahs(id) ON DELETE CASCADE,
    tajweed_text TEXT NOT NULL,
    source_id INTEGER REFERENCES sources(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tajweed_ayah ON tajweed(ayah_id);

COMMENT ON TABLE tajweed IS 'التجويد - أحكام التجويد (6,236 آية)';

-- الوقف (Waqf)
CREATE TABLE waqf (
    id SERIAL PRIMARY KEY,
    ayah_id INTEGER NOT NULL REFERENCES ayahs(id) ON DELETE CASCADE,
    position INTEGER,
    waqf_type TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_waqf_ayah ON waqf(ayah_id);

COMMENT ON TABLE waqf IS 'الوقف - مواضع الوقف (4,374 موضع)';

-- السجدات (Sajda)
CREATE TABLE sajda (
    id SERIAL PRIMARY KEY,
    ayah_id INTEGER UNIQUE NOT NULL REFERENCES ayahs(id) ON DELETE CASCADE,
    sajda_type TEXT NOT NULL CHECK (sajda_type IN ('recommended', 'obligatory', 'مستحبة', 'واجبة')),
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sajda_ayah ON sajda(ayah_id);

COMMENT ON TABLE sajda IS 'السجدات - سجدات التلاوة (15 سجدة)';

-- أسباب النزول (Nuzul)
CREATE TABLE nuzul (
    id SERIAL PRIMARY KEY,
    ayah_id INTEGER NOT NULL REFERENCES ayahs(id) ON DELETE CASCADE,
    nuzul_text TEXT NOT NULL,
    source_id INTEGER REFERENCES sources(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_nuzul_ayah ON nuzul(ayah_id);

COMMENT ON TABLE nuzul IS 'أسباب النزول - أسباب نزول الآيات (201 سبب)';

-- ═══════════════════════════════════════════════════════════════════════════
-- Topics & Categories (المواضيع والتصنيفات)
-- ═══════════════════════════════════════════════════════════════════════════

-- التصنيفات الموضوعية (Topic Categories)
CREATE TABLE topic_categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id INTEGER REFERENCES topic_categories(id),
    level INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_topic_categories_parent ON topic_categories(parent_id);

COMMENT ON TABLE topic_categories IS 'التصنيفات - التصنيف الموضوعي الهرمي (6,145 تصنيف)';

-- المواضيع (Topics)
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES topic_categories(id),
    name TEXT NOT NULL,
    description TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_topics_category ON topics(category_id);

COMMENT ON TABLE topics IS 'المواضيع - مواضيع القرآن';

-- ربط الآيات بالمواضيع (Ayah-Topic Link)
CREATE TABLE ayah_topics (
    id SERIAL PRIMARY KEY,
    ayah_id INTEGER NOT NULL REFERENCES ayahs(id) ON DELETE CASCADE,
    topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(ayah_id, topic_id)
);

CREATE INDEX idx_ayah_topics_ayah ON ayah_topics(ayah_id);
CREATE INDEX idx_ayah_topics_topic ON ayah_topics(topic_id);

COMMENT ON TABLE ayah_topics IS 'ربط الآيات بالمواضيع (46,404 علاقة)';

-- ═══════════════════════════════════════════════════════════════════════════
-- Statistics Tables (جداول الإحصائيات)
-- ═══════════════════════════════════════════════════════════════════════════

-- إحصائيات الكلمات (Word Statistics)
CREATE TABLE word_statistics (
    id SERIAL PRIMARY KEY,
    word_id INTEGER UNIQUE NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    occurrence_count INTEGER DEFAULT 0,
    surah_count INTEGER DEFAULT 0,
    ayah_count INTEGER DEFAULT 0,
    sequence_in_similar INTEGER,
    root_occurrence_count INTEGER,
    metadata JSONB DEFAULT '{}',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_word_statistics_word ON word_statistics(word_id);

COMMENT ON TABLE word_statistics IS 'إحصائيات الكلمات - إحصائيات تفصيلية لكل كلمة';

-- إحصائيات السور (Surah Statistics)
CREATE TABLE surah_statistics (
    id SERIAL PRIMARY KEY,
    surah_id INTEGER UNIQUE NOT NULL REFERENCES surahs(id) ON DELETE CASCADE,
    word_count INTEGER DEFAULT 0,
    char_count INTEGER DEFAULT 0,
    unique_words INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_surah_statistics_surah ON surah_statistics(surah_id);

COMMENT ON TABLE surah_statistics IS 'إحصائيات السور - إحصائيات تفصيلية لكل سورة';

-- ═══════════════════════════════════════════════════════════════════════════
-- Triggers (المحفزات التلقائية)
-- ═══════════════════════════════════════════════════════════════════════════

-- تحديث search_vector تلقائياً عند إضافة/تعديل آية
CREATE OR REPLACE FUNCTION update_ayah_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('arabic', COALESCE(NEW.text_uthmani, '')), 'A') ||
        setweight(to_tsvector('arabic', COALESCE(NEW.text_simple, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_ayah_search_vector
    BEFORE INSERT OR UPDATE ON ayahs
    FOR EACH ROW
    EXECUTE FUNCTION update_ayah_search_vector();

-- تحديث updated_at تلقائياً
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_surahs_updated_at
    BEFORE UPDATE ON surahs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ═══════════════════════════════════════════════════════════════════════════
-- Views (العروض المحسوبة)
-- ═══════════════════════════════════════════════════════════════════════════

-- عرض السور مع الإحصائيات
CREATE OR REPLACE VIEW v_surahs_with_stats AS
SELECT
    s.*,
    ss.word_count,
    ss.char_count,
    ss.unique_words,
    COUNT(DISTINCT a.id) as ayah_count_calc
FROM surahs s
LEFT JOIN surah_statistics ss ON ss.surah_id = s.id
LEFT JOIN ayahs a ON a.surah_id = s.id
GROUP BY s.id, ss.word_count, ss.char_count, ss.unique_words;

-- عرض الآيات الكاملة مع معلومات السورة
CREATE OR REPLACE VIEW v_ayahs_full AS
SELECT
    a.*,
    s.number as surah_number,
    s.name_arabic as surah_name_arabic,
    s.name_transliteration as surah_name_transliteration
FROM ayahs a
JOIN surahs s ON s.id = a.surah_id;

-- ═══════════════════════════════════════════════════════════════════════════
-- Initial Data (بيانات أولية)
-- ═══════════════════════════════════════════════════════════════════════════

-- إضافة بعض المصادر الأساسية
INSERT INTO sources (title, author, source_type, language, description) VALUES
('تفسير الطبري', 'محمد بن جرير الطبري', 'tafseer', 'ar', 'جامع البيان في تأويل القرآن'),
('تفسير ابن كثير', 'إسماعيل بن كثير', 'tafseer', 'ar', 'تفسير القرآن العظيم'),
('تفسير السعدي', 'عبد الرحمن السعدي', 'tafseer', 'ar', 'تيسير الكريم الرحمن'),
('التفسير الميسر', 'مجمع الملك فهد', 'tafseer', 'ar', 'التفسير الميسر'),
('تفسير الجلالين', 'جلال الدين المحلي والسيوطي', 'tafseer', 'ar', 'تفسير الجلالين'),
('Sahih International', 'Sahih International', 'translation', 'en', 'English Translation'),
('Pickthall', 'Mohammed Marmaduke Pickthall', 'translation', 'en', 'English Translation'),
('Yusuf Ali', 'Abdullah Yusuf Ali', 'translation', 'en', 'English Translation');

-- ═══════════════════════════════════════════════════════════════════════════
-- Performance Optimization (تحسين الأداء)
-- ═══════════════════════════════════════════════════════════════════════════

-- VACUUM و ANALYZE للأداء الأمثل
VACUUM ANALYZE;

-- عرض معلومات Schema
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- ═══════════════════════════════════════════════════════════════════════════
-- End of Schema
-- تم بحمد الله
-- ═══════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════
-- 📖 المستوى 0: النواة الصلبة (Core Tables)
-- ═══════════════════════════════════════════════════════════════
-- الجداول: surahs, ayahs, words
-- ═══════════════════════════════════════════════════════════════

\c quran_hierarchical_db
SET search_path TO quran, public;

BEGIN;

-- ═══════════════════════════════════════════════════════════════
-- جدول 1: surahs (السور) - 114 سجل
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS quran.surahs (
    -- المعرفات
    sur_id SMALLINT PRIMARY KEY CHECK (sur_id BETWEEN 1 AND 114),
    sur_uuid UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,

    -- الأسماء
    sur_name_ar VARCHAR(50) NOT NULL,
    sur_name_ar_trans VARCHAR(50),
    sur_name_en VARCHAR(50),
    sur_name_alt JSONB DEFAULT '[]'::jsonb,

    -- الإحصائيات الأساسية
    sur_ayah_count SMALLINT NOT NULL CHECK (sur_ayah_count > 0),
    sur_word_count INTEGER CHECK (sur_word_count >= 0),
    sur_letter_count INTEGER CHECK (sur_letter_count >= 0),

    -- معلومات النزول
    sur_revelation_type quran.revelation_type NOT NULL,
    sur_revelation_order SMALLINT CHECK (sur_revelation_order BETWEEN 1 AND 114),
    sur_revelation_place VARCHAR(100),

    -- الموقع في المصحف
    sur_juz_start SMALLINT CHECK (sur_juz_start BETWEEN 1 AND 30),
    sur_juz_end SMALLINT CHECK (sur_juz_end BETWEEN 1 AND 30),
    sur_page_start SMALLINT CHECK (sur_page_start BETWEEN 1 AND 604),
    sur_page_end SMALLINT CHECK (sur_page_end BETWEEN 1 AND 604),

    -- معلومات خاصة
    sur_has_bismillah BOOLEAN DEFAULT TRUE,
    sur_has_sajda BOOLEAN DEFAULT FALSE,
    sur_sajda_type quran.sajda_type,
    sur_sajda_ayah SMALLINT,

    -- الموضوعات والكلمات المفتاحية
    sur_main_themes JSONB DEFAULT '[]'::jsonb,
    sur_main_topics TEXT[] DEFAULT ARRAY[]::TEXT[],
    sur_keywords TEXT[] DEFAULT ARRAY[]::TEXT[],

    -- إحصائيات متقدمة
    sur_stats JSONB DEFAULT '{}'::jsonb,

    -- حقول إضافية
    sur_purpose TEXT,
    sur_audio_intro_url TEXT,
    sur_metadata JSONB DEFAULT '{}'::jsonb,

    -- الختم الزمني
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- قيود إضافية
    CONSTRAINT sur_juz_order CHECK (sur_juz_start <= sur_juz_end),
    CONSTRAINT sur_page_order CHECK (sur_page_start <= sur_page_end),
    CONSTRAINT sur_sajda_check CHECK (
        (sur_has_sajda = FALSE AND sur_sajda_type IS NULL AND sur_sajda_ayah IS NULL) OR
        (sur_has_sajda = TRUE AND sur_sajda_type IS NOT NULL AND sur_sajda_ayah IS NOT NULL)
    )
);

-- تعليقات على الجدول والأعمدة
COMMENT ON TABLE quran.surahs IS
'جدول السور القرآنية - 114 سورة';

COMMENT ON COLUMN quran.surahs.sur_id IS
'رقم السورة في المصحف (1-114)';

COMMENT ON COLUMN quran.surahs.sur_name_alt IS
'أسماء بديلة توقيفية للسورة بصيغة JSONB ["الاسم1", "الاسم2"]';

COMMENT ON COLUMN quran.surahs.sur_main_themes IS
'الموضوعات الرئيسية بصيغة JSONB للبحث المرن';

COMMENT ON COLUMN quran.surahs.sur_stats IS
'إحصائيات متقدمة: {"unique_roots": 100, "verse_lengths": {...}}';

-- الفهارس
CREATE UNIQUE INDEX idx_surahs_uuid ON quran.surahs(sur_uuid);
CREATE INDEX idx_surahs_revelation_type ON quran.surahs(sur_revelation_type);
CREATE INDEX idx_surahs_revelation_order ON quran.surahs(sur_revelation_order);
CREATE INDEX idx_surahs_topics ON quran.surahs USING GIN(sur_main_topics);
CREATE INDEX idx_surahs_keywords ON quran.surahs USING GIN(sur_keywords);
CREATE INDEX idx_surahs_themes ON quran.surahs USING GIN(sur_main_themes);

-- Trigger لتحديث updated_at تلقائياً
CREATE TRIGGER trg_surahs_updated_at
    BEFORE UPDATE ON quran.surahs
    FOR EACH ROW
    EXECUTE FUNCTION quran.update_updated_at_column();

-- ═══════════════════════════════════════════════════════════════
-- جدول 2: ayahs (الآيات) - 6,236 سجل
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS quran.ayahs (
    -- المعرفات
    aya_id SERIAL PRIMARY KEY,
    aya_uuid UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,
    aya_global_id INTEGER NOT NULL UNIQUE CHECK (aya_global_id BETWEEN 1 AND 6236),

    -- الربط مع السورة
    aya_sur_id SMALLINT NOT NULL,
    aya_number SMALLINT NOT NULL CHECK (aya_number > 0),

    -- نصوص الآية (رسومات مختلفة)
    aya_text_uthmani TEXT NOT NULL,
    aya_text_simple TEXT NOT NULL,
    aya_text_imlaai TEXT,
    aya_text_search TSVECTOR, -- للبحث النصي الكامل

    -- الموقع في المصحف
    aya_juz SMALLINT CHECK (aya_juz BETWEEN 1 AND 30),
    aya_hizb SMALLINT CHECK (aya_hizb BETWEEN 1 AND 60),
    aya_quarter SMALLINT CHECK (aya_quarter BETWEEN 1 AND 240),
    aya_page SMALLINT CHECK (aya_page BETWEEN 1 AND 604),
    aya_manzil SMALLINT CHECK (aya_manzil BETWEEN 1 AND 7),
    aya_ruku SMALLINT,

    -- معلومات خاصة
    aya_has_sajda BOOLEAN DEFAULT FALSE,
    aya_sajda_type quran.sajda_type,
    aya_has_bismillah BOOLEAN DEFAULT FALSE,
    aya_is_first BOOLEAN DEFAULT FALSE,
    aya_is_last BOOLEAN DEFAULT FALSE,

    -- الإحصائيات
    aya_word_count SMALLINT,
    aya_letter_count SMALLINT,
    aya_unique_words SMALLINT,

    -- التحليل اللغوي
    aya_roots TEXT[] DEFAULT ARRAY[]::TEXT[],
    aya_patterns TEXT[] DEFAULT ARRAY[]::TEXT[],
    aya_pos_summary JSONB DEFAULT '{}'::jsonb, -- {"noun": 5, "verb": 3, ...}

    -- سياق النزول
    aya_revelation_context_id INTEGER,
    aya_revelation_order INTEGER,

    -- الموضوعات
    aya_topics TEXT[] DEFAULT ARRAY[]::TEXT[],
    aya_primary_topic_id INTEGER,
    aya_keywords TEXT[] DEFAULT ARRAY[]::TEXT[],

    -- تحليلات متقدمة
    aya_analysis JSONB DEFAULT '{}'::jsonb,
    aya_is_mutashabih BOOLEAN DEFAULT FALSE,

    -- Vector Embeddings للبحث الدلالي
    aya_embedding_v1 vector(768), -- نموذج كبير
    aya_embedding_v2 vector(384), -- نموذج صغير

    -- بيانات وصفية
    aya_metadata JSONB DEFAULT '{}'::jsonb,

    -- الختم الزمني
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- القيود
    CONSTRAINT aya_unique_per_surah UNIQUE (aya_sur_id, aya_number),
    CONSTRAINT aya_sajda_check CHECK (
        (aya_has_sajda = FALSE AND aya_sajda_type IS NULL) OR
        (aya_has_sajda = TRUE AND aya_sajda_type IS NOT NULL)
    )
);

-- تعليقات
COMMENT ON TABLE quran.ayahs IS
'جدول الآيات القرآنية - 6,236 آية';

COMMENT ON COLUMN quran.ayahs.aya_global_id IS
'الرقم العالمي الفريد للآية من 1 إلى 6236';

COMMENT ON COLUMN quran.ayahs.aya_text_search IS
'حقل مُفهرس للبحث النصي الكامل (يُحدّث تلقائياً)';

COMMENT ON COLUMN quran.ayahs.aya_pos_summary IS
'ملخص أنواع الكلمات: {"noun": 5, "verb": 3, "particle": 1}';

COMMENT ON COLUMN quran.ayahs.aya_embedding_v1 IS
'متجه نصي 768 بُعد (مثل: sentence-transformers/paraphrase-multilingual-mpnet-base-v2)';

COMMENT ON COLUMN quran.ayahs.aya_embedding_v2 IS
'متجه نصي 384 بُعد للبحث الأسرع (مثل: all-MiniLM-L6-v2)';

-- الفهارس
CREATE UNIQUE INDEX idx_ayahs_uuid ON quran.ayahs(aya_uuid);
CREATE UNIQUE INDEX idx_ayahs_global_id ON quran.ayahs(aya_global_id);
CREATE INDEX idx_ayahs_surah ON quran.ayahs(aya_sur_id, aya_number);
CREATE INDEX idx_ayahs_juz ON quran.ayahs(aya_juz);
CREATE INDEX idx_ayahs_page ON quran.ayahs(aya_page);
CREATE INDEX idx_ayahs_hizb ON quran.ayahs(aya_hizb);
CREATE INDEX idx_ayahs_topics ON quran.ayahs USING GIN(aya_topics);
CREATE INDEX idx_ayahs_roots ON quran.ayahs USING GIN(aya_roots);
CREATE INDEX idx_ayahs_patterns ON quran.ayahs USING GIN(aya_patterns);
CREATE INDEX idx_ayahs_keywords ON quran.ayahs USING GIN(aya_keywords);

-- فهرس البحث النصي الكامل
CREATE INDEX idx_ayahs_text_search ON quran.ayahs USING GIN(aya_text_search);

-- فهرس البحث الدلالي (Vector Similarity)
CREATE INDEX idx_ayahs_embedding_v1 ON quran.ayahs USING ivfflat (aya_embedding_v1 vector_cosine_ops);
CREATE INDEX idx_ayahs_embedding_v2 ON quran.ayahs USING ivfflat (aya_embedding_v2 vector_cosine_ops);

-- Trigger لتحديث aya_text_search تلقائياً
CREATE OR REPLACE FUNCTION quran.ayahs_update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.aya_text_search := to_tsvector('quran.arabic_quran', NEW.aya_text_simple);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_ayahs_update_search
    BEFORE INSERT OR UPDATE OF aya_text_simple ON quran.ayahs
    FOR EACH ROW
    EXECUTE FUNCTION quran.ayahs_update_search_vector();

-- Trigger لتحديث updated_at
CREATE TRIGGER trg_ayahs_updated_at
    BEFORE UPDATE ON quran.ayahs
    FOR EACH ROW
    EXECUTE FUNCTION quran.update_updated_at_column();

-- ═══════════════════════════════════════════════════════════════
-- جدول 3: words (الكلمات) - 77,430+ سجل
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS quran.words (
    -- المعرفات
    wrd_id SERIAL PRIMARY KEY,
    wrd_uuid UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,
    wrd_global_id INTEGER NOT NULL UNIQUE CHECK (wrd_global_id > 0),

    -- الربط مع الآية
    wrd_aya_id INTEGER NOT NULL,
    wrd_position SMALLINT NOT NULL CHECK (wrd_position > 0),

    -- نصوص الكلمة
    wrd_text_uthmani VARCHAR(100) NOT NULL,
    wrd_text_simple VARCHAR(100) NOT NULL,
    wrd_text_clean VARCHAR(100),
    wrd_text_buckwalter VARCHAR(100),

    -- الحروف والتشكيل
    wrd_letters CHAR[] DEFAULT ARRAY[]::CHAR[],
    wrd_diacritics VARCHAR(50),
    wrd_has_shadda BOOLEAN DEFAULT FALSE,
    wrd_has_hamza BOOLEAN DEFAULT FALSE,

    -- التحليل الصرفي
    wrd_root VARCHAR(20),
    wrd_root_type quran.root_type,
    wrd_pattern VARCHAR(30),
    wrd_pattern_buckwalter VARCHAR(30),

    -- نوع الكلمة (Part of Speech)
    wrd_pos quran.word_pos,
    wrd_pos_detailed VARCHAR(50),

    -- الخصائص النحوية
    wrd_gender quran.gender_type,
    wrd_number quran.number_type,
    wrd_person SMALLINT CHECK (wrd_person BETWEEN 1 AND 3), -- 1=متكلم, 2=مخاطب, 3=غائب
    wrd_case quran.case_type,
    wrd_tense quran.tense_type,
    wrd_mood VARCHAR(20), -- مرفوع، منصوب، مجزوم
    wrd_voice quran.voice_type,

    -- المعنى
    wrd_lemma VARCHAR(50), -- الصيغة الأصلية
    wrd_gloss_ar VARCHAR(200), -- المعنى بالعربية
    wrd_gloss_en VARCHAR(200), -- المعنى بالإنجليزية
    wrd_semantic_class VARCHAR(50), -- الفئة الدلالية

    -- تحليل CAMeL Tools
    wrd_camel_analysis JSONB DEFAULT '{}'::jsonb,
    wrd_morphological_features JSONB DEFAULT '{}'::jsonb,

    -- البنية الصرفية
    wrd_stem VARCHAR(50), -- جذع الكلمة
    wrd_prefix VARCHAR(20), -- السوابق (و، ف، ب، ال...)
    wrd_suffix VARCHAR(20), -- اللواحق (ضمائر، علامات...)
    wrd_length SMALLINT,

    -- الإحصائيات
    wrd_frequency_surah SMALLINT DEFAULT 1,
    wrd_frequency_quran INTEGER DEFAULT 1,

    -- التحليل الصوتي
    wrd_phonetic VARCHAR(100),
    wrd_syllables TEXT[] DEFAULT ARRAY[]::TEXT[],

    -- Vector Embedding
    wrd_embedding vector(512),

    -- المصدر
    wrd_source_corpus VARCHAR(50) DEFAULT 'QAC', -- QAC, CAMeL, manual

    -- بيانات وصفية
    wrd_metadata JSONB DEFAULT '{}'::jsonb,

    -- الختم الزمني
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- القيود
    CONSTRAINT wrd_unique_per_ayah UNIQUE (wrd_aya_id, wrd_position)
);

-- تعليقات
COMMENT ON TABLE quran.words IS
'جدول الكلمات القرآنية مع التحليل الصرفي والنحوي الكامل - 77,430+ كلمة';

COMMENT ON COLUMN quran.words.wrd_global_id IS
'الرقم العالمي الفريد للكلمة في تسلسل المصحف (1-77430)';

COMMENT ON COLUMN quran.words.wrd_camel_analysis IS
'نتائج التحليل التفصيلي من مكتبة CAMeL Tools';

COMMENT ON COLUMN quran.words.wrd_lemma IS
'الصيغة الأصلية للكلمة (المصدر أو الفعل المجرد)';

-- الفهارس
CREATE UNIQUE INDEX idx_words_uuid ON quran.words(wrd_uuid);
CREATE UNIQUE INDEX idx_words_global_id ON quran.words(wrd_global_id);
CREATE INDEX idx_words_ayah ON quran.words(wrd_aya_id, wrd_position);
CREATE INDEX idx_words_root ON quran.words(wrd_root);
CREATE INDEX idx_words_pattern ON quran.words(wrd_pattern);
CREATE INDEX idx_words_pos ON quran.words(wrd_pos);
CREATE INDEX idx_words_lemma ON quran.words(wrd_lemma);
CREATE INDEX idx_words_text_simple ON quran.words(wrd_text_simple);

-- فهرس البحث الصوتي (Trigram للبحث الضبابي)
CREATE INDEX idx_words_text_trgm ON quran.words USING GIN(wrd_text_simple gin_trgm_ops);

-- فهرس Vector Embedding
CREATE INDEX idx_words_embedding ON quran.words USING ivfflat (wrd_embedding vector_cosine_ops);

-- Trigger لحساب wrd_length تلقائياً
CREATE OR REPLACE FUNCTION quran.words_calculate_length()
RETURNS TRIGGER AS $$
BEGIN
    NEW.wrd_length := length(quran.remove_tashkeel(NEW.wrd_text_simple));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_words_calculate_length
    BEFORE INSERT OR UPDATE OF wrd_text_simple ON quran.words
    FOR EACH ROW
    EXECUTE FUNCTION quran.words_calculate_length();

-- Trigger لتحديث updated_at
CREATE TRIGGER trg_words_updated_at
    BEFORE UPDATE ON quran.words
    FOR EACH ROW
    EXECUTE FUNCTION quran.update_updated_at_column();

-- ═══════════════════════════════════════════════════════════════
-- إضافة Foreign Keys
-- ═══════════════════════════════════════════════════════════════

-- ayahs → surahs
ALTER TABLE quran.ayahs
    ADD CONSTRAINT fk_ayahs_surah
    FOREIGN KEY (aya_sur_id)
    REFERENCES quran.surahs(sur_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

-- words → ayahs
ALTER TABLE quran.words
    ADD CONSTRAINT fk_words_ayah
    FOREIGN KEY (wrd_aya_id)
    REFERENCES quran.ayahs(aya_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

-- ═══════════════════════════════════════════════════════════════
COMMIT;

-- ═══════════════════════════════════════════════════════════════
-- ✅ تم إنشاء جداول المستوى 0 بنجاح!
-- ═══════════════════════════════════════════════════════════════
-- الخطوة التالية: تشغيل 03_level1_morphology.sql
-- ═══════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════
-- 📚 المستويات 1-5: الجداول المتبقية
-- ═══════════════════════════════════════════════════════════════

\c quran_hierarchical_db
SET search_path TO quran, public;

BEGIN;

-- ═══════════════════════════════════════════════════════════════
-- المستوى 1: التحليل الصرفي
-- ═══════════════════════════════════════════════════════════════

-- جدول 4: roots (الجذور)
CREATE TABLE IF NOT EXISTS quran.roots (
    root_id SERIAL PRIMARY KEY,
    root_uuid UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,
    root_text VARCHAR(20) NOT NULL UNIQUE,
    root_text_clean VARCHAR(20) NOT NULL,
    root_letters CHAR[] DEFAULT ARRAY[]::CHAR[],
    root_type quran.root_type NOT NULL,
    root_meaning_ar TEXT,
    root_meaning_en TEXT,
    root_semantic_field VARCHAR(100),
    root_word_count INTEGER DEFAULT 0,
    root_ayah_count INTEGER DEFAULT 0,
    root_frequency INTEGER DEFAULT 0,
    root_derivatives JSONB DEFAULT '[]'::jsonb,
    root_patterns TEXT[] DEFAULT ARRAY[]::TEXT[],
    root_synonyms TEXT[] DEFAULT ARRAY[]::TEXT[],
    root_antonyms TEXT[] DEFAULT ARRAY[]::TEXT[],
    root_related TEXT[] DEFAULT ARRAY[]::TEXT[],
    root_semantic_analysis JSONB DEFAULT '{}'::jsonb,
    root_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_roots_text ON quran.roots(root_text);
CREATE INDEX idx_roots_type ON quran.roots(root_type);
CREATE INDEX idx_roots_semantic_field ON quran.roots(root_semantic_field);
CREATE INDEX idx_roots_patterns ON quran.roots USING GIN(root_patterns);

COMMENT ON TABLE quran.roots IS 'جدول الجذور اللغوية الفريدة في القرآن (~2000 جذر)';

-- جدول 5: patterns (الأوزان الصرفية)
CREATE TABLE IF NOT EXISTS quran.patterns (
    pat_id SERIAL PRIMARY KEY,
    pat_uuid UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,
    pat_text VARCHAR(30) NOT NULL UNIQUE,
    pat_text_buckwalter VARCHAR(30),
    pat_template VARCHAR(30),
    pat_type VARCHAR(30),
    pat_form SMALLINT CHECK (pat_form BETWEEN 1 AND 15),
    pat_meaning_ar VARCHAR(200),
    pat_meaning_en VARCHAR(200),
    pat_semantic_function VARCHAR(100),
    pat_word_count INTEGER DEFAULT 0,
    pat_frequency INTEGER DEFAULT 0,
    pat_examples JSONB DEFAULT '[]'::jsonb,
    pat_related_patterns TEXT[] DEFAULT ARRAY[]::TEXT[],
    pat_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patterns_text ON quran.patterns(pat_text);
CREATE INDEX idx_patterns_type ON quran.patterns(pat_type);
CREATE INDEX idx_patterns_form ON quran.patterns(pat_form) WHERE pat_form IS NOT NULL;

COMMENT ON TABLE quran.patterns IS 'جدول الأوزان الصرفية الفريدة (~300 وزن)';

-- ═══════════════════════════════════════════════════════════════
-- المستوى 2: المحتوى الإثرائي
-- ═══════════════════════════════════════════════════════════════

-- جدول 6: mufassireen (المفسرون)
CREATE TABLE IF NOT EXISTS quran.mufassireen (
    muf_id SERIAL PRIMARY KEY,
    muf_uuid UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,
    muf_name_ar VARCHAR(100) NOT NULL,
    muf_name_en VARCHAR(100),
    muf_full_name VARCHAR(200),
    muf_kunya VARCHAR(50),
    muf_laqab VARCHAR(50),
    muf_birth_year SMALLINT,
    muf_death_year SMALLINT,
    muf_birth_place VARCHAR(100),
    muf_death_place VARCHAR(100),
    muf_era VARCHAR(50),
    muf_school VARCHAR(50),
    muf_methodology VARCHAR(100),
    muf_tafsir_name VARCHAR(200),
    muf_tafsir_volumes SMALLINT,
    muf_other_works JSONB DEFAULT '[]'::jsonb,
    muf_specialization TEXT[] DEFAULT ARRAY[]::TEXT[],
    muf_influence_score SMALLINT CHECK (muf_influence_score BETWEEN 1 AND 10),
    muf_biography_ar TEXT,
    muf_biography_en TEXT,
    muf_references JSONB DEFAULT '[]'::jsonb,
    muf_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_mufassireen_name_ar ON quran.mufassireen(muf_name_ar);
CREATE INDEX idx_mufassireen_era ON quran.mufassireen(muf_era);

COMMENT ON TABLE quran.mufassireen IS 'جدول المفسرين وأصحاب كتب التفسير (~50 مفسر)';

-- جدول 7: tafsir (التفاسير)
CREATE TABLE IF NOT EXISTS quran.tafsir (
    taf_id BIGSERIAL PRIMARY KEY,
    taf_uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    taf_aya_id INTEGER NOT NULL,
    taf_mufassir_id INTEGER NOT NULL,
    taf_text TEXT NOT NULL,
    taf_summary TEXT,
    taf_language CHAR(2) DEFAULT 'ar',
    taf_type quran.tafsir_type,
    taf_methodology VARCHAR(50),
    taf_references JSONB DEFAULT '[]'::jsonb,
    taf_ayah_refs INTEGER[] DEFAULT ARRAY[]::INTEGER[],
    taf_hadith_refs JSONB DEFAULT '[]'::jsonb,
    taf_topics TEXT[] DEFAULT ARRAY[]::TEXT[],
    taf_keywords TEXT[] DEFAULT ARRAY[]::TEXT[],
    taf_quality_score SMALLINT CHECK (taf_quality_score BETWEEN 1 AND 10),
    taf_verified BOOLEAN DEFAULT FALSE,
    taf_verified_by INTEGER,
    taf_verified_at TIMESTAMP WITH TIME ZONE,
    taf_embedding vector(768),
    taf_search_vector TSVECTOR,
    taf_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT taf_unique_per_ayah_mufassir UNIQUE (taf_aya_id, taf_mufassir_id)
);

CREATE INDEX idx_tafsir_ayah ON quran.tafsir(taf_aya_id);
CREATE INDEX idx_tafsir_mufassir ON quran.tafsir(taf_mufassir_id);
CREATE INDEX idx_tafsir_type ON quran.tafsir(taf_type);
CREATE INDEX idx_tafsir_search ON quran.tafsir USING GIN(taf_search_vector);
CREATE INDEX idx_tafsir_topics ON quran.tafsir USING GIN(taf_topics);
CREATE INDEX idx_tafsir_embedding ON quran.tafsir USING ivfflat (taf_embedding vector_cosine_ops);

COMMENT ON TABLE quran.tafsir IS 'جدول التفاسير لكل آية (~60,000+ سجل)';

-- جدول 8: translators (المترجمون)
CREATE TABLE IF NOT EXISTS quran.translators (
    trt_id SERIAL PRIMARY KEY,
    trt_name_en VARCHAR(100) NOT NULL,
    trt_name_ar VARCHAR(100),
    trt_language CHAR(2) NOT NULL,
    trt_biography TEXT,
    trt_style VARCHAR(50),
    trt_source TEXT,
    trt_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE quran.translators IS 'جدول المترجمين وجهات الترجمة';

-- جدول 9: translations (الترجمات)
CREATE TABLE IF NOT EXISTS quran.translations (
    trl_id BIGSERIAL PRIMARY KEY,
    trl_uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    trl_aya_id INTEGER NOT NULL,
    trl_translator_id INTEGER NOT NULL,
    trl_text TEXT NOT NULL,
    trl_language CHAR(2) NOT NULL,
    trl_script VARCHAR(20) DEFAULT 'Latin',
    trl_type quran.translation_type,
    trl_style VARCHAR(50),
    trl_quality_score SMALLINT CHECK (trl_quality_score BETWEEN 1 AND 10),
    trl_verified BOOLEAN DEFAULT FALSE,
    trl_popular_rank SMALLINT,
    trl_search_vector TSVECTOR,
    trl_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT trl_unique_per_ayah_translator UNIQUE (trl_aya_id, trl_translator_id)
);

CREATE INDEX idx_translations_ayah ON quran.translations(trl_aya_id);
CREATE INDEX idx_translations_translator ON quran.translations(trl_translator_id);
CREATE INDEX idx_translations_language ON quran.translations(trl_language);
CREATE INDEX idx_translations_search ON quran.translations USING GIN(trl_search_vector);

COMMENT ON TABLE quran.translations IS 'جدول ترجمات معاني القرآن (~300,000+ سجل)';

-- ═══════════════════════════════════════════════════════════════
-- المستوى 3: السياق والعلوم القرآنية
-- ═══════════════════════════════════════════════════════════════

-- جدول 10: revelation_contexts (أسباب النزول)
CREATE TABLE IF NOT EXISTS quran.revelation_contexts (
    ctx_id SERIAL PRIMARY KEY,
    ctx_uuid UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,
    ctx_aya_id_start INTEGER NOT NULL,
    ctx_aya_id_end INTEGER,
    ctx_reason_ar TEXT NOT NULL,
    ctx_reason_en TEXT,
    ctx_summary TEXT,
    ctx_date_hijri VARCHAR(50),
    ctx_location VARCHAR(100),
    ctx_event TEXT,
    ctx_people_involved TEXT[] DEFAULT ARRAY[]::TEXT[],
    ctx_sources JSONB DEFAULT '[]'::jsonb,
    ctx_authenticity quran.authenticity_level DEFAULT 'unknown',
    ctx_related_events INTEGER[] DEFAULT ARRAY[]::INTEGER[],
    ctx_related_ayahs INTEGER[] DEFAULT ARRAY[]::INTEGER[],
    ctx_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ctx_ayah_order CHECK (ctx_aya_id_start <= COALESCE(ctx_aya_id_end, ctx_aya_id_start))
);

CREATE INDEX idx_contexts_ayah_start ON quran.revelation_contexts(ctx_aya_id_start);
CREATE INDEX idx_contexts_location ON quran.revelation_contexts(ctx_location);
CREATE INDEX idx_contexts_authenticity ON quran.revelation_contexts(ctx_authenticity);

COMMENT ON TABLE quran.revelation_contexts IS 'جدول أسباب النزول والسياقات التاريخية (~500 سبب)';

-- جدول 11: topics (الموضوعات - شجري)
CREATE TABLE IF NOT EXISTS quran.topics (
    top_id SERIAL PRIMARY KEY,
    top_uuid UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,
    top_name_ar VARCHAR(200) NOT NULL,
    top_name_en VARCHAR(200),
    top_description_ar TEXT,
    top_description_en TEXT,
    top_parent_id INTEGER, -- Self-referencing
    top_level SMALLINT DEFAULT 0,
    top_path TEXT,
    top_category VARCHAR(100),
    top_subcategory VARCHAR(100),
    top_ayah_count INTEGER DEFAULT 0,
    top_importance_score SMALLINT CHECK (top_importance_score BETWEEN 1 AND 10),
    top_related_topics INTEGER[] DEFAULT ARRAY[]::INTEGER[],
    top_keywords TEXT[] DEFAULT ARRAY[]::TEXT[],
    top_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_topics_parent ON quran.topics(top_parent_id);
CREATE INDEX idx_topics_path ON quran.topics(top_path);
CREATE INDEX idx_topics_category ON quran.topics(top_category);

COMMENT ON TABLE quran.topics IS 'جدول الموضوعات القرآنية الهرمية (~1000+ موضوع)';

-- جدول 12: ayah_topics (جدول وسيط M:N)
CREATE TABLE IF NOT EXISTS quran.ayah_topics (
    ayt_aya_id INTEGER NOT NULL,
    ayt_top_id INTEGER NOT NULL,
    ayt_relevance_score NUMERIC(3,2) CHECK (ayt_relevance_score BETWEEN 0 AND 1) DEFAULT 1.0,
    ayt_is_primary BOOLEAN DEFAULT FALSE,
    ayt_notes TEXT,
    ayt_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ayt_aya_id, ayt_top_id)
);

CREATE INDEX idx_ayah_topics_ayah ON quran.ayah_topics(ayt_aya_id);
CREATE INDEX idx_ayah_topics_topic ON quran.ayah_topics(ayt_top_id);
CREATE INDEX idx_ayah_topics_primary ON quran.ayah_topics(ayt_is_primary) WHERE ayt_is_primary = TRUE;

COMMENT ON TABLE quran.ayah_topics IS 'جدول العلاقة بين الآيات والموضوعات (N:M)';

-- جدول 13: sources (المصادر والمراجع)
CREATE TABLE IF NOT EXISTS quran.sources (
    src_id SERIAL PRIMARY KEY,
    src_title_ar VARCHAR(200),
    src_title_en VARCHAR(200),
    src_author_name VARCHAR(100),
    src_type VARCHAR(50),
    src_publication_year SMALLINT,
    src_url TEXT,
    src_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE quran.sources IS 'جدول المصادر والمراجع الموحد';

-- جدول 14: qiraat (القراءات)
CREATE TABLE IF NOT EXISTS quran.qiraat (
    qiraa_id SERIAL PRIMARY KEY,
    qiraa_wrd_id INTEGER NOT NULL,
    qiraa_sur_id SMALLINT,
    qiraa_aya_id INTEGER,
    qiraa_type VARCHAR(20), -- أصول، فرش
    qiraa_readers TEXT[] DEFAULT ARRAY[]::TEXT[],
    qiraa_text_uthmani VARCHAR(100),
    qiraa_description TEXT,
    qiraa_source_id INTEGER,
    qiraa_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_qiraat_word ON quran.qiraat(qiraa_wrd_id);
CREATE INDEX idx_qiraat_surah ON quran.qiraat(qiraa_sur_id);

COMMENT ON TABLE quran.qiraat IS 'جدول القراءات والفروقات (~5000+ فرشة)';

-- ═══════════════════════════════════════════════════════════════
-- المستوى 4: الوسائط المتعددة
-- ═══════════════════════════════════════════════════════════════

-- جدول 15: reciters (القراء)
CREATE TABLE IF NOT EXISTS quran.reciters (
    rct_id SERIAL PRIMARY KEY,
    rct_name_ar VARCHAR(100) NOT NULL,
    rct_name_en VARCHAR(100),
    rct_biography TEXT,
    rct_riwayah_default VARCHAR(50) DEFAULT 'حفص عن عاصم',
    rct_style_default quran.recitation_style DEFAULT 'murattal',
    rct_avatar_url TEXT,
    rct_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE quran.reciters IS 'جدول القراء المشهورين (~100 قارئ)';

-- جدول 16: recitations (التلاوات)
CREATE TABLE IF NOT EXISTS quran.recitations (
    rec_id BIGSERIAL PRIMARY KEY,
    rec_uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    rec_aya_id INTEGER NOT NULL,
    rec_reciter_id INTEGER NOT NULL,
    rec_file_url TEXT NOT NULL,
    rec_file_format VARCHAR(10) DEFAULT 'mp3',
    rec_file_size BIGINT,
    rec_duration NUMERIC(7,2),
    rec_bitrate VARCHAR(20),
    rec_riwayah VARCHAR(50),
    rec_style quran.recitation_style,
    rec_quality_score SMALLINT CHECK (rec_quality_score BETWEEN 1 AND 10),
    rec_verified BOOLEAN DEFAULT FALSE,
    rec_play_count BIGINT DEFAULT 0,
    rec_download_count BIGINT DEFAULT 0,
    rec_rating NUMERIC(2,1) CHECK (rec_rating BETWEEN 1 AND 5),
    rec_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT rec_unique_per_ayah_reciter UNIQUE (rec_aya_id, rec_reciter_id)
);

CREATE INDEX idx_recitations_ayah ON quran.recitations(rec_aya_id);
CREATE INDEX idx_recitations_reciter ON quran.recitations(rec_reciter_id);
CREATE INDEX idx_recitations_riwayah ON quran.recitations(rec_riwayah);

COMMENT ON TABLE quran.recitations IS 'جدول التلاوات الصوتية (~300,000+ ملف)';

-- ═══════════════════════════════════════════════════════════════
-- المستوى 5: المستخدمون والتفاعل
-- ═══════════════════════════════════════════════════════════════

-- جدول 17: users (المستخدمون)
CREATE TABLE IF NOT EXISTS community.users (
    usr_id SERIAL PRIMARY KEY,
    usr_uuid UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,
    usr_username VARCHAR(50) NOT NULL UNIQUE,
    usr_email VARCHAR(100) NOT NULL UNIQUE,
    usr_password_hash VARCHAR(255) NOT NULL,
    usr_full_name VARCHAR(100),
    usr_display_name VARCHAR(50),
    usr_avatar_url TEXT,
    usr_bio TEXT,
    usr_language CHAR(2) DEFAULT 'ar',
    usr_preferred_translation INTEGER,
    usr_preferred_reciter INTEGER,
    usr_theme VARCHAR(20) DEFAULT 'light',
    usr_last_read_aya INTEGER,
    usr_total_read_time INTEGER DEFAULT 0,
    usr_streak_days SMALLINT DEFAULT 0,
    usr_contribution_count INTEGER DEFAULT 0,
    usr_contribution_points INTEGER DEFAULT 0,
    usr_level SMALLINT DEFAULT 1,
    usr_badges JSONB DEFAULT '[]'::jsonb,
    usr_role community.user_role DEFAULT 'user',
    usr_is_active BOOLEAN DEFAULT TRUE,
    usr_is_verified BOOLEAN DEFAULT FALSE,
    usr_is_contributor BOOLEAN DEFAULT FALSE,
    usr_is_admin BOOLEAN DEFAULT FALSE,
    usr_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_username ON community.users(usr_username);
CREATE INDEX idx_users_email ON community.users(usr_email);
CREATE INDEX idx_users_role ON community.users(usr_role);

COMMENT ON TABLE community.users IS 'جدول المستخدمين المسجلين';

-- جدول 18: bookmarks (العلامات المرجعية)
CREATE TABLE IF NOT EXISTS community.bookmarks (
    bmk_id SERIAL PRIMARY KEY,
    bmk_uuid UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,
    bmk_usr_id INTEGER NOT NULL,
    bmk_aya_id INTEGER NOT NULL,
    bmk_title VARCHAR(100),
    bmk_notes TEXT,
    bmk_color VARCHAR(20),
    bmk_tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    bmk_category VARCHAR(50),
    bmk_position SMALLINT,
    bmk_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT bmk_unique_per_user_ayah UNIQUE (bmk_usr_id, bmk_aya_id)
);

CREATE INDEX idx_bookmarks_user ON community.bookmarks(bmk_usr_id);
CREATE INDEX idx_bookmarks_ayah ON community.bookmarks(bmk_aya_id);

COMMENT ON TABLE community.bookmarks IS 'جدول العلامات المرجعية للمستخدمين';

-- جدول 19: annotations (الشروح المجتمعية)
CREATE TABLE IF NOT EXISTS community.annotations (
    note_id SERIAL PRIMARY KEY,
    note_usr_id INTEGER NOT NULL,
    note_type VARCHAR(50) NOT NULL,
    note_scope VARCHAR(20) NOT NULL,
    note_scope_id INTEGER NOT NULL,
    note_text TEXT NOT NULL,
    note_status community.contribution_status DEFAULT 'pending',
    note_is_public BOOLEAN DEFAULT FALSE,
    note_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_annotations_user ON community.annotations(note_usr_id);
CREATE INDEX idx_annotations_scope ON community.annotations(note_scope, note_scope_id);
CREATE INDEX idx_annotations_status ON community.annotations(note_status);

COMMENT ON TABLE community.annotations IS 'جدول الشروح والتدبرات المجتمعية';

-- ═══════════════════════════════════════════════════════════════
-- إضافة جميع Foreign Keys
-- ═══════════════════════════════════════════════════════════════

-- tafsir
ALTER TABLE quran.tafsir ADD CONSTRAINT fk_tafsir_ayah
    FOREIGN KEY (taf_aya_id) REFERENCES quran.ayahs(aya_id) ON DELETE RESTRICT;
ALTER TABLE quran.tafsir ADD CONSTRAINT fk_tafsir_mufassir
    FOREIGN KEY (taf_mufassir_id) REFERENCES quran.mufassireen(muf_id) ON DELETE RESTRICT;

-- translations
ALTER TABLE quran.translations ADD CONSTRAINT fk_translations_ayah
    FOREIGN KEY (trl_aya_id) REFERENCES quran.ayahs(aya_id) ON DELETE RESTRICT;
ALTER TABLE quran.translations ADD CONSTRAINT fk_translations_translator
    FOREIGN KEY (trl_translator_id) REFERENCES quran.translators(trt_id) ON DELETE RESTRICT;

-- revelation_contexts
ALTER TABLE quran.revelation_contexts ADD CONSTRAINT fk_contexts_ayah_start
    FOREIGN KEY (ctx_aya_id_start) REFERENCES quran.ayahs(aya_id) ON DELETE RESTRICT;

-- topics (self-referencing)
ALTER TABLE quran.topics ADD CONSTRAINT fk_topics_parent
    FOREIGN KEY (top_parent_id) REFERENCES quran.topics(top_id) ON DELETE CASCADE;

-- ayah_topics
ALTER TABLE quran.ayah_topics ADD CONSTRAINT fk_ayah_topics_ayah
    FOREIGN KEY (ayt_aya_id) REFERENCES quran.ayahs(aya_id) ON DELETE CASCADE;
ALTER TABLE quran.ayah_topics ADD CONSTRAINT fk_ayah_topics_topic
    FOREIGN KEY (ayt_top_id) REFERENCES quran.topics(top_id) ON DELETE CASCADE;

-- qiraat
ALTER TABLE quran.qiraat ADD CONSTRAINT fk_qiraat_word
    FOREIGN KEY (qiraa_wrd_id) REFERENCES quran.words(wrd_id) ON DELETE RESTRICT;
ALTER TABLE quran.qiraat ADD CONSTRAINT fk_qiraat_source
    FOREIGN KEY (qiraa_source_id) REFERENCES quran.sources(src_id) ON DELETE SET NULL;

-- recitations
ALTER TABLE quran.recitations ADD CONSTRAINT fk_recitations_ayah
    FOREIGN KEY (rec_aya_id) REFERENCES quran.ayahs(aya_id) ON DELETE RESTRICT;
ALTER TABLE quran.recitations ADD CONSTRAINT fk_recitations_reciter
    FOREIGN KEY (rec_reciter_id) REFERENCES quran.reciters(rct_id) ON DELETE RESTRICT;

-- bookmarks
ALTER TABLE community.bookmarks ADD CONSTRAINT fk_bookmarks_user
    FOREIGN KEY (bmk_usr_id) REFERENCES community.users(usr_id) ON DELETE CASCADE;
ALTER TABLE community.bookmarks ADD CONSTRAINT fk_bookmarks_ayah
    FOREIGN KEY (bmk_aya_id) REFERENCES quran.ayahs(aya_id) ON DELETE CASCADE;

-- annotations
ALTER TABLE community.annotations ADD CONSTRAINT fk_annotations_user
    FOREIGN KEY (note_usr_id) REFERENCES community.users(usr_id) ON DELETE CASCADE;

-- ayahs -> revelation_contexts (optional FK)
ALTER TABLE quran.ayahs ADD CONSTRAINT fk_ayahs_context
    FOREIGN KEY (aya_revelation_context_id) REFERENCES quran.revelation_contexts(ctx_id)
    ON DELETE SET NULL;

-- ayahs -> topics (optional FK للموضوع الرئيسي)
ALTER TABLE quran.ayahs ADD CONSTRAINT fk_ayahs_primary_topic
    FOREIGN KEY (aya_primary_topic_id) REFERENCES quran.topics(top_id)
    ON DELETE SET NULL;

COMMIT;

-- ═══════════════════════════════════════════════════════════════
-- ✅ تم إنشاء جميع الجداول والعلاقات بنجاح!
-- ═══════════════════════════════════════════════════════════════

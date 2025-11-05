-- ═══════════════════════════════════════════════════════════════
-- قاعدة بيانات القرآن الكريم - بسيطة ومترابطة
-- ═══════════════════════════════════════════════════════════════

-- ───────────────────────────────────────────────────────────────
-- جدول السور (114 سورة)
-- ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS surahs (
    id INTEGER PRIMARY KEY,
    name_ar TEXT NOT NULL,
    name_en TEXT NOT NULL,
    ayah_count INTEGER NOT NULL,
    ayat_from INTEGER,
    ayat_to INTEGER,
    word_count INTEGER,
    letter_count INTEGER,
    juz TEXT,
    page_from INTEGER,
    page_to INTEGER,
    page_start INTEGER,
    page_count INTEGER,
    category TEXT,
    revelation_place TEXT,        -- مكية/مدنية
    revelation_order INTEGER,
    revelation_details TEXT,
    central_theme TEXT,
    virtues TEXT,
    remarks TEXT,
    rukus INTEGER
);

-- ───────────────────────────────────────────────────────────────
-- جدول الآيات (6236 آية مع كل القراءات والأنماط)
-- ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ayahs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,

    -- معلومات الموقع
    page INTEGER,
    juz INTEGER,
    line_start INTEGER,
    line_end INTEGER,

    -- القراءات والأنماط (18 نوع)
    text_awwal TEXT,              -- الرسم الأول
    text_uthmani TEXT,            -- الرسم العثماني الكامل (من hafsData)
    text_uthmani_min TEXT,        -- العثماني المبسط
    text_hafs TEXT,               -- قراءة حفص
    text_warsh TEXT,              -- قراءة ورش
    text_qaloun TEXT,             -- قراءة قالون
    text_douri TEXT,              -- قراءة الدوري
    text_shuba TEXT,              -- قراءة شعبة
    text_sousi TEXT,              -- قراءة السوسي
    text_amiry TEXT,              -- أميري مشكل
    text_imlaei TEXT,             -- إملائي مشكل
    text_imlaei_mini TEXT,        -- إملائي مبسط
    text_imlaei_plain TEXT,       -- إملائي بدون تشكيل
    text_simple_fasel TEXT,       -- مبسط مع الفاصلة
    text_simple_tam TEXT,         -- مبسط تام
    text_ajami TEXT,              -- عجمي
    text_latin TEXT,              -- لاتيني (Transliteration)
    text_tajweed TEXT,            -- مع أحكام التجويد

    FOREIGN KEY (surah_id) REFERENCES surahs(id),
    UNIQUE(surah_id, ayah_id)
);

-- ───────────────────────────────────────────────────────────────
-- جدول الكلمات (77432 كلمة)
-- ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY,        -- من 1 إلى 77432
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    word_no_in_ayah INTEGER NOT NULL,
    word_no_in_surah INTEGER NOT NULL,

    -- الكلمة
    word_text TEXT NOT NULL,       -- الكلمة مشكلة
    word_imlaei1 TEXT,            -- إملائي 1
    word_imlaei2 TEXT,            -- إملائي 2

    -- الإحصائيات
    harf_no_in_word INTEGER,
    harf_no_total INTEGER,

    -- الجذر والإحصائيات
    root TEXT,
    repeat_count INTEGER,
    root_repeat_count INTEGER,
    seq_in_similar_words INTEGER,
    seq_in_similar_roots INTEGER,
    ayah_count_with_word INTEGER,
    ayah_count_with_root INTEGER,
    surah_count_with_word INTEGER,
    surah_count_with_root INTEGER,

    FOREIGN KEY (surah_id) REFERENCES surahs(id)
);

-- ───────────────────────────────────────────────────────────────
-- جدول تفاصيل الكلمات (إعراب، صرف، معاني، رسم)
-- ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS word_details (
    word_id INTEGER PRIMARY KEY,

    -- الإعراب
    irab TEXT,

    -- الصرف
    sarf TEXT,

    -- المعنى
    meaning TEXT,

    -- الرسم القرآني
    rasm TEXT,

    FOREIGN KEY (word_id) REFERENCES words(id)
);

-- ═══════════════════════════════════════════════════════════════
-- الفهارس للبحث السريع
-- ═══════════════════════════════════════════════════════════════

-- فهارس الآيات
CREATE INDEX IF NOT EXISTS idx_ayahs_surah ON ayahs(surah_id, ayah_id);
CREATE INDEX IF NOT EXISTS idx_ayahs_page ON ayahs(page);
CREATE INDEX IF NOT EXISTS idx_ayahs_juz ON ayahs(juz);

-- فهارس الكلمات
CREATE INDEX IF NOT EXISTS idx_words_location ON words(surah_id, ayah_id, word_no_in_ayah);
CREATE INDEX IF NOT EXISTS idx_words_root ON words(root);
CREATE INDEX IF NOT EXISTS idx_words_text ON words(word_text);

-- فهارس البحث النصي الكامل (FTS5)
CREATE VIRTUAL TABLE IF NOT EXISTS ayahs_fts USING fts5(
    surah_id,
    ayah_id,
    text_uthmani,
    text_hafs,
    text_simple_fasel,
    content='ayahs'
);

-- فهرس البحث في الكلمات
CREATE VIRTUAL TABLE IF NOT EXISTS words_fts USING fts5(
    word_id,
    word_text,
    root,
    meaning,
    content='words'
);

-- ═══════════════════════════════════════════════════════════════
-- Views مفيدة
-- ═══════════════════════════════════════════════════════════════

-- عرض الآيات مع معلومات السورة
CREATE VIEW IF NOT EXISTS v_ayahs_complete AS
SELECT
    a.id,
    a.surah_id,
    a.ayah_id,
    s.name_ar as surah_name_ar,
    s.name_en as surah_name_en,
    a.page,
    a.juz,
    a.text_uthmani,
    a.text_hafs,
    a.text_simple_fasel,
    a.text_imlaei,
    a.text_tajweed
FROM ayahs a
JOIN surahs s ON a.surah_id = s.id;

-- عرض الكلمات مع تفاصيلها
CREATE VIEW IF NOT EXISTS v_words_complete AS
SELECT
    w.*,
    wd.irab,
    wd.sarf,
    wd.meaning,
    wd.rasm
FROM words w
LEFT JOIN word_details wd ON w.id = wd.word_id;

-- ═══════════════════════════════════════════════════════════════
-- نهاية Schema
-- ═══════════════════════════════════════════════════════════════

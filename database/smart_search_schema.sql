-- =====================================================
-- 🗄️ قاعدة البيانات العصبية للبحث الذكي - دُحى TV
-- =====================================================
-- نظام بحث فوري وذكي مع ربط عصبي بين جميع العناصر
-- =====================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;  -- للأداء الأفضل
PRAGMA synchronous = NORMAL;
PRAGMA temp_store = MEMORY;
PRAGMA cache_size = -64000;  -- 64MB cache

-- =====================================================
-- 1️⃣ جداول القرآن الكريم
-- =====================================================

-- جدول السور
CREATE TABLE IF NOT EXISTS surahs (
    surah_id INTEGER PRIMARY KEY,
    surah_name_arabic TEXT NOT NULL,
    surah_name_english TEXT,
    revelation_type TEXT CHECK(revelation_type IN ('مكية', 'مدنية')),
    verses_count INTEGER NOT NULL,
    revelation_order INTEGER,
    juz_start INTEGER,
    page_start INTEGER,
    UNIQUE(surah_id)
);

-- جدول الآيات (9 رسوم مختلفة)
CREATE TABLE IF NOT EXISTS verses (
    verse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    verse_number INTEGER NOT NULL,
    page_number INTEGER,
    juz_number INTEGER,
    hizb_number INTEGER,
    rub_number INTEGER,

    -- الرسوم المختلفة
    text_othmani TEXT NOT NULL,           -- العثماني
    text_othmani_no_tashkeel TEXT,        -- العثماني بدون تشكيل
    text_othmani_light TEXT,              -- العثماني تشكيل خفيف
    text_emlai TEXT,                      -- الإملائي
    text_emlai_no_tashkeel TEXT,          -- الإملائي بدون تشكيل
    text_kufi TEXT,                       -- الكوفي
    text_maghrebi TEXT,                   -- المغربي
    text_indopak TEXT,                    -- الهندي الباكستاني
    text_simplified TEXT,                 -- مبسط للبحث

    -- معلومات إضافية
    sajdah_type TEXT,                     -- نوع السجدة
    sajdah_number INTEGER,                -- رقم السجدة

    FOREIGN KEY (surah_id) REFERENCES surahs(surah_id),
    UNIQUE(surah_id, verse_number)
);

-- جدول الكلمات
CREATE TABLE IF NOT EXISTS words (
    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    word_position INTEGER NOT NULL,      -- موضع الكلمة في الآية

    -- نصوص الكلمة
    word_text TEXT NOT NULL,              -- الكلمة الأصلية
    word_no_tashkeel TEXT,                -- بدون تشكيل
    word_simplified TEXT,                 -- مبسطة للبحث

    -- التحليل اللغوي
    root TEXT,                            -- الجذر
    stem TEXT,                            -- الجذع
    lemma TEXT,                           -- اللمّة

    -- النحو والصرف
    grammar_type TEXT,                    -- اسم / فعل / حرف
    grammar_details TEXT,                 -- تفاصيل إعرابية (JSON)
    morphology TEXT,                      -- الصرف (JSON)

    -- الأوزان
    pattern TEXT,                         -- الوزن الصرفي

    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    UNIQUE(verse_id, word_position)
);

-- =====================================================
-- 2️⃣ جداول التفاسير والترجمات
-- =====================================================

-- جدول كتب التفاسير
CREATE TABLE IF NOT EXISTS tafseer_books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name_arabic TEXT NOT NULL,
    book_name_english TEXT,
    author_name TEXT,
    category TEXT,                        -- معاصرة / أمهات / لغوية
    language TEXT DEFAULT 'ar',
    is_active BOOLEAN DEFAULT 1,
    UNIQUE(book_name_arabic)
);

-- جدول نصوص التفاسير
CREATE TABLE IF NOT EXISTS tafseer_texts (
    tafseer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    verse_id INTEGER NOT NULL,
    tafseer_text TEXT NOT NULL,

    FOREIGN KEY (book_id) REFERENCES tafseer_books(book_id),
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    UNIQUE(book_id, verse_id)
);

-- جدول كتب الترجمات
CREATE TABLE IF NOT EXISTS translation_books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL,
    translator_name TEXT,
    language_code TEXT NOT NULL,          -- en, fr, de, tr, etc.
    language_name TEXT,
    is_active BOOLEAN DEFAULT 1,
    UNIQUE(book_name, language_code)
);

-- جدول نصوص الترجمات
CREATE TABLE IF NOT EXISTS translation_texts (
    translation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    verse_id INTEGER NOT NULL,
    translation_text TEXT NOT NULL,

    FOREIGN KEY (book_id) REFERENCES translation_books(book_id),
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    UNIQUE(book_id, verse_id)
);

-- =====================================================
-- 3️⃣ جداول الموضوعات والعلوم
-- =====================================================

-- جدول الموضوعات الهرمية
CREATE TABLE IF NOT EXISTS topics (
    topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_name TEXT NOT NULL,
    parent_id INTEGER,                    -- للهيكل الشجري
    level INTEGER DEFAULT 1,              -- المستوى (1,2,3,4)
    sort_order INTEGER DEFAULT 0,
    description TEXT,

    FOREIGN KEY (parent_id) REFERENCES topics(topic_id),
    UNIQUE(topic_name, parent_id)
);

-- جدول ربط الآيات بالموضوعات
CREATE TABLE IF NOT EXISTS verse_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    relevance_score REAL DEFAULT 1.0,     -- درجة الصلة

    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
    UNIQUE(verse_id, topic_id)
);

-- جدول علوم القرآن
CREATE TABLE IF NOT EXISTS quran_sciences (
    science_id INTEGER PRIMARY KEY AUTOINCREMENT,
    science_type TEXT NOT NULL,           -- أسباب النزول / الناسخ والمنسوخ...
    verse_id INTEGER NOT NULL,
    science_text TEXT NOT NULL,
    source TEXT,                          -- المرجع

    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- جدول التدبرات
CREATE TABLE IF NOT EXISTS tadabbur (
    tadabbur_id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    tadabbur_text TEXT NOT NULL,
    author TEXT,
    source TEXT,

    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- =====================================================
-- 4️⃣ جدول الربط العصبي (Neural Links)
-- =====================================================

CREATE TABLE IF NOT EXISTS neural_links (
    link_id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- المصدر
    source_type TEXT NOT NULL,            -- verse, word, topic, surah
    source_id INTEGER NOT NULL,

    -- الهدف
    target_type TEXT NOT NULL,            -- verse, word, topic, surah
    target_id INTEGER NOT NULL,

    -- نوع العلاقة
    relation_type TEXT NOT NULL,          -- similar, related, opposite, explains

    -- قوة الارتباط
    weight REAL DEFAULT 1.0,

    -- بيانات إضافية
    metadata TEXT,                        -- JSON للبيانات الإضافية

    -- تاريخ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(source_type, source_id, target_type, target_id, relation_type)
);

-- =====================================================
-- 5️⃣ جداول FTS5 للبحث السريع
-- =====================================================

-- فهرس البحث في القرآن
CREATE VIRTUAL TABLE IF NOT EXISTS quran_fts USING fts5(
    verse_id UNINDEXED,
    surah_id UNINDEXED,
    verse_number UNINDEXED,
    text_othmani,
    text_no_tashkeel,
    text_simplified,
    tokenize = 'unicode61 remove_diacritics 2'
);

-- فهرس البحث في الكلمات
CREATE VIRTUAL TABLE IF NOT EXISTS words_fts USING fts5(
    word_id UNINDEXED,
    verse_id UNINDEXED,
    word_text,
    word_no_tashkeel,
    root,
    stem,
    tokenize = 'trigram'
);

-- فهرس البحث في التفاسير
CREATE VIRTUAL TABLE IF NOT EXISTS tafseer_fts USING fts5(
    tafseer_id UNINDEXED,
    book_id UNINDEXED,
    verse_id UNINDEXED,
    tafseer_text,
    tokenize = 'unicode61'
);

-- فهرس البحث في الموضوعات
CREATE VIRTUAL TABLE IF NOT EXISTS topics_fts USING fts5(
    topic_id UNINDEXED,
    topic_name,
    description,
    tokenize = 'unicode61'
);

-- =====================================================
-- 6️⃣ جداول الإحصائيات والتحليل
-- =====================================================

-- إحصائيات الآيات
CREATE TABLE IF NOT EXISTS verse_stats (
    verse_id INTEGER PRIMARY KEY,
    letters_count INTEGER,
    words_count INTEGER,
    tashkeel_count INTEGER,
    unique_words_count INTEGER,

    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- إحصائيات الكلمات
CREATE TABLE IF NOT EXISTS word_stats (
    word_text TEXT PRIMARY KEY,
    total_occurrences INTEGER DEFAULT 0,
    unique_verses INTEGER DEFAULT 0,
    first_occurrence_verse INTEGER,
    last_occurrence_verse INTEGER
);

-- إحصائيات البحث (لتحسين الأداء)
CREATE TABLE IF NOT EXISTS search_stats (
    search_id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_query TEXT NOT NULL,
    search_count INTEGER DEFAULT 1,
    last_searched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    avg_time_ms REAL
);

-- =====================================================
-- 7️⃣ الفهارس للأداء العالي
-- =====================================================

-- فهارس الآيات
CREATE INDEX IF NOT EXISTS idx_verses_surah ON verses(surah_id);
CREATE INDEX IF NOT EXISTS idx_verses_page ON verses(page_number);
CREATE INDEX IF NOT EXISTS idx_verses_juz ON verses(juz_number);
CREATE INDEX IF NOT EXISTS idx_verses_location ON verses(surah_id, verse_number);
CREATE INDEX IF NOT EXISTS idx_verses_sajdah ON verses(sajdah_type) WHERE sajdah_type IS NOT NULL;

-- فهارس الكلمات
CREATE INDEX IF NOT EXISTS idx_words_verse ON words(verse_id);
CREATE INDEX IF NOT EXISTS idx_words_position ON words(verse_id, word_position);
CREATE INDEX IF NOT EXISTS idx_words_root ON words(root);
CREATE INDEX IF NOT EXISTS idx_words_stem ON words(stem);
CREATE INDEX IF NOT EXISTS idx_words_grammar ON words(grammar_type);
CREATE INDEX IF NOT EXISTS idx_words_text ON words(word_no_tashkeel);

-- فهارس التفاسير
CREATE INDEX IF NOT EXISTS idx_tafseer_book ON tafseer_texts(book_id);
CREATE INDEX IF NOT EXISTS idx_tafseer_verse ON tafseer_texts(verse_id);
CREATE INDEX IF NOT EXISTS idx_tafseer_lookup ON tafseer_texts(book_id, verse_id);

-- فهارس الترجمات
CREATE INDEX IF NOT EXISTS idx_translation_book ON translation_texts(book_id);
CREATE INDEX IF NOT EXISTS idx_translation_verse ON translation_texts(verse_id);
CREATE INDEX IF NOT EXISTS idx_translation_lookup ON translation_texts(book_id, verse_id);

-- فهارس الموضوعات
CREATE INDEX IF NOT EXISTS idx_topics_parent ON topics(parent_id);
CREATE INDEX IF NOT EXISTS idx_topics_level ON topics(level);
CREATE INDEX IF NOT EXISTS idx_verse_topics_verse ON verse_topics(verse_id);
CREATE INDEX IF NOT EXISTS idx_verse_topics_topic ON verse_topics(topic_id);
CREATE INDEX IF NOT EXISTS idx_verse_topics_relevance ON verse_topics(relevance_score DESC);

-- فهارس الربط العصبي
CREATE INDEX IF NOT EXISTS idx_neural_source ON neural_links(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_neural_target ON neural_links(target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_neural_relation ON neural_links(relation_type);
CREATE INDEX IF NOT EXISTS idx_neural_weight ON neural_links(weight DESC);
CREATE INDEX IF NOT EXISTS idx_neural_compound ON neural_links(source_type, source_id, relation_type);

-- =====================================================
-- 8️⃣ الـ Triggers للتحديث التلقائي
-- =====================================================

-- تحديث فهرس FTS عند إضافة آية
CREATE TRIGGER IF NOT EXISTS verse_insert_fts
AFTER INSERT ON verses
BEGIN
    INSERT INTO quran_fts(verse_id, surah_id, verse_number, text_othmani, text_no_tashkeel, text_simplified)
    VALUES (NEW.verse_id, NEW.surah_id, NEW.verse_number, NEW.text_othmani, NEW.text_othmani_no_tashkeel, NEW.text_simplified);
END;

-- تحديث فهرس FTS عند تعديل آية
CREATE TRIGGER IF NOT EXISTS verse_update_fts
AFTER UPDATE ON verses
BEGIN
    UPDATE quran_fts
    SET text_othmani = NEW.text_othmani,
        text_no_tashkeel = NEW.text_othmani_no_tashkeel,
        text_simplified = NEW.text_simplified
    WHERE verse_id = NEW.verse_id;
END;

-- تحديث فهرس FTS عند حذف آية
CREATE TRIGGER IF NOT EXISTS verse_delete_fts
AFTER DELETE ON verses
BEGIN
    DELETE FROM quran_fts WHERE verse_id = OLD.verse_id;
END;

-- تحديث إحصائيات البحث
CREATE TRIGGER IF NOT EXISTS update_search_stats
AFTER INSERT ON search_stats
BEGIN
    UPDATE search_stats
    SET search_count = search_count + 1,
        last_searched = CURRENT_TIMESTAMP
    WHERE search_query = NEW.search_query AND search_id != NEW.search_id;
END;

-- =====================================================
-- 9️⃣ الـ Views للاستعلامات السريعة
-- =====================================================

-- عرض كامل للآيات مع معلومات السورة
CREATE VIEW IF NOT EXISTS v_verses_full AS
SELECT
    v.verse_id,
    v.surah_id,
    v.verse_number,
    v.page_number,
    v.juz_number,
    v.text_othmani,
    v.text_othmani_no_tashkeel,
    v.text_simplified,
    s.surah_name_arabic,
    s.surah_name_english,
    s.revelation_type,
    s.verses_count AS surah_verses_count
FROM verses v
JOIN surahs s ON v.surah_id = s.surah_id;

-- عرض الكلمات مع تفاصيلها
CREATE VIEW IF NOT EXISTS v_words_full AS
SELECT
    w.word_id,
    w.verse_id,
    w.word_position,
    w.word_text,
    w.word_no_tashkeel,
    w.root,
    w.stem,
    w.grammar_type,
    v.surah_id,
    v.verse_number,
    v.text_othmani AS verse_text
FROM words w
JOIN verses v ON w.verse_id = v.verse_id;

-- عرض الموضوعات الهرمية
CREATE VIEW IF NOT EXISTS v_topics_hierarchy AS
WITH RECURSIVE topic_tree AS (
    -- المستوى الأول
    SELECT
        topic_id,
        topic_name,
        parent_id,
        level,
        topic_name AS full_path,
        sort_order
    FROM topics
    WHERE parent_id IS NULL

    UNION ALL

    -- المستويات التالية
    SELECT
        t.topic_id,
        t.topic_name,
        t.parent_id,
        t.level,
        tt.full_path || ' > ' || t.topic_name,
        t.sort_order
    FROM topics t
    JOIN topic_tree tt ON t.parent_id = tt.topic_id
)
SELECT * FROM topic_tree
ORDER BY full_path, sort_order;

-- =====================================================
-- 🔟 إدخال بيانات أساسية
-- =====================================================

-- إدخال السور
INSERT OR IGNORE INTO surahs (surah_id, surah_name_arabic, surah_name_english, revelation_type, verses_count, revelation_order) VALUES
(1, 'الفاتحة', 'Al-Fatihah', 'مكية', 7, 5),
(2, 'البقرة', 'Al-Baqarah', 'مدنية', 286, 87),
(3, 'آل عمران', 'Ali Imran', 'مدنية', 200, 89),
(4, 'النساء', 'An-Nisa', 'مدنية', 176, 92),
(5, 'المائدة', 'Al-Maidah', 'مدنية', 120, 112),
(6, 'الأنعام', 'Al-Anam', 'مكية', 165, 55),
(7, 'الأعراف', 'Al-Araf', 'مكية', 206, 39);
-- ... (يتم إدخال باقي السور)

-- إدخال أنواع الموضوعات الرئيسية
INSERT OR IGNORE INTO topics (topic_name, parent_id, level) VALUES
('العقيدة', NULL, 1),
('العبادات', NULL, 1),
('المعاملات', NULL, 1),
('الأخلاق', NULL, 1),
('القصص القرآني', NULL, 1),
('الأحكام', NULL, 1);

-- الموضوعات الفرعية للعقيدة
INSERT OR IGNORE INTO topics (topic_name, parent_id, level) VALUES
('التوحيد', 1, 2),
('الإيمان بالله', 1, 2),
('الإيمان بالملائكة', 1, 2),
('الإيمان بالكتب', 1, 2),
('الإيمان بالرسل', 1, 2),
('الإيمان باليوم الآخر', 1, 2),
('الإيمان بالقدر', 1, 2);

-- إدخال كتب التفاسير الشائعة
INSERT OR IGNORE INTO tafseer_books (book_name_arabic, book_name_english, author_name, category) VALUES
('تفسير الطبري', 'Tafsir al-Tabari', 'ابن جرير الطبري', 'أمهات'),
('تفسير ابن كثير', 'Tafsir Ibn Kathir', 'ابن كثير', 'أمهات'),
('تفسير القرطبي', 'Tafsir al-Qurtubi', 'القرطبي', 'أمهات'),
('التفسير الميسر', 'Al-Tafsir Al-Muyassar', 'مجمع الملك فهد', 'معاصرة'),
('المختصر في التفسير', 'Al-Mukhtasar fi al-Tafsir', 'مركز تفسير', 'معاصرة'),
('تيسير الكريم الرحمن', 'Tafsir As-Saadi', 'السعدي', 'معاصرة'),
('أيسر التفاسير', 'Aysar at-Tafasir', 'الجزائري', 'معاصرة');

-- =====================================================
-- 🎯 استعلامات مفيدة للبحث
-- =====================================================

-- البحث السريع في القرآن
-- SELECT * FROM quran_fts WHERE text_simplified MATCH 'الحمد' ORDER BY rank LIMIT 50;

-- البحث في كلمة بجذرها
-- SELECT * FROM words_fts WHERE root MATCH 'حمد' LIMIT 100;

-- البحث في التفاسير
-- SELECT * FROM tafseer_fts WHERE tafseer_text MATCH 'الإيمان' LIMIT 100;

-- البحث في الموضوعات
-- SELECT * FROM topics_fts WHERE topic_name MATCH 'التوحيد';

-- جلب الروابط العصبية لآية
-- SELECT * FROM neural_links WHERE source_type = 'verse' AND source_id = 1 ORDER BY weight DESC;

-- =====================================================
-- ✅ انتهى تصميم قاعدة البيانات
-- =====================================================

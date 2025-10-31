-- ============================================================================
-- 📊 سكريبت إنشاء قاعدة بيانات القرآن الكريم v4.0 Ultimate
-- ============================================================================
-- 🎯 يحتوي على كل الجداول المطلوبة للتطبيق المتكامل
-- 📅 التاريخ: 2025-10-31
-- 👨‍💻 المطور: Claude AI + Mustafa Yakoub
-- ============================================================================

-- إزالة الجداول القديمة إن وجدت (اختياري - احذر من فقدان البيانات!)
-- DROP TABLE IF EXISTS quran_text;
-- DROP TABLE IF EXISTS quran_tajweed;
-- DROP TABLE IF EXISTS surahs_info;
-- ... إلخ

-- ============================================================================
-- الجداول الأساسية (PRIORITY 1 - ضرورية جداً)
-- ============================================================================

-- 1. معلومات السور
CREATE TABLE IF NOT EXISTS surahs_info (
    id INTEGER PRIMARY KEY,
    name_ar TEXT NOT NULL,
    name_en TEXT,
    name_translation TEXT,
    type TEXT CHECK(type IN ('makkiyah', 'madaniyah')),
    ayahs_count INTEGER NOT NULL,
    revelation_order INTEGER,
    rukus_count INTEGER,
    revelation_place TEXT
);

-- 2. النص القرآني الرئيسي
CREATE TABLE IF NOT EXISTS quran_text (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    text_simple TEXT,
    text_imlaai TEXT,
    juz INTEGER,
    page INTEGER,
    hizb INTEGER,
    manzil INTEGER,
    ruku INTEGER,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 3. النص بالتجويد الملون
CREATE TABLE IF NOT EXISTS quran_tajweed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    tajweed_text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 4. التفسير الميسر
CREATE TABLE IF NOT EXISTS tafsir_muyassar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 5. العلامات المرجعية
CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    color TEXT,
    category TEXT,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id)
);

-- 6. إعدادات المستخدم
CREATE TABLE IF NOT EXISTS user_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT NOT NULL UNIQUE,
    setting_value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- الجداول المهمة (PRIORITY 2)
-- ============================================================================

-- 7. تفسير السعدي
CREATE TABLE IF NOT EXISTS tafsir_saadi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 8. تفسير البغوي
CREATE TABLE IF NOT EXISTS tafsir_baghawi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 9. تفسير الجلالين
CREATE TABLE IF NOT EXISTS tafsir_jalalayn (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 10. تفسير الطبري
CREATE TABLE IF NOT EXISTS tafsir_tabari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL, -- 0 = مقدمة السورة
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 11. الترجمة الإنجليزية
CREATE TABLE IF NOT EXISTS translation_english (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    translator TEXT,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 12. الترجمة الفرنسية
CREATE TABLE IF NOT EXISTS translation_french (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    translator TEXT,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 13. الإعراب النحوي
CREATE TABLE IF NOT EXISTS irab (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 14. التحليل الصرفي
CREATE TABLE IF NOT EXISTS sarf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 15. الموضوعات القرآنية
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_name TEXT NOT NULL UNIQUE,
    topic_category TEXT,
    description TEXT
);

-- 16. ربط الموضوعات بالآيات
CREATE TABLE IF NOT EXISTS topics_verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    relevance INTEGER DEFAULT 5 CHECK(relevance BETWEEN 1 AND 10),
    FOREIGN KEY (topic_id) REFERENCES topics(id),
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(topic_id, surah_id, ayah_id)
);

-- ============================================================================
-- الجداول الاختيارية (PRIORITY 3)
-- ============================================================================

-- 17. كلمات القرآن
CREATE TABLE IF NOT EXISTS words_quran (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    word_position INTEGER NOT NULL,
    word_text TEXT NOT NULL,
    word_root TEXT,
    word_type TEXT CHECK(word_type IN ('اسم', 'فعل', 'حرف')),
    word_meaning TEXT,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id, word_position)
);

-- 18. آيات السجدة
CREATE TABLE IF NOT EXISTS sajda_ayahs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    sajda_type TEXT CHECK(sajda_type IN ('واجبة', 'مستحبة')),
    sajda_number INTEGER,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 19. جذور الكلمات
CREATE TABLE IF NOT EXISTS word_roots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    root TEXT NOT NULL UNIQUE,
    root_meaning TEXT,
    derivatives_count INTEGER DEFAULT 0
);

-- 20. الأوزان الصرفية
CREATE TABLE IF NOT EXISTS word_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern TEXT NOT NULL UNIQUE,
    pattern_type TEXT,
    examples TEXT
);

-- 21. القراءات المختلفة
CREATE TABLE IF NOT EXISTS qiraah (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    qiraah_type TEXT NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id, qiraah_type)
);

-- 22. أسباب النزول
CREATE TABLE IF NOT EXISTS asbab_nuzul (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    sabab TEXT NOT NULL,
    source TEXT,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- 23. سجل القراءة
CREATE TABLE IF NOT EXISTS reading_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    visited_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    duration_seconds INTEGER,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id)
);

-- 24. إحصائيات عامة
CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_key TEXT NOT NULL UNIQUE,
    stat_value INTEGER NOT NULL,
    description TEXT
);

-- ============================================================================
-- الفهارس (Indexes) لتحسين الأداء
-- ============================================================================

-- فهارس للجدول الرئيسي
CREATE INDEX IF NOT EXISTS idx_quran_surah ON quran_text(surah_id);
CREATE INDEX IF NOT EXISTS idx_quran_ayah ON quran_text(ayah_id);
CREATE INDEX IF NOT EXISTS idx_quran_juz ON quran_text(juz);
CREATE INDEX IF NOT EXISTS idx_quran_page ON quran_text(page);
CREATE INDEX IF NOT EXISTS idx_quran_text ON quran_text(text_simple); -- للبحث

-- فهارس للتفاسير
CREATE INDEX IF NOT EXISTS idx_tafsir_muyassar_surah ON tafsir_muyassar(surah_id);
CREATE INDEX IF NOT EXISTS idx_tafsir_saadi_surah ON tafsir_saadi(surah_id);
CREATE INDEX IF NOT EXISTS idx_tafsir_baghawi_surah ON tafsir_baghawi(surah_id);

-- فهارس للترجمات
CREATE INDEX IF NOT EXISTS idx_translation_en_surah ON translation_english(surah_id);
CREATE INDEX IF NOT EXISTS idx_translation_fr_surah ON translation_french(surah_id);

-- فهارس للموضوعات
CREATE INDEX IF NOT EXISTS idx_topics_verses_topic ON topics_verses(topic_id);
CREATE INDEX IF NOT EXISTS idx_topics_verses_surah ON topics_verses(surah_id);

-- فهارس للعلامات
CREATE INDEX IF NOT EXISTS idx_bookmarks_surah ON bookmarks(surah_id);
CREATE INDEX IF NOT EXISTS idx_bookmarks_date ON bookmarks(created_at);

-- فهارس للكلمات
CREATE INDEX IF NOT EXISTS idx_words_surah ON words_quran(surah_id);
CREATE INDEX IF NOT EXISTS idx_words_root ON words_quran(word_root);

-- ============================================================================
-- بيانات أولية (Initial Data)
-- ============================================================================

-- إدراج بعض الإحصائيات الثابتة
INSERT OR IGNORE INTO statistics (stat_key, stat_value, description) VALUES
    ('total_suras', 114, 'عدد السور في القرآن الكريم'),
    ('total_ayahs', 6236, 'عدد الآيات في القرآن الكريم'),
    ('total_juz', 30, 'عدد الأجزاء'),
    ('total_hizb', 60, 'عدد الأحزاب'),
    ('total_pages', 604, 'عدد الصفحات (مصحف المدينة)');

-- إدراج بعض الموضوعات الأساسية
INSERT OR IGNORE INTO topics (topic_name, topic_category, description) VALUES
    ('العقيدة والإيمان', 'أصول الدين', 'الآيات المتعلقة بالإيمان بالله والملائكة والكتب والرسل'),
    ('العبادات', 'فروع الدين', 'الآيات المتعلقة بالصلاة والزكاة والصيام والحج'),
    ('الأخلاق والآداب', 'الأخلاق', 'الآيات المتعلقة بالصبر والشكر والتواضع وحسن الخلق'),
    ('القصص القرآني', 'القصص', 'قصص الأنبياء والأمم السابقة'),
    ('الأحكام الشرعية', 'الفقه', 'الآيات المتعلقة بالحلال والحرام والأحكام'),
    ('الجنة والنار', 'الآخرة', 'وصف الجنة والنار والبعث والحساب'),
    ('الرحمة والمغفرة', 'صفات الله', 'آيات رحمة الله ومغفرته للعباد'),
    ('الدعاء والذكر', 'العبادات', 'الأدعية القرآنية وفضل الذكر');

-- إدراج بعض الإعدادات الافتراضية
INSERT OR IGNORE INTO user_settings (setting_key, setting_value) VALUES
    ('last_surah', '1'),
    ('last_ayah', '1'),
    ('font_size', '18'),
    ('theme', 'claude_colors'),
    ('show_tajweed', 'true'),
    ('show_translation', 'false'),
    ('language', 'ar');

-- إدراج آيات السجدة الـ 15
INSERT OR IGNORE INTO sajda_ayahs (surah_id, ayah_id, sajda_type, sajda_number) VALUES
    (7, 206, 'مستحبة', 1),
    (13, 15, 'مستحبة', 2),
    (16, 50, 'مستحبة', 3),
    (17, 109, 'مستحبة', 4),
    (19, 58, 'مستحبة', 5),
    (22, 18, 'مستحبة', 6),
    (22, 77, 'مستحبة', 7),
    (25, 60, 'مستحبة', 8),
    (27, 26, 'مستحبة', 9),
    (32, 15, 'واجبة', 10),
    (38, 24, 'مستحبة', 11),
    (41, 38, 'واجبة', 12),
    (53, 62, 'واجبة', 13),
    (84, 21, 'مستحبة', 14),
    (96, 19, 'واجبة', 15);

-- ============================================================================
-- معلومات أساسية عن السور (عينة)
-- ============================================================================

-- السور الأولى كمثال (يمكن إكمال الباقي)
INSERT OR IGNORE INTO surahs_info (id, name_ar, name_en, name_translation, type, ayahs_count, revelation_order) VALUES
    (1, 'الفاتحة', 'Al-Fatihah', 'The Opening', 'makkiyah', 7, 5),
    (2, 'البقرة', 'Al-Baqarah', 'The Cow', 'madaniyah', 286, 87),
    (3, 'آل عمران', 'Ali Imran', 'The Family of Imran', 'madaniyah', 200, 89),
    (4, 'النساء', 'An-Nisa', 'The Women', 'madaniyah', 176, 92),
    (5, 'المائدة', 'Al-Maidah', 'The Table Spread', 'madaniyah', 120, 112);
-- ... يمكن إكمال باقي السور

-- ============================================================================
-- استعلامات تحقق (Verification Queries)
-- ============================================================================

-- التحقق من إنشاء الجداول
-- SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- عدد الجداول
-- SELECT COUNT(*) as total_tables FROM sqlite_master WHERE type='table';

-- عدد الفهارس
-- SELECT COUNT(*) as total_indexes FROM sqlite_master WHERE type='index';

-- ============================================================================
-- ملاحظات مهمة
-- ============================================================================

/*
📝 ملاحظات:

1. هذا السكريبت ينشئ الهيكل الأساسي لقاعدة البيانات
2. يجب ملء البيانات الفعلية (نصوص القرآن، التفاسير، إلخ) من مصادر موثوقة
3. الفهارس مهمة جداً للأداء - لا تحذفها
4. يمكن إضافة المزيد من الجداول حسب الحاجة
5. جميع الأسماء باللغة الإنجليزية لتوافق أفضل

🔗 العلاقات:
- كل آية في quran_text مرتبطة بسورة في surahs_info
- كل تفسير مرتبط بآية محددة
- الموضوعات مرتبطة بالآيات عبر جدول topics_verses

⚡ تحسين الأداء:
- استخدم الفهارس للبحث السريع
- استخدم UNIQUE constraints لمنع التكرار
- استخدم FOREIGN KEY للحفاظ على سلامة البيانات

✅ التوافق:
- متوافق مع SQLite 3
- يعمل على Windows, Linux, macOS
- يدعم UTF-8 للنصوص العربية
*/

-- ============================================================================
-- نهاية السكريبت
-- ============================================================================

SELECT 'قاعدة البيانات جاهزة! ✅' as status;
SELECT COUNT(*) || ' جدول تم إنشاؤه' as tables_count
    FROM sqlite_master WHERE type='table';

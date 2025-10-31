-- ============================================================================
-- سكريبت إنشاء قاعدة البيانات النهائية
-- Final Database Creation Script
-- ============================================================================
-- هذا السكريبت يطابق بدقة الأسماء المستخدمة في الكود
-- This script EXACTLY matches the names used in quran_app_ultimate_final_v4.py
-- ============================================================================

-- حذف الجداول إذا كانت موجودة
DROP TABLE IF EXISTS topics_verses;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS bookmarks;
DROP TABLE IF EXISTS user_settings;
DROP TABLE IF EXISTS sajda_ayahs;
DROP TABLE IF EXISTS sarf;
DROP TABLE IF EXISTS irab;
DROP TABLE IF EXISTS translation_french;
DROP TABLE IF EXISTS translation_english;
DROP TABLE IF EXISTS tafsir_baghawi;
DROP TABLE IF EXISTS tafsir_saadi;
DROP TABLE IF EXISTS tafsir_muyassar;
DROP TABLE IF EXISTS quran_tajweed;
DROP TABLE IF EXISTS quran_text;
DROP TABLE IF EXISTS surahs_info;

-- ============================================================================
-- 1. جدول معلومات السور
-- Table: surahs_info
-- ============================================================================
CREATE TABLE surahs_info (
    id INTEGER PRIMARY KEY,              -- رقم السورة (1-114)
    name_ar TEXT NOT NULL,               -- اسم السورة بالعربية
    ayahs_count INTEGER NOT NULL,        -- عدد الآيات في السورة
    type TEXT,                           -- نوع السورة (مكية/مدنية)
    name_en TEXT,                        -- اسم السورة بالإنجليزية
    revelation_order INTEGER             -- ترتيب النزول
);

-- ============================================================================
-- 2. جدول النص القرآني
-- Table: quran_text
-- ============================================================================
CREATE TABLE quran_text (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,           -- رقم السورة
    ayah_id INTEGER NOT NULL,            -- رقم الآية
    text TEXT NOT NULL,                  -- النص الكامل (بالتشكيل)
    text_simple TEXT,                    -- النص البسيط (بدون تشكيل)
    juz INTEGER,                         -- رقم الجزء
    page INTEGER,                        -- رقم الصفحة
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- ============================================================================
-- 3. جدول نص التجويد
-- Table: quran_tajweed
-- ============================================================================
CREATE TABLE quran_tajweed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,           -- رقم السورة
    ayah_id INTEGER NOT NULL,            -- رقم الآية
    tajweed_text TEXT NOT NULL,          -- النص مع علامات التجويد XML
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- ملاحظة: تنسيق tajweed_text:
-- يستخدم tags XML بالشكل: <1>نص</1> للإظهار، <2>نص</2> للإدغام، إلخ
-- الأرقام من 1-15 تمثل أحكام التجويد الـ15

-- ============================================================================
-- 4. جدول التفسير الميسر
-- Table: tafsir_muyassar
-- ============================================================================
CREATE TABLE tafsir_muyassar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,                  -- نص التفسير
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- ============================================================================
-- 5. جدول تفسير السعدي
-- Table: tafsir_saadi
-- ============================================================================
CREATE TABLE tafsir_saadi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- ============================================================================
-- 6. جدول تفسير البغوي
-- Table: tafsir_baghawi
-- ============================================================================
CREATE TABLE tafsir_baghawi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- ============================================================================
-- 7. جدول الترجمة الإنجليزية
-- Table: translation_english
-- ============================================================================
CREATE TABLE translation_english (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- ============================================================================
-- 8. جدول الترجمة الفرنسية
-- Table: translation_french
-- ============================================================================
CREATE TABLE translation_french (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- ============================================================================
-- 9. جدول الإعراب
-- Table: irab
-- ============================================================================
CREATE TABLE irab (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,                  -- نص الإعراب
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- ============================================================================
-- 10. جدول الصرف
-- Table: sarf
-- ============================================================================
CREATE TABLE sarf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    text TEXT NOT NULL,                  -- نص الصرف
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- ============================================================================
-- 11. جدول آيات السجدة
-- Table: sajda_ayahs
-- ============================================================================
CREATE TABLE sajda_ayahs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    sajda_type TEXT,                     -- نوع السجدة (واجبة/مستحبة)
    sajda_number INTEGER,                -- رقم السجدة (1-15)
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(surah_id, ayah_id)
);

-- ============================================================================
-- 12. جدول المواضيع
-- Table: topics
-- ============================================================================
CREATE TABLE topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,           -- اسم الموضوع
    description TEXT,                    -- وصف الموضوع
    category TEXT                        -- التصنيف
);

-- ============================================================================
-- 13. جدول ربط المواضيع بالآيات
-- Table: topics_verses
-- ============================================================================
CREATE TABLE topics_verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id),
    UNIQUE(topic_id, surah_id, ayah_id)
);

-- ============================================================================
-- 14. جدول العلامات المرجعية
-- Table: bookmarks
-- ============================================================================
CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surah_id INTEGER NOT NULL,
    ayah_id INTEGER NOT NULL,
    note TEXT,                           -- ملاحظة المستخدم
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    color TEXT,                          -- لون العلامة
    category TEXT,                       -- تصنيف العلامة
    FOREIGN KEY (surah_id) REFERENCES surahs_info(id)
);

-- ============================================================================
-- 15. جدول إعدادات المستخدم
-- Table: user_settings
-- ============================================================================
CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT NOT NULL UNIQUE,    -- مفتاح الإعداد
    setting_value TEXT,                  -- قيمة الإعداد
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- الفهارس لتحسين الأداء
-- Indexes for Performance
-- ============================================================================

-- فهرس البحث في النص القرآني
CREATE INDEX idx_quran_text_surah_ayah ON quran_text(surah_id, ayah_id);
CREATE INDEX idx_quran_text_search ON quran_text(text);

-- فهرس البحث في التجويد
CREATE INDEX idx_tajweed_surah_ayah ON quran_tajweed(surah_id, ayah_id);

-- فهرس البحث في التفاسير
CREATE INDEX idx_tafsir_muyassar_surah_ayah ON tafsir_muyassar(surah_id, ayah_id);
CREATE INDEX idx_tafsir_saadi_surah_ayah ON tafsir_saadi(surah_id, ayah_id);
CREATE INDEX idx_tafsir_baghawi_surah_ayah ON tafsir_baghawi(surah_id, ayah_id);

-- فهرس البحث في الترجمات
CREATE INDEX idx_translation_en_surah_ayah ON translation_english(surah_id, ayah_id);
CREATE INDEX idx_translation_fr_surah_ayah ON translation_french(surah_id, ayah_id);

-- فهرس البحث في الإعراب والصرف
CREATE INDEX idx_irab_surah_ayah ON irab(surah_id, ayah_id);
CREATE INDEX idx_sarf_surah_ayah ON sarf(surah_id, ayah_id);

-- فهرس للمواضيع
CREATE INDEX idx_topics_verses_topic ON topics_verses(topic_id);
CREATE INDEX idx_topics_verses_verse ON topics_verses(surah_id, ayah_id);

-- فهرس للعلامات المرجعية
CREATE INDEX idx_bookmarks_surah_ayah ON bookmarks(surah_id, ayah_id);
CREATE INDEX idx_bookmarks_created ON bookmarks(created_at);

-- ============================================================================
-- بيانات أولية: معلومات السور (114 سورة)
-- Initial Data: Surahs Information
-- ============================================================================

INSERT INTO surahs_info (id, name_ar, ayahs_count, type, name_en, revelation_order) VALUES
(1, 'الفاتحة', 7, 'مكية', 'Al-Fatiha', 5),
(2, 'البقرة', 286, 'مدنية', 'Al-Baqarah', 87),
(3, 'آل عمران', 200, 'مدنية', 'Aal-e-Imran', 89),
(4, 'النساء', 176, 'مدنية', 'An-Nisa', 92),
(5, 'المائدة', 120, 'مدنية', 'Al-Ma\'idah', 112),
(6, 'الأنعام', 165, 'مكية', 'Al-An\'am', 55),
(7, 'الأعراف', 206, 'مكية', 'Al-A\'raf', 39),
(8, 'الأنفال', 75, 'مدنية', 'Al-Anfal', 88),
(9, 'التوبة', 129, 'مدنية', 'At-Tawbah', 113),
(10, 'يونس', 109, 'مكية', 'Yunus', 51),
(11, 'هود', 123, 'مكية', 'Hud', 52),
(12, 'يوسف', 111, 'مكية', 'Yusuf', 53),
(13, 'الرعد', 43, 'مدنية', 'Ar-Ra\'d', 96),
(14, 'إبراهيم', 52, 'مكية', 'Ibrahim', 72),
(15, 'الحجر', 99, 'مكية', 'Al-Hijr', 54),
(16, 'النحل', 128, 'مكية', 'An-Nahl', 70),
(17, 'الإسراء', 111, 'مكية', 'Al-Isra', 50),
(18, 'الكهف', 110, 'مكية', 'Al-Kahf', 69),
(19, 'مريم', 98, 'مكية', 'Maryam', 44),
(20, 'طه', 135, 'مكية', 'Taha', 45),
(21, 'الأنبياء', 112, 'مكية', 'Al-Anbya', 73),
(22, 'الحج', 78, 'مدنية', 'Al-Hajj', 103),
(23, 'المؤمنون', 118, 'مكية', 'Al-Mu\'minun', 74),
(24, 'النور', 64, 'مدنية', 'An-Nur', 102),
(25, 'الفرقان', 77, 'مكية', 'Al-Furqan', 42),
(26, 'الشعراء', 227, 'مكية', 'Ash-Shu\'ara', 47),
(27, 'النمل', 93, 'مكية', 'An-Naml', 48),
(28, 'القصص', 88, 'مكية', 'Al-Qasas', 49),
(29, 'العنكبوت', 69, 'مكية', 'Al-Ankabut', 85),
(30, 'الروم', 60, 'مكية', 'Ar-Rum', 84),
(31, 'لقمان', 34, 'مكية', 'Luqman', 57),
(32, 'السجدة', 30, 'مكية', 'As-Sajdah', 75),
(33, 'الأحزاب', 73, 'مدنية', 'Al-Ahzab', 90),
(34, 'سبأ', 54, 'مكية', 'Saba', 58),
(35, 'فاطر', 45, 'مكية', 'Fatir', 43),
(36, 'يس', 83, 'مكية', 'Ya-Sin', 41),
(37, 'الصافات', 182, 'مكية', 'As-Saffat', 56),
(38, 'ص', 88, 'مكية', 'Sad', 38),
(39, 'الزمر', 75, 'مكية', 'Az-Zumar', 59),
(40, 'غافر', 85, 'مكية', 'Ghafir', 60),
(41, 'فصلت', 54, 'مكية', 'Fussilat', 61),
(42, 'الشورى', 53, 'مكية', 'Ash-Shuraa', 62),
(43, 'الزخرف', 89, 'مكية', 'Az-Zukhruf', 63),
(44, 'الدخان', 59, 'مكية', 'Ad-Dukhan', 64),
(45, 'الجاثية', 37, 'مكية', 'Al-Jathiyah', 65),
(46, 'الأحقاف', 35, 'مكية', 'Al-Ahqaf', 66),
(47, 'محمد', 38, 'مدنية', 'Muhammad', 95),
(48, 'الفتح', 29, 'مدنية', 'Al-Fath', 111),
(49, 'الحجرات', 18, 'مدنية', 'Al-Hujurat', 106),
(50, 'ق', 45, 'مكية', 'Qaf', 34),
(51, 'الذاريات', 60, 'مكية', 'Adh-Dhariyat', 67),
(52, 'الطور', 49, 'مكية', 'At-Tur', 76),
(53, 'النجم', 62, 'مكية', 'An-Najm', 23),
(54, 'القمر', 55, 'مكية', 'Al-Qamar', 37),
(55, 'الرحمن', 78, 'مدنية', 'Ar-Rahman', 97),
(56, 'الواقعة', 96, 'مكية', 'Al-Waqi\'ah', 46),
(57, 'الحديد', 29, 'مدنية', 'Al-Hadid', 94),
(58, 'المجادلة', 22, 'مدنية', 'Al-Mujadila', 105),
(59, 'الحشر', 24, 'مدنية', 'Al-Hashr', 101),
(60, 'الممتحنة', 13, 'مدنية', 'Al-Mumtahanah', 91),
(61, 'الصف', 14, 'مدنية', 'As-Saf', 109),
(62, 'الجمعة', 11, 'مدنية', 'Al-Jumu\'ah', 110),
(63, 'المنافقون', 11, 'مدنية', 'Al-Munafiqun', 104),
(64, 'التغابن', 18, 'مدنية', 'At-Taghabun', 108),
(65, 'الطلاق', 12, 'مدنية', 'At-Talaq', 99),
(66, 'التحريم', 12, 'مدنية', 'At-Tahrim', 107),
(67, 'الملك', 30, 'مكية', 'Al-Mulk', 77),
(68, 'القلم', 52, 'مكية', 'Al-Qalam', 2),
(69, 'الحاقة', 52, 'مكية', 'Al-Haqqah', 78),
(70, 'المعارج', 44, 'مكية', 'Al-Ma\'arij', 79),
(71, 'نوح', 28, 'مكية', 'Nuh', 71),
(72, 'الجن', 28, 'مكية', 'Al-Jinn', 40),
(73, 'المزمل', 20, 'مكية', 'Al-Muzzammil', 3),
(74, 'المدثر', 56, 'مكية', 'Al-Muddaththir', 4),
(75, 'القيامة', 40, 'مكية', 'Al-Qiyamah', 31),
(76, 'الإنسان', 31, 'مدنية', 'Al-Insan', 98),
(77, 'المرسلات', 50, 'مكية', 'Al-Mursalat', 33),
(78, 'النبأ', 40, 'مكية', 'An-Naba', 80),
(79, 'النازعات', 46, 'مكية', 'An-Nazi\'at', 81),
(80, 'عبس', 42, 'مكية', 'Abasa', 24),
(81, 'التكوير', 29, 'مكية', 'At-Takwir', 7),
(82, 'الانفطار', 19, 'مكية', 'Al-Infitar', 82),
(83, 'المطففين', 36, 'مكية', 'Al-Mutaffifin', 86),
(84, 'الانشقاق', 25, 'مكية', 'Al-Inshiqaq', 83),
(85, 'البروج', 22, 'مكية', 'Al-Buruj', 27),
(86, 'الطارق', 17, 'مكية', 'At-Tariq', 36),
(87, 'الأعلى', 19, 'مكية', 'Al-A\'la', 8),
(88, 'الغاشية', 26, 'مكية', 'Al-Ghashiyah', 68),
(89, 'الفجر', 30, 'مكية', 'Al-Fajr', 10),
(90, 'البلد', 20, 'مكية', 'Al-Balad', 35),
(91, 'الشمس', 15, 'مكية', 'Ash-Shams', 26),
(92, 'الليل', 21, 'مكية', 'Al-Lail', 9),
(93, 'الضحى', 11, 'مكية', 'Ad-Duhaa', 11),
(94, 'الشرح', 8, 'مكية', 'Ash-Sharh', 12),
(95, 'التين', 8, 'مكية', 'At-Tin', 28),
(96, 'العلق', 19, 'مكية', 'Al-Alaq', 1),
(97, 'القدر', 5, 'مكية', 'Al-Qadr', 25),
(98, 'البينة', 8, 'مدنية', 'Al-Bayyinah', 100),
(99, 'الزلزلة', 8, 'مدنية', 'Az-Zalzalah', 93),
(100, 'العاديات', 11, 'مكية', 'Al-Adiyat', 14),
(101, 'القارعة', 11, 'مكية', 'Al-Qari\'ah', 30),
(102, 'التكاثر', 8, 'مكية', 'At-Takathur', 16),
(103, 'العصر', 3, 'مكية', 'Al-Asr', 13),
(104, 'الهمزة', 9, 'مكية', 'Al-Humazah', 32),
(105, 'الفيل', 5, 'مكية', 'Al-Fil', 19),
(106, 'قريش', 4, 'مكية', 'Quraysh', 29),
(107, 'الماعون', 7, 'مكية', 'Al-Ma\'un', 17),
(108, 'الكوثر', 3, 'مكية', 'Al-Kawthar', 15),
(109, 'الكافرون', 6, 'مكية', 'Al-Kafirun', 18),
(110, 'النصر', 3, 'مدنية', 'An-Nasr', 114),
(111, 'المسد', 5, 'مكية', 'Al-Masad', 6),
(112, 'الإخلاص', 4, 'مكية', 'Al-Ikhlas', 22),
(113, 'الفلق', 5, 'مكية', 'Al-Falaq', 20),
(114, 'الناس', 6, 'مكية', 'An-Nas', 21);

-- ============================================================================
-- بيانات أولية: آيات السجدة (15 سجدة)
-- Initial Data: Prostration Verses
-- ============================================================================

INSERT INTO sajda_ayahs (surah_id, ayah_id, sajda_type, sajda_number) VALUES
(7, 206, 'مستحبة', 1),
(13, 15, 'مستحبة', 2),
(16, 50, 'مستحبة', 3),
(17, 109, 'مستحبة', 4),
(19, 58, 'مستحبة', 5),
(22, 18, 'مستحبة', 6),
(25, 60, 'مستحبة', 7),
(27, 26, 'مستحبة', 8),
(32, 15, 'واجبة', 9),
(38, 24, 'مستحبة', 10),
(41, 38, 'واجبة', 11),
(53, 62, 'واجبة', 12),
(84, 21, 'واجبة', 13),
(96, 19, 'مستحبة', 14),
(22, 77, 'مستحبة', 15);

-- ============================================================================
-- بيانات أولية: إعدادات افتراضية
-- Initial Data: Default Settings
-- ============================================================================

INSERT INTO user_settings (setting_key, setting_value) VALUES
('last_surah', '1'),
('last_ayah', '1'),
('font_size', '28'),
('show_tajweed', 'True'),
('theme', 'default');

-- ============================================================================
-- نهاية السكريبت
-- End of Script
-- ============================================================================

-- ملاحظات مهمة للمستخدم:
-- Important Notes:
-- ============================================================================
-- 1. يحتوي هذا السكريبت على البنية الأساسية وبيانات السور فقط
-- 2. يجب إضافة بيانات الآيات القرآنية من المصادر المتاحة
-- 3. أسماء الجداول والأعمدة تطابق بدقة ما في الكود
-- 4. يمكن البدء بإضافة البيانات تدريجياً لكل جدول
-- ============================================================================

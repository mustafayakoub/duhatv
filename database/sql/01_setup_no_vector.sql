-- ═══════════════════════════════════════════════════════════════
-- 🚀 إعداد قاعدة البيانات القرآنية الهرمية الذكية (بدون pgvector)
-- ═══════════════════════════════════════════════════════════════
-- الإصدار: 1.0.0
-- التاريخ: 2025-10-30
-- PostgreSQL 15+
-- ملاحظة: pgvector معطل مؤقتاً (يمكن إضافته لاحقاً)
-- ═══════════════════════════════════════════════════════════════

-- إنشاء قاعدة البيانات
CREATE DATABASE quran_hierarchical_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    TEMPLATE = template0;

COMMENT ON DATABASE quran_hierarchical_db IS
'قاعدة البيانات القرآنية الهرمية الشاملة - Quran Hierarchical Encyclopedia Database';

-- الاتصال بقاعدة البيانات
\c quran_hierarchical_db

-- ═══════════════════════════════════════════════════════════════
-- تفعيل الامتدادات (Extensions)
-- ═══════════════════════════════════════════════════════════════

-- 1. UUID Generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"
SCHEMA public
VERSION "1.1";

COMMENT ON EXTENSION "uuid-ossp" IS
'لتوليد معرفات UUID فريدة عالمياً';

-- 2. pgcrypto (للتشفير)
CREATE EXTENSION IF NOT EXISTS "pgcrypto"
SCHEMA public;

COMMENT ON EXTENSION "pgcrypto" IS
'دوال التشفير (لكلمات المرور وغيرها)';

-- 3. Vector Extension (تم تعطيله مؤقتاً)
-- CREATE EXTENSION IF NOT EXISTS "vector" SCHEMA public;
-- سيتم إضافته لاحقاً عند توفر الإنترنت

-- 4. pg_trgm (للبحث الغامض)
CREATE EXTENSION IF NOT EXISTS "pg_trgm"
SCHEMA public;

COMMENT ON EXTENSION "pg_trgm" IS
'دعم البحث الغامض والمتشابه (Fuzzy Search)';

-- 5. unaccent (لإزالة التشكيل)
CREATE EXTENSION IF NOT EXISTS "unaccent"
SCHEMA public;

COMMENT ON EXTENSION "unaccent" IS
'إزالة التشكيل والحركات من النصوص';

-- ═══════════════════════════════════════════════════════════════
-- إنشاء المخططات (Schemas)
-- ═══════════════════════════════════════════════════════════════

-- 1. المخطط الرئيسي للقرآن
CREATE SCHEMA IF NOT EXISTS quran
    AUTHORIZATION postgres;

COMMENT ON SCHEMA quran IS
'المخطط الرئيسي لجداول القرآن الكريم';

-- 2. مخطط التحليلات والإحصائيات
CREATE SCHEMA IF NOT EXISTS analytics
    AUTHORIZATION postgres;

COMMENT ON SCHEMA analytics IS
'Views والتحليلات والإحصائيات';

-- 3. مخطط المجتمع
CREATE SCHEMA IF NOT EXISTS community
    AUTHORIZATION postgres;

COMMENT ON SCHEMA community IS
'جداول المستخدمين والتفضيلات والمشاركات';

-- ═══════════════════════════════════════════════════════════════
-- إنشاء الأنواع المخصصة (Custom Types)
-- ═══════════════════════════════════════════════════════════════

-- 1. نوع الوحي
CREATE TYPE quran.revelation_type AS ENUM ('meccan', 'medinan', 'mixed');

-- 2. الموقع في القرآن
CREATE TYPE quran.word_pos AS ENUM (
    'noun',           -- اسم
    'verb',           -- فعل
    'particle',       -- حرف
    'pronoun',        -- ضمير
    'proper_noun',    -- علم
    'adjective'       -- صفة
);

-- 3. حالة الإعراب
CREATE TYPE quran.word_case AS ENUM (
    'nominative',     -- مرفوع
    'accusative',     -- منصوب
    'genitive',       -- مجرور
    'jussive'         -- مجزوم
);

-- 4. نوع الجذر
CREATE TYPE quran.root_type AS ENUM (
    'trilateral',     -- ثلاثي
    'quadrilateral',  -- رباعي
    'quinqueliteral'  -- خماسي
);

-- 5. نوع التفسير
CREATE TYPE quran.tafsir_type AS ENUM (
    'linguistic',     -- لغوي
    'juristic',       -- فقهي
    'theological',    -- عقدي
    'mystical',       -- صوفي
    'modern',         -- معاصر
    'classical'       -- كلاسيكي
);

-- 6. مذهب المفسر
CREATE TYPE quran.mufassir_school AS ENUM (
    'sunni_hanafi',
    'sunni_maliki',
    'sunni_shafii',
    'sunni_hanbali',
    'shia_jafari',
    'ibadi',
    'modern'
);

-- 7. عصر المفسر
CREATE TYPE quran.mufassir_era AS ENUM (
    'classical',      -- كلاسيكي (القرون الأولى)
    'medieval',       -- وسيط
    'modern',         -- حديث
    'contemporary'    -- معاصر
);

-- 8. نوع السبب (أسباب النزول)
CREATE TYPE quran.revelation_reason_type AS ENUM (
    'event',          -- حدث
    'question',       -- سؤال
    'situation',      -- موقف
    'command'         -- أمر
);

-- 9. مستوى الموضوع
CREATE TYPE quran.topic_level AS ENUM (
    'primary',        -- رئيسي
    'secondary',      -- فرعي
    'tertiary'        -- تفصيلي
);

-- 10. نوع القراءة
CREATE TYPE quran.qiraa_category AS ENUM (
    'mutawatir',      -- متواترة
    'mashhur',        -- مشهورة
    'ahad',           -- آحاد
    'shadh'           -- شاذة
);

-- 11. نوع الصوت
CREATE TYPE quran.audio_quality AS ENUM (
    'low',            -- منخفضة 32-64kbps
    'medium',         -- متوسطة 64-128kbps
    'high',           -- عالية 128-192kbps
    'lossless'        -- بدون فقدان FLAC/WAV
);

-- 12. حالة التلاوة
CREATE TYPE quran.recitation_status AS ENUM (
    'active',         -- نشطة
    'archived',       -- مؤرشفة
    'pending',        -- قيد المراجعة
    'removed'         -- محذوفة
);

-- 13. نوع الإشارة المرجعية
CREATE TYPE community.bookmark_type AS ENUM (
    'ayah',           -- آية
    'surah',          -- سورة
    'page',           -- صفحة
    'juz',            -- جزء
    'hizb'            -- حزب
);

-- 14. حالة التعليق
CREATE TYPE community.annotation_status AS ENUM (
    'private',        -- خاص
    'shared',         -- مشارك
    'public'          -- عام
);

-- 15. مستوى المستخدم
CREATE TYPE community.user_role AS ENUM (
    'reader',         -- قارئ
    'contributor',    -- مساهم
    'moderator',      -- مشرف
    'admin'           -- مدير
);

-- ═══════════════════════════════════════════════════════════════
-- دوال مساعدة
-- ═══════════════════════════════════════════════════════════════

-- دالة إزالة التشكيل
CREATE OR REPLACE FUNCTION quran.remove_tashkeel(text_with_tashkeel TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN regexp_replace(
        text_with_tashkeel,
        '[\u064B-\u0652\u0670\u0640]',
        '',
        'g'
    );
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION quran.remove_tashkeel(TEXT) IS
'إزالة جميع التشكيلات والحركات من النص العربي';

-- دالة تطبيع النص العربي
CREATE OR REPLACE FUNCTION quran.normalize_arabic(arabic_text TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN regexp_replace(
        regexp_replace(
            regexp_replace(arabic_text, '[إأآ]', 'ا', 'g'),
            '[ىي]', 'ي', 'g'
        ),
        '[ةه]', 'ه', 'g'
    );
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION quran.normalize_arabic(TEXT) IS
'تطبيع النص العربي (توحيد الألف والياء والهاء)';

-- ═══════════════════════════════════════════════════════════════
-- الأدوار والصلاحيات
-- ═══════════════════════════════════════════════════════════════

-- دور القراءة فقط
CREATE ROLE quran_readonly;
GRANT USAGE ON SCHEMA quran TO quran_readonly;
GRANT USAGE ON SCHEMA analytics TO quran_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA quran TO quran_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO quran_readonly;

-- دور القراءة والكتابة (للتطبيقات)
CREATE ROLE quran_app;
GRANT USAGE ON SCHEMA quran TO quran_app;
GRANT USAGE ON SCHEMA analytics TO quran_app;
GRANT USAGE ON SCHEMA community TO quran_app;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA community TO quran_app;
GRANT SELECT ON ALL TABLES IN SCHEMA quran TO quran_app;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO quran_app;

COMMENT ON ROLE quran_readonly IS 'دور للقراءة فقط';
COMMENT ON ROLE quran_app IS 'دور للتطبيقات (قراءة القرآن + كتابة في جداول المجتمع)';

-- ═══════════════════════════════════════════════════════════════
-- النهاية
-- ═══════════════════════════════════════════════════════════════

\echo '✅ تم الإعداد الأولي بنجاح'
\echo '📊 الامتدادات: uuid-ossp, pgcrypto, pg_trgm, unaccent'
\echo '📂 المخططات: quran, analytics, community'
\echo '🔖 الأنواع المخصصة: 15 نوع'
\echo '🔐 الأدوار: quran_readonly, quran_app'
\echo ''
\echo '⚠️  ملاحظة: pgvector معطل مؤقتاً (يمكن إضافته لاحقاً)'

-- ═══════════════════════════════════════════════════════════════
-- 🚀 إعداد قاعدة البيانات القرآنية الهرمية الذكية
-- ═══════════════════════════════════════════════════════════════
-- الإصدار: 1.0.0
-- التاريخ: 2025-10-30
-- PostgreSQL 15+
-- ═══════════════════════════════════════════════════════════════

-- إنشاء قاعدة البيانات
CREATE DATABASE quran_hierarchical_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ar_EG.UTF-8'
    LC_CTYPE = 'ar_EG.UTF-8'
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

-- 3. Vector Extension (للبحث الدلالي)
CREATE EXTENSION IF NOT EXISTS "vector"
SCHEMA public;

COMMENT ON EXTENSION "vector" IS
'دعم Vector Embeddings للبحث الدلالي المتقدم';

-- 4. Full-Text Search (للبحث النصي)
-- مُضمّن في PostgreSQL، لكن نحتاج إعداد القواميس

-- 5. pg_trgm (للبحث الضبابي)
CREATE EXTENSION IF NOT EXISTS "pg_trgm"
SCHEMA public;

COMMENT ON EXTENSION "pg_trgm" IS
'دعم البحث الضبابي (Fuzzy Search) باستخدام Trigrams';

-- 6. unaccent (لإزالة التشكيل في البحث)
CREATE EXTENSION IF NOT EXISTS "unaccent"
SCHEMA public;

COMMENT ON EXTENSION "unaccent" IS
'إزالة علامات التشكيل العربية للبحث المرن';

-- ═══════════════════════════════════════════════════════════════
-- إنشاء Schema منفصل (اختياري)
-- ═══════════════════════════════════════════════════════════════

CREATE SCHEMA IF NOT EXISTS quran;
COMMENT ON SCHEMA quran IS 'جميع جداول القرآن الكريم';

CREATE SCHEMA IF NOT EXISTS analytics;
COMMENT ON SCHEMA analytics IS 'جداول التحليلات والإحصائيات';

CREATE SCHEMA IF NOT EXISTS community;
COMMENT ON SCHEMA community IS 'جداول المستخدمين والمساهمات';

-- تعيين مسار البحث الافتراضي
SET search_path TO quran, public;

-- ═══════════════════════════════════════════════════════════════
-- إنشاء الأنواع المخصصة (Custom Types)
-- ═══════════════════════════════════════════════════════════════

-- 1. نوع النزول
CREATE TYPE quran.revelation_type AS ENUM (
    'meccan',      -- مكي
    'medinan',     -- مدني
    'mixed'        -- مختلط (بعض الآيات مكية وبعضها مدني)
);

COMMENT ON TYPE quran.revelation_type IS
'أنواع نزول السور: مكي، مدني، مختلط';

-- 2. نوع السجدة
CREATE TYPE quran.sajda_type AS ENUM (
    'obligatory',  -- سجدة واجبة
    'recommended'  -- سجدة مستحبة
);

-- 3. نوع الكلمة (Part of Speech)
CREATE TYPE quran.word_pos AS ENUM (
    'noun',        -- اسم
    'verb',        -- فعل
    'particle',    -- حرف
    'pronoun',     -- ضمير
    'proper_noun', -- اسم علم
    'adjective'    -- صفة
);

-- 4. الجنس
CREATE TYPE quran.gender_type AS ENUM (
    'masculine',   -- مذكر
    'feminine'     -- مؤنث
);

-- 5. العدد
CREATE TYPE quran.number_type AS ENUM (
    'singular',    -- مفرد
    'dual',        -- مثنى
    'plural'       -- جمع
);

-- 6. الحالة الإعرابية
CREATE TYPE quran.case_type AS ENUM (
    'nominative',  -- رفع
    'accusative',  -- نصب
    'genitive'     -- جر
);

-- 7. الزمن (للأفعال)
CREATE TYPE quran.tense_type AS ENUM (
    'past',        -- ماض
    'present',     -- مضارع
    'imperative'   -- أمر
);

-- 8. البناء (للأفعال)
CREATE TYPE quran.voice_type AS ENUM (
    'active',      -- مبني للمعلوم
    'passive'      -- مبني للمجهول
);

-- 9. نوع الجذر
CREATE TYPE quran.root_type AS ENUM (
    'triliteral',  -- ثلاثي
    'quadriliteral', -- رباعي
    'quinqueliteral' -- خماسي
);

-- 10. نوع التفسير
CREATE TYPE quran.tafsir_type AS ENUM (
    'linguistic',   -- لغوي
    'juristic',     -- فقهي
    'historical',   -- تاريخي
    'scientific',   -- علمي
    'mystical',     -- إشاري/صوفي
    'comprehensive' -- شامل
);

-- 11. نوع الترجمة
CREATE TYPE quran.translation_type AS ENUM (
    'literal',      -- حرفية
    'interpretive', -- تفسيرية
    'free'          -- حرة
);

-- 12. درجة صحة الرواية
CREATE TYPE quran.authenticity_level AS ENUM (
    'sahih',        -- صحيح
    'hasan',        -- حسن
    'daif',         -- ضعيف
    'mawdu',        -- موضوع
    'unknown'       -- غير معروف
);

-- 13. أسلوب التلاوة
CREATE TYPE quran.recitation_style AS ENUM (
    'murattal',     -- مرتل
    'mujawwad',     -- مجود
    'muallim'       -- معلم
);

-- 14. دور المستخدم
CREATE TYPE community.user_role AS ENUM (
    'user',         -- مستخدم عادي
    'contributor',  -- مساهم
    'researcher',   -- باحث
    'moderator',    -- مشرف
    'admin'         -- مدير
);

-- 15. حالة المساهمة
CREATE TYPE community.contribution_status AS ENUM (
    'pending',      -- قيد المراجعة
    'approved',     -- مقبول
    'rejected',     -- مرفوض
    'needs_revision' -- يحتاج مراجعة
);

-- ═══════════════════════════════════════════════════════════════
-- إنشاء قاموس بحث نصي للغة العربية
-- ═══════════════════════════════════════════════════════════════

-- استخدام القاموس العربي المدمج
-- يمكن تحسينه لاحقاً بقاموس مخصص للنصوص القرآنية

CREATE TEXT SEARCH CONFIGURATION quran.arabic_quran (COPY = arabic);

COMMENT ON TEXT SEARCH CONFIGURATION quran.arabic_quran IS
'قاموس بحث نصي مخصص للنصوص القرآنية';

-- ═══════════════════════════════════════════════════════════════
-- إنشاء دوال مساعدة عامة
-- ═══════════════════════════════════════════════════════════════

-- دالة لتوليد UUID v4
CREATE OR REPLACE FUNCTION quran.generate_uuid()
RETURNS UUID AS $$
BEGIN
    RETURN uuid_generate_v4();
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION quran.generate_uuid() IS
'توليد معرف UUID فريد';

-- دالة لتحديث ختم updated_at تلقائياً
CREATE OR REPLACE FUNCTION quran.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION quran.update_updated_at_column() IS
'Trigger function لتحديث عمود updated_at تلقائياً عند UPDATE';

-- دالة لحساب عدد الكلمات في نص
CREATE OR REPLACE FUNCTION quran.count_words(text_input TEXT)
RETURNS INTEGER AS $$
BEGIN
    RETURN array_length(regexp_split_to_array(trim(text_input), E'\\s+'), 1);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION quran.count_words(TEXT) IS
'حساب عدد الكلمات في نص معين';

-- دالة لحساب عدد الحروف (بدون تشكيل)
CREATE OR REPLACE FUNCTION quran.count_letters(text_input TEXT)
RETURNS INTEGER AS $$
DECLARE
    clean_text TEXT;
BEGIN
    -- إزالة المسافات والتشكيل
    clean_text := regexp_replace(text_input, E'[\\s\\u064B-\\u0652\\u0670]', '', 'g');
    RETURN length(clean_text);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION quran.count_letters(TEXT) IS
'حساب عدد الحروف (بدون مسافات أو تشكيل)';

-- دالة لإزالة التشكيل من النص
CREATE OR REPLACE FUNCTION quran.remove_tashkeel(text_input TEXT)
RETURNS TEXT AS $$
BEGIN
    -- إزالة علامات التشكيل العربية (Unicode: U+064B to U+0652 + U+0670)
    RETURN regexp_replace(text_input, E'[\\u064B-\\u0652\\u0670]', '', 'g');
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION quran.remove_tashkeel(TEXT) IS
'إزالة علامات التشكيل من النص العربي';

-- ═══════════════════════════════════════════════════════════════
-- إعدادات الأداء
-- ═══════════════════════════════════════════════════════════════

-- زيادة shared_buffers (يتم في postgresql.conf)
-- shared_buffers = 2GB (مثال)

-- تفعيل parallel queries
SET max_parallel_workers_per_gather = 4;
SET max_parallel_workers = 8;

-- تحسين إعدادات الذاكرة
SET work_mem = '256MB';
SET maintenance_work_mem = '1GB';

-- تحسين cost planner
SET random_page_cost = 1.1; -- لـ SSD
SET effective_cache_size = '4GB';

-- ═══════════════════════════════════════════════════════════════
-- إنشاء مستخدمين ومجموعات الصلاحيات
-- ═══════════════════════════════════════════════════════════════

-- مستخدم للقراءة فقط
CREATE ROLE quran_readonly;
GRANT CONNECT ON DATABASE quran_hierarchical_db TO quran_readonly;
GRANT USAGE ON SCHEMA quran, analytics TO quran_readonly;
-- سنمنح SELECT لاحقاً بعد إنشاء الجداول

-- مستخدم للكتابة (للتطبيقات)
CREATE ROLE quran_readwrite;
GRANT CONNECT ON DATABASE quran_hierarchical_db TO quran_readwrite;
GRANT USAGE, CREATE ON SCHEMA quran, analytics, community TO quran_readwrite;
-- سنمنح SELECT, INSERT, UPDATE لاحقاً

-- ═══════════════════════════════════════════════════════════════
-- تفعيل logging للتدقيق
-- ═══════════════════════════════════════════════════════════════

ALTER DATABASE quran_hierarchical_db SET log_statement = 'mod';
ALTER DATABASE quran_hierarchical_db SET log_duration = on;

-- ═══════════════════════════════════════════════════════════════
COMMIT;

-- ═══════════════════════════════════════════════════════════════
-- ✅ تم إعداد قاعدة البيانات بنجاح!
-- ═══════════════════════════════════════════════════════════════
-- الخطوة التالية: تشغيل 02_level0_core_tables.sql
-- ═══════════════════════════════════════════════════════════════

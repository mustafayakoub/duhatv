#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت إنشاء القواعد الأربعة للمشروع القرآني
====================================================

يقوم بإنشاء:
1. SURAHS_DATABASE.db - قاعدة السور وعلومها
2. AYAHS_DATABASE.db - قاعدة الآيات والتفاسير
3. WORDS_DATABASE.db - قاعدة الكلمات والإعراب
4. LETTERS_DATABASE.db - قاعدة إحصائيات الحروف (اختياري)

الاستخدام:
    python3 create_databases.py
    python3 create_databases.py --skip-letters  # بدون قاعدة الحروف

المؤلف: مشروع القرآن الرقمي
التاريخ: 3 نوفمبر 2025
"""

import sqlite3
import os
import sys
import argparse
from datetime import datetime


class DatabaseCreator:
    """منشئ القواعد الأربعة"""

    def __init__(self, output_dir="databases"):
        """
        Args:
            output_dir: مجلد حفظ القواعد
        """
        self.output_dir = output_dir
        self.databases = {}

        # إنشاء المجلد إن لم يكن موجوداً
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"✅ تم إنشاء مجلد: {output_dir}")

    def create_surahs_database(self):
        """إنشاء قاعدة السور"""
        db_path = os.path.join(self.output_dir, "SURAHS_DATABASE.db")
        print(f"\n🕌 إنشاء قاعدة السور: {db_path}")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. جدول السور الرئيسي
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS surahs (
            surah_id INTEGER PRIMARY KEY,
            surah_number INTEGER NOT NULL UNIQUE,

            -- الأسماء
            name_arabic TEXT NOT NULL,
            name_simple TEXT NOT NULL,
            name_english TEXT NOT NULL,
            name_transliteration TEXT,

            -- التصنيف
            revelation_type TEXT CHECK(revelation_type IN ('Meccan', 'Medinan')),
            revelation_order INTEGER,

            -- الإحصائيات
            ayah_count INTEGER NOT NULL,
            word_count INTEGER,
            letter_count INTEGER,

            -- الحروف المقطعة
            opening_letters TEXT,

            -- الموضوع
            main_theme_ar TEXT,
            main_theme_en TEXT,

            -- ملاحظات
            notes TEXT,

            -- التواريخ
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 2. جدول الأسماء المتعددة
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS surah_names (
            name_id INTEGER PRIMARY KEY AUTOINCREMENT,
            surah_id INTEGER NOT NULL,
            name_arabic TEXT NOT NULL,
            name_type TEXT DEFAULT 'alternative',
            reference TEXT,

            FOREIGN KEY (surah_id) REFERENCES surahs(surah_id)
        )
        """)

        # 3. جدول الموضوعات
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS surah_themes (
            theme_id INTEGER PRIMARY KEY AUTOINCREMENT,
            surah_id INTEGER NOT NULL,
            theme_arabic TEXT NOT NULL,
            theme_english TEXT,
            description TEXT,

            FOREIGN KEY (surah_id) REFERENCES surahs(surah_id)
        )
        """)

        # 4. جدول أسباب النزول
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS revelation_occasions (
            occasion_id INTEGER PRIMARY KEY AUTOINCREMENT,
            surah_id INTEGER,
            ayah_start INTEGER,
            ayah_end INTEGER,
            occasion_arabic TEXT NOT NULL,
            occasion_english TEXT,
            source TEXT,
            authenticity TEXT,

            FOREIGN KEY (surah_id) REFERENCES surahs(surah_id)
        )
        """)

        # 5. جدول الإحصائيات المتقدمة
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS surah_statistics (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            surah_id INTEGER NOT NULL UNIQUE,

            unique_words INTEGER DEFAULT 0,
            repeated_words INTEGER DEFAULT 0,
            unique_letters INTEGER DEFAULT 0,

            most_common_letter TEXT,
            least_common_letter TEXT,
            most_repeated_word TEXT,
            most_repeated_word_count INTEGER DEFAULT 0,

            FOREIGN KEY (surah_id) REFERENCES surahs(surah_id)
        )
        """)

        # إنشاء الفهارس
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_surahs_name ON surahs(name_simple)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_surahs_type ON surahs(revelation_type)")

        conn.commit()
        conn.close()

        self.databases['surahs'] = db_path
        print(f"✅ تم إنشاء قاعدة السور بنجاح!")
        print(f"   📊 5 جداول: surahs, surah_names, surah_themes, revelation_occasions, surah_statistics")

    def create_ayahs_database(self):
        """إنشاء قاعدة الآيات"""
        db_path = os.path.join(self.output_dir, "AYAHS_DATABASE.db")
        print(f"\n📖 إنشاء قاعدة الآيات: {db_path}")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. جدول الآيات الرئيسي
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ayahs (
            ayah_id INTEGER PRIMARY KEY,
            surah_id INTEGER NOT NULL,
            ayah_number INTEGER NOT NULL,

            -- النص
            ayah_text TEXT NOT NULL,
            ayah_text_simple TEXT NOT NULL,
            ayah_text_uthmani TEXT,

            -- الإحصائيات
            word_count INTEGER NOT NULL,
            letter_count INTEGER NOT NULL,

            -- التصنيف
            juz INTEGER CHECK(juz BETWEEN 1 AND 30),
            hizb INTEGER CHECK(hizb BETWEEN 1 AND 60),
            page_mushaf INTEGER,

            -- السجدة
            sajdah_type TEXT CHECK(sajdah_type IN ('recommended', 'obligatory', NULL)),

            -- البحث
            search_text TEXT,

            -- ملاحظات
            notes TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(surah_id, ayah_number)
        )
        """)

        # 2. جدول التفاسير
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tafsir (
            tafsir_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ayah_id INTEGER NOT NULL,
            tafsir_name TEXT NOT NULL,
            tafsir_text TEXT NOT NULL,
            language TEXT DEFAULT 'ar',
            author TEXT,
            source TEXT,

            FOREIGN KEY (ayah_id) REFERENCES ayahs(ayah_id)
        )
        """)

        # 3. جدول الترجمات
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS translations (
            translation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ayah_id INTEGER NOT NULL,
            language_code TEXT NOT NULL,
            translation_text TEXT NOT NULL,
            translator_name TEXT,
            source TEXT,

            FOREIGN KEY (ayah_id) REFERENCES ayahs(ayah_id),
            UNIQUE(ayah_id, language_code, translator_name)
        )
        """)

        # 4. جدول موضوعات الآيات
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ayah_topics (
            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ayah_id INTEGER NOT NULL,
            topic_arabic TEXT NOT NULL,
            topic_english TEXT,
            category TEXT,

            FOREIGN KEY (ayah_id) REFERENCES ayahs(ayah_id)
        )
        """)

        # 5. جدول العلاقات بين الآيات
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ayah_relations (
            relation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ayah_id_1 INTEGER NOT NULL,
            ayah_id_2 INTEGER NOT NULL,
            relation_type TEXT NOT NULL,
            description TEXT,

            FOREIGN KEY (ayah_id_1) REFERENCES ayahs(ayah_id),
            FOREIGN KEY (ayah_id_2) REFERENCES ayahs(ayah_id)
        )
        """)

        # إنشاء الفهارس
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ayahs_surah ON ayahs(surah_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ayahs_juz ON ayahs(juz)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ayahs_search ON ayahs(search_text)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tafsir_ayah ON tafsir(ayah_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tafsir_name ON tafsir(tafsir_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_translations_ayah ON translations(ayah_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_translations_lang ON translations(language_code)")

        conn.commit()
        conn.close()

        self.databases['ayahs'] = db_path
        print(f"✅ تم إنشاء قاعدة الآيات بنجاح!")
        print(f"   📊 5 جداول: ayahs, tafsir, translations, ayah_topics, ayah_relations")

    def create_words_database(self):
        """إنشاء قاعدة الكلمات"""
        db_path = os.path.join(self.output_dir, "WORDS_DATABASE.db")
        print(f"\n📝 إنشاء قاعدة الكلمات: {db_path}")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. جدول الكلمات الرئيسي
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            word_id INTEGER PRIMARY KEY,
            surah_id INTEGER NOT NULL,
            ayah_id INTEGER NOT NULL,
            word_position INTEGER NOT NULL,

            -- النص
            word_text TEXT NOT NULL,
            word_simple TEXT NOT NULL,
            word_uthmani TEXT,

            -- التحليل اللغوي
            root TEXT,
            root_type TEXT,

            -- التصنيف
            word_type TEXT,
            word_category TEXT,

            -- الإحصائيات
            letter_count INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(ayah_id, word_position)
        )
        """)

        # 2. جدول الإعراب
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS irab (
            irab_id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,

            irab_text TEXT NOT NULL,
            irab_position TEXT,
            irab_case TEXT,
            irab_sign TEXT,

            source TEXT,
            notes TEXT,

            FOREIGN KEY (word_id) REFERENCES words(word_id)
        )
        """)

        # 3. جدول التحليل الصرفي
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS morphology (
            morph_id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,

            form TEXT,
            gender TEXT,
            person TEXT,
            tense TEXT,
            pattern TEXT,

            notes TEXT,

            FOREIGN KEY (word_id) REFERENCES words(word_id)
        )
        """)

        # 4. جدول معاني الكلمات
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS word_meanings (
            meaning_id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,
            language_code TEXT DEFAULT 'ar',
            meaning_text TEXT NOT NULL,
            context_usage TEXT,

            FOREIGN KEY (word_id) REFERENCES words(word_id)
        )
        """)

        # 5. جدول إحصائيات الكلمات
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS word_statistics (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_simple TEXT NOT NULL UNIQUE,

            total_count INTEGER DEFAULT 0,
            meccan_count INTEGER DEFAULT 0,
            medinan_count INTEGER DEFAULT 0,

            first_occurrence_ayah_id INTEGER,
            last_occurrence_ayah_id INTEGER,

            surahs_appeared TEXT
        )
        """)

        # إنشاء الفهارس
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_ayah ON words(ayah_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_root ON words(root)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_simple ON words(word_simple)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_type ON words(word_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_irab_word ON irab(word_id)")

        conn.commit()
        conn.close()

        self.databases['words'] = db_path
        print(f"✅ تم إنشاء قاعدة الكلمات بنجاح!")
        print(f"   📊 5 جداول: words, irab, morphology, word_meanings, word_statistics")

    def create_letters_database(self):
        """إنشاء قاعدة الحروف (اختياري)"""
        db_path = os.path.join(self.output_dir, "LETTERS_DATABASE.db")
        print(f"\n🔤 إنشاء قاعدة الحروف: {db_path}")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. جدول الحروف
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS letters (
            letter_id INTEGER PRIMARY KEY AUTOINCREMENT,
            letter TEXT NOT NULL UNIQUE,
            letter_name TEXT NOT NULL,
            letter_type TEXT,

            total_count INTEGER DEFAULT 0,
            in_words_count INTEGER DEFAULT 0,
            in_particles_count INTEGER DEFAULT 0
        )
        """)

        # 2. جدول مواقع الحروف
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS letter_positions (
            position_id INTEGER PRIMARY KEY AUTOINCREMENT,
            letter_id INTEGER NOT NULL,
            word_id INTEGER NOT NULL,
            position_in_word INTEGER NOT NULL,
            has_tashkeel BOOLEAN DEFAULT 0,
            tashkeel_type TEXT,

            FOREIGN KEY (letter_id) REFERENCES letters(letter_id)
        )
        """)

        # 3. جدول إحصائيات الحروف
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS letter_statistics (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            letter_id INTEGER NOT NULL UNIQUE,

            count_at_start INTEGER DEFAULT 0,
            count_at_middle INTEGER DEFAULT 0,
            count_at_end INTEGER DEFAULT 0,

            count_with_fatha INTEGER DEFAULT 0,
            count_with_damma INTEGER DEFAULT 0,
            count_with_kasra INTEGER DEFAULT 0,
            count_with_sukun INTEGER DEFAULT 0,
            count_with_shadda INTEGER DEFAULT 0,

            FOREIGN KEY (letter_id) REFERENCES letters(letter_id)
        )
        """)

        # إنشاء الفهارس
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_letters_name ON letters(letter)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_positions_letter ON letter_positions(letter_id)")

        conn.commit()
        conn.close()

        self.databases['letters'] = db_path
        print(f"✅ تم إنشاء قاعدة الحروف بنجاح!")
        print(f"   📊 3 جداول: letters, letter_positions, letter_statistics")

    def create_all(self, skip_letters=False):
        """إنشاء جميع القواعد"""
        print("="*70)
        print("🚀 بدء إنشاء القواعد الأربعة")
        print("="*70)

        self.create_surahs_database()
        self.create_ayahs_database()
        self.create_words_database()

        if not skip_letters:
            self.create_letters_database()
        else:
            print("\n⏭️  تم تخطي قاعدة الحروف")

        print("\n" + "="*70)
        print("✅ تم إنشاء جميع القواعد بنجاح!")
        print("="*70)
        print(f"\n📂 الموقع: {os.path.abspath(self.output_dir)}/")
        print(f"\n📊 القواعد المُنشأة:")
        for name, path in self.databases.items():
            size = os.path.getsize(path) / 1024  # KB
            print(f"   • {os.path.basename(path):30s} ({size:.2f} KB)")

        return self.databases


def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description="إنشاء القواعد الأربعة للمشروع القرآني",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
    python3 create_databases.py
    python3 create_databases.py --output-dir data/databases
    python3 create_databases.py --skip-letters
        """
    )

    parser.add_argument(
        '--output-dir',
        default='databases',
        help='مجلد حفظ القواعد (افتراضي: databases)'
    )

    parser.add_argument(
        '--skip-letters',
        action='store_true',
        help='تخطي إنشاء قاعدة الحروف'
    )

    args = parser.parse_args()

    try:
        creator = DatabaseCreator(output_dir=args.output_dir)
        databases = creator.create_all(skip_letters=args.skip_letters)

        print(f"\n🎉 النجاح! يمكنك الآن:")
        print(f"   1. استيراد البيانات باستخدام import_from_excel.py")
        print(f"   2. التحقق من البيانات باستخدام verify_data.py")

        return 0

    except Exception as e:
        print(f"\n❌ خطأ: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

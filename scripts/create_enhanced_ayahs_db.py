#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت إنشاء قاعدة بيانات الآيات المحسّنة
========================================

البنية الجديدة:
- دعم 23 إصدار مختلف من النص القرآني
- دعم القراءات المختلفة (حفص، ورش، قالون، إلخ)
- دعم أنواع النصوص المختلفة (عثماني، إملائي، مع/بدون تشكيل)
- تصميم معياري وقابل للتوسع

المؤلف: مشروع القرآن الرقمي
التاريخ: 4 نوفمبر 2025
"""

import sqlite3
import sys
from pathlib import Path


def create_enhanced_ayahs_database(db_path="databases/AYAHS_DATABASE_ENHANCED.db"):
    """
    إنشاء قاعدة بيانات الآيات المحسّنة مع دعم النصوص المتعددة

    البنية:
    1. ayahs - معلومات الآيات الأساسية
    2. text_versions - أنواع النصوص المتاحة (23 نوع)
    3. ayah_texts - النصوص الفعلية لكل آية بكل إصدار
    4. tafsir - التفاسير (جدول موسع)
    5. translations - الترجمات (جدول موسع)
    """

    print("="*70)
    print("🏗️  إنشاء قاعدة بيانات الآيات المحسّنة")
    print("="*70)

    # إنشاء المجلد إن لم يكن موجوداً
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # حذف القاعدة القديمة إن وجدت
    if db_path.exists():
        print(f"⚠️  حذف قاعدة البيانات القديمة: {db_path}")
        db_path.unlink()

    # الاتصال وإنشاء القاعدة الجديدة
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"\n📊 إنشاء الجداول...")

    # ========================================
    # الجدول 1: ayahs - معلومات الآيات الأساسية
    # ========================================
    cursor.execute("""
        CREATE TABLE ayahs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sura_no INTEGER NOT NULL,
            aya_no INTEGER NOT NULL,
            jozz INTEGER NOT NULL,
            page INTEGER NOT NULL,
            line_start INTEGER,
            line_end INTEGER,

            -- علاقة مع قاعدة السور
            -- FOREIGN KEY (sura_no) REFERENCES SURAHS_DATABASE.surahs(number)

            -- فهرس فريد لكل آية
            UNIQUE(sura_no, aya_no)
        )
    """)
    print("   ✅ ayahs - الآيات الأساسية")

    # فهارس للأداء
    cursor.execute("CREATE INDEX idx_ayahs_sura ON ayahs(sura_no)")
    cursor.execute("CREATE INDEX idx_ayahs_jozz ON ayahs(jozz)")
    cursor.execute("CREATE INDEX idx_ayahs_page ON ayahs(page)")

    # ========================================
    # الجدول 2: text_versions - أنواع النصوص
    # ========================================
    cursor.execute("""
        CREATE TABLE text_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_code TEXT NOT NULL UNIQUE,
            version_name_en TEXT NOT NULL,
            version_name_ar TEXT NOT NULL,
            qiraa TEXT,
            script_type TEXT,
            tashkeel_type TEXT,
            description TEXT,
            source_file TEXT,
            is_default BOOLEAN DEFAULT 0,

            -- معلومات إضافية
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✅ text_versions - أنواع النصوص")

    # إدراج الأنواع الـ 23 المتاحة
    versions = [
        # النص الأساسي - قراءة حفص
        ('hafs_smart_v8', 'Hafs Reading (Smart v8)', 'حفص - ذكي', 'حفص عن عاصم', 'عثماني', 'كامل', 'النص القرآني الأساسي بقراءة حفص', 'hafs_smart_v8.json', 1),

        # القراءات السبع الأخرى
        ('warsh', 'Warsh Reading', 'ورش', 'ورش عن نافع', 'عثماني', 'كامل', 'قراءة ورش عن نافع', 'warsh.txt', 0),
        ('qaloon', 'Qaloon Reading', 'قالون', 'قالون عن نافع', 'عثماني', 'كامل', 'قراءة قالون عن نافع', 'qaloon.txt', 0),
        ('aldori', 'Al-Dori Reading', 'الدوري', 'الدوري عن أبي عمرو', 'عثماني', 'كامل', 'قراءة الدوري عن أبي عمرو', 'aldori.txt', 0),
        ('alsosi', 'Al-Sosi Reading', 'السوسي', 'السوسي عن أبي عمرو', 'عثماني', 'كامل', 'قراءة السوسي عن أبي عمرو', 'alsosi.txt', 0),
        ('shobah', 'Sho\'bah Reading', 'شعبة', 'شعبة عن عاصم', 'عثماني', 'كامل', 'قراءة شعبة عن عاصم', 'shobah.txt', 0),
        ('khalaf', 'Khalaf Reading', 'خلف', 'خلف عن حمزة', 'عثماني', 'كامل', 'قراءة خلف عن حمزة', 'khalaf.txt', 0),
        ('khallad', 'Khallad Reading', 'خلاد', 'خلاد عن حمزة', 'عثماني', 'كامل', 'قراءة خلاد عن حمزة', 'khallad.txt', 0),

        # أنواع النصوص المختلفة
        ('uthmani_full', 'Uthmani Script (Full Tashkeel)', 'عثماني - تشكيل كامل', 'حفص', 'عثماني', 'كامل', 'الرسم العثماني مع تشكيل كامل', 'uthmani_full.txt', 0),
        ('uthmani_minimal', 'Uthmani Script (Minimal)', 'عثماني - تشكيل بسيط', 'حفص', 'عثماني', 'بسيط', 'الرسم العثماني مع تشكيل بسيط', 'uthmani_minimal.txt', 0),
        ('uthmani_none', 'Uthmani Script (No Tashkeel)', 'عثماني - بدون تشكيل', 'حفص', 'عثماني', 'بدون', 'الرسم العثماني بدون تشكيل', 'uthmani_none.txt', 0),

        ('imlaey_full', 'Imlaey Script (Full Tashkeel)', 'إملائي - تشكيل كامل', 'حفص', 'إملائي', 'كامل', 'الرسم الإملائي مع تشكيل كامل', 'imlaey_full.txt', 0),
        ('imlaey_minimal', 'Imlaey Script (Minimal)', 'إملائي - تشكيل بسيط', 'حفص', 'إملائي', 'بسيط', 'الرسم الإملائي مع تشكيل بسيط', 'imlaey_minimal.txt', 0),
        ('imlaey_none', 'Imlaey Script (No Tashkeel)', 'إملائي - بدون تشكيل', 'حفص', 'إملائي', 'بدون', 'الرسم الإملائي بدون تشكيل', 'imlaey_none.txt', 0),

        # نصوص خاصة
        ('amiri', 'Amiri Font Version', 'خط أميري', 'حفص', 'عثماني', 'كامل', 'نص محسن لخط أميري', 'amiri.txt', 0),
        ('simple', 'Simple Clean Text', 'نص بسيط', 'حفص', 'إملائي', 'بدون', 'نص بسيط للبحث', 'simple.txt', 0),

        # نصوص مع علامات الوقف
        ('with_waqf', 'With Stop Signs', 'مع علامات الوقف', 'حفص', 'عثماني', 'كامل', 'يحتوي على علامات الوقف', 'with_waqf.txt', 0),

        # نسخ النطق
        ('latin', 'Latin Transliteration', 'نطق لاتيني', 'حفص', 'لاتيني', 'N/A', 'النطق بالحروف اللاتينية', 'latin.txt', 0),
        ('phonetic', 'IPA Phonetic', 'نطق صوتي IPA', 'حفص', 'IPA', 'N/A', 'النطق بالرموز الصوتية الدولية', 'phonetic.txt', 0),

        # نسخ خاصة
        ('ajami', 'Ajami Script', 'الأعجمي', 'حفص', 'أعجمي', 'N/A', 'النص بالحروف الأعجمية', 'ajami.txt', 0),

        # نسخ بتنسيقات مختلفة
        ('unicode', 'Unicode Normalized', 'يونيكود قياسي', 'حفص', 'عثماني', 'كامل', 'نص محسن للمعايير القياسية', 'unicode.txt', 0),
        ('ascii', 'ASCII Compatible', 'متوافق ASCII', 'حفص', 'لاتيني', 'N/A', 'نص متوافق مع ASCII', 'ascii.txt', 0),

        # نسخة برايل للمكفوفين
        ('braille', 'Braille Version', 'برايل', 'حفص', 'برايل', 'N/A', 'نص برايل للمكفوفين', 'braille.txt', 0)
    ]

    cursor.executemany("""
        INSERT INTO text_versions
        (version_code, version_name_en, version_name_ar, qiraa, script_type, tashkeel_type, description, source_file, is_default)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, versions)

    print(f"   📥 تم إدراج {len(versions)} نوع من النصوص")

    # ========================================
    # الجدول 3: ayah_texts - النصوص الفعلية
    # ========================================
    cursor.execute("""
        CREATE TABLE ayah_texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ayah_id INTEGER NOT NULL,
            version_id INTEGER NOT NULL,

            -- النصوص
            aya_text TEXT NOT NULL,
            aya_text_emlaey TEXT,
            search_text TEXT,

            -- معلومات إضافية
            word_count INTEGER,
            letter_count INTEGER,

            -- العلاقات
            FOREIGN KEY (ayah_id) REFERENCES ayahs(id) ON DELETE CASCADE,
            FOREIGN KEY (version_id) REFERENCES text_versions(id) ON DELETE CASCADE,

            -- كل آية لها نص واحد فقط لكل إصدار
            UNIQUE(ayah_id, version_id)
        )
    """)
    print("   ✅ ayah_texts - النصوص الفعلية")

    # فهارس للأداء
    cursor.execute("CREATE INDEX idx_texts_ayah ON ayah_texts(ayah_id)")
    cursor.execute("CREATE INDEX idx_texts_version ON ayah_texts(version_id)")
    cursor.execute("CREATE INDEX idx_texts_search ON ayah_texts(search_text)")

    # ========================================
    # الجدول 4: tafsir - التفاسير (موسع)
    # ========================================
    cursor.execute("""
        CREATE TABLE tafsir (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ayah_id INTEGER NOT NULL,
            tafsir_source TEXT NOT NULL,
            tafsir_author TEXT,
            tafsir_text TEXT NOT NULL,
            tafsir_lang TEXT DEFAULT 'ar',

            -- معلومات إضافية
            is_verified BOOLEAN DEFAULT 0,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (ayah_id) REFERENCES ayahs(id) ON DELETE CASCADE
        )
    """)
    print("   ✅ tafsir - التفاسير")

    cursor.execute("CREATE INDEX idx_tafsir_ayah ON tafsir(ayah_id)")
    cursor.execute("CREATE INDEX idx_tafsir_source ON tafsir(tafsir_source)")

    # ========================================
    # الجدول 5: translations - الترجمات (موسع)
    # ========================================
    cursor.execute("""
        CREATE TABLE translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ayah_id INTEGER NOT NULL,
            language_code TEXT NOT NULL,
            language_name TEXT NOT NULL,
            translator_name TEXT,
            translation_text TEXT NOT NULL,

            -- معلومات إضافية
            is_verified BOOLEAN DEFAULT 0,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (ayah_id) REFERENCES ayahs(id) ON DELETE CASCADE,

            -- كل آية لها ترجمة واحدة فقط لكل مترجم بكل لغة
            UNIQUE(ayah_id, language_code, translator_name)
        )
    """)
    print("   ✅ translations - الترجمات")

    cursor.execute("CREATE INDEX idx_trans_ayah ON translations(ayah_id)")
    cursor.execute("CREATE INDEX idx_trans_lang ON translations(language_code)")

    # ========================================
    # الجدول 6: ayah_topics - مواضيع الآيات
    # ========================================
    cursor.execute("""
        CREATE TABLE ayah_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ayah_id INTEGER NOT NULL,
            topic_name_ar TEXT NOT NULL,
            topic_name_en TEXT,
            category TEXT,

            FOREIGN KEY (ayah_id) REFERENCES ayahs(id) ON DELETE CASCADE
        )
    """)
    print("   ✅ ayah_topics - مواضيع الآيات")

    cursor.execute("CREATE INDEX idx_topics_ayah ON ayah_topics(ayah_id)")
    cursor.execute("CREATE INDEX idx_topics_category ON ayah_topics(category)")

    # ========================================
    # الجدول 7: ayah_relations - علاقات بين الآيات
    # ========================================
    cursor.execute("""
        CREATE TABLE ayah_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ayah_id_1 INTEGER NOT NULL,
            ayah_id_2 INTEGER NOT NULL,
            relation_type TEXT NOT NULL,
            relation_desc TEXT,

            FOREIGN KEY (ayah_id_1) REFERENCES ayahs(id) ON DELETE CASCADE,
            FOREIGN KEY (ayah_id_2) REFERENCES ayahs(id) ON DELETE CASCADE
        )
    """)
    print("   ✅ ayah_relations - علاقات الآيات")

    cursor.execute("CREATE INDEX idx_rel_ayah1 ON ayah_relations(ayah_id_1)")
    cursor.execute("CREATE INDEX idx_rel_ayah2 ON ayah_relations(ayah_id_2)")

    # ========================================
    # Views للاستعلامات السريعة
    # ========================================

    # View: الآيات مع النص الافتراضي (حفص)
    cursor.execute("""
        CREATE VIEW v_ayahs_default AS
        SELECT
            a.id,
            a.sura_no,
            a.aya_no,
            a.jozz,
            a.page,
            t.aya_text,
            t.aya_text_emlaey,
            t.search_text
        FROM ayahs a
        JOIN ayah_texts t ON a.id = t.ayah_id
        JOIN text_versions v ON t.version_id = v.id
        WHERE v.is_default = 1
    """)
    print("   ✅ v_ayahs_default - عرض الآيات بالنص الافتراضي")

    # View: إحصائيات النصوص
    cursor.execute("""
        CREATE VIEW v_text_stats AS
        SELECT
            v.version_code,
            v.version_name_ar,
            v.qiraa,
            COUNT(t.id) as ayah_count,
            SUM(t.word_count) as total_words,
            SUM(t.letter_count) as total_letters
        FROM text_versions v
        LEFT JOIN ayah_texts t ON v.id = t.version_id
        GROUP BY v.id
    """)
    print("   ✅ v_text_stats - إحصائيات النصوص")

    # الحفظ والإغلاق
    conn.commit()
    conn.close()

    print(f"\n✅ تم إنشاء قاعدة البيانات بنجاح!")
    print(f"📂 المسار: {db_path.absolute()}")
    print(f"📊 الحجم: {db_path.stat().st_size / 1024:.2f} KB")

    print(f"\n📋 الجداول المنشأة:")
    print(f"   1. ayahs - الآيات الأساسية")
    print(f"   2. text_versions - 23 نوع نص")
    print(f"   3. ayah_texts - النصوص الفعلية")
    print(f"   4. tafsir - التفاسير")
    print(f"   5. translations - الترجمات")
    print(f"   6. ayah_topics - المواضيع")
    print(f"   7. ayah_relations - العلاقات")

    print(f"\n📊 Views:")
    print(f"   • v_ayahs_default - الآيات بالنص الافتراضي")
    print(f"   • v_text_stats - إحصائيات النصوص")

    return db_path


def main():
    """الدالة الرئيسية"""
    try:
        db_path = create_enhanced_ayahs_database()

        print(f"\n🎉 النجاح! القاعدة جاهزة للاستيراد")
        print(f"\n💡 الخطوة التالية:")
        print(f"   python3 scripts/import_quran_smart.py")

        return 0

    except Exception as e:
        print(f"\n❌ خطأ: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

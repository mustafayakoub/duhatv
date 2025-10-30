#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت إنشاء الفهارس لتحسين الأداء
يقوم بإنشاء فهارس على الأعمدة المهمة لتسريع الاستعلامات
"""

import sqlite3
import os
import sys
from pathlib import Path
import time

def find_database():
    """البحث عن قاعدة البيانات"""
    possible_paths = [
        r"C:\QYRAN5\QYRAN62\surah_database_app_v32.db",
        r"C:\QYRAN5\QYRAN62\quran.db",
        r"C:\QYRAN5\surah_database_app_v32.db",
        "surah_database_app_v32.db",
        "quran.db",
    ]

    # البحث في المجلد الحالي
    current_dir = Path(".")
    for db_file in current_dir.glob("*.db"):
        if db_file.is_file() and db_file.stat().st_size > 1000000:
            possible_paths.insert(0, str(db_file))

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None

def create_indexes(db_path):
    """إنشاء الفهارس"""
    print("="*80)
    print("🚀 بدء إنشاء الفهارس لتحسين الأداء")
    print("="*80)
    print(f"\n📁 قاعدة البيانات: {db_path}\n")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # الحصول على قائمة الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        print(f"✅ تم العثور على {len(tables)} جدول\n")

        # عداد الفهارس المنشأة
        indexes_created = 0

        # إنشاء فهارس على الجداول الرئيسية
        indexes_to_create = [
            # جداول السور
            ("idx_surah_id", "surahs", "id"),
            ("idx_surah_name", "surahs", "name"),

            # جداول الآيات
            ("idx_verse_surah", "verses", "surah_id"),
            ("idx_verse_id", "verses", "verse_id"),
            ("idx_verse_text", "verses", "text"),

            # جداول القرآن
            ("idx_quran_surah", "quran", "surah_id"),
            ("idx_quran_verse", "quran", "verse_id"),
            ("idx_quran_text", "quran", "text"),

            # جداول الكلمات
            ("idx_word_surah", "words", "surah_id"),
            ("idx_word_verse", "words", "verse_id"),
            ("idx_word_text", "words", "word"),
            ("idx_word_root", "words", "root"),

            # جداول التفسير
            ("idx_tafseer_surah", "tafseer", "surah_id"),
            ("idx_tafseer_verse", "tafseer", "verse_id"),
            ("idx_tafsir_surah", "tafsir", "surah_id"),
            ("idx_tafsir_verse", "tafsir", "verse_id"),

            # جداول الإعراب
            ("idx_erab_surah", "erab", "surah_id"),
            ("idx_erab_verse", "erab", "verse_id"),
            ("idx_i3rab_surah", "i3rab", "surah_id"),
            ("idx_i3rab_verse", "i3rab", "verse_id"),

            # جداول الترجمة
            ("idx_translation_surah", "translation", "surah_id"),
            ("idx_translation_verse", "translation", "verse_id"),

            # جداول الجذور
            ("idx_roots_root", "roots", "root"),
            ("idx_roots_word", "roots", "word"),
        ]

        for index_name, table_name, column_name in indexes_to_create:
            if table_name in tables:
                # التحقق من وجود العمود
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]

                if column_name in columns:
                    try:
                        # محاولة إنشاء الفهرس
                        query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column_name})"
                        start_time = time.time()
                        cursor.execute(query)
                        elapsed = time.time() - start_time

                        print(f"✅ تم إنشاء فهرس: {index_name} على {table_name}.{column_name} ({elapsed:.2f}s)")
                        indexes_created += 1

                    except Exception as e:
                        print(f"⚠️  تحذير: لم يتم إنشاء {index_name}: {e}")

        # تحليل قاعدة البيانات لتحسين الأداء
        print("\n📊 تحليل قاعدة البيانات...")
        cursor.execute("ANALYZE")

        # حفظ التغييرات
        conn.commit()

        print("\n" + "="*80)
        print(f"✅ تم بنجاح! تم إنشاء {indexes_created} فهرس")
        print("="*80)

        # عرض إحصائيات
        print("\n📊 إحصائيات قاعدة البيانات:")

        for table in tables:
            if any(keyword in table.lower() for keyword in ['surah', 'verse', 'quran', 'word']):
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count:,} صف")

        conn.close()

        print("\n✨ الآن قاعدة البيانات جاهزة للاستخدام بأداء محسّن!")

    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        return False

    return True

def main():
    """نقطة البداية"""
    print("\n" + "="*80)
    print("🔧 أداة إنشاء الفهارس - تحسين أداء قاعدة البيانات")
    print("="*80)

    db_path = find_database()

    if not db_path:
        print("\n❌ لم يتم العثور على قاعدة البيانات!")
        print("\n💡 تلميح:")
        print("  1. ضع قاعدة البيانات في: C:\\QYRAN5\\QYRAN62\\")
        print("  2. أو في نفس المجلد مع هذا السكريبت")
        return

    # إنشاء نسخة احتياطية (اختياري)
    print("\n💾 نسخة احتياطية:")
    print("  يُنصح بإنشاء نسخة احتياطية من قاعدة البيانات قبل المتابعة")
    print("  (اضغط Ctrl+C للإلغاء)\n")

    try:
        input("اضغط Enter للمتابعة...")
    except KeyboardInterrupt:
        print("\n\n❌ تم الإلغاء")
        return

    # إنشاء الفهارس
    if create_indexes(db_path):
        print("\n✅ تمت العملية بنجاح!")
    else:
        print("\n❌ حدث خطأ أثناء إنشاء الفهارس")

if __name__ == "__main__":
    main()

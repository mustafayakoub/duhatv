#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت استكشاف قاعدة البيانات
يستكشف بنية قاعدة البيانات ويحلل الجداول والعلاقات
"""

import sqlite3
import os
import sys
from pathlib import Path

def find_database():
    """البحث عن قاعدة البيانات في المسارات المحتملة"""
    possible_paths = [
        r"C:\QYRAN5\QYRAN62\surah_database_app_v32.db",
        r"C:\QYRAN5\surah_database_app_v32.db",
        "surah_database_app_v32.db",
        "./surah_database_app_v32.db",
        "../surah_database_app_v32.db",
    ]

    # البحث في المجلد الحالي عن أي ملف .db
    current_dir = Path(".")
    for db_file in current_dir.glob("*.db"):
        if db_file.is_file():
            possible_paths.insert(0, str(db_file))

    # البحث في المجلد الأب
    parent_dir = Path("..")
    for db_file in parent_dir.glob("*.db"):
        if db_file.is_file():
            possible_paths.insert(0, str(db_file))

    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ تم العثور على قاعدة البيانات: {path}")
            return path

    print("❌ لم يتم العثور على قاعدة البيانات في المسارات المعتادة")
    print("\nالمسارات التي تم البحث فيها:")
    for path in possible_paths:
        print(f"  - {path}")
    return None

def explore_database(db_path):
    """استكشاف شامل لقاعدة البيانات"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("\n" + "="*80)
        print("📊 تحليل قاعدة البيانات")
        print("="*80)

        # الحصول على قائمة الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()

        print(f"\n✅ عدد الجداول: {len(tables)}")
        print("\n" + "-"*80)

        important_tables = {
            'quran': 'القرآن الكريم',
            'surahs': 'السور',
            'verses': 'الآيات',
            'words': 'الكلمات',
            'tafseer': 'التفسير',
            'tafsir': 'التفسير',
            'erab': 'الإعراب',
            'i3rab': 'الإعراب',
            'translation': 'الترجمة',
            'roots': 'الجذور',
            'morphology': 'الصرف',
        }

        table_info = {}

        for table in tables:
            table_name = table[0]

            # الحصول على عدد الصفوف
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]

            # الحصول على أسماء الأعمدة
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]

            table_info[table_name] = {
                'count': count,
                'columns': column_names
            }

            # تحديد إذا كان الجدول مهم
            is_important = any(key in table_name.lower() for key in important_tables.keys())
            icon = "⭐" if is_important else "  "

            print(f"{icon} {table_name:<30} | {count:>10,} صف | {len(column_names)} عمود")

            if is_important:
                print(f"     الأعمدة: {', '.join(column_names[:10])}")
                if len(column_names) > 10:
                    print(f"     ... و {len(column_names) - 10} عمود آخر")
                print()

        print("\n" + "="*80)
        print("📋 الجداول الرئيسية المكتشفة")
        print("="*80)

        # تحليل الجداول المهمة
        for key, description in important_tables.items():
            matching_tables = [t for t in table_info.keys() if key in t.lower()]
            if matching_tables:
                print(f"\n✅ {description} ({key}):")
                for table_name in matching_tables:
                    info = table_info[table_name]
                    print(f"   - {table_name}: {info['count']:,} صف")
                    print(f"     الأعمدة: {', '.join(info['columns'])}")

        # عرض نموذج من البيانات
        print("\n" + "="*80)
        print("📖 نماذج من البيانات")
        print("="*80)

        # محاولة عرض نموذج من السور
        surah_tables = [t for t in table_info.keys() if 'surah' in t.lower() or 'sura' in t.lower()]
        if surah_tables:
            table_name = surah_tables[0]
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            if rows:
                print(f"\n📚 نموذج من {table_name}:")
                columns = table_info[table_name]['columns']
                for row in rows:
                    print(f"   {dict(zip(columns, row))}")

        # محاولة عرض نموذج من الآيات
        verse_tables = [t for t in table_info.keys() if 'verse' in t.lower() or 'aya' in t.lower()]
        if verse_tables:
            table_name = verse_tables[0]
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
            rows = cursor.fetchall()
            if rows:
                print(f"\n📝 نموذج من {table_name}:")
                columns = table_info[table_name]['columns']
                for row in rows:
                    print(f"   {dict(zip(columns, row))}")

        conn.close()
        return table_info

    except Exception as e:
        print(f"❌ خطأ في تحليل قاعدة البيانات: {e}")
        return None

if __name__ == "__main__":
    print("="*80)
    print("🔍 برنامج استكشاف قاعدة بيانات القرآن الكريم")
    print("="*80)

    db_path = find_database()
    if db_path:
        explore_database(db_path)
    else:
        print("\n💡 تلميح: ضع ملف قاعدة البيانات في نفس المجلد مع هذا السكريبت")
        print("   أو حدد المسار الصحيح في الكود")

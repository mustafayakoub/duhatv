#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لفحص بنية قاعدة بيانات القرآن
يقوم بفحص جميع الجداول والأعمدة وعرض البنية الكاملة
"""

import sqlite3
import os
import json
from pathlib import Path

def find_database(base_path=r"C:\quran9"):
    """البحث عن ملفات قاعدة البيانات"""
    db_files = []

    if os.path.exists(base_path):
        for file in Path(base_path).glob("*.db"):
            if file.stat().st_size > 100000:  # أكبر من 100KB
                db_files.append(str(file))

    return db_files

def analyze_database(db_path):
    """تحليل بنية قاعدة البيانات"""
    print(f"\n{'='*70}")
    print(f"تحليل قاعدة البيانات: {db_path}")
    print(f"{'='*70}\n")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # الحصول على قائمة الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print(f"📊 عدد الجداول: {len(tables)}\n")

        database_structure = {
            "db_path": db_path,
            "tables": {}
        }

        for table in tables:
            table_name = table[0]
            print(f"\n{'─'*70}")
            print(f"📋 الجدول: {table_name}")
            print(f"{'─'*70}")

            # الحصول على معلومات الأعمدة
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            print(f"\n   الأعمدة ({len(columns)}):")
            column_list = []

            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                print(f"   {col_id+1:2d}. {col_name:30s} {col_type:15s}", end="")

                if pk:
                    print(" [PRIMARY KEY]", end="")
                if not_null:
                    print(" [NOT NULL]", end="")
                print()

                column_list.append({
                    "name": col_name,
                    "type": col_type,
                    "not_null": bool(not_null),
                    "primary_key": bool(pk)
                })

            # عدد السجلات
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"\n   📝 عدد السجلات: {count:,}")
            except:
                count = 0

            # عينة من البيانات (أول صف)
            try:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                sample = cursor.fetchone()
                if sample:
                    print(f"\n   🔍 عينة من البيانات:")
                    for i, col in enumerate(columns):
                        col_name = col[1]
                        value = sample[i] if i < len(sample) else None
                        if value:
                            value_str = str(value)[:100]
                            print(f"      {col_name}: {value_str}")
            except Exception as e:
                print(f"   ⚠️ خطأ في قراءة البيانات: {e}")

            database_structure["tables"][table_name] = {
                "columns": column_list,
                "row_count": count
            }

        conn.close()

        # حفظ البنية في ملف JSON
        output_file = db_path.replace('.db', '_structure.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(database_structure, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*70}")
        print(f"✅ تم حفظ بنية قاعدة البيانات في: {output_file}")
        print(f"{'='*70}\n")

        return database_structure

    except Exception as e:
        print(f"❌ خطأ في تحليل قاعدة البيانات: {e}")
        return None

def main():
    """الدالة الرئيسية"""
    print("🔍 البحث عن قواعد بيانات القرآن...\n")

    # البحث في C:\quran9
    db_files = find_database(r"C:\quran9")

    if not db_files:
        print("⚠️ لم يتم العثور على ملفات قاعدة بيانات في C:\\quran9")
        print("\nيرجى إدخال المسار الكامل لملف قاعدة البيانات:")
        custom_path = input("> ")
        if os.path.exists(custom_path):
            db_files = [custom_path]
        else:
            print("❌ الملف غير موجود!")
            return

    print(f"✅ تم العثور على {len(db_files)} قاعدة بيانات:\n")
    for i, db in enumerate(db_files, 1):
        print(f"{i}. {db}")

    # تحليل كل قاعدة بيانات
    for db_file in db_files:
        analyze_database(db_file)

    print("\n✅ اكتمل التحليل!")
    print("\nارسل ملفات *_structure.json إلى Claude لتحديث التطبيق\n")

if __name__ == "__main__":
    main()

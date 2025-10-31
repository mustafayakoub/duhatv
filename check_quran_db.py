#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص سريع لقاعدة بيانات quran_ultimate_final.db
"""

import sqlite3
import json

db_path = r"C:\quran9\quran_ultimate_final.db"

print("🔍 فحص قاعدة البيانات...\n")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # الجداول
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    print(f"✅ تم الاتصال بنجاح!")
    print(f"📊 عدد الجداول: {len(tables)}\n")

    structure = {}

    for table in tables:
        table_name = table[0]
        print(f"\n{'─'*70}")
        print(f"📋 الجدول: {table_name}")
        print(f"{'─'*70}")

        # الأعمدة
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        col_names = [c[1] for c in columns]
        structure[table_name] = col_names

        print(f"\nالأعمدة ({len(columns)}):")
        for i, col in enumerate(columns, 1):
            print(f"  {i:2d}. {col[1]:30s} {col[2]:15s}")

        # عدد السجلات
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"\n📝 عدد السجلات: {count:,}")

        # عينة من البيانات
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        row = cursor.fetchone()
        if row:
            print(f"\n🔍 عينة من البيانات (أول صف):")
            for i, col in enumerate(columns):
                if i < len(row) and row[i]:
                    value = str(row[i])[:80]
                    print(f"  {col[1]}: {value}")

    conn.close()

    # حفظ البنية
    with open("database_structure.json", "w", encoding="utf-8") as f:
        json.dump(structure, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*70}")
    print("✅ تم حفظ البنية في: database_structure.json")
    print("📤 أرسل هذا الملف إلى Claude")
    print(f"{'='*70}\n")

except Exception as e:
    print(f"❌ خطأ: {e}")
    print("\nتأكد من:")
    print("1. وجود الملف في C:\\quran9\\quran_ultimate_final.db")
    print("2. لديك صلاحيات القراءة")

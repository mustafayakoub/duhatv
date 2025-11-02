#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص بنية قاعدة surah_database_app_v32.db
"""

import sqlite3

DB = r"C:\quran11\surah_database_app_v32.db"

print("\n" + "🔍" * 35)
print("        فحص قاعدة surah_database_app_v32.db")
print("🔍" * 35 + "\n")

conn = sqlite3.connect(DB)
cursor = conn.cursor()

# الحصول على جميع الجداول
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]

print("📋 الجداول الموجودة:")
print("=" * 70)
for table in tables:
    print(f"  ✓ {table}")
print()

# فحص كل جدول
for table in tables:
    if 'irab' in table.lower() or 'sarf' in table.lower() or 'word' in table.lower():
        print("=" * 70)
        print(f"📊 جدول: {table}")
        print("=" * 70)

        # الأعمدة
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()

        print("الأعمدة:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

        # عدد السجلات
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"\nعدد السجلات: {count:,}")

        # عينة من البيانات
        if count > 0:
            print("\nعينة من البيانات (أول سجل):")
            cursor.execute(f"SELECT * FROM {table} LIMIT 1")
            sample = cursor.fetchone()
            for i, col in enumerate(columns):
                value = sample[i] if sample and i < len(sample) else None
                if value and isinstance(value, str):
                    value = value[:50] + "..." if len(str(value)) > 50 else value
                print(f"  {col[1]}: {value}")

        print()

conn.close()

print("=" * 70)
print("✅ انتهى الفحص")
print("=" * 70)

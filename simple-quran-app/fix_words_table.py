#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح جدول words - إضافة العمود المفقود
"""

import sqlite3

DB_PATH = r"C:\quran11\quran_unified.db"

print("=" * 70)
print("🔧 إصلاح جدول words")
print("=" * 70)
print()

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # التحقق من وجود العمود
    cursor.execute("PRAGMA table_info(words)")
    columns = [row[1] for row in cursor.fetchall()]

    print(f"📋 الأعمدة الحالية في جدول words:")
    for col in columns:
        print(f"   • {col}")
    print()

    if 'root_text' not in columns:
        print("➕ إضافة عمود root_text...")
        cursor.execute("ALTER TABLE words ADD COLUMN root_text TEXT")
        conn.commit()
        print("✅ تم إضافة عمود root_text بنجاح!")
    else:
        print("✅ عمود root_text موجود بالفعل!")

    print()
    print("=" * 70)
    print("✅ اكتمل الإصلاح! يمكنك الآن تشغيل السكريبت الرئيسي")
    print("=" * 70)

    conn.close()

except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()

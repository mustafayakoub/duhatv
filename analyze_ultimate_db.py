#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت فحص شامل لقاعدة بيانات quran_ultimate_final.db
"""

import sqlite3
import json

db_path = r"C:\quran9\quran_ultimate_final.db"

print("🔍 فحص شامل لقاعدة البيانات...\n")

conn = sqlite3.connect(db_path)
c = conn.cursor()

# 1. الجداول
c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [t[0] for t in c.fetchall()]

print(f"✅ عدد الجداول: {len(tables)}\n")

# 2. فحص بنية الجداول المرقمة (السور)
numbered_tables = [t for t in tables if t.isdigit()]
other_tables = [t for t in tables if not t.isdigit()]

print(f"📖 الجداول المرقمة (السور): {len(numbered_tables)}")
print(f"📋 جداول أخرى: {len(other_tables)}")
if other_tables:
    print(f"   {other_tables}\n")

# 3. فحص بنية جدول سورة نموذجي
sample_table = '001'
c.execute(f"PRAGMA table_info('{sample_table}')")
columns = c.fetchall()

print(f"\n{'='*70}")
print(f"بنية الجداول (نموذج: {sample_table})")
print(f"{'='*70}")
print(f"الأعمدة ({len(columns)}):")
for col in columns:
    print(f"  - {col[1]:20s} {col[2]:10s}")

# 4. فحص محتوى نموذجي
print(f"\n{'='*70}")
print("تحليل المحتوى")
print(f"{'='*70}")

# عدد السجلات في كل سورة
print("\n📊 عدد السجلات في أول 10 سور:")
for table in numbered_tables[:10]:
    c.execute(f"SELECT COUNT(*) FROM '{table}'")
    count = c.fetchone()[0]
    print(f"  سورة {table}: {count} سجل")

# فحص أرقام التفاسير
print(f"\n📚 أنواع التفاسير الموجودة:")
c.execute(f"SELECT DISTINCT NTafsir FROM '{sample_table}' ORDER BY NTafsir")
tafsir_nums = [t[0] for t in c.fetchall()]
print(f"  أرقام التفاسير: {tafsir_nums}")
print(f"  عدد التفاسير: {len(tafsir_nums)}")

# عينات من البيانات
print(f"\n🔍 عينات من البيانات (سورة 001):")
for tafsir_num in tafsir_nums[:3]:
    c.execute(f"SELECT * FROM '001' WHERE NTafsir = ? LIMIT 1", (tafsir_num,))
    row = c.fetchone()
    if row:
        print(f"\n  التفسير رقم {tafsir_num}:")
        print(f"    رقم الآية: {row[0]}")
        text = row[2][:150] if row[2] else ""
        print(f"    النص: {text}...")

# 5. فحص سورة أطول (البقرة)
print(f"\n{'='*70}")
print("فحص سورة البقرة (002)")
print(f"{'='*70}")

c.execute("SELECT COUNT(*) FROM '002'")
total = c.fetchone()[0]
print(f"إجمالي السجلات: {total}")

c.execute("SELECT COUNT(DISTINCT NAya) FROM '002'")
ayah_count = c.fetchone()[0]
print(f"عدد الآيات: {ayah_count}")

c.execute("SELECT COUNT(DISTINCT NTafsir) FROM '002'")
tafsir_count = c.fetchone()[0]
print(f"عدد التفاسير: {tafsir_count}")

# عينة من آية
c.execute("SELECT * FROM '002' WHERE NAya = 1 ORDER BY NTafsir LIMIT 3")
rows = c.fetchall()
print(f"\nآية 1 من البقرة (أول 3 تفاسير):")
for row in rows:
    print(f"\n  تفسير {row[1]}:")
    text = row[2][:200] if row[2] else ""
    print(f"    {text}...")

# 6. حفظ النتائج
structure = {
    "total_tables": len(tables),
    "surah_tables": numbered_tables,
    "other_tables": other_tables,
    "columns": [{"name": col[1], "type": col[2]} for col in columns],
    "tafsir_numbers": tafsir_nums,
    "sample_surah_002": {
        "total_records": total,
        "ayah_count": ayah_count,
        "tafsir_count": tafsir_count
    }
}

with open("db_structure.json", "w", encoding="utf-8") as f:
    json.dump(structure, f, ensure_ascii=False, indent=2)

print(f"\n{'='*70}")
print("✅ تم حفظ البنية في: db_structure.json")
print(f"{'='*70}\n")

conn.close()

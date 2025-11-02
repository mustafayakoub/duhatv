#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════════════════
إعادة البناء الكاملة - من القواعد الموجودة
Complete Rebuild from Existing Databases
════════════════════════════════════════════════════════════════════════════
"""

import sqlite3
import os
import sys

# المسارات
DB_TARGET = r"C:\quran11\quran_unified.db"
DB_ULTIMATE = r"C:\quran11\quran_ultimate_final.db"  # للسور والآيات
DB_SURAHS = r"C:\quran11\surah_database_app_v32.db"  # للكلمات والإعراب

print("\n" + "🌙" * 35)
print("        إعادة البناء الكاملة من الصفر")
print("🌙" * 35 + "\n")

# التحقق من وجود القواعد
print("📋 فحص القواعد:")
if not os.path.exists(DB_ULTIMATE):
    print(f"❌ {DB_ULTIMATE} غير موجود!")
    sys.exit(1)
if not os.path.exists(DB_SURAHS):
    print(f"❌ {DB_SURAHS} غير موجود!")
    sys.exit(1)

print(f"✅ {DB_ULTIMATE}")
print(f"✅ {DB_SURAHS}")
print()

# حذف القديمة
if os.path.exists(DB_TARGET):
    os.remove(DB_TARGET)
    print("🗑️  تم حذف القاعدة القديمة\n")

# ═══════════════════════════════════════════════════════════════════════════
# المرحلة 1: إنشاء الجداول
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("المرحلة 1: إنشاء الجداول")
print("=" * 70)

conn = sqlite3.connect(DB_TARGET)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE surahs (
        surah_id INTEGER PRIMARY KEY,
        name_arabic TEXT NOT NULL,
        name_english TEXT,
        ayah_count INTEGER,
        revelation_type TEXT
    )
""")
print("✅ جدول السور")

cursor.execute("""
    CREATE TABLE ayahs (
        ayah_id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah_id INTEGER NOT NULL,
        ayah_number INTEGER NOT NULL,
        text_uthmani TEXT NOT NULL,
        juz_number INTEGER,
        page_number INTEGER,
        UNIQUE(surah_id, ayah_number)
    )
""")
print("✅ جدول الآيات")

cursor.execute("""
    CREATE TABLE words (
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ayah_id INTEGER NOT NULL,
        word_position INTEGER NOT NULL,
        word_text TEXT NOT NULL,
        word_simple TEXT,
        root_text TEXT,
        UNIQUE(ayah_id, word_position)
    )
""")
print("✅ جدول الكلمات")

cursor.execute("""
    CREATE TABLE irab (
        irab_id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_id INTEGER NOT NULL,
        irab_text TEXT,
        UNIQUE(word_id)
    )
""")
print("✅ جدول الإعراب")

cursor.execute("""
    CREATE TABLE sarf (
        sarf_id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_id INTEGER NOT NULL,
        sarf_text TEXT,
        UNIQUE(word_id)
    )
""")
print("✅ جدول الصرف")

conn.commit()
print()

# ═══════════════════════════════════════════════════════════════════════════
# المرحلة 2: نقل السور
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("المرحلة 2: نقل السور")
print("=" * 70)

conn_old = sqlite3.connect(DB_ULTIMATE)
cursor_old = conn_old.cursor()

cursor_old.execute("""
    SELECT SurahNo, SurahNameArabic, SurahNameEnglish, CountOfAyahs, RevelationType
    FROM Surahs ORDER BY SurahNo
""")

for row in cursor_old.fetchall():
    cursor.execute("""
        INSERT INTO surahs VALUES (?, ?, ?, ?, ?)
    """, row)

conn.commit()
conn_old.close()

cursor.execute("SELECT COUNT(*) FROM surahs")
print(f"✅ تم نقل {cursor.fetchone()[0]} سورة")
print()

# ═══════════════════════════════════════════════════════════════════════════
# المرحلة 3: نقل الآيات
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("المرحلة 3: نقل الآيات")
print("=" * 70)

conn_old = sqlite3.connect(DB_ULTIMATE)
cursor_old = conn_old.cursor()

cursor_old.execute("""
    SELECT SurahNo, AyahNo, AyahText, JuzNo, PageNo
    FROM Ayahs ORDER BY SurahNo, AyahNo
""")

for row in cursor_old.fetchall():
    cursor.execute("""
        INSERT INTO ayahs (surah_id, ayah_number, text_uthmani, juz_number, page_number)
        VALUES (?, ?, ?, ?, ?)
    """, row)

conn.commit()
conn_old.close()

cursor.execute("SELECT COUNT(*) FROM ayahs")
print(f"✅ تم نقل {cursor.fetchone()[0]} آية")
print()

# ═══════════════════════════════════════════════════════════════════════════
# المرحلة 4: نقل الكلمات (الطريقة الذكية من migrate_words_smart.py)
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("المرحلة 4: نقل الكلمات بالطريقة الذكية")
print("=" * 70)

conn_old = sqlite3.connect(DB_SURAHS)
conn_old.row_factory = sqlite3.Row
cursor_old = conn_old.cursor()

print("🔍 قراءة الكلمات باستخدام INNER JOIN...")

cursor_old.execute("""
    SELECT
        qw.surahNo, qw.ayahNo, qw.wordNo,
        qw.wordWithHaraqah, qw.wordWithOutHaraqah, qw.Root,
        wi.irabMushakkal,
        ws.sarf
    FROM word_content_irab wi
    INNER JOIN QuranWordInfo qw
        ON wi.surahNo = qw.surahNo
        AND wi.ayahNo = qw.ayahNo
        AND wi.wordNo = qw.wordNo
    LEFT JOIN word_content_sarf ws
        ON wi.surahNo = ws.surahNo
        AND wi.ayahNo = ws.ayahNo
        AND wi.wordNo = ws.wordNo
    ORDER BY wi.surahNo, wi.ayahNo, wi.wordNo
""")

all_words = cursor_old.fetchall()
total = len(all_words)
print(f"✅ تم قراءة {total:,} كلمة")

if total == 77432:
    print("✅ العدد صحيح: 77,432 كلمة")
else:
    print(f"⚠️  العدد المتوقع 77,432 لكن حصلنا على {total:,}")

print("\n📝 جاري النقل...")

# كاش للآيات
ayah_cache = {}

processed = 0
for row in all_words:
    # الحصول على ayah_id
    cache_key = (row['surahNo'], row['ayahNo'])
    if cache_key not in ayah_cache:
        cursor.execute("""
            SELECT ayah_id FROM ayahs
            WHERE surah_id = ? AND ayah_number = ?
        """, (row['surahNo'], row['ayahNo']))
        result = cursor.fetchone()
        ayah_cache[cache_key] = result[0] if result else None

    ayah_id = ayah_cache[cache_key]
    if not ayah_id:
        continue

    # إدخال الكلمة
    cursor.execute("""
        INSERT INTO words (ayah_id, word_position, word_text, word_simple, root_text)
        VALUES (?, ?, ?, ?, ?)
    """, (ayah_id, row['wordNo'], row['wordWithHaraqah'], row['wordWithOutHaraqah'], row['Root']))

    word_id = cursor.lastrowid

    # إدخال الإعراب
    if row['irabMushakkal']:
        cursor.execute("INSERT INTO irab (word_id, irab_text) VALUES (?, ?)",
                      (word_id, row['irabMushakkal']))

    # إدخال الصرف
    if row['sarf']:
        cursor.execute("INSERT INTO sarf (word_id, sarf_text) VALUES (?, ?)",
                      (word_id, row['sarf']))

    processed += 1
    if processed % 1000 == 0:
        conn.commit()
        print(f"⏳ {processed:,}/{total:,} ({(processed/total)*100:.1f}%)", end='\r')

conn.commit()
conn_old.close()
print(f"\n✅ تم نقل {processed:,} كلمة")
print()

# ═══════════════════════════════════════════════════════════════════════════
# التحقق النهائي
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("🔍 التحقق النهائي")
print("=" * 70)

cursor.execute("SELECT COUNT(*) FROM surahs")
surahs = cursor.fetchone()[0]
print(f"السور: {surahs:,} {'✅' if surahs == 114 else '❌'}")

cursor.execute("SELECT COUNT(*) FROM ayahs")
ayahs = cursor.fetchone()[0]
print(f"الآيات: {ayahs:,} {'✅' if ayahs == 6236 else '❌'}")

cursor.execute("SELECT COUNT(*) FROM words")
words = cursor.fetchone()[0]
print(f"الكلمات: {words:,} {'✅' if words == 77432 else '❌'}")

cursor.execute("SELECT COUNT(*) FROM irab")
irab = cursor.fetchone()[0]
print(f"الإعراب: {irab:,} ✅")

cursor.execute("SELECT COUNT(*) FROM sarf")
sarf = cursor.fetchone()[0]
print(f"الصرف: {sarf:,} ✅")

conn.close()

if surahs == 114 and ayahs == 6236 and words == 77432:
    print("\n" + "="*70)
    print("✅ ✅ ✅ تم بنجاح! القاعدة جاهزة! ✅ ✅ ✅")
    print("="*70)
    print("\n🚀 شغّل الآن: RUN_TREE_VIEWER.bat")
else:
    print("\n⚠️ تحذير: الأرقام غير مطابقة!")

print("\n" + "🌙" * 35)

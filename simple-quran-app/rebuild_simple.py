#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════════════════
إعادة بناء quran_unified.db - بسيط ومباشر
من القواعد الموجودة لديك
════════════════════════════════════════════════════════════════════════════
"""

import sqlite3
import os
import sys

# القواعد المتاحة لديك
DB_TARGET = r"C:\quran11\quran_unified.db"
DB_ULTIMATE = r"C:\quran11\quran_ultimate_final.db"
DB_SURAHS = r"C:\quran11\surah_database_app_v32.db"

print("\n" + "🌙" * 35)
print("        إعادة بناء quran_unified.db")
print("🌙" * 35 + "\n")

# التحقق من وجود القواعد
print("📋 فحص القواعد المتاحة:")
print(f"1. quran_ultimate_final.db: {'✅ موجود' if os.path.exists(DB_ULTIMATE) else '❌ غير موجود'}")
print(f"2. surah_database_app_v32.db: {'✅ موجود' if os.path.exists(DB_SURAHS) else '❌ غير موجود'}")

if not os.path.exists(DB_ULTIMATE):
    print("\n❌ خطأ: quran_ultimate_final.db غير موجود!")
    print("تأكد من وجود الملف في: C:\\quran11\\")
    sys.exit(1)

if not os.path.exists(DB_SURAHS):
    print("\n❌ خطأ: surah_database_app_v32.db غير موجود!")
    print("تأكد من وجود الملف في: C:\\quran11\\")
    sys.exit(1)

print("\n✅ جميع القواعد موجودة!")

# حذف القاعدة القديمة
print("\n🗑️  حذف القاعدة القديمة...")
if os.path.exists(DB_TARGET):
    os.remove(DB_TARGET)
    print("✅ تم الحذف")
else:
    print("ℹ️  لا توجد قاعدة قديمة")

# إنشاء قاعدة جديدة
print("\n🔨 إنشاء قاعدة جديدة...")
conn = sqlite3.connect(DB_TARGET)
cursor = conn.cursor()

# إنشاء الجداول
cursor.execute("""
    CREATE TABLE IF NOT EXISTS surahs (
        surah_id INTEGER PRIMARY KEY,
        name_arabic TEXT NOT NULL,
        name_english TEXT,
        ayah_count INTEGER,
        revelation_type TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ayahs (
        ayah_id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah_id INTEGER NOT NULL,
        ayah_number INTEGER NOT NULL,
        text_uthmani TEXT NOT NULL,
        juz_number INTEGER,
        page_number INTEGER,
        FOREIGN KEY (surah_id) REFERENCES surahs(surah_id),
        UNIQUE(surah_id, ayah_number)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ayah_id INTEGER NOT NULL,
        word_position INTEGER NOT NULL,
        word_text TEXT NOT NULL,
        word_simple TEXT,
        root_text TEXT,
        FOREIGN KEY (ayah_id) REFERENCES ayahs(ayah_id),
        UNIQUE(ayah_id, word_position)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS irab (
        irab_id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_id INTEGER NOT NULL,
        irab_text TEXT,
        FOREIGN KEY (word_id) REFERENCES words(word_id),
        UNIQUE(word_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sarf (
        sarf_id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_id INTEGER NOT NULL,
        sarf_text TEXT,
        FOREIGN KEY (word_id) REFERENCES words(word_id),
        UNIQUE(word_id)
    )
""")

# إنشاء الفهارس
cursor.execute("CREATE INDEX IF NOT EXISTS idx_ayahs_surah ON ayahs(surah_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_ayah ON words(ayah_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_root ON words(root_text)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_irab_word ON irab(word_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_sarf_word ON sarf(word_id)")

conn.commit()
print("✅ تم إنشاء الجداول")

# نقل السور
print("\n📚 نقل السور...")
conn_old = sqlite3.connect(DB_ULTIMATE)
cursor_old = conn_old.cursor()

cursor_old.execute("""
    SELECT SurahNo, SurahNameArabic, SurahNameEnglish, CountOfAyahs, RevelationType
    FROM Surahs
    ORDER BY SurahNo
""")

surahs = cursor_old.fetchall()
for surah in surahs:
    cursor.execute("""
        INSERT OR IGNORE INTO surahs (surah_id, name_arabic, name_english, ayah_count, revelation_type)
        VALUES (?, ?, ?, ?, ?)
    """, surah)

conn.commit()
conn_old.close()
print(f"✅ تم نقل {len(surahs)} سورة")

# نقل الآيات
print("\n📖 نقل الآيات...")
conn_old = sqlite3.connect(DB_ULTIMATE)
cursor_old = conn_old.cursor()

cursor_old.execute("""
    SELECT SurahNo, AyahNo, AyahText, JuzNo, PageNo
    FROM Ayahs
    ORDER BY SurahNo, AyahNo
""")

ayahs = cursor_old.fetchall()
for ayah in ayahs:
    cursor.execute("""
        INSERT OR IGNORE INTO ayahs (surah_id, ayah_number, text_uthmani, juz_number, page_number)
        VALUES (?, ?, ?, ?, ?)
    """, ayah)

conn.commit()
conn_old.close()
print(f"✅ تم نقل {len(ayahs)} آية")

# نقل الكلمات
print("\n📝 نقل الكلمات والإعراب والصرف...")
conn_old = sqlite3.connect(DB_SURAHS)
conn_old.row_factory = sqlite3.Row
cursor_old = conn_old.cursor()

cursor_old.execute("""
    SELECT
        wi.surahNo, wi.ayahNo, wi.wordNo,
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

words_data = cursor_old.fetchall()
total = len(words_data)
print(f"إجمالي الكلمات: {total:,}")

processed = 0
for word in words_data:
    # الحصول على ayah_id
    cursor.execute("""
        SELECT ayah_id FROM ayahs
        WHERE surah_id = ? AND ayah_number = ?
    """, (word['surahNo'], word['ayahNo']))

    ayah_row = cursor.fetchone()
    if not ayah_row:
        continue

    ayah_id = ayah_row[0]

    # إدراج الكلمة
    cursor.execute("""
        INSERT OR IGNORE INTO words (ayah_id, word_position, word_text, word_simple, root_text)
        VALUES (?, ?, ?, ?, ?)
    """, (ayah_id, word['wordNo'], word['wordWithHaraqah'], word['wordWithOutHaraqah'], word['Root']))

    # الحصول على word_id
    cursor.execute("""
        SELECT word_id FROM words
        WHERE ayah_id = ? AND word_position = ?
    """, (ayah_id, word['wordNo']))

    word_row = cursor.fetchone()
    if word_row:
        word_id = word_row[0]

        # إدراج الإعراب
        if word['irabMushakkal']:
            cursor.execute("""
                INSERT OR IGNORE INTO irab (word_id, irab_text)
                VALUES (?, ?)
            """, (word_id, word['irabMushakkal']))

        # إدراج الصرف
        if word['sarf']:
            cursor.execute("""
                INSERT OR IGNORE INTO sarf (word_id, sarf_text)
                VALUES (?, ?)
            """, (word_id, word['sarf']))

    processed += 1
    if processed % 10000 == 0:
        conn.commit()
        print(f"  {processed:,} / {total:,}")

conn.commit()
conn_old.close()
print(f"✅ تم نقل {total:,} كلمة")

# التحقق
print("\n🔍 التحقق من القاعدة...")
cursor.execute("SELECT COUNT(*) FROM surahs")
surahs_count = cursor.fetchone()[0]
print(f"السور: {surahs_count:,} {'✅' if surahs_count == 114 else '❌'}")

cursor.execute("SELECT COUNT(*) FROM ayahs")
ayahs_count = cursor.fetchone()[0]
print(f"الآيات: {ayahs_count:,} {'✅' if ayahs_count == 6236 else '❌'}")

cursor.execute("SELECT COUNT(*) FROM words")
words_count = cursor.fetchone()[0]
print(f"الكلمات: {words_count:,} {'✅' if words_count == 77432 else '❌'}")

cursor.execute("SELECT COUNT(*) FROM irab")
irab_count = cursor.fetchone()[0]
print(f"الإعراب: {irab_count:,} {'✅' if irab_count > 0 else '❌'}")

cursor.execute("SELECT COUNT(*) FROM sarf")
sarf_count = cursor.fetchone()[0]
print(f"الصرف: {sarf_count:,} {'✅' if sarf_count > 0 else '❌'}")

conn.close()

if surahs_count == 114 and ayahs_count == 6236 and words_count == 77432:
    print("\n" + "="*70)
    print("✅ ✅ ✅ تم بنجاح! القاعدة جاهزة للاستخدام! ✅ ✅ ✅")
    print("="*70)
    print("\nالخطوة التالية: شغّل RUN_TREE_VIEWER.bat")
else:
    print("\n⚠️ تحذير: الأرقام غير مطابقة!")

print("\n" + "🌙" * 35)

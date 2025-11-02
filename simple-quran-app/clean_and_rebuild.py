#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════════════════
سكريبت تنظيف وإعادة بناء قاعدة البيانات
يحذف القاعدة القديمة ويبنيها من الصفر بدون تكرار
════════════════════════════════════════════════════════════════════════════
"""

import sqlite3
import os
import sys

# مسارات قواعد البيانات
DB_TARGET = r"C:\quran11\quran_unified.db"
DB2_PATH = r"C:\quran11\Quran.db"
DB3_PATH = r"C:\quran11\Quran_irab_sarf.db"

def print_header(text):
    """طباعة عنوان منسق"""
    print("\n" + "═" * 70)
    print(f"  {text}")
    print("═" * 70 + "\n")

def delete_old_database():
    """حذف قاعدة البيانات القديمة"""
    print_header("🗑️  الخطوة 1: حذف القاعدة القديمة")

    if os.path.exists(DB_TARGET):
        try:
            os.remove(DB_TARGET)
            print(f"✅ تم حذف القاعدة القديمة: {DB_TARGET}")
        except Exception as e:
            print(f"❌ خطأ في حذف القاعدة القديمة: {e}")
            sys.exit(1)
    else:
        print(f"ℹ️  لا توجد قاعدة قديمة للحذف")

def create_fresh_database():
    """إنشاء قاعدة بيانات جديدة مع الجداول"""
    print_header("🔨 الخطوة 2: إنشاء قاعدة بيانات جديدة")

    conn = sqlite3.connect(DB_TARGET)
    cursor = conn.cursor()

    # جدول السور
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS surahs (
            surah_id INTEGER PRIMARY KEY,
            name_arabic TEXT NOT NULL,
            name_english TEXT,
            ayah_count INTEGER,
            revelation_type TEXT
        )
    """)
    print("✅ تم إنشاء جدول السور")

    # جدول الآيات
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
    print("✅ تم إنشاء جدول الآيات")

    # جدول الكلمات
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
    print("✅ تم إنشاء جدول الكلمات")

    # جدول الإعراب
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS irab (
            irab_id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,
            irab_text TEXT,
            FOREIGN KEY (word_id) REFERENCES words(word_id),
            UNIQUE(word_id)
        )
    """)
    print("✅ تم إنشاء جدول الإعراب")

    # جدول الصرف
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sarf (
            sarf_id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,
            sarf_text TEXT,
            FOREIGN KEY (word_id) REFERENCES words(word_id),
            UNIQUE(word_id)
        )
    """)
    print("✅ تم إنشاء جدول الصرف")

    # إنشاء الفهارس لتسريع البحث
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ayahs_surah ON ayahs(surah_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_ayah ON words(ayah_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_root ON words(root_text)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_irab_word ON irab(word_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sarf_word ON sarf(word_id)")
    print("✅ تم إنشاء الفهارس")

    conn.commit()
    conn.close()
    print("\n✅ تم إنشاء قاعدة البيانات بنجاح!")

def migrate_surahs():
    """نقل السور"""
    print_header("📚 الخطوة 3: نقل السور")

    conn_old = sqlite3.connect(DB2_PATH)
    conn_new = sqlite3.connect(DB_TARGET)

    cursor_old = conn_old.cursor()
    cursor_new = conn_new.cursor()

    cursor_old.execute("""
        SELECT SurahNo, SurahNameArabic, SurahNameEnglish, CountOfAyahs, RevelationType
        FROM Surahs
        ORDER BY SurahNo
    """)

    surahs = cursor_old.fetchall()

    for surah in surahs:
        cursor_new.execute("""
            INSERT OR IGNORE INTO surahs (surah_id, name_arabic, name_english, ayah_count, revelation_type)
            VALUES (?, ?, ?, ?, ?)
        """, surah)

    conn_new.commit()

    count = cursor_new.execute("SELECT COUNT(*) FROM surahs").fetchone()[0]
    print(f"✅ تم نقل {count} سورة")

    conn_old.close()
    conn_new.close()

def migrate_ayahs():
    """نقل الآيات"""
    print_header("📖 الخطوة 4: نقل الآيات")

    conn_old = sqlite3.connect(DB2_PATH)
    conn_new = sqlite3.connect(DB_TARGET)

    cursor_old = conn_old.cursor()
    cursor_new = conn_new.cursor()

    cursor_old.execute("""
        SELECT SurahNo, AyahNo, AyahText, JuzNo, PageNo
        FROM Ayahs
        ORDER BY SurahNo, AyahNo
    """)

    ayahs = cursor_old.fetchall()

    for ayah in ayahs:
        cursor_new.execute("""
            INSERT OR IGNORE INTO ayahs (surah_id, ayah_number, text_uthmani, juz_number, page_number)
            VALUES (?, ?, ?, ?, ?)
        """, ayah)

    conn_new.commit()

    count = cursor_new.execute("SELECT COUNT(*) FROM ayahs").fetchone()[0]
    print(f"✅ تم نقل {count} آية")

    conn_old.close()
    conn_new.close()

def migrate_words():
    """نقل الكلمات مع الإعراب والصرف - بدون تكرار"""
    print_header("📝 الخطوة 5: نقل الكلمات والإعراب والصرف")

    conn_old2 = sqlite3.connect(DB2_PATH)
    conn_old3 = sqlite3.connect(DB3_PATH)
    conn_new = sqlite3.connect(DB_TARGET)

    conn_old2.row_factory = sqlite3.Row
    conn_old3.row_factory = sqlite3.Row
    conn_new.row_factory = sqlite3.Row

    cursor_old2 = conn_old2.cursor()
    cursor_old3 = conn_old3.cursor()
    cursor_new = conn_new.cursor()

    print("جاري نقل الكلمات...")

    # استخدام INNER JOIN مع word_content_irab كقائمة أساسية (77,432 كلمة فقط)
    cursor_old3.execute("""
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

    words_data = cursor_old3.fetchall()
    total_words = len(words_data)

    print(f"إجمالي الكلمات للنقل: {total_words:,}")

    processed = 0
    words_inserted = 0
    irab_inserted = 0
    sarf_inserted = 0

    for word in words_data:
        # الحصول على ayah_id
        cursor_new.execute("""
            SELECT ayah_id FROM ayahs
            WHERE surah_id = ? AND ayah_number = ?
        """, (word['surahNo'], word['ayahNo']))

        ayah_row = cursor_new.fetchone()
        if not ayah_row:
            continue

        ayah_id = ayah_row['ayah_id']

        # إدراج الكلمة (INSERT OR IGNORE لتجنب التكرار)
        cursor_new.execute("""
            INSERT OR IGNORE INTO words (ayah_id, word_position, word_text, word_simple, root_text)
            VALUES (?, ?, ?, ?, ?)
        """, (ayah_id, word['wordNo'], word['wordWithHaraqah'], word['wordWithOutHaraqah'], word['Root']))

        if cursor_new.rowcount > 0:
            words_inserted += 1

        # الحصول على word_id
        cursor_new.execute("""
            SELECT word_id FROM words
            WHERE ayah_id = ? AND word_position = ?
        """, (ayah_id, word['wordNo']))

        word_row = cursor_new.fetchone()
        if word_row:
            word_id = word_row['word_id']

            # إدراج الإعراب
            if word['irabMushakkal']:
                cursor_new.execute("""
                    INSERT OR IGNORE INTO irab (word_id, irab_text)
                    VALUES (?, ?)
                """, (word_id, word['irabMushakkal']))

                if cursor_new.rowcount > 0:
                    irab_inserted += 1

            # إدراج الصرف
            if word['sarf']:
                cursor_new.execute("""
                    INSERT OR IGNORE INTO sarf (word_id, sarf_text)
                    VALUES (?, ?)
                """, (word_id, word['sarf']))

                if cursor_new.rowcount > 0:
                    sarf_inserted += 1

        processed += 1

        # تقرير التقدم
        if processed % 10000 == 0:
            conn_new.commit()
            print(f"  تم معالجة {processed:,} / {total_words:,} كلمة...")

    conn_new.commit()

    print(f"\n✅ تم نقل {words_inserted:,} كلمة")
    print(f"✅ تم نقل {irab_inserted:,} إعراب")
    print(f"✅ تم نقل {sarf_inserted:,} صرف")

    conn_old2.close()
    conn_old3.close()
    conn_new.close()

def verify_database():
    """التحقق من صحة القاعدة"""
    print_header("🔍 الخطوة 6: التحقق من القاعدة")

    conn = sqlite3.connect(DB_TARGET)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # عد السور
    cursor.execute("SELECT COUNT(*) as count FROM surahs")
    surahs_count = cursor.fetchone()['count']
    print(f"السور: {surahs_count:,} {'✅' if surahs_count == 114 else '❌'}")

    # عد الآيات
    cursor.execute("SELECT COUNT(*) as count FROM ayahs")
    ayahs_count = cursor.fetchone()['count']
    print(f"الآيات: {ayahs_count:,} {'✅' if ayahs_count == 6236 else '❌'}")

    # عد الكلمات
    cursor.execute("SELECT COUNT(*) as count FROM words")
    words_count = cursor.fetchone()['count']
    print(f"الكلمات: {words_count:,} {'✅' if words_count == 77432 else '❌'}")

    # عد الإعراب
    cursor.execute("SELECT COUNT(*) as count FROM irab")
    irab_count = cursor.fetchone()['count']
    print(f"الإعراب: {irab_count:,} {'✅' if irab_count > 0 else '❌'}")

    # عد الصرف
    cursor.execute("SELECT COUNT(*) as count FROM sarf")
    sarf_count = cursor.fetchone()['count']
    print(f"الصرف: {sarf_count:,} {'✅' if sarf_count > 0 else '❌'}")

    # عينة من البيانات
    print("\n📋 عينة من البيانات:")
    cursor.execute("""
        SELECT
            w.word_text,
            w.word_simple,
            w.root_text,
            i.irab_text,
            s.sarf_text
        FROM words w
        LEFT JOIN irab i ON w.word_id = i.word_id
        LEFT JOIN sarf s ON w.word_id = s.word_id
        LIMIT 3
    """)

    for row in cursor.fetchall():
        print(f"\n  الكلمة: {row['word_text']}")
        print(f"  بدون تشكيل: {row['word_simple']}")
        print(f"  الجذر: {row['root_text']}")
        print(f"  الإعراب: {row['irab_text'][:50] if row['irab_text'] else 'لا يوجد'}...")
        print(f"  الصرف: {row['sarf_text'][:50] if row['sarf_text'] else 'لا يوجد'}...")

    conn.close()

    # التحقق النهائي
    if surahs_count == 114 and ayahs_count == 6236 and words_count == 77432:
        print("\n" + "="*70)
        print("✅ ✅ ✅ القاعدة صحيحة ومكتملة! ✅ ✅ ✅")
        print("="*70)
        return True
    else:
        print("\n" + "="*70)
        print("⚠️  تحذير: القاعدة غير مكتملة!")
        print("="*70)
        return False

def main():
    """الدالة الرئيسية"""
    print("\n" + "🌙" * 35)
    print("        تنظيف وإعادة بناء قاعدة القرآن الموحدة")
    print("🌙" * 35)

    try:
        # التحقق من وجود قواعد البيانات المصدر
        if not os.path.exists(DB2_PATH):
            print(f"❌ لم يتم العثور على: {DB2_PATH}")
            sys.exit(1)

        if not os.path.exists(DB3_PATH):
            print(f"❌ لم يتم العثور على: {DB3_PATH}")
            sys.exit(1)

        # تأكيد من المستخدم
        print(f"\n⚠️  سيتم حذف القاعدة القديمة وإعادة بنائها من الصفر!")
        print(f"📁 المسار: {DB_TARGET}")

        # حذف القاعدة القديمة
        delete_old_database()

        # إنشاء قاعدة جديدة
        create_fresh_database()

        # نقل البيانات
        migrate_surahs()
        migrate_ayahs()
        migrate_words()

        # التحقق
        verify_database()

        print_header("🎉 اكتمل التنظيف وإعادة البناء بنجاح!")

    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

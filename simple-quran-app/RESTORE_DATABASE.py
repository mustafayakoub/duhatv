#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════════════════
سكريبت الاستعادة الطارئة
يستعيد quran_unified.db من القواعد الأصلية
════════════════════════════════════════════════════════════════════════════
"""

import sqlite3
import os
import sys
import shutil

# مسارات قواعد البيانات الأصلية (الصحيحة!)
DB_TARGET = r"C:\quran11\quran_unified.db"
DB_ORIGINAL_1 = r"C:\quran11\Quran.db"
DB_ORIGINAL_2 = r"C:\quran11\Quran_irab_sarf.db"

# القواعد البديلة (إذا لم تكن الأصلية موجودة)
DB_BACKUP_1 = r"C:\quran11\quran_ultimate_final.db"
DB_BACKUP_2 = r"C:\quran11\surah_database_app_v32.db"

def print_header(text):
    """طباعة عنوان منسق"""
    print("\n" + "═" * 70)
    print(f"  {text}")
    print("═" * 70 + "\n")

def check_original_databases():
    """التحقق من وجود القواعد الأصلية"""
    print_header("🔍 الخطوة 1: التحقق من القواعد الأصلية")

    original_1_exists = os.path.exists(DB_ORIGINAL_1)
    original_2_exists = os.path.exists(DB_ORIGINAL_2)

    print(f"Quran.db: {'✅ موجود' if original_1_exists else '❌ غير موجود'}")
    print(f"Quran_irab_sarf.db: {'✅ موجود' if original_2_exists else '❌ غير موجود'}")

    return original_1_exists and original_2_exists

def check_backup_databases():
    """التحقق من وجود قواعد بديلة"""
    print_header("🔍 التحقق من القواعد البديلة")

    backup_1_exists = os.path.exists(DB_BACKUP_1)
    backup_2_exists = os.path.exists(DB_BACKUP_2)

    print(f"quran_ultimate_final.db: {'✅ موجود' if backup_1_exists else '❌ غير موجود'}")
    print(f"surah_database_app_v32.db: {'✅ موجود' if backup_2_exists else '❌ غير موجود'}")

    if backup_1_exists:
        # فحص إذا كانت البديلة صالحة
        try:
            conn = sqlite3.connect(DB_BACKUP_1)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            if 'surahs' in tables and 'ayahs' in tables and 'words' in tables:
                cursor.execute("SELECT COUNT(*) FROM words")
                words_count = cursor.fetchone()[0]
                conn.close()

                print(f"\n✅ quran_ultimate_final.db تبدو جيدة!")
                print(f"   تحتوي على {words_count:,} كلمة")
                return 'backup_1'
        except:
            pass

    return None

def restore_from_backup(backup_type):
    """استعادة من نسخة بديلة"""
    print_header("🔄 استعادة من النسخة البديلة")

    if backup_type == 'backup_1':
        print(f"جاري نسخ {DB_BACKUP_1} إلى {DB_TARGET}")
        try:
            shutil.copy2(DB_BACKUP_1, DB_TARGET)
            print("✅ تمت الاستعادة بنجاح!")
            return True
        except Exception as e:
            print(f"❌ خطأ: {e}")
            return False

    return False

def rebuild_from_original():
    """إعادة البناء من القواعد الأصلية"""
    print_header("🔨 إعادة البناء من القواعد الأصلية")

    try:
        # حذف القاعدة القديمة إذا كانت موجودة
        if os.path.exists(DB_TARGET):
            os.remove(DB_TARGET)
            print("✅ تم حذف القاعدة القديمة")

        # إنشاء قاعدة جديدة
        conn = sqlite3.connect(DB_TARGET)
        cursor = conn.cursor()

        # إنشاء الجداول
        print("📝 إنشاء الجداول...")

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
        conn_old = sqlite3.connect(DB_ORIGINAL_1)
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
        conn_old = sqlite3.connect(DB_ORIGINAL_1)
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
        conn_old = sqlite3.connect(DB_ORIGINAL_2)
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
        total_words = len(words_data)
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
                print(f"  تم معالجة {processed:,} / {total_words:,} كلمة...")

        conn.commit()
        conn_old.close()
        print(f"✅ تم نقل {total_words:,} كلمة")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_database():
    """التحقق من القاعدة المستعادة"""
    print_header("🔍 التحقق من القاعدة")

    try:
        conn = sqlite3.connect(DB_TARGET)
        cursor = conn.cursor()

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
        print(f"الإعراب: {irab:,} {'✅' if irab > 0 else '❌'}")

        cursor.execute("SELECT COUNT(*) FROM sarf")
        sarf = cursor.fetchone()[0]
        print(f"الصرف: {sarf:,} {'✅' if sarf > 0 else '❌'}")

        conn.close()

        if surahs == 114 and ayahs == 6236 and words == 77432:
            print("\n" + "="*70)
            print("✅ ✅ ✅ القاعدة تم استعادتها بنجاح! ✅ ✅ ✅")
            print("="*70)
            return True
        else:
            print("\n⚠️ القاعدة غير مكتملة")
            return False

    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("\n" + "🚨" * 35)
    print("        استعادة quran_unified.db الطارئة")
    print("🚨" * 35)

    # التحقق من القواعد الأصلية
    if check_original_databases():
        print("\n✅ القواعد الأصلية موجودة!")
        print("📝 جاري إعادة البناء من القواعد الأصلية...")

        if rebuild_from_original():
            verify_database()
            print_header("🎉 تمت الاستعادة بنجاح!")
            print("يمكنك الآن تشغيل التطبيق باستخدام: RUN_TREE_VIEWER.bat")
        else:
            print_header("❌ فشلت الاستعادة!")

    else:
        print("\n⚠️ القواعد الأصلية غير موجودة!")

        # التحقق من البدائل
        backup = check_backup_databases()

        if backup:
            print("\n✅ تم العثور على نسخة بديلة!")
            if restore_from_backup(backup):
                verify_database()
                print_header("🎉 تمت الاستعادة من النسخة البديلة!")
            else:
                print_header("❌ فشلت الاستعادة!")
        else:
            print_header("❌ لا توجد قواعد بيانات للاستعادة منها!")
            print("\nالحلول المتاحة:")
            print("1. استعادة من نسخة احتياطية إذا كانت موجودة")
            print("2. الحصول على القواعد الأصلية:")
            print("   - Quran.db")
            print("   - Quran_irab_sarf.db")

if __name__ == '__main__':
    main()

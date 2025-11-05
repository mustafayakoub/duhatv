#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت استيراد البيانات القرآنية إلى قاعدة البيانات SQLite
"""

import sqlite3
import json
import os
import sys
from pathlib import Path

# محاولة استيراد openpyxl لقراءة Excel
try:
    import openpyxl
except ImportError:
    print("⚠️ تحذير: openpyxl غير مثبت")
    print("قم بتثبيته: pip install openpyxl")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# إعدادات المسارات
# ═══════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "quran.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

AYAT_DIR = DATA_DIR / "ayat"
SURAHS_FILE = DATA_DIR / "surahs" / "suar_quran_Mustafa_Yakoub.xlsx"
WORDS_DIR = DATA_DIR / "words"

# ═══════════════════════════════════════════════════════════════
# دوال مساعدة
# ═══════════════════════════════════════════════════════════════

def init_database():
    """إنشاء قاعدة البيانات وتطبيق Schema"""
    print("📚 إنشاء قاعدة البيانات...")

    # حذف قاعدة البيانات القديمة إن وجدت
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("  ✓ حذف قاعدة البيانات القديمة")

    # إنشاء قاعدة بيانات جديدة
    conn = sqlite3.connect(DB_PATH)

    # تطبيق Schema
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
        conn.executescript(schema_sql)

    conn.commit()
    print("  ✓ تم إنشاء قاعدة البيانات بنجاح")

    return conn


def import_surahs(conn):
    """استيراد بيانات السور من ملف Excel"""
    print("\n📖 استيراد بيانات السور...")

    if not SURAHS_FILE.exists():
        print(f"  ⚠️ ملف السور غير موجود: {SURAHS_FILE}")
        return False

    try:
        wb = openpyxl.load_workbook(SURAHS_FILE)
        ws = wb.active

        cursor = conn.cursor()
        count = 0

        # قراءة البيانات (تخطي الصف الأول - العناوين)
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]:  # تخطي الصفوف الفارغة
                continue

            cursor.execute("""
                INSERT INTO surahs (
                    id, name_ar, name_en, ayah_count, ayat_from, ayat_to,
                    word_count, letter_count, juz, page_from, page_to,
                    page_start, page_count, category, revelation_place,
                    revelation_order, revelation_details, central_theme,
                    virtues, remarks, rukus
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row[0],   # Number
                row[2],   # Surah Name (Arabic)
                row[1],   # surahNameEnglish
                row[3],   # Ayat Count
                row[4],   # surahAyatFrom
                row[5],   # surahAyatTo
                row[6],   # Number of Words
                row[7],   # Number of Letters
                row[8],   # Juz' and Hizb
                row[9],   # From Page
                row[10],  # To Page
                row[11],  # Surah Start Page
                row[12],  # Number of Pages
                row[13],  # Category
                row[14],  # Meccan or Medinan
                row[15],  # Order of Revelation
                row[16],  # Details of Revelation
                row[20],  # Central Theme/Purpose
                row[25],  # Virtues
                row[33],  # surahRemarks
                row[34],  # Rukus
            ))
            count += 1

        conn.commit()
        print(f"  ✓ تم استيراد {count} سورة")
        return True

    except Exception as e:
        print(f"  ❌ خطأ في استيراد السور: {e}")
        return False


def read_txt_ayahs(file_path):
    """قراءة ملف txt للآيات (صيغة: surah|ayah|text)"""
    ayahs = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split('|')
            if len(parts) >= 3:
                surah_id = int(parts[0])
                ayah_id = int(parts[1])
                text = parts[2]

                key = (surah_id, ayah_id)
                ayahs[key] = text

    return ayahs


def read_json_ayahs(file_path):
    """قراءة ملف JSON للآيات"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    ayahs = {}
    for item in data:
        surah_id = item.get('sura_no') or item.get('surahNo')
        ayah_id = item.get('aya_no') or item.get('ayahNo')
        text = item.get('aya_text') or item.get('text')

        if surah_id and ayah_id and text:
            key = (surah_id, ayah_id)
            ayahs[key] = text

    return ayahs


def import_ayahs(conn):
    """استيراد بيانات الآيات من جميع الملفات"""
    print("\n📝 استيراد بيانات الآيات...")

    # خريطة الملفات والأعمدة
    files_map = {
        'AlAWWal.txt': 'text_awwal',
        'quran-uthmani-min_-Mushakkal.txt': 'text_uthmani_min',
        'hafsData_v2-0.json': 'text_hafs',
        'warshData_v2-1.json': 'text_warsh',
        'QalounData_v2-1.json': 'text_qaloun',
        'DouriData_v2-0.json': 'text_douri',
        'shubaData_v2-0.json': 'text_shuba',
        'SousiData_v2-0.json': 'text_sousi',
        'Amiry-Mushakkal.txt': 'text_amiry',
        'Emalei_-Mushakkal_fasel.txt': 'text_imlaei',
        'Emalei_-Mini_Mushakkal_fasel.txt': 'text_imlaei_mini',
        'Emalei_-No-Mushakkal_fasel.txt': 'text_imlaei_plain',
        'quran-simple-plain_-Mushakkal_Fasel.txt': 'text_simple_fasel',
        'quran-simple-plain_-Mushakkal_Tam.txt': 'text_simple_tam',
        'Ajami-.txt': 'text_ajami',
        'Transliteration_Latin.txt': 'text_latin',
        'quran_text_with_tajweed.json': 'text_tajweed',
    }

    # قراءة كل الملفات
    ayahs_data = {}

    for filename, column_name in files_map.items():
        file_path = AYAT_DIR / filename

        if not file_path.exists():
            print(f"  ⚠️ ملف غير موجود: {filename}")
            continue

        print(f"  📄 قراءة: {filename}...")

        try:
            if filename.endswith('.json'):
                data = read_json_ayahs(file_path)
            else:
                data = read_txt_ayahs(file_path)

            # دمج البيانات
            for key, text in data.items():
                if key not in ayahs_data:
                    ayahs_data[key] = {}
                ayahs_data[key][column_name] = text

            print(f"    ✓ تم قراءة {len(data)} آية")

        except Exception as e:
            print(f"    ❌ خطأ: {e}")

    # إدخال البيانات في قاعدة البيانات
    print("\n  💾 إدخال البيانات في قاعدة البيانات...")

    cursor = conn.cursor()
    count = 0

    for (surah_id, ayah_id), texts in sorted(ayahs_data.items()):
        # استخدام text_hafs كأساس للعثماني الكامل إذا لم يكن موجوداً
        text_uthmani = texts.get('text_hafs') or texts.get('text_uthmani_min') or ''

        cursor.execute("""
            INSERT INTO ayahs (
                surah_id, ayah_id,
                text_awwal, text_uthmani, text_uthmani_min,
                text_hafs, text_warsh, text_qaloun, text_douri,
                text_shuba, text_sousi, text_amiry,
                text_imlaei, text_imlaei_mini, text_imlaei_plain,
                text_simple_fasel, text_simple_tam,
                text_ajami, text_latin, text_tajweed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            surah_id, ayah_id,
            texts.get('text_awwal'),
            text_uthmani,
            texts.get('text_uthmani_min'),
            texts.get('text_hafs'),
            texts.get('text_warsh'),
            texts.get('text_qaloun'),
            texts.get('text_douri'),
            texts.get('text_shuba'),
            texts.get('text_sousi'),
            texts.get('text_amiry'),
            texts.get('text_imlaei'),
            texts.get('text_imlaei_mini'),
            texts.get('text_imlaei_plain'),
            texts.get('text_simple_fasel'),
            texts.get('text_simple_tam'),
            texts.get('text_ajami'),
            texts.get('text_latin'),
            texts.get('text_tajweed'),
        ))

        count += 1

        if count % 1000 == 0:
            conn.commit()
            print(f"    ... {count} آية")

    conn.commit()
    print(f"  ✓ تم استيراد {count} آية")
    return True


def import_words(conn):
    """استيراد بيانات الكلمات"""
    print("\n🔤 استيراد بيانات الكلمات...")

    words_file = WORDS_DIR / "quran_word Mustafa_Y2.txt"

    if not words_file.exists():
        print(f"  ⚠️ ملف الكلمات غير موجود: {words_file}")
        return False

    cursor = conn.cursor()
    count = 0

    with open(words_file, 'r', encoding='utf-8') as f:
        # تخطي الصف الأول (العناوين)
        next(f)

        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split('|')
            if len(parts) >= 9:
                cursor.execute("""
                    INSERT INTO words (
                        id, word_text, harf_no_in_word,
                        word_imlaei1, word_imlaei2,
                        surah_id, ayah_id, word_no_in_ayah, harf_no_total
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    int(parts[0]),   # Word No In Quran
                    parts[1],        # الكلمة مشكلة
                    int(parts[2]),   # Harf No in Word
                    parts[3],        # emlai1
                    parts[4],        # emlai2
                    int(parts[5]),   # sura
                    int(parts[6]),   # Aya
                    int(parts[7]),   # No In Aya
                    int(parts[8]),   # harf no
                ))

                count += 1

                if count % 10000 == 0:
                    conn.commit()
                    print(f"    ... {count} كلمة")

    conn.commit()
    print(f"  ✓ تم استيراد {count} كلمة")
    return True


def import_word_statistics(conn):
    """استيراد إحصائيات الكلمات"""
    print("\n📊 استيراد إحصائيات الكلمات...")

    stats_file = WORDS_DIR / "word_statistics.json"

    if not stats_file.exists():
        print(f"  ⚠️ ملف الإحصائيات غير موجود")
        return False

    with open(stats_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cursor = conn.cursor()
    count = 0

    for item in data:
        word_id = item.get('ID')
        if not word_id:
            continue

        cursor.execute("""
            UPDATE words SET
                root = ?,
                repeat_count = ?,
                root_repeat_count = ?,
                seq_in_similar_words = ?,
                seq_in_similar_roots = ?,
                ayah_count_with_word = ?,
                ayah_count_with_root = ?,
                surah_count_with_word = ?,
                surah_count_with_root = ?,
                word_no_in_surah = ?
            WHERE id = ?
        """, (
            item.get('root'),
            item.get('repeatitionCount'),
            item.get('rootRepeatitionCount'),
            item.get('sequenceInSimilarWords'),
            item.get('sequenceInSimilarRoots'),
            item.get('ayahCountWithWord'),
            item.get('ayahCountWithRoot'),
            item.get('surahCountWithWord'),
            item.get('surahCountWithRoot'),
            item.get('wordNoInSurah'),
            word_id,
        ))

        count += 1

        if count % 10000 == 0:
            conn.commit()
            print(f"    ... {count} كلمة")

    conn.commit()
    print(f"  ✓ تم تحديث {count} كلمة")
    return True


def import_word_details(conn):
    """استيراد تفاصيل الكلمات (إعراب، صرف، معاني، رسم)"""
    print("\n📚 استيراد تفاصيل الكلمات...")

    files_map = {
        'word_content_irab.json': 'irab',
        'word_content_sarf.json': 'sarf',
        'word_content_meaning.json': 'meaning',
        'word_content_rasm.json': 'rasm',
    }

    cursor = conn.cursor()

    for filename, column_name in files_map.items():
        file_path = WORDS_DIR / filename

        if not file_path.exists():
            print(f"  ⚠️ ملف غير موجود: {filename}")
            continue

        print(f"  📄 قراءة: {filename}...")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        for item in data:
            word_no = item.get('wordNo')
            surah_no = item.get('surahNo')
            ayah_no = item.get('ayahNo')

            if not all([word_no, surah_no, ayah_no]):
                continue

            # البحث عن word_id من جدول words
            cursor.execute("""
                SELECT id FROM words
                WHERE surah_id = ? AND ayah_id = ? AND word_no_in_ayah = ?
            """, (surah_no, ayah_no, word_no))

            result = cursor.fetchone()
            if not result:
                continue

            word_id = result[0]

            # الحصول على القيمة المناسبة
            if column_name == 'irab':
                value = item.get('irabMushakkal')
            elif column_name == 'rasm':
                value = item.get('rasm')
            else:
                value = item.get(column_name)

            # إدخال أو تحديث
            cursor.execute(f"""
                INSERT INTO word_details (word_id, {column_name})
                VALUES (?, ?)
                ON CONFLICT(word_id) DO UPDATE SET {column_name} = ?
            """, (word_id, value, value))

            count += 1

            if count % 10000 == 0:
                conn.commit()
                print(f"    ... {count} كلمة")

        conn.commit()
        print(f"    ✓ تم إدخال {count} سجل")

    return True


# ═══════════════════════════════════════════════════════════════
# البرنامج الرئيسي
# ═══════════════════════════════════════════════════════════════

def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║      📖 استيراد البيانات القرآنية - Quran Clean      ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # التحقق من وجود المجلدات
    if not DATA_DIR.exists():
        print("❌ مجلد data/ غير موجود!")
        print("   قم بإنشائه ووضع الملفات فيه")
        return

    try:
        # إنشاء قاعدة البيانات
        conn = init_database()

        # استيراد البيانات
        import_surahs(conn)
        import_ayahs(conn)
        import_words(conn)
        import_word_statistics(conn)
        import_word_details(conn)

        # إغلاق الاتصال
        conn.close()

        print("\n" + "═" * 60)
        print("✅ تم استيراد جميع البيانات بنجاح!")
        print("═" * 60)
        print()
        print("📂 قاعدة البيانات: quran.db")
        print("🚀 الآن يمكنك تشغيل التطبيق: python app.py")
        print()

    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

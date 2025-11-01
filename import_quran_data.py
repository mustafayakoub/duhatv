#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت استيراد البيانات المُصدّرة
Import Exported Quran Data

يستورد البيانات من ملفات JSON المُصدّرة إلى قاعدة البيانات الجديدة
"""

import sqlite3
import json
import os
import glob
from pathlib import Path

# ============================================================================
# الإعدادات
# ============================================================================

# مجلد البيانات المُصدّرة
IMPORT_DIR = "quran_export"

# قاعدة البيانات الهدف
TARGET_DB = "quran_ultimate.db"

# ============================================================================


def import_schema(schema_file):
    """استيراد بنية قاعدة البيانات"""
    print("\n" + "="*70)
    print("📦 استيراد بنية قاعدة البيانات...")
    print("="*70)

    try:
        # حذف قاعدة البيانات القديمة
        if os.path.exists(TARGET_DB):
            os.remove(TARGET_DB)
            print(f"✅ تم حذف قاعدة البيانات القديمة")

        # الاتصال وإنشاء قاعدة جديدة
        conn = sqlite3.connect(TARGET_DB)
        cursor = conn.cursor()

        # قراءة وتنفيذ SQL
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            cursor.executescript(sql_script)

        conn.commit()
        conn.close()

        print(f"✅ تم إنشاء قاعدة البيانات: {TARGET_DB}")
        return True

    except Exception as e:
        print(f"❌ خطأ في استيراد البنية: {e}")
        return False


def import_json_file(db_path, json_file):
    """استيراد ملف JSON واحد"""
    try:
        # قراءة ملف JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not data:
            return 0

        # استخراج اسم الجدول من اسم الملف
        filename = os.path.basename(json_file)
        table_name = filename.replace('.json', '').split('_part')[0]

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # الحصول على أسماء الأعمدة
        columns = list(data[0].keys())
        placeholders = ','.join(['?' for _ in columns])
        column_names = ','.join(columns)

        # إدراج البيانات
        insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

        rows_inserted = 0
        for row in data:
            values = [row[col] for col in columns]
            cursor.execute(insert_sql, values)
            rows_inserted += 1

        conn.commit()
        conn.close()

        return rows_inserted

    except Exception as e:
        print(f"  ❌ خطأ في استيراد {json_file}: {e}")
        return 0


def import_sample_data(sample_file):
    """استيراد ملف العينة"""
    print("\n" + "="*70)
    print("📥 استيراد بيانات العينة...")
    print("="*70 + "\n")

    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            all_data = json.load(f)

        conn = sqlite3.connect(TARGET_DB)
        cursor = conn.cursor()

        total_rows = 0

        for table_name, data in all_data.items():
            if not data:
                print(f"  ⚠️  {table_name}: فارغ - تخطي")
                continue

            # الحصول على أسماء الأعمدة
            columns = list(data[0].keys())
            placeholders = ','.join(['?' for _ in columns])
            column_names = ','.join(columns)

            # إدراج البيانات
            insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

            rows_inserted = 0
            for row in data:
                try:
                    values = [row[col] for col in columns]
                    cursor.execute(insert_sql, values)
                    rows_inserted += 1
                except sqlite3.IntegrityError:
                    # تخطي السجلات المكررة
                    pass

            conn.commit()
            total_rows += rows_inserted
            print(f"  ✓ {table_name}: {rows_inserted:,} سجل")

        conn.close()

        print(f"\n✅ تم استيراد {total_rows:,} سجل من العينة")
        return total_rows

    except Exception as e:
        print(f"❌ خطأ في استيراد العينة: {e}")
        import traceback
        traceback.print_exc()
        return 0


def import_all_json_files():
    """استيراد جميع ملفات JSON"""
    print("\n" + "="*70)
    print("📥 استيراد جميع ملفات JSON...")
    print("="*70 + "\n")

    # البحث عن جميع ملفات JSON (ما عدا العينة)
    json_files = []
    for file in glob.glob(os.path.join(IMPORT_DIR, "*.json")):
        if "sample_data" not in file:
            json_files.append(file)

    json_files.sort()

    if not json_files:
        print("⚠️  لم يتم العثور على ملفات JSON")
        return 0

    print(f"📊 عدد الملفات: {len(json_files)}\n")

    total_rows = 0
    file_groups = {}

    # تجميع الملفات حسب الجدول
    for json_file in json_files:
        filename = os.path.basename(json_file)
        table_name = filename.replace('.json', '').split('_part')[0]

        if table_name not in file_groups:
            file_groups[table_name] = []
        file_groups[table_name].append(json_file)

    # استيراد كل جدول
    for table_name, files in sorted(file_groups.items()):
        files.sort()  # ترتيب الأجزاء
        table_rows = 0

        if len(files) == 1:
            # ملف واحد
            rows = import_json_file(TARGET_DB, files[0])
            table_rows = rows
            file_size = os.path.getsize(files[0]) / 1024
            print(f"  ✓ {table_name}: {rows:,} سجل ({file_size:.1f} KB)")
        else:
            # ملفات متعددة
            print(f"  📦 {table_name}: {len(files)} ملف")
            for i, json_file in enumerate(files, 1):
                rows = import_json_file(TARGET_DB, json_file)
                table_rows += rows
                file_size = os.path.getsize(json_file) / 1024
                print(f"    ✓ الجزء {i}/{len(files)}: {rows:,} سجل ({file_size:.1f} KB)")

        total_rows += table_rows

    print(f"\n✅ تم استيراد {total_rows:,} سجل إجمالي")
    return total_rows


def verify_import():
    """التحقق من الاستيراد"""
    print("\n" + "="*70)
    print("🔍 التحقق من البيانات المستوردة...")
    print("="*70 + "\n")

    try:
        conn = sqlite3.connect(TARGET_DB)
        cursor = conn.cursor()

        # عدد السور
        cursor.execute("SELECT COUNT(*) FROM surahs_info")
        surahs_count = cursor.fetchone()[0]
        print(f"  📚 عدد السور: {surahs_count}")

        # عدد الآيات
        cursor.execute("SELECT COUNT(*) FROM quran_text")
        verses_count = cursor.fetchone()[0]
        print(f"  📖 عدد الآيات: {verses_count:,}")

        # عدد آيات التجويد
        cursor.execute("SELECT COUNT(*) FROM quran_tajweed")
        tajweed_count = cursor.fetchone()[0]
        print(f"  🎨 آيات التجويد: {tajweed_count:,}")

        # عدد التفاسير
        cursor.execute("SELECT COUNT(*) FROM tafsir_muyassar")
        tafsir1_count = cursor.fetchone()[0]
        print(f"  📚 التفسير الميسر: {tafsir1_count:,}")

        cursor.execute("SELECT COUNT(*) FROM tafsir_saadi")
        tafsir2_count = cursor.fetchone()[0]
        print(f"  📚 تفسير السعدي: {tafsir2_count:,}")

        # عدد الترجمات
        cursor.execute("SELECT COUNT(*) FROM translation_english")
        trans_en_count = cursor.fetchone()[0]
        print(f"  🌍 الترجمة الإنجليزية: {trans_en_count:,}")

        cursor.execute("SELECT COUNT(*) FROM translation_french")
        trans_fr_count = cursor.fetchone()[0]
        print(f"  🌍 الترجمة الفرنسية: {trans_fr_count:,}")

        # اختبار استعلام معقد
        print("\n  🧪 اختبار استعلام معقد...")
        cursor.execute("""
            SELECT qt.text, qtj.tajweed_text, tm.text
            FROM quran_text qt
            LEFT JOIN quran_tajweed qtj ON qt.surah_id = qtj.surah_id AND qt.ayah_id = qtj.ayah_id
            LEFT JOIN tafsir_muyassar tm ON qt.surah_id = tm.surah_id AND qt.ayah_id = tm.ayah_id
            WHERE qt.surah_id = 1 AND qt.ayah_id = 1
        """)
        result = cursor.fetchone()

        if result and result[0]:
            print(f"  ✅ الآية الأولى: {result[0][:50]}...")
            if result[1]:
                print(f"  ✅ التجويد موجود")
            if result[2]:
                print(f"  ✅ التفسير موجود")
        else:
            print(f"  ⚠️  لم يتم العثور على البيانات!")

        conn.close()

        # حجم قاعدة البيانات
        db_size = os.path.getsize(TARGET_DB) / (1024 * 1024)
        print(f"\n  💾 حجم قاعدة البيانات: {db_size:.2f} MB")

        return True

    except Exception as e:
        print(f"  ❌ خطأ في التحقق: {e}")
        return False


def main():
    """الدالة الرئيسية"""

    print("="*70)
    print("📥 استيراد بيانات القرآن الكريم")
    print("="*70)

    # التحقق من وجود مجلد البيانات
    if not os.path.exists(IMPORT_DIR):
        print(f"\n❌ مجلد البيانات غير موجود: {IMPORT_DIR}")
        print("\n💡 تأكد من:")
        print(f"   1. تشغيل سكريبت التصدير أولاً على جهازك")
        print(f"   2. رفع مجلد '{IMPORT_DIR}' إلى هنا")
        return

    # البحث عن ملف البنية
    schema_file = os.path.join(IMPORT_DIR, "01_schema.sql")
    if not os.path.exists(schema_file):
        # استخدام البنية الموجودة
        schema_file = "create_quran_database_final.sql"
        print(f"\n⚠️  لم يتم العثور على البنية المُصدّرة")
        print(f"✅ سيتم استخدام: {schema_file}")

    # استيراد البنية
    if not import_schema(schema_file):
        return

    # البحث عن ملف العينة
    sample_file = os.path.join(IMPORT_DIR, "sample_data.json")

    # البحث عن ملفات JSON
    json_files = glob.glob(os.path.join(IMPORT_DIR, "*.json"))
    json_files = [f for f in json_files if "sample_data" not in f]

    # السؤال عن نوع الاستيراد
    if os.path.exists(sample_file) and json_files:
        print("\n" + "="*70)
        print("اختر نوع الاستيراد:")
        print("="*70)
        print("1. استيراد العينة فقط (سريع - للاختبار)")
        print("2. استيراد البيانات الكاملة")

        choice = input("\nاختيارك (1/2) [افتراضي: 2]: ").strip() or "2"

        if choice == "1":
            import_sample_data(sample_file)
        else:
            import_all_json_files()

    elif os.path.exists(sample_file):
        import_sample_data(sample_file)

    elif json_files:
        import_all_json_files()

    else:
        print("\n❌ لم يتم العثور على ملفات JSON للاستيراد")
        return

    # التحقق من الاستيراد
    verify_import()

    # النتيجة النهائية
    print("\n" + "="*70)
    print("✅ اكتمل الاستيراد بنجاح!")
    print("="*70)
    print(f"\n📍 قاعدة البيانات: {os.path.abspath(TARGET_DB)}")
    print(f"\n🚀 جاهز للتشغيل:")
    print(f"   python quran_app_ultimate_final_v4.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  تم الإلغاء بواسطة المستخدم")
    except Exception as e:
        print(f"\n\n❌ خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()

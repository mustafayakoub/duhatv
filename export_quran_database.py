#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تصدير البيانات من قاعدة بيانات كبيرة
Export Data from Large Database

استخدم هذا السكريبت على جهازك لتصدير البيانات من quran_ultimate_final.db
"""

import sqlite3
import json
import os
from pathlib import Path

# ============================================================================
# الإعدادات - عدّل هذه القيم حسب موقع قاعدة بياناتك
# ============================================================================

# مسار قاعدة البيانات الأصلية (على Windows مثلاً)
SOURCE_DB = "quran_ultimate_final.db"  # أو المسار الكامل مثل: r"C:\quran9\quran_ultimate_final.db"

# مجلد الإخراج
OUTPUT_DIR = "quran_export"

# ============================================================================

def create_output_dir():
    """إنشاء مجلد الإخراج"""
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    print(f"📁 مجلد الإخراج: {OUTPUT_DIR}")


def analyze_database(db_path):
    """تحليل قاعدة البيانات"""
    print("\n" + "="*70)
    print("🔍 تحليل قاعدة البيانات...")
    print("="*70)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # الحصول على قائمة الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]

        print(f"\n📊 عدد الجداول: {len(tables)}")
        print("\nالجداول الموجودة:")

        table_info = {}
        total_rows = 0

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            table_info[table] = count
            total_rows += count
            print(f"  • {table}: {count:,} سجل")

        print(f"\n📈 إجمالي السجلات: {total_rows:,}")

        # حجم الملف
        file_size = os.path.getsize(db_path) / (1024 * 1024)
        print(f"💾 حجم الملف: {file_size:.2f} MB")

        conn.close()
        return table_info

    except Exception as e:
        print(f"❌ خطأ في التحليل: {e}")
        return {}


def export_table_structure(db_path):
    """تصدير بنية الجداول (CREATE TABLE statements)"""
    print("\n" + "="*70)
    print("📝 تصدير بنية الجداول...")
    print("="*70)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        output_file = os.path.join(OUTPUT_DIR, "01_schema.sql")

        with open(output_file, 'w', encoding='utf-8') as f:
            # الحصول على جميع أوامر CREATE
            cursor.execute("""
                SELECT sql FROM sqlite_master
                WHERE type IN ('table', 'index')
                AND name NOT LIKE 'sqlite_%'
                ORDER BY type DESC, name
            """)

            f.write("-- ============================================================================\n")
            f.write("-- بنية قاعدة البيانات\n")
            f.write("-- Database Schema\n")
            f.write("-- ============================================================================\n\n")

            for row in cursor.fetchall():
                if row[0]:
                    f.write(row[0] + ";\n\n")

        conn.close()

        file_size = os.path.getsize(output_file) / 1024
        print(f"✅ تم التصدير: {output_file} ({file_size:.1f} KB)")

        return output_file

    except Exception as e:
        print(f"❌ خطأ في تصدير البنية: {e}")
        return None


def export_table_to_json(db_path, table_name, chunk_size=1000):
    """تصدير جدول إلى ملفات JSON (مقسم إلى أجزاء)"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # عدد السجلات
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_rows = cursor.fetchone()[0]

        if total_rows == 0:
            print(f"  ⚠️  {table_name}: فارغ - تخطي")
            conn.close()
            return

        print(f"  📦 {table_name}: {total_rows:,} سجل", end="")

        # إذا كان الجدول صغير، ملف واحد
        if total_rows <= chunk_size:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = [dict(row) for row in cursor.fetchall()]

            output_file = os.path.join(OUTPUT_DIR, f"{table_name}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(rows, f, ensure_ascii=False, indent=2)

            file_size = os.path.getsize(output_file) / 1024
            print(f" → {file_size:.1f} KB")

        # إذا كان الجدول كبير، تقسيم إلى أجزاء
        else:
            num_chunks = (total_rows + chunk_size - 1) // chunk_size
            print(f" → {num_chunks} ملف")

            for chunk_num in range(num_chunks):
                offset = chunk_num * chunk_size
                cursor.execute(f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET {offset}")
                rows = [dict(row) for row in cursor.fetchall()]

                output_file = os.path.join(OUTPUT_DIR, f"{table_name}_part{chunk_num+1:03d}.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(rows, f, ensure_ascii=False, indent=2)

                file_size = os.path.getsize(output_file) / 1024
                print(f"    ✓ الجزء {chunk_num+1}/{num_chunks}: {file_size:.1f} KB")

        conn.close()

    except Exception as e:
        print(f"❌ خطأ في تصدير {table_name}: {e}")


def export_all_data_json(db_path, table_info):
    """تصدير جميع البيانات إلى JSON"""
    print("\n" + "="*70)
    print("📤 تصدير البيانات إلى JSON...")
    print("="*70 + "\n")

    # ترتيب الجداول حسب الأهمية
    priority_tables = [
        'surahs_info',
        'quran_text',
        'quran_tajweed',
        'tafsir_muyassar',
        'tafsir_saadi',
        'tafsir_baghawi',
        'translation_english',
        'translation_french',
        'irab',
        'sarf',
        'sajda_ayahs',
        'topics',
        'topics_verses',
        'user_settings'
    ]

    # تصدير الجداول ذات الأولوية أولاً
    exported = set()
    for table in priority_tables:
        if table in table_info:
            export_table_to_json(db_path, table)
            exported.add(table)

    # تصدير باقي الجداول
    for table in table_info:
        if table not in exported and not table.startswith('sqlite_'):
            export_table_to_json(db_path, table)


def export_sample_data(db_path):
    """تصدير عينة صغيرة للاختبار السريع"""
    print("\n" + "="*70)
    print("🎯 تصدير عينة للاختبار (أول 100 سجل من كل جدول)...")
    print("="*70)

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        output_file = os.path.join(OUTPUT_DIR, "sample_data.json")

        # الحصول على قائمة الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]

        sample_data = {}

        for table in tables:
            if table.startswith('sqlite_'):
                continue

            cursor.execute(f"SELECT * FROM {table} LIMIT 100")
            rows = [dict(row) for row in cursor.fetchall()]
            sample_data[table] = rows
            print(f"  ✓ {table}: {len(rows)} سجل")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)

        conn.close()

        file_size = os.path.getsize(output_file) / 1024
        print(f"\n✅ عينة الاختبار: {output_file} ({file_size:.1f} KB)")

        return output_file

    except Exception as e:
        print(f"❌ خطأ في تصدير العينة: {e}")
        return None


def create_import_instructions():
    """إنشاء ملف تعليمات الاستيراد"""
    instructions = """
# 📋 تعليمات استيراد البيانات
# Import Instructions

## الملفات المُصدّرة:

1. **01_schema.sql** - بنية قاعدة البيانات (الجداول والفهارس)
2. **sample_data.json** - عينة صغيرة للاختبار السريع
3. **[table_name].json** - بيانات كاملة لجداول صغيرة
4. **[table_name]_partXXX.json** - بيانات مقسمة لجداول كبيرة

## كيفية الاستيراد:

### الطريقة 1: رفع الملفات يدوياً
1. ارفع جميع ملفات JSON إلى الخادم
2. سيتم إنشاء سكريبت استيراد تلقائي

### الطريقة 2: استخدام العينة للاختبار
1. ارفع فقط `sample_data.json`
2. اختبر التطبيق مع البيانات العينة
3. ثم ارفع الملفات الكاملة لاحقاً

## حجم الملفات:

انظر إلى حجم كل ملف JSON:
- الملفات < 5 MB يمكن رفعها مباشرة
- الملفات الكبيرة تم تقسيمها تلقائياً

## ملاحظات:

- جميع الملفات بترميز UTF-8
- البيانات بصيغة JSON للسهولة
- يمكنك نسخ ولصق محتوى الملفات الصغيرة مباشرة

---

*تم التصدير بواسطة: export_quran_database.py*
"""

    readme_file = os.path.join(OUTPUT_DIR, "README.txt")
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(instructions)

    print(f"\n📄 تعليمات الاستيراد: {readme_file}")


def main():
    """الدالة الرئيسية"""

    print("="*70)
    print("🚀 أداة تصدير بيانات القرآن الكريم")
    print("="*70)

    # التحقق من وجود قاعدة البيانات
    if not os.path.exists(SOURCE_DB):
        print(f"\n❌ لم يتم العثور على قاعدة البيانات: {SOURCE_DB}")
        print("\n💡 تأكد من:")
        print(f"   1. أن الملف موجود في نفس المجلد مع هذا السكريبت")
        print(f"   2. أو عدّل متغير SOURCE_DB في أعلى الملف ليشير إلى المسار الصحيح")
        print(f"\nمثال على Windows:")
        print(f'   SOURCE_DB = r"C:\\quran9\\quran_ultimate_final.db"')
        return

    # إنشاء مجلد الإخراج
    create_output_dir()

    # تحليل قاعدة البيانات
    table_info = analyze_database(SOURCE_DB)

    if not table_info:
        print("\n❌ فشل تحليل قاعدة البيانات")
        return

    # السؤال عن نوع التصدير
    print("\n" + "="*70)
    print("اختر نوع التصدير:")
    print("="*70)
    print("1. تصدير عينة صغيرة للاختبار (سريع - موصى به أولاً)")
    print("2. تصدير البيانات الكاملة (قد يستغرق وقتاً)")
    print("3. كلاهما")

    choice = input("\nاختيارك (1/2/3) [افتراضي: 1]: ").strip() or "1"

    # تصدير البنية دائماً
    export_table_structure(SOURCE_DB)

    # تصدير حسب الاختيار
    if choice == "1":
        export_sample_data(SOURCE_DB)
    elif choice == "2":
        export_all_data_json(SOURCE_DB, table_info)
    elif choice == "3":
        export_sample_data(SOURCE_DB)
        export_all_data_json(SOURCE_DB, table_info)

    # إنشاء ملف التعليمات
    create_import_instructions()

    # النتيجة النهائية
    print("\n" + "="*70)
    print("✅ تم التصدير بنجاح!")
    print("="*70)

    # حساب حجم المجلد
    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            file_count += 1

    print(f"\n📊 الإحصائيات:")
    print(f"   • عدد الملفات: {file_count}")
    print(f"   • الحجم الإجمالي: {total_size / (1024*1024):.2f} MB")
    print(f"   • المجلد: {os.path.abspath(OUTPUT_DIR)}")

    print("\n📤 الخطوة التالية:")
    print(f"   1. افتح مجلد: {OUTPUT_DIR}")
    print(f"   2. ارفع الملفات المُصدّرة")
    print(f"   3. سيتم إنشاء سكريبت استيراد تلقائي")

    print("\n" + "="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  تم الإلغاء بواسطة المستخدم")
    except Exception as e:
        print(f"\n\n❌ خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()

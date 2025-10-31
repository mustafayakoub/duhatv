#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تشخيصي لفحص قواعد البيانات
Diagnostic Script for Database Analysis
"""

import sqlite3
import os
from pathlib import Path

def analyze_database(db_path: str):
    """تحليل قاعدة بيانات واحدة"""

    print("\n" + "="*80)
    print(f"📊 تحليل قاعدة البيانات: {db_path}")
    print("="*80)

    if not os.path.exists(db_path):
        print(f"❌ الملف غير موجود: {db_path}")
        return False

    file_size = os.path.getsize(db_path) / (1024 * 1024)  # MB
    print(f"📏 حجم الملف: {file_size:.2f} MB")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # الحصول على قائمة الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print(f"\n📋 عدد الجداول: {len(tables)}")
        print("-" * 80)

        for table in tables:
            table_name = table[0]
            print(f"\n🔹 الجدول: {table_name}")

            # عدد السجلات
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   عدد السجلات: {count}")

            # الأعمدة
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"   عدد الأعمدة: {len(columns)}")
            print(f"   الأعمدة:")

            for col in columns:
                col_id, col_name, col_type, col_notnull, col_default, col_pk = col
                print(f"      • {col_name} ({col_type})")

            # عينة من البيانات (أول سطر)
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                sample = cursor.fetchone()
                if sample:
                    print(f"\n   📄 عينة من البيانات (أول سطر):")
                    for i, col in enumerate(columns):
                        col_name = col[1]
                        value = sample[i] if i < len(sample) else "N/A"
                        # عرض جزء من القيمة إذا كانت طويلة
                        if isinstance(value, str) and len(value) > 100:
                            value = value[:100] + "..."
                        print(f"      {col_name}: {value}")

        conn.close()
        print("\n" + "="*80)
        print("✅ تم التحليل بنجاح")
        return True

    except Exception as e:
        print(f"\n❌ خطأ في التحليل: {e}")
        return False


def main():
    """الدالة الرئيسية"""

    print("\n" + "="*80)
    print("🔍 سكريبت تشخيصي لقواعد البيانات")
    print("Database Diagnostic Script")
    print("="*80)

    # قائمة المسارات المحتملة
    possible_paths = [
        r"C:\quran9\quran_ultimate_final.db",
        r"C:\quran9\surah_database_app_v32.db",
        r"C:\quran9\Quran_Crystalline.db",
        "quran_ultimate_final.db",
        "surah_database_app_v32.db",
        "Quran_Crystalline.db",
        "./quran_ultimate_final.db",
        "./surah_database_app_v32.db",
        "./Quran_Crystalline.db",
    ]

    # البحث عن ملفات .db في المجلد الحالي
    current_dir = Path(".")
    for db_file in current_dir.glob("*.db"):
        if str(db_file) not in possible_paths:
            possible_paths.insert(0, str(db_file))

    found_databases = []

    print("\n🔎 البحث عن قواعد البيانات...")
    print("-" * 80)

    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ تم العثور على: {path}")
            found_databases.append(path)
        # else:
        #     print(f"❌ غير موجود: {path}")

    if not found_databases:
        print("\n⚠️ لم يتم العثور على أي قاعدة بيانات!")
        print("\nيرجى وضع أحد الملفات التالية:")
        print("  • quran_ultimate_final.db")
        print("  • surah_database_app_v32.db")
        print("  • Quran_Crystalline.db")
        print("\nفي أحد المواقع التالية:")
        print("  • نفس مجلد السكريبت")
        print("  • C:\\quran9\\")
        return

    print(f"\n✅ تم العثور على {len(found_databases)} قاعدة بيانات")

    # تحليل كل قاعدة
    for db_path in found_databases:
        analyze_database(db_path)

    print("\n" + "="*80)
    print("✅ انتهى التحليل!")
    print("="*80)
    print("\n💡 نصيحة:")
    print("   ابحث عن الجدول الذي يحتوي على أعمدة مثل:")
    print("   • sora أو surah (رقم السورة)")
    print("   • aya_no أو ayah_no (رقم الآية)")
    print("   • aya_text أو verse_text (نص الآية)")
    print("   • tafseer_moysar (التفسير الميسر)")
    print("\n")


if __name__ == "__main__":
    main()

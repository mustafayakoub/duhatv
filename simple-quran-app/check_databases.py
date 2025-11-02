#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════════════════
سكريبت الاستعادة السريعة
يفحص القواعد المتاحة ويستعيد quran_unified.db
════════════════════════════════════════════════════════════════════════════
"""

import sqlite3
import os
import sys

print("\n" + "🔍" * 35)
print("        فحص قواعد البيانات المتاحة")
print("🔍" * 35 + "\n")

# جميع قواعد البيانات المحتملة
databases_to_check = {
    "القاعدة الأصلية 1": r"C:\quran11\Quran.db",
    "القاعدة الأصلية 2": r"C:\quran11\Quran_irab_sarf.db",
    "القاعدة النهائية": r"C:\quran11\quran_ultimate_final.db",
    "قاعدة التطبيق": r"C:\quran11\surah_database_app_v32.db",
    "القاعدة الموحدة (الهدف)": r"C:\quran11\quran_unified.db",
}

print("=" * 70)
print("📊 حالة قواعد البيانات:")
print("=" * 70 + "\n")

available_databases = {}

for name, path in databases_to_check.items():
    exists = os.path.exists(path)
    status = "✅ موجود" if exists else "❌ غير موجود"

    if exists:
        size = os.path.getsize(path) / (1024 * 1024)  # Convert to MB
        print(f"{status} - {name}")
        print(f"   المسار: {path}")
        print(f"   الحجم: {size:.2f} MB")
        available_databases[name] = path

        # فحص الجداول
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()

            # فحص الجداول الموجودة
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"   الجداول: {', '.join(tables[:5])}{'...' if len(tables) > 5 else ''}")

            # فحص عدد البيانات إذا كانت الجداول القياسية موجودة
            if 'Surahs' in tables or 'surahs' in tables:
                try:
                    cursor.execute("SELECT COUNT(*) FROM Surahs")
                    surahs = cursor.fetchone()[0]
                    print(f"   السور: {surahs}")
                except:
                    try:
                        cursor.execute("SELECT COUNT(*) FROM surahs")
                        surahs = cursor.fetchone()[0]
                        print(f"   السور: {surahs}")
                    except:
                        pass

            if 'Ayahs' in tables or 'ayahs' in tables:
                try:
                    cursor.execute("SELECT COUNT(*) FROM Ayahs")
                    ayahs = cursor.fetchone()[0]
                    print(f"   الآيات: {ayahs}")
                except:
                    try:
                        cursor.execute("SELECT COUNT(*) FROM ayahs")
                        ayahs = cursor.fetchone()[0]
                        print(f"   الآيات: {ayahs}")
                    except:
                        pass

            if 'QuranWordInfo' in tables or 'words' in tables:
                try:
                    cursor.execute("SELECT COUNT(*) FROM QuranWordInfo")
                    words = cursor.fetchone()[0]
                    print(f"   الكلمات: {words}")
                except:
                    try:
                        cursor.execute("SELECT COUNT(*) FROM words")
                        words = cursor.fetchone()[0]
                        print(f"   الكلمات: {words}")
                    except:
                        pass

            conn.close()
        except Exception as e:
            print(f"   ⚠️ لا يمكن قراءة القاعدة: {str(e)[:50]}")
    else:
        print(f"{status} - {name}")
        print(f"   المسار: {path}")

    print()

print("\n" + "=" * 70)
print("📋 التوصيات:")
print("=" * 70 + "\n")

# تحديد أفضل استراتيجية للاستعادة
if "القاعدة الأصلية 1" in available_databases and "القاعدة الأصلية 2" in available_databases:
    print("✅ الحل الأمثل: القواعد الأصلية موجودة!")
    print("   يمكننا استعادة quran_unified.db بشكل كامل")
    print("\n📝 الخطوة التالية:")
    print("   شغّل: restore_from_original.py")

elif "القاعدة النهائية" in available_databases:
    print("⚠️ القاعدة الأصلية الأولى غير موجودة")
    print("   لكن quran_ultimate_final.db موجودة")
    print("\n📝 تحقق من بنية quran_ultimate_final.db:")
    print("   قد تكون هي القاعدة الجيدة!")
    print("   يمكن نسخها كـ quran_unified.db")

elif "قاعدة التطبيق" in available_databases:
    print("⚠️ فقط surah_database_app_v32.db موجودة")
    print("   نحتاج لفحص إذا كانت تحتوي على البيانات الكاملة")

else:
    print("❌ لا توجد قواعد بيانات متاحة!")
    print("   نحتاج لاستعادة من نسخة احتياطية")

print("\n" + "🔍" * 35)
print("        انتهى الفحص")
print("🔍" * 35 + "\n")

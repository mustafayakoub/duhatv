#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت التحقق من قاعدة الآيات المحسّنة
====================================

يتحقق من:
- عدد الآيات والنصوص المستوردة
- صحة الإحصائيات (كلمات، حروف)
- سلامة العلاقات بين الجداول
- صحة Views
- توفر جميع الإصدارات

المؤلف: مشروع القرآن الرقمي
التاريخ: 4 نوفمبر 2025
"""

import sqlite3
import sys
from pathlib import Path


def verify_enhanced_database(db_path="databases/AYAHS_DATABASE_ENHANCED.db"):
    """
    التحقق من قاعدة البيانات المحسّنة

    Args:
        db_path: مسار قاعدة البيانات
    """
    db_path = Path(db_path)

    if not db_path.exists():
        print(f"❌ قاعدة البيانات غير موجودة: {db_path}")
        return False

    print("="*70)
    print("🔍 التحقق من قاعدة الآيات المحسّنة")
    print("="*70)
    print(f"📂 المسار: {db_path}")
    print(f"📊 الحجم: {db_path.stat().st_size / 1024:.2f} KB\n")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    all_passed = True

    # ==========================================
    # الاختبار 1: البنية الأساسية
    # ==========================================
    print("🔹 اختبار 1: البنية الأساسية")
    print("-"*70)

    required_tables = ['ayahs', 'text_versions', 'ayah_texts', 'tafsir',
                       'translations', 'ayah_topics', 'ayah_relations']

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]

    for table in required_tables:
        if table in existing_tables:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} - مفقود!")
            all_passed = False

    # ==========================================
    # الاختبار 2: Views
    # ==========================================
    print("\n🔹 اختبار 2: Views")
    print("-"*70)

    required_views = ['v_ayahs_default', 'v_text_stats']

    cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
    existing_views = [row[0] for row in cursor.fetchall()]

    for view in required_views:
        if view in existing_views:
            print(f"   ✅ {view}")
        else:
            print(f"   ❌ {view} - مفقود!")
            all_passed = False

    # ==========================================
    # الاختبار 3: الإصدارات (23 إصدار)
    # ==========================================
    print("\n🔹 اختبار 3: إصدارات النصوص")
    print("-"*70)

    version_count = cursor.execute("SELECT COUNT(*) FROM text_versions").fetchone()[0]
    print(f"   📊 عدد الإصدارات المسجلة: {version_count}/23")

    if version_count == 23:
        print(f"   ✅ جميع الإصدارات متوفرة")
    else:
        print(f"   ⚠️  بعض الإصدارات مفقودة")

    # الإصدار الافتراضي
    default_version = cursor.execute(
        "SELECT version_code FROM text_versions WHERE is_default = 1"
    ).fetchone()

    if default_version:
        print(f"   ✅ الإصدار الافتراضي: {default_version[0]}")
    else:
        print(f"   ❌ لا يوجد إصدار افتراضي!")
        all_passed = False

    # ==========================================
    # الاختبار 4: البيانات المستوردة
    # ==========================================
    print("\n🔹 اختبار 4: البيانات المستوردة")
    print("-"*70)

    total_ayahs = cursor.execute("SELECT COUNT(*) FROM ayahs").fetchone()[0]
    total_texts = cursor.execute("SELECT COUNT(*) FROM ayah_texts").fetchone()[0]
    versions_with_data = cursor.execute(
        "SELECT COUNT(DISTINCT version_id) FROM ayah_texts"
    ).fetchone()[0]

    print(f"   📖 إجمالي الآيات: {total_ayahs}")
    print(f"   📝 إجمالي النصوص: {total_texts}")
    print(f"   🔢 الإصدارات المستوردة: {versions_with_data}/23")

    if total_ayahs > 0:
        print(f"   ✅ يوجد بيانات مستوردة")
    else:
        print(f"   ⚠️  لا يوجد بيانات بعد")

    # ==========================================
    # الاختبار 5: الإحصائيات
    # ==========================================
    print("\n🔹 اختبار 5: الإحصائيات")
    print("-"*70)

    if total_texts > 0:
        total_words = cursor.execute("SELECT SUM(word_count) FROM ayah_texts").fetchone()[0]
        total_letters = cursor.execute("SELECT SUM(letter_count) FROM ayah_texts").fetchone()[0]
        avg_words = total_words / total_texts if total_texts > 0 else 0
        avg_letters = total_letters / total_texts if total_texts > 0 else 0

        print(f"   📊 إجمالي الكلمات: {total_words:,}")
        print(f"   📊 إجمالي الحروف: {total_letters:,}")
        print(f"   📊 متوسط الكلمات/آية: {avg_words:.1f}")
        print(f"   📊 متوسط الحروف/آية: {avg_letters:.1f}")
        print(f"   ✅ الإحصائيات محسوبة")
    else:
        print(f"   ⚠️  لا توجد إحصائيات بعد")

    # ==========================================
    # الاختبار 6: نص البحث
    # ==========================================
    print("\n🔹 اختبار 6: نص البحث (تطبيع)")
    print("-"*70)

    if total_texts > 0:
        # عينة من نصوص البحث
        cursor.execute("""
            SELECT aya_text, search_text
            FROM ayah_texts
            WHERE search_text IS NOT NULL AND search_text != ''
            LIMIT 3
        """)

        has_search_text = False
        for aya_text, search_text in cursor.fetchall():
            has_search_text = True
            print(f"   الأصل: {aya_text[:40]}...")
            print(f"   بحث:  {search_text[:40]}...")
            print()

        if has_search_text:
            print(f"   ✅ نص البحث متوفر")
        else:
            print(f"   ⚠️  نص البحث غير متوفر")
    else:
        print(f"   ⚠️  لا توجد نصوص بعد")

    # ==========================================
    # الاختبار 7: العلاقات بين الجداول
    # ==========================================
    print("\n🔹 اختبار 7: العلاقات بين الجداول")
    print("-"*70)

    if total_texts > 0:
        # التحقق من أن كل نص له آية مقابلة
        orphan_texts = cursor.execute("""
            SELECT COUNT(*)
            FROM ayah_texts t
            WHERE NOT EXISTS (SELECT 1 FROM ayahs a WHERE a.id = t.ayah_id)
        """).fetchone()[0]

        if orphan_texts == 0:
            print(f"   ✅ جميع النصوص مرتبطة بآيات")
        else:
            print(f"   ❌ {orphan_texts} نص غير مرتبط!")
            all_passed = False

        # التحقق من أن كل نص له إصدار مقابل
        orphan_versions = cursor.execute("""
            SELECT COUNT(*)
            FROM ayah_texts t
            WHERE NOT EXISTS (SELECT 1 FROM text_versions v WHERE v.id = t.version_id)
        """).fetchone()[0]

        if orphan_versions == 0:
            print(f"   ✅ جميع النصوص مرتبطة بإصدارات")
        else:
            print(f"   ❌ {orphan_versions} نص بدون إصدار!")
            all_passed = False
    else:
        print(f"   ⚠️  لا توجد بيانات للتحقق")

    # ==========================================
    # الاختبار 8: View v_ayahs_default
    # ==========================================
    print("\n🔹 اختبار 8: View v_ayahs_default")
    print("-"*70)

    try:
        count = cursor.execute("SELECT COUNT(*) FROM v_ayahs_default").fetchone()[0]
        print(f"   📊 عدد السجلات في View: {count}")

        if count == total_ayahs:
            print(f"   ✅ View يعمل بشكل صحيح")
        else:
            print(f"   ⚠️  View يعرض {count} بدلاً من {total_ayahs}")
    except Exception as e:
        print(f"   ❌ خطأ في View: {e}")
        all_passed = False

    # ==========================================
    # الاختبار 9: View v_text_stats
    # ==========================================
    print("\n🔹 اختبار 9: View v_text_stats")
    print("-"*70)

    try:
        cursor.execute("SELECT * FROM v_text_stats WHERE ayah_count > 0")
        stats = cursor.fetchall()

        if stats:
            print(f"   📊 إصدارات بها بيانات: {len(stats)}")
            for stat in stats:
                print(f"      • {stat[1]}: {stat[3]} آية، {stat[4]} كلمة")
            print(f"   ✅ View يعمل بشكل صحيح")
        else:
            print(f"   ⚠️  لا توجد إحصائيات بعد")
    except Exception as e:
        print(f"   ❌ خطأ في View: {e}")
        all_passed = False

    # ==========================================
    # الاختبار 10: الفهارس
    # ==========================================
    print("\n🔹 اختبار 10: الفهارس")
    print("-"*70)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
    indexes = cursor.fetchall()

    print(f"   📊 عدد الفهارس المخصصة: {len(indexes)}")
    for idx in indexes:
        print(f"      • {idx[0]}")

    if len(indexes) > 0:
        print(f"   ✅ الفهارس متوفرة")
    else:
        print(f"   ⚠️  لا توجد فهارس")

    conn.close()

    # ==========================================
    # النتيجة النهائية
    # ==========================================
    print("\n" + "="*70)
    if all_passed and total_ayahs > 0:
        print("✅ جميع الاختبارات نجحت! القاعدة سليمة ✅")
    elif all_passed and total_ayahs == 0:
        print("⚠️  القاعدة سليمة لكن لا توجد بيانات بعد")
    else:
        print("❌ بعض الاختبارات فشلت!")
    print("="*70)

    return all_passed


def main():
    """الدالة الرئيسية"""
    try:
        result = verify_enhanced_database()
        return 0 if result else 1

    except Exception as e:
        print(f"\n❌ خطأ: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

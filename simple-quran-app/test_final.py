#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════════════════
اختبار نهائي - التحقق من نجاح النقل
Final Test - Verify Migration Success
════════════════════════════════════════════════════════════════════════════
"""

import sqlite3

DB_PATH = r"C:\quran11\quran_unified.db"

print()
print("═" * 70)
print("  🌙 اختبار نهائي - قاعدة البيانات الموحدة")
print("  Final Test - Unified Quran Database")
print("═" * 70)
print()

try:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ═══════════════════════════════════════════════════════════════
    # التحقق من الأعداد
    # ═══════════════════════════════════════════════════════════════

    print("📊 التحقق من الأعداد:")
    print("─" * 70)

    # السور
    cursor.execute("SELECT COUNT(*) as count FROM surahs")
    surahs_count = cursor.fetchone()['count']
    surahs_ok = "✅" if surahs_count == 114 else "❌"
    print(f"{surahs_ok} السور:        {surahs_count:,} (المتوقع: 114)")

    # الآيات
    cursor.execute("SELECT COUNT(*) as count FROM ayahs")
    ayahs_count = cursor.fetchone()['count']
    ayahs_ok = "✅" if ayahs_count == 6236 else "❌"
    print(f"{ayahs_ok} الآيات:       {ayahs_count:,} (المتوقع: 6,236)")

    # الكلمات
    cursor.execute("SELECT COUNT(*) as count FROM words")
    words_count = cursor.fetchone()['count']
    words_ok = "✅" if words_count == 77432 else "❌"
    print(f"{words_ok} الكلمات:      {words_count:,} (المتوقع: 77,432)")

    # الإعراب
    cursor.execute("SELECT COUNT(*) as count FROM irab")
    irab_count = cursor.fetchone()['count']
    irab_ok = "✅" if irab_count > 70000 else "⚠️"
    print(f"{irab_ok} الإعراب:      {irab_count:,}")

    # الصرف
    cursor.execute("SELECT COUNT(*) as count FROM sarf")
    sarf_count = cursor.fetchone()['count']
    sarf_ok = "✅" if sarf_count > 70000 else "⚠️"
    print(f"{sarf_ok} الصرف:        {sarf_count:,}")

    print()

    # ═══════════════════════════════════════════════════════════════
    # عينة من البيانات
    # ═══════════════════════════════════════════════════════════════

    print("📋 عينة من البيانات:")
    print("─" * 70)

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
        LIMIT 5
    """)

    for idx, row in enumerate(cursor.fetchall(), 1):
        print(f"\n{idx}. الكلمة: {row['word_text']}")
        if row['word_simple']:
            print(f"   بدون حركات: {row['word_simple']}")
        if row['root_text']:
            print(f"   الجذر: {row['root_text']}")
        if row['irab_text']:
            print(f"   الإعراب: {row['irab_text'][:50]}...")
        if row['sarf_text']:
            print(f"   الصرف: {row['sarf_text'][:50]}...")

    print()
    print("─" * 70)

    # ═══════════════════════════════════════════════════════════════
    # إحصائيات متقدمة
    # ═══════════════════════════════════════════════════════════════

    print()
    print("📈 إحصائيات إضافية:")
    print("─" * 70)

    # متوسط الكلمات لكل آية
    avg_words = words_count / ayahs_count if ayahs_count > 0 else 0
    print(f"📊 متوسط الكلمات/آية:  {avg_words:.2f}")

    # متوسط الآيات لكل سورة
    avg_ayahs = ayahs_count / surahs_count if surahs_count > 0 else 0
    print(f"📊 متوسط الآيات/سورة:  {avg_ayahs:.2f}")

    # نسبة الإعراب المكتمل
    irab_percentage = (irab_count / words_count * 100) if words_count > 0 else 0
    print(f"📊 نسبة الإعراب المكتمل: {irab_percentage:.1f}%")

    # نسبة الصرف المكتمل
    sarf_percentage = (sarf_count / words_count * 100) if words_count > 0 else 0
    print(f"📊 نسبة الصرف المكتمل:  {sarf_percentage:.1f}%")

    print()

    # ═══════════════════════════════════════════════════════════════
    # التحقق من سورة الفاتحة
    # ═══════════════════════════════════════════════════════════════

    print("🕋 اختبار سورة الفاتحة:")
    print("─" * 70)

    cursor.execute("""
        SELECT name_arabic, ayah_count
        FROM surahs
        WHERE surah_id = 1
    """)
    fatiha = cursor.fetchone()
    print(f"السورة: {fatiha['name_arabic']}")
    print(f"عدد الآيات: {fatiha['ayah_count']}")

    cursor.execute("""
        SELECT COUNT(*) as count
        FROM words w
        JOIN ayahs a ON w.ayah_id = a.ayah_id
        WHERE a.surah_id = 1
    """)
    fatiha_words = cursor.fetchone()['count']
    print(f"عدد الكلمات: {fatiha_words}")

    # عرض الآية الأولى
    cursor.execute("""
        SELECT text_uthmani
        FROM ayahs
        WHERE surah_id = 1 AND ayah_number = 1
    """)
    first_ayah = cursor.fetchone()
    if first_ayah:
        print(f"الآية الأولى: {first_ayah['text_uthmani']}")

    print()

    # ═══════════════════════════════════════════════════════════════
    # النتيجة النهائية
    # ═══════════════════════════════════════════════════════════════

    print("═" * 70)

    all_ok = (
        surahs_count == 114 and
        ayahs_count == 6236 and
        words_count == 77432 and
        irab_count > 70000 and
        sarf_count > 70000
    )

    if all_ok:
        print("✅ النتيجة: نجح الاختبار! القاعدة جاهزة 100%")
        print()
        print("🎉 تهانينا! قاعدة البيانات الموحدة جاهزة للاستخدام")
        print()
        print("محتويات القاعدة:")
        print(f"  ✓ {surahs_count:,} سورة")
        print(f"  ✓ {ayahs_count:,} آية")
        print(f"  ✓ {words_count:,} كلمة")
        print(f"  ✓ {irab_count:,} إعراب")
        print(f"  ✓ {sarf_count:,} صرف")
    else:
        print("⚠️  النتيجة: بعض البيانات ناقصة")
        print()
        print("تحقق من:")
        if surahs_count != 114:
            print(f"  ❌ السور: {surahs_count} (يجب أن تكون 114)")
        if ayahs_count != 6236:
            print(f"  ❌ الآيات: {ayahs_count} (يجب أن تكون 6,236)")
        if words_count != 77432:
            print(f"  ❌ الكلمات: {words_count} (يجب أن تكون 77,432)")
        if irab_count < 70000:
            print(f"  ⚠️  الإعراب: {irab_count} (قليل)")
        if sarf_count < 70000:
            print(f"  ⚠️  الصرف: {sarf_count} (قليل)")

    print("═" * 70)
    print()

    conn.close()

except Exception as e:
    print(f"❌ خطأ في الاختبار: {e}")
    import traceback
    traceback.print_exc()

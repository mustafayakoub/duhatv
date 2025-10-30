#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نظام ألوان التجويد
"""

import re

class TajweedColors:
    """نظام ألوان أحكام التجويد"""

    RULES = {
        '<#>': {'name': 'إخفاء', 'color': '#D4AF37'},
        '<$>': {'name': 'إدغام', 'color': '#228B22'},
        '<@>': {'name': 'قلقلة', 'color': '#4169E1'},
        '<|>': {'name': 'مد', 'color': '#DC143C'},
        '<||>': {'name': 'مد لازم', 'color': '#B22222'},
        '<|||>': {'name': 'مد متصل', 'color': '#8B0000'},
        '<~>': {'name': 'غنة', 'color': '#FF8C00'},
        '<%>': {'name': 'إقلاب', 'color': '#9370DB'},
        '<^>': {'name': 'إظهار', 'color': '#696969'},
        '<o>': {'name': 'سكون', 'color': '#2F4F4F'},
        '<*>': {'name': 'تفخيم', 'color': '#8B4513'},
        '<+>': {'name': 'ترقيق', 'color': '#4682B4'},
    }

    @classmethod
    def convert_to_html(cls, text: str) -> str:
        """تحويل النص من رموز التجويد إلى HTML ملون"""
        if not text:
            return ""

        sorted_symbols = sorted(cls.RULES.keys(), key=len, reverse=True)
        result = text

        for symbol in sorted_symbols:
            info = cls.RULES[symbol]
            escaped = re.escape(symbol)

            # نمط 1: <symbol>text<symbol>
            pattern1 = f"{escaped}([^<>]+?){escaped}"

            # نمط 2: <symbol>text
            pattern2 = f"{escaped}([^\\s<>]+)"

            matches = list(re.finditer(pattern1, result))
            if matches:
                for match in reversed(matches):
                    colored_text = f'<span style="color: {info["color"]}; font-weight: bold;">{match.group(1)}</span>'
                    result = result[:match.start()] + colored_text + result[match.end():]
            else:
                matches = list(re.finditer(pattern2, result))
                if matches:
                    for match in reversed(matches):
                        colored_text = f'<span style="color: {info["color"]}; font-weight: bold;">{match.group(1)}</span>'
                        result = result[:match.start()] + colored_text + result[match.end():]

        # إزالة أي رموز متبقية
        result = re.sub(r'<[#$@|~%^o*+]+>', '', result)
        return result


# اختبارات
print("=" * 70)
print("اختبار نظام ألوان التجويد")
print("=" * 70)

# مثال 1: نمط محاط
test1 = "قال <#>نُون<#> في البيت"
result1 = TajweedColors.convert_to_html(test1)
print(f"\nالمدخل: {test1}")
print(f"المخرج: {result1}")
print()

# مثال 2: نمط بداية فقط
test2 = "قال <#>نُون في البيت"
result2 = TajweedColors.convert_to_html(test2)
print(f"المدخل: {test2}")
print(f"المخرج: {result2}")
print()

# مثال 3: رموز متعددة
test3 = "وَمِنَ <#>ٱلنَّاسِ<#> مَن <$>يَقُولُ<$>"
result3 = TajweedColors.convert_to_html(test3)
print(f"المدخل: {test3}")
print(f"المخرج: {result3}")
print()

# اختبار من قاعدة البيانات
print("\n" + "=" * 70)
print("اختبار من قاعدة البيانات")
print("=" * 70)

import sqlite3
try:
    conn = sqlite3.connect('surah_database_app_v32.db')
    cursor = conn.cursor()

    # جلب آية واحدة
    cursor.execute('SELECT tajweedText FROM quran_text_with_tajweed WHERE surahNo=2 AND ayahNo=8 LIMIT 1')
    row = cursor.fetchone()

    if row:
        original = row[0]
        print(f"\nالنص الأصلي:")
        print(original)
        print(f"\nطول النص: {len(original)}")

        # البحث عن الرموز
        symbols_found = re.findall(r'<[^>]+>', original)
        print(f"\nالرموز المكتشفة: {set(symbols_found) if symbols_found else 'لا توجد'}")

        # التحويل
        converted = TajweedColors.convert_to_html(original)
        print(f"\nالنص المحول:")
        print(converted)
        print(f"\nطول النص المحول: {len(converted)}")

        # التحقق
        if '<span' in converted:
            print("\n✅ نجح التحويل - تم إضافة ألوان!")
        else:
            print("\n❌ فشل التحويل - لم تتم إضافة ألوان!")

    conn.close()

except Exception as e:
    print(f"خطأ: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)

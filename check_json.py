#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص ملفات JSON للقرآن
التحقق من البنية وعدد الآيات الصحيح
"""

import json
import sys
from pathlib import Path

def check_json_file(file_path):
    """فحص ملف JSON"""

    print(f"\n{'='*70}")
    print(f"🔍 فحص: {Path(file_path).name}")
    print(f"{'='*70}\n")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("❌ الملف ليس JSON array")
            return False

        print(f"📊 إجمالي السجلات: {len(data)}")

        # تحليل السجلات
        valid_ayahs = 0
        empty_texts = 0
        missing_ayano = 0
        sura_names = 0
        basmala_count = 0

        sura_ayah_counts = {}

        for i, item in enumerate(data, 1):
            # تحقق من وجود aya_no
            if 'aya_no' not in item:
                missing_ayano += 1
                continue

            # تحقق من وجود نص
            aya_text = item.get('aya_text', '')
            aya_text_emlaey = item.get('aya_text_emlaey', '')

            if not aya_text and not aya_text_emlaey:
                empty_texts += 1
                continue

            # عد الآيات الصحيحة
            valid_ayahs += 1

            # إحصاء الآيات لكل سورة
            sura_no = item.get('sura_no', 0)
            if sura_no not in sura_ayah_counts:
                sura_ayah_counts[sura_no] = 0
            sura_ayah_counts[sura_no] += 1

            # عد البسملات
            if aya_text_emlaey == "بسم الله الرحمن الرحيم":
                basmala_count += 1

        print(f"\n📋 التحليل:")
        print(f"   ✅ آيات صحيحة: {valid_ayahs}")
        print(f"   ⚠️  سجلات فارغة: {empty_texts}")
        print(f"   ⚠️  سجلات بدون aya_no: {missing_ayano}")
        print(f"   🕌 بسملات: {basmala_count}")

        print(f"\n📖 السور:")
        print(f"   عدد السور: {len(sura_ayah_counts)}")

        # عرض أول 5 سور
        for sura in sorted(sura_ayah_counts.keys())[:5]:
            print(f"   السورة {sura}: {sura_ayah_counts[sura]} آية")

        # عرض آخر 5 سور
        if len(sura_ayah_counts) > 5:
            print(f"   ...")
            for sura in sorted(sura_ayah_counts.keys())[-5:]:
                print(f"   السورة {sura}: {sura_ayah_counts[sura]} آية")

        # التحقق من العدد الصحيح
        print(f"\n🎯 التحقق:")
        if valid_ayahs == 6236:
            print(f"   ✅ العدد صحيح: 6,236 آية")
        else:
            print(f"   ⚠️  العدد غير صحيح: {valid_ayahs} (المتوقع: 6,236)")

        if len(sura_ayah_counts) == 114:
            print(f"   ✅ عدد السور صحيح: 114 سورة")
        else:
            print(f"   ⚠️  عدد السور غير صحيح: {len(sura_ayah_counts)} (المتوقع: 114)")

        # عرض عينة من البيانات
        print(f"\n📄 عينة من البيانات:")
        for i in [0, 6, 7]:  # أول آية، آخر آية من الفاتحة، أول آية من البقرة
            if i < len(data):
                item = data[i]
                print(f"\n   [{i+1}] سورة {item.get('sura_no')} آية {item.get('aya_no')}:")
                print(f"       {item.get('aya_text_emlaey', 'N/A')[:50]}...")

        return True

    except json.JSONDecodeError as e:
        print(f"❌ خطأ في قراءة JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print("الاستخدام: python check_json.py <path_to_json_file>")
        sys.exit(1)

    check_json_file(file_path)

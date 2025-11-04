#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
استيراد ذكي لجميع ملفات القرآن
يدعم JSON و TXT
"""

import os
import sys
import subprocess
from pathlib import Path

def import_all_files(directory):
    """استيراد جميع ملفات JSON و TXT من مجلد"""

    directory = Path(directory)

    if not directory.exists():
        print(f"❌ المجلد غير موجود: {directory}")
        return

    print("="*70)
    print("🚀 استيراد جميع ملفات القرآن")
    print("="*70)
    print()

    # قائمة الملفات مع أنواعها
    files_map = {
        # JSON files
        'hafsData_v2-0.json': 'hafs',
        'warshData_v2-1.json': 'warsh',
        'QalounData_v2-1.json': 'qaloon',
        'DouriData_v2-0.json': 'aldori',
        'SousiData_v2-0.json': 'alsosi',
        'shubaData_v2-0.json': 'shobah',

        # TXT files (سيتم اكتشافها تلقائياً)
    }

    # البحث عن ملفات JSON
    json_files = list(directory.glob('*.json'))
    # استبعاد ملفات العينات
    json_files = [f for f in json_files if 'sample' not in f.name.lower() and 'test' not in f.name.lower()]

    # البحث عن ملفات TXT
    txt_files = list(directory.glob('*.txt'))

    all_files = json_files + txt_files

    print(f"📊 عدد الملفات: {len(all_files)}")
    print(f"   • JSON: {len(json_files)}")
    print(f"   • TXT: {len(txt_files)}")
    print()

    if not all_files:
        print("❌ لم يتم العثور على ملفات!")
        return

    success = 0
    failed = 0

    for i, file_path in enumerate(all_files, 1):
        print(f"[{i}/{len(all_files)}] 📥 {file_path.name}")

        # تحديد نوع القراءة من اسم الملف
        version = None
        filename_lower = file_path.name.lower()

        if 'hafs' in filename_lower:
            version = 'hafs'
        elif 'warsh' in filename_lower:
            version = 'warsh'
        elif 'qaloun' in filename_lower:
            version = 'qaloon'
        elif 'douri' in filename_lower or 'aldori' in filename_lower:
            version = 'aldori'
        elif 'sousi' in filename_lower or 'alsosi' in filename_lower:
            version = 'alsosi'
        elif 'shuba' in filename_lower or 'shobah' in filename_lower:
            version = 'shobah'
        elif 'khalaf' in filename_lower:
            version = 'khalaf'
        elif 'khallad' in filename_lower:
            version = 'khallad'

        # بناء الأمر
        cmd = [sys.executable, 'scripts/import_quran_smart.py', '--file', str(file_path)]
        if version:
            cmd.extend(['--version', version])

        # تنفيذ الاستيراد
        try:
            result = subprocess.run(cmd, capture_output=False, text=True)
            if result.returncode == 0:
                print(f"   ✅ نجح\n")
                success += 1
            else:
                print(f"   ❌ فشل\n")
                failed += 1
        except Exception as e:
            print(f"   ❌ خطأ: {e}\n")
            failed += 1

    print("="*70)
    print("📊 النتيجة النهائية:")
    print(f"   ✅ نجح: {success}")
    print(f"   ❌ فشل: {failed}")
    print("="*70)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # المسار الافتراضي
        directory = "C:/QURAN2/data/sources/quran_Ayat"

    import_all_files(directory)

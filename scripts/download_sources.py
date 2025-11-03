#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تحميل البيانات القرآنية من المصادر الموثوقة
==================================================

المصادر:
1. tanzil.net - النص القرآني الأساسي
2. corpus.quran.com - التحليل الصرفي والإعراب
3. GitHub repositories - بيانات إضافية

الاستخدام:
    python3 download_sources.py
    python3 download_sources.py --source tanzil
    python3 download_sources.py --source corpus

المؤلف: مشروع القرآن الرقمي
التاريخ: 3 نوفمبر 2025
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path


class QuranDataDownloader:
    """محمّل البيانات القرآنية"""

    def __init__(self, output_dir="data/sources"):
        """
        Args:
            output_dir: مجلد حفظ البيانات المحملة
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # المصادر الموثوقة
        self.sources = {
            'tanzil': {
                'name': 'Tanzil.net',
                'description': 'نص قرآني دقيق خالي من الأخطاء',
                'urls': {
                    'uthmani': 'https://tanzil.net/pub/download/data/quran-uthmani.txt',
                    'simple': 'https://tanzil.net/pub/download/data/quran-simple.txt',
                    'metadata': 'https://raw.githubusercontent.com/risan/quran-json/master/data/meta.json'
                }
            },
            'quran-json': {
                'name': 'Quran JSON (GitHub)',
                'description': 'بيانات JSON كاملة',
                'urls': {
                    'surahs': 'https://raw.githubusercontent.com/risan/quran-json/master/data/meta.json',
                    'arabic': 'https://raw.githubusercontent.com/semarketir/quranjson/master/source/quran.json'
                }
            },
            'corpus': {
                'name': 'Quranic Arabic Corpus',
                'description': 'التحليل الصرفي (يحتاج تسجيل)',
                'note': '⚠️  يحتاج تحميل يدوي من: https://corpus.quran.com/download/'
            }
        }

    def download_file(self, url, filename):
        """تحميل ملف من URL"""
        output_path = self.output_dir / filename

        try:
            print(f"📥 تحميل: {filename}")
            print(f"   من: {url}")

            # إضافة User-Agent لتجنب الحظر
            headers = {
                'User-Agent': 'Mozilla/5.0 (Quran Digital Project; +https://github.com)'
            }

            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req) as response:
                data = response.read()

            with open(output_path, 'wb') as f:
                f.write(data)

            size = len(data) / 1024  # KB
            print(f"✅ تم التحميل: {size:.2f} KB")
            print(f"   المسار: {output_path}")

            return output_path

        except urllib.error.URLError as e:
            print(f"❌ خطأ في التحميل: {e}")
            return None
        except Exception as e:
            print(f"❌ خطأ: {e}")
            return None

    def download_tanzil(self):
        """تحميل بيانات Tanzil"""
        print("\n" + "="*70)
        print("📖 تحميل بيانات Tanzil.net")
        print("="*70)

        tanzil_dir = self.output_dir / "tanzil"
        tanzil_dir.mkdir(exist_ok=True)

        urls = self.sources['tanzil']['urls']

        # تحميل النص العثماني
        self.download_file(urls['uthmani'], 'tanzil/quran-uthmani.txt')

        # تحميل النص البسيط
        self.download_file(urls['simple'], 'tanzil/quran-simple.txt')

        # تحميل metadata
        self.download_file(urls['metadata'], 'tanzil/metadata.json')

    def download_quran_json(self):
        """تحميل بيانات JSON"""
        print("\n" + "="*70)
        print("📊 تحميل بيانات Quran JSON")
        print("="*70)

        json_dir = self.output_dir / "quran-json"
        json_dir.mkdir(exist_ok=True)

        urls = self.sources['quran-json']['urls']

        # تحميل معلومات السور
        self.download_file(urls['surahs'], 'quran-json/surahs-meta.json')

        # تحميل النص العربي الكامل
        self.download_file(urls['arabic'], 'quran-json/quran-arabic.json')

    def show_corpus_instructions(self):
        """عرض تعليمات تحميل Corpus"""
        print("\n" + "="*70)
        print("📝 تعليمات تحميل Quranic Arabic Corpus")
        print("="*70)

        print("""
⚠️  Quranic Arabic Corpus يحتاج تحميل يدوي:

الخطوات:
1. اذهب إلى: https://corpus.quran.com/download/
2. أدخل بريدك الإلكتروني
3. حمّل ملف: quranic-corpus-morphology-0.4.txt
4. ضعه في المجلد: data/sources/corpus/

الملف يحتوي على:
✅ 77,430 كلمة قرآنية
✅ التحليل الصرفي الكامل
✅ الجذور والأنماط
✅ أنواع الكلمات

بعد التحميل، يمكنك استيراده باستخدام: import_data.py
        """)

    def download_all(self):
        """تحميل جميع المصادر المتاحة"""
        print("="*70)
        print("🚀 بدء تحميل البيانات القرآنية من المصادر الموثوقة")
        print("="*70)

        # تحميل Tanzil
        self.download_tanzil()

        # تحميل Quran JSON
        self.download_quran_json()

        # عرض تعليمات Corpus
        self.show_corpus_instructions()

        print("\n" + "="*70)
        print("✅ اكتمل التحميل!")
        print("="*70)
        print(f"\n📂 الموقع: {self.output_dir.absolute()}")

        # عرض ملخص الملفات المحملة
        print(f"\n📊 الملفات المحملة:")
        for file in self.output_dir.rglob('*'):
            if file.is_file():
                size = file.stat().st_size / 1024  # KB
                rel_path = file.relative_to(self.output_dir)
                print(f"   • {rel_path} ({size:.2f} KB)")

    def list_sources(self):
        """عرض قائمة المصادر المتاحة"""
        print("="*70)
        print("📚 المصادر الموثوقة المتاحة")
        print("="*70)

        for key, source in self.sources.items():
            print(f"\n🔹 {source['name']}")
            print(f"   الوصف: {source['description']}")

            if 'urls' in source:
                print(f"   الملفات:")
                for name in source['urls'].keys():
                    print(f"      • {name}")

            if 'note' in source:
                print(f"   {source['note']}")


def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description="تحميل البيانات القرآنية من المصادر الموثوقة",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
    python3 download_sources.py                    # تحميل جميع المصادر
    python3 download_sources.py --list             # عرض قائمة المصادر
    python3 download_sources.py --source tanzil    # تحميل مصدر واحد
        """
    )

    parser.add_argument(
        '--output-dir',
        default='data/sources',
        help='مجلد حفظ البيانات المحملة'
    )

    parser.add_argument(
        '--source',
        choices=['tanzil', 'quran-json', 'corpus', 'all'],
        default='all',
        help='المصدر المراد تحميله'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='عرض قائمة المصادر المتاحة'
    )

    args = parser.parse_args()

    try:
        downloader = QuranDataDownloader(output_dir=args.output_dir)

        if args.list:
            downloader.list_sources()
            return 0

        if args.source == 'all':
            downloader.download_all()
        elif args.source == 'tanzil':
            downloader.download_tanzil()
        elif args.source == 'quran-json':
            downloader.download_quran_json()
        elif args.source == 'corpus':
            downloader.show_corpus_instructions()

        print(f"\n🎉 النجاح! الخطوة التالية:")
        print(f"   python3 import_data.py --source {args.source}")

        return 0

    except Exception as e:
        print(f"\n❌ خطأ: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

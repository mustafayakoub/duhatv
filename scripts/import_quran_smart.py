#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت الاستيراد الذكي للقرآن الكريم
===================================

يدعم:
- استيراد من ملفات JSON (مثل hafs_smart_v8.json)
- استيراد من ملفات TXT (الصيغة: surah_no|ayah_no|text)
- 23 إصدار مختلف من النص القرآني
- القراءات المختلفة (حفص، ورش، قالون، إلخ)
- حساب إحصائيات تلقائية (عدد الكلمات، الحروف)
- إنشاء نص بحث محسن (بدون تشكيل)

المؤلف: مشروع القرآن الرقمي
التاريخ: 4 نوفمبر 2025
"""

import sqlite3
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class QuranSmartImporter:
    """مستورد ذكي للقرآن الكريم"""

    def __init__(
        self,
        ayahs_db_path="databases/AYAHS_DATABASE_ENHANCED.db",
        surahs_db_path="databases/SURAHS_DATABASE.db"
    ):
        """
        Args:
            ayahs_db_path: مسار قاعدة بيانات الآيات المحسنة
            surahs_db_path: مسار قاعدة بيانات السور (للتحقق)
        """
        self.ayahs_db_path = Path(ayahs_db_path)
        self.surahs_db_path = Path(surahs_db_path)

        # التحقق من وجود القواعد
        if not self.ayahs_db_path.exists():
            raise FileNotFoundError(f"❌ قاعدة الآيات غير موجودة: {self.ayahs_db_path}")

        # الإحصائيات
        self.stats = {
            'ayahs_imported': 0,
            'texts_imported': 0,
            'errors': 0,
            'skipped': 0
        }

    def normalize_arabic(self, text: str) -> str:
        """
        تطبيع النص العربي (إزالة التشكيل)

        Args:
            text: النص الأصلي

        Returns:
            النص بدون تشكيل
        """
        if not text:
            return ""

        # علامات التشكيل
        diacritics = "ًٌٍَُِّْٰۣۡۢۖۗۘۙۚۛۜ۟۠ۤۥۦۧۨ۩ۭۮۯ"

        # إزالة التشكيل
        normalized = ''.join(c for c in text if c not in diacritics)

        # تنظيف المسافات
        normalized = ' '.join(normalized.split())

        return normalized

    def count_words(self, text: str) -> int:
        """
        حساب عدد الكلمات في النص

        Args:
            text: النص

        Returns:
            عدد الكلمات
        """
        if not text:
            return 0

        # إزالة التشكيل أولاً
        clean_text = self.normalize_arabic(text)

        # الكلمات = مفصولة بمسافات
        words = clean_text.split()

        return len(words)

    def count_letters(self, text: str) -> int:
        """
        حساب عدد الحروف (بدون المسافات والتشكيل)

        Args:
            text: النص

        Returns:
            عدد الحروف
        """
        if not text:
            return 0

        # إزالة التشكيل والمسافات
        clean_text = self.normalize_arabic(text).replace(' ', '')

        return len(clean_text)

    def get_version_id(self, version_code: str) -> Optional[int]:
        """
        الحصول على معرّف الإصدار من القاعدة

        Args:
            version_code: كود الإصدار (مثل: hafs_smart_v8)

        Returns:
            معرف الإصدار أو None
        """
        conn = sqlite3.connect(self.ayahs_db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM text_versions WHERE version_code = ?",
            (version_code,)
        )

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    def detect_version_from_filename(self, filename: str) -> str:
        """
        اكتشاف نوع الإصدار من اسم الملف

        Args:
            filename: اسم الملف

        Returns:
            كود الإصدار
        """
        filename = filename.lower()

        # خريطة أسماء الملفات إلى أكواد الإصدارات
        mapping = {
            'hafs_smart_v8': 'hafs_smart_v8',
            'hafs': 'hafs',
            'warsh': 'warsh',
            'qaloon': 'qaloon',
            'aldori': 'aldori',
            'alsosi': 'alsosi',
            'shobah': 'shobah',
            'khalaf': 'khalaf',
            'khallad': 'khallad',
            'tajweed': 'tajweed',
            'تجويد': 'tajweed',
            'uthmani_full': 'uthmani_full',
            'uthmani_minimal': 'uthmani_minimal',
            'uthmani_none': 'uthmani_none',
            'imlaey_full': 'imlaey_full',
            'imlaey_minimal': 'imlaey_minimal',
            'imlaey_none': 'imlaey_none',
            'amiri': 'amiri',
            'simple': 'simple',
            'with_waqf': 'with_waqf',
            'latin': 'latin',
            'phonetic': 'phonetic',
            'ajami': 'ajami',
            'unicode': 'unicode',
            'ascii': 'ascii',
            'braille': 'braille'
        }

        for key, value in mapping.items():
            if key in filename:
                return value

        # افتراضي: hafs
        print(f"⚠️  لم يتم التعرف على الإصدار من اسم الملف: {filename}")
        print(f"   سيتم استخدام hafs_smart_v8 كافتراضي")
        return 'hafs_smart_v8'

    def import_from_json(self, json_path: str, version_code: Optional[str] = None) -> bool:
        """
        استيراد من ملف JSON

        Args:
            json_path: مسار ملف JSON
            version_code: كود الإصدار (اختياري - يتم اكتشافه تلقائياً)

        Returns:
            True إذا نجح الاستيراد
        """
        json_path = Path(json_path)

        if not json_path.exists():
            print(f"❌ الملف غير موجود: {json_path}")
            return False

        print(f"\n{'='*70}")
        print(f"📥 استيراد من JSON: {json_path.name}")
        print(f"{'='*70}")

        # اكتشاف الإصدار
        if not version_code:
            version_code = self.detect_version_from_filename(json_path.name)

        version_id = self.get_version_id(version_code)
        if not version_id:
            print(f"❌ الإصدار غير موجود في القاعدة: {version_code}")
            return False

        print(f"📌 الإصدار: {version_code} (ID: {version_id})")

        # قراءة JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ خطأ في قراءة JSON: {e}")
            return False

        if not isinstance(data, list):
            print(f"❌ التنسيق غير صحيح: يجب أن يكون JSON array")
            return False

        print(f"📊 عدد الآيات في الملف: {len(data)}")

        # الاتصال بالقاعدة
        conn = sqlite3.connect(self.ayahs_db_path)
        cursor = conn.cursor()

        # استيراد كل آية
        imported_ayahs = 0
        imported_texts = 0
        errors = 0

        for i, item in enumerate(data, 1):
            try:
                # استخراج البيانات (دعم تنسيقات مختلفة)
                # التنسيق الأول: sura_no, aya_no
                sura_no = item.get('sura_no') or item.get('surahNo')
                aya_no = item.get('aya_no') or item.get('ayahNo')
                jozz = item.get('jozz', 1)
                page = item.get('page') or item.get('pageNo') or 1
                line_start = item.get('line_start')
                line_end = item.get('line_end')

                # النصوص (دعم التجويد)
                aya_text = item.get('aya_text', '') or item.get('tajweedText', '')
                aya_text_emlaey = item.get('aya_text_emlaey', '') or aya_text

                # التحقق من البيانات الأساسية
                if not sura_no or not aya_no:
                    print(f"⚠️  تخطي السجل {i}: بيانات ناقصة")
                    self.stats['skipped'] += 1
                    continue

                # 1. إدراج أو تحديث الآية في جدول ayahs
                cursor.execute("""
                    INSERT INTO ayahs (sura_no, aya_no, jozz, page, line_start, line_end)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(sura_no, aya_no) DO UPDATE SET
                        jozz = excluded.jozz,
                        page = excluded.page,
                        line_start = excluded.line_start,
                        line_end = excluded.line_end
                """, (sura_no, aya_no, jozz, page, line_start, line_end))

                # الحصول على ayah_id
                ayah_id = cursor.execute(
                    "SELECT id FROM ayahs WHERE sura_no = ? AND aya_no = ?",
                    (sura_no, aya_no)
                ).fetchone()[0]

                if cursor.rowcount > 0:
                    imported_ayahs += 1

                # 2. إدراج النص في جدول ayah_texts
                search_text = self.normalize_arabic(aya_text)
                word_count = self.count_words(aya_text)
                letter_count = self.count_letters(aya_text)

                cursor.execute("""
                    INSERT INTO ayah_texts
                    (ayah_id, version_id, aya_text, aya_text_emlaey, search_text, word_count, letter_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(ayah_id, version_id) DO UPDATE SET
                        aya_text = excluded.aya_text,
                        aya_text_emlaey = excluded.aya_text_emlaey,
                        search_text = excluded.search_text,
                        word_count = excluded.word_count,
                        letter_count = excluded.letter_count
                """, (ayah_id, version_id, aya_text, aya_text_emlaey, search_text, word_count, letter_count))

                imported_texts += 1

                # عرض التقدم
                if i % 100 == 0:
                    print(f"   ⏳ تم معالجة: {i}/{len(data)} آية...")

            except Exception as e:
                print(f"❌ خطأ في السجل {i}: {e}")
                errors += 1
                continue

        # الحفظ والإغلاق
        conn.commit()
        conn.close()

        # عرض النتائج
        print(f"\n{'='*70}")
        print(f"✅ اكتمل الاستيراد من {json_path.name}")
        print(f"{'='*70}")
        print(f"📊 الإحصائيات:")
        print(f"   • الآيات المستوردة: {imported_ayahs}")
        print(f"   • النصوص المستوردة: {imported_texts}")
        print(f"   • الأخطاء: {errors}")
        print(f"   • المتخطاة: {self.stats['skipped']}")

        # تحديث الإحصائيات العامة
        self.stats['ayahs_imported'] += imported_ayahs
        self.stats['texts_imported'] += imported_texts
        self.stats['errors'] += errors

        return True

    def import_from_txt(self, txt_path: str, version_code: Optional[str] = None) -> bool:
        """
        استيراد من ملف TXT (الصيغة: surah_no|ayah_no|text)

        Args:
            txt_path: مسار ملف TXT
            version_code: كود الإصدار (اختياري - يتم اكتشافه تلقائياً)

        Returns:
            True إذا نجح الاستيراد
        """
        txt_path = Path(txt_path)

        if not txt_path.exists():
            print(f"❌ الملف غير موجود: {txt_path}")
            return False

        print(f"\n{'='*70}")
        print(f"📥 استيراد من TXT: {txt_path.name}")
        print(f"{'='*70}")

        # اكتشاف الإصدار
        if not version_code:
            version_code = self.detect_version_from_filename(txt_path.name)

        version_id = self.get_version_id(version_code)
        if not version_id:
            print(f"❌ الإصدار غير موجود في القاعدة: {version_code}")
            return False

        print(f"📌 الإصدار: {version_code} (ID: {version_id})")

        # قراءة الملف
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"❌ خطأ في قراءة الملف: {e}")
            return False

        print(f"📊 عدد السطور: {len(lines)}")

        # الاتصال بالقاعدة
        conn = sqlite3.connect(self.ayahs_db_path)
        cursor = conn.cursor()

        imported_texts = 0
        errors = 0

        for i, line in enumerate(lines, 1):
            try:
                line = line.strip()
                if not line:
                    continue

                # الصيغة: surah_no|ayah_no|text
                parts = line.split('|', 2)
                if len(parts) < 3:
                    print(f"⚠️  تخطي السطر {i}: صيغة غير صحيحة")
                    self.stats['skipped'] += 1
                    continue

                sura_no = int(parts[0])
                aya_no = int(parts[1])
                aya_text = parts[2]

                # الحصول على ayah_id
                ayah_id_result = cursor.execute(
                    "SELECT id FROM ayahs WHERE sura_no = ? AND aya_no = ?",
                    (sura_no, aya_no)
                ).fetchone()

                if not ayah_id_result:
                    print(f"⚠️  الآية غير موجودة: {sura_no}:{aya_no}")
                    self.stats['skipped'] += 1
                    continue

                ayah_id = ayah_id_result[0]

                # إدراج النص
                search_text = self.normalize_arabic(aya_text)
                word_count = self.count_words(aya_text)
                letter_count = self.count_letters(aya_text)

                cursor.execute("""
                    INSERT INTO ayah_texts
                    (ayah_id, version_id, aya_text, aya_text_emlaey, search_text, word_count, letter_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(ayah_id, version_id) DO UPDATE SET
                        aya_text = excluded.aya_text,
                        search_text = excluded.search_text,
                        word_count = excluded.word_count,
                        letter_count = excluded.letter_count
                """, (ayah_id, version_id, aya_text, aya_text, search_text, word_count, letter_count))

                imported_texts += 1

                # عرض التقدم
                if i % 500 == 0:
                    print(f"   ⏳ تم معالجة: {i}/{len(lines)} سطر...")

            except Exception as e:
                print(f"❌ خطأ في السطر {i}: {e}")
                errors += 1
                continue

        # الحفظ والإغلاق
        conn.commit()
        conn.close()

        # عرض النتائج
        print(f"\n{'='*70}")
        print(f"✅ اكتمل الاستيراد من {txt_path.name}")
        print(f"{'='*70}")
        print(f"📊 الإحصائيات:")
        print(f"   • النصوص المستوردة: {imported_texts}")
        print(f"   • الأخطاء: {errors}")
        print(f"   • المتخطاة: {self.stats['skipped']}")

        # تحديث الإحصائيات العامة
        self.stats['texts_imported'] += imported_texts
        self.stats['errors'] += errors

        return True

    def import_all_from_directory(self, dir_path: str) -> Dict:
        """
        استيراد جميع الملفات من مجلد

        Args:
            dir_path: مسار المجلد

        Returns:
            إحصائيات الاستيراد
        """
        dir_path = Path(dir_path)

        if not dir_path.exists():
            print(f"❌ المجلد غير موجود: {dir_path}")
            return self.stats

        print(f"\n{'='*70}")
        print(f"📂 استيراد جميع الملفات من: {dir_path}")
        print(f"{'='*70}")

        # البحث عن الملفات
        json_files = list(dir_path.glob('*.json'))
        txt_files = list(dir_path.glob('*.txt'))

        print(f"📊 الملفات المكتشفة:")
        print(f"   • JSON: {len(json_files)}")
        print(f"   • TXT: {len(txt_files)}")

        # استيراد JSON أولاً
        for json_file in json_files:
            self.import_from_json(json_file)

        # استيراد TXT
        for txt_file in txt_files:
            self.import_from_txt(txt_file)

        return self.stats

    def show_final_stats(self):
        """عرض الإحصائيات النهائية"""
        print(f"\n{'='*70}")
        print(f"🎉 اكتمل الاستيراد!")
        print(f"{'='*70}")
        print(f"📊 الإحصائيات النهائية:")
        print(f"   ✅ الآيات المستوردة: {self.stats['ayahs_imported']}")
        print(f"   ✅ النصوص المستوردة: {self.stats['texts_imported']}")
        print(f"   ❌ الأخطاء: {self.stats['errors']}")
        print(f"   ⏭️  المتخطاة: {self.stats['skipped']}")

        # إحصائيات من القاعدة
        conn = sqlite3.connect(self.ayahs_db_path)
        cursor = conn.cursor()

        total_ayahs = cursor.execute("SELECT COUNT(*) FROM ayahs").fetchone()[0]
        total_texts = cursor.execute("SELECT COUNT(*) FROM ayah_texts").fetchone()[0]
        versions_with_data = cursor.execute(
            "SELECT COUNT(DISTINCT version_id) FROM ayah_texts"
        ).fetchone()[0]

        conn.close()

        print(f"\n📊 إحصائيات القاعدة:")
        print(f"   • إجمالي الآيات: {total_ayahs}")
        print(f"   • إجمالي النصوص: {total_texts}")
        print(f"   • الإصدارات المستوردة: {versions_with_data}/23")


def main():
    """الدالة الرئيسية"""
    import argparse

    parser = argparse.ArgumentParser(
        description="استيراد ذكي للقرآن الكريم (JSON/TXT)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
    # استيراد ملف JSON واحد
    python3 import_quran_smart.py --file data/sources/quran_Ayat/hafs_smart_v8.json

    # استيراد ملف TXT واحد
    python3 import_quran_smart.py --file data/sources/quran_Ayat/warsh.txt --version warsh

    # استيراد جميع الملفات من مجلد
    python3 import_quran_smart.py --directory data/sources/quran_Ayat/

    # استيراد ملف الاختبار
    python3 import_quran_smart.py --file data/sources/quran_Ayat/test_sample.json
        """
    )

    parser.add_argument(
        '--file',
        help='مسار ملف JSON أو TXT للاستيراد'
    )

    parser.add_argument(
        '--directory',
        help='مسار مجلد يحتوي على ملفات للاستيراد'
    )

    parser.add_argument(
        '--version',
        help='كود الإصدار (اختياري - يتم اكتشافه تلقائياً)'
    )

    args = parser.parse_args()

    try:
        importer = QuranSmartImporter()

        if args.file:
            file_path = Path(args.file)
            if file_path.suffix == '.json':
                importer.import_from_json(args.file, args.version)
            elif file_path.suffix == '.txt':
                importer.import_from_txt(args.file, args.version)
            else:
                print(f"❌ نوع ملف غير مدعوم: {file_path.suffix}")
                return 1

        elif args.directory:
            importer.import_all_from_directory(args.directory)

        else:
            print("❌ يجب تحديد --file أو --directory")
            parser.print_help()
            return 1

        # عرض الإحصائيات النهائية
        importer.show_final_stats()

        print(f"\n💡 الخطوة التالية:")
        print(f"   python3 scripts/verify_data.py")

        return 0

    except Exception as e:
        print(f"\n❌ خطأ: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

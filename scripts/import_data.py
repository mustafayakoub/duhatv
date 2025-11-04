#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت استيراد البيانات القرآنية إلى القواعد الأربعة
====================================================

يستورد البيانات من:
1. surahs_basic.json → SURAHS_DATABASE.db
2. ملفات Tanzil → AYAHS_DATABASE.db
3. Quranic Corpus → WORDS_DATABASE.db

الاستخدام:
    python3 import_data.py --all
    python3 import_data.py --surahs
    python3 import_data.py --ayahs

المؤلف: مشروع القرآن الرقمي
التاريخ: 3 نوفمبر 2025
"""

import os
import sys
import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime


class QuranDataImporter:
    """مستورد البيانات القرآنية"""

    def __init__(self, db_dir="databases", source_dir="data/sources"):
        """
        Args:
            db_dir: مجلد قواعد البيانات
            source_dir: مجلد البيانات المصدرية
        """
        self.db_dir = Path(db_dir)
        self.source_dir = Path(source_dir)

        # مسارات القواعد
        self.db_paths = {
            'surahs': self.db_dir / "SURAHS_DATABASE.db",
            'ayahs': self.db_dir / "AYAHS_DATABASE.db",
            'words': self.db_dir / "WORDS_DATABASE.db",
            'letters': self.db_dir / "LETTERS_DATABASE.db"
        }

        # التحقق من وجود القواعد
        self._verify_databases()

    def _verify_databases(self):
        """التحقق من وجود قواعد البيانات"""
        for name, path in self.db_paths.items():
            if not path.exists():
                raise FileNotFoundError(
                    f"❌ قاعدة البيانات غير موجودة: {path}\n"
                    f"   قم بإنشائها أولاً: python3 scripts/create_databases.py"
                )

    def normalize_arabic(self, text):
        """إزالة التشكيل من النص العربي للبحث"""
        if not text:
            return ""

        # علامات التشكيل
        diacritics = "ًٌٍَُِّْٰ"

        # إزالة التشكيل
        normalized = ''.join(c for c in text if c not in diacritics)

        return normalized

    def import_surahs(self):
        """استيراد بيانات السور من surahs_basic.json"""
        print("\n" + "="*70)
        print("📚 استيراد بيانات السور")
        print("="*70)

        # قراءة الملف JSON
        json_path = self.source_dir / "surahs_basic.json"

        if not json_path.exists():
            print(f"❌ ملف البيانات غير موجود: {json_path}")
            return False

        print(f"📖 قراءة: {json_path}")

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        surahs = data.get('surahs', [])
        print(f"✅ تم قراءة {len(surahs)} سورة")

        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect(self.db_paths['surahs'])
        cursor = conn.cursor()

        # التحقق من وجود بيانات سابقة
        existing_count = cursor.execute("SELECT COUNT(*) FROM surahs").fetchone()[0]

        if existing_count > 0:
            print(f"⚠️  يوجد {existing_count} سورة في القاعدة")
            response = input("   هل تريد حذف البيانات السابقة؟ (y/N): ")

            if response.lower() == 'y':
                cursor.execute("DELETE FROM surahs")
                cursor.execute("DELETE FROM surah_statistics")
                print("✅ تم حذف البيانات السابقة")
            else:
                print("⏭️  تخطي الاستيراد")
                conn.close()
                return True

        # استيراد السور
        imported = 0
        errors = []

        for surah in surahs:
            try:
                # إدراج السورة الرئيسية
                cursor.execute("""
                    INSERT INTO surahs (
                        surah_id, surah_number,
                        name_arabic, name_simple, name_english, name_transliteration,
                        revelation_type, revelation_order,
                        ayah_count, opening_letters,
                        main_theme_ar, main_theme_en
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    surah['id'],
                    surah['id'],
                    surah['name_ar'],
                    self.normalize_arabic(surah['name_ar']),
                    surah['name_en'],
                    surah.get('transliteration', ''),
                    surah['type'],
                    surah.get('order', 0),
                    surah['ayahs'],
                    surah.get('opening_letters'),
                    surah.get('theme_ar', ''),
                    surah.get('theme_en', '')
                ))

                # إدراج إحصائيات أولية
                cursor.execute("""
                    INSERT INTO surah_statistics (surah_id)
                    VALUES (?)
                """, (surah['id'],))

                imported += 1

                if imported % 10 == 0:
                    print(f"   📝 تم استيراد {imported} سورة...")

            except sqlite3.Error as e:
                errors.append(f"سورة {surah['id']}: {e}")

        conn.commit()
        conn.close()

        print(f"\n✅ تم استيراد {imported} سورة بنجاح!")

        if errors:
            print(f"\n⚠️  حدثت {len(errors)} أخطاء:")
            for error in errors[:5]:  # عرض أول 5 أخطاء
                print(f"   • {error}")

        return imported == len(surahs)

    def import_ayahs_from_tanzil(self, tanzil_file=None):
        """استيراد الآيات من ملف Tanzil"""
        print("\n" + "="*70)
        print("📖 استيراد بيانات الآيات من Tanzil")
        print("="*70)

        # البحث عن ملف Tanzil
        if tanzil_file is None:
            tanzil_file = self.source_dir / "tanzil" / "quran-simple.txt"

            # إذا لم يكن موجوداً، جرب البحث
            if not tanzil_file.exists():
                print("⚠️  ملف Tanzil غير موجود")
                print("   سأحاول إنشاء بيانات آيات أساسية...")
                return self._create_basic_ayahs()

        print(f"📖 قراءة: {tanzil_file}")

        # قراءة ملف Tanzil
        with open(tanzil_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        print(f"✅ تم قراءة {len(lines)} سطر")

        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect(self.db_paths['ayahs'])
        cursor = conn.cursor()

        # التحقق من وجود بيانات سابقة
        existing_count = cursor.execute("SELECT COUNT(*) FROM ayahs").fetchone()[0]

        if existing_count > 0:
            print(f"⚠️  يوجد {existing_count} آية في القاعدة")
            response = input("   هل تريد حذف البيانات السابقة؟ (y/N): ")

            if response.lower() == 'y':
                cursor.execute("DELETE FROM ayahs")
                print("✅ تم حذف البيانات السابقة")
            else:
                print("⏭️  تخطي الاستيراد")
                conn.close()
                return True

        # معالجة الآيات
        imported = 0
        ayah_id = 1
        errors = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            try:
                # تنسيق Tanzil: surah|ayah|text
                parts = line.split('|')
                if len(parts) != 3:
                    continue

                surah_id = int(parts[0])
                ayah_number = int(parts[1])
                ayah_text = parts[2].strip()

                # إدراج الآية
                cursor.execute("""
                    INSERT INTO ayahs (
                        ayah_id, surah_id, ayah_number,
                        ayah_text, ayah_text_simple,
                        search_text,
                        word_count, letter_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ayah_id,
                    surah_id,
                    ayah_number,
                    ayah_text,
                    ayah_text,
                    self.normalize_arabic(ayah_text),
                    len(ayah_text.split()),
                    len(ayah_text.replace(' ', ''))
                ))

                imported += 1
                ayah_id += 1

                if imported % 500 == 0:
                    print(f"   📝 تم استيراد {imported} آية...")

            except Exception as e:
                errors.append(f"سطر {line[:50]}: {e}")

        conn.commit()
        conn.close()

        print(f"\n✅ تم استيراد {imported} آية بنجاح!")

        if errors:
            print(f"\n⚠️  حدثت {len(errors)} أخطاء:")
            for error in errors[:5]:
                print(f"   • {error}")

        return imported > 0

    def _create_basic_ayahs(self):
        """إنشاء بيانات آيات أساسية (نموذج للاختبار)"""
        print("\n📝 إنشاء بيانات آيات أساسية...")

        # عدد الآيات لكل سورة (العد الكوفي)
        ayah_counts = [
            7, 286, 200, 176, 120, 165, 206, 75, 129, 109,
            123, 111, 43, 52, 99, 128, 111, 110, 98, 135,
            112, 78, 118, 64, 77, 227, 93, 88, 69, 60,
            34, 30, 73, 54, 45, 83, 182, 88, 75, 85,
            54, 53, 89, 59, 37, 35, 38, 29, 18, 45,
            60, 49, 62, 55, 78, 96, 29, 22, 24, 13,
            14, 11, 11, 18, 12, 12, 30, 52, 52, 44,
            28, 28, 20, 56, 40, 31, 50, 40, 46, 42,
            29, 19, 36, 25, 22, 17, 19, 26, 30, 20,
            15, 21, 11, 8, 8, 19, 5, 8, 8, 11,
            11, 8, 3, 9, 5, 4, 7, 3, 6, 3,
            5, 4, 5, 6
        ]

        conn = sqlite3.connect(self.db_paths['ayahs'])
        cursor = conn.cursor()

        # حذف البيانات السابقة
        cursor.execute("DELETE FROM ayahs")

        ayah_id = 1
        imported = 0

        for surah_id, count in enumerate(ayah_counts, 1):
            for ayah_num in range(1, count + 1):
                # نص نموذجي
                ayah_text = f"[نص الآية {ayah_num} من سورة {surah_id} - يحتاج استيراد من مصدر]"

                cursor.execute("""
                    INSERT INTO ayahs (
                        ayah_id, surah_id, ayah_number,
                        ayah_text, ayah_text_simple, search_text,
                        word_count, letter_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ayah_id, surah_id, ayah_num,
                    ayah_text, ayah_text, ayah_text,
                    0, 0
                ))

                ayah_id += 1
                imported += 1

        conn.commit()
        conn.close()

        print(f"✅ تم إنشاء {imported} آية نموذجية")
        print("⚠️  ملاحظة: هذه بيانات نموذجية - يجب استيراد النصوص الحقيقية")

        return True

    def get_statistics(self):
        """عرض إحصائيات القواعد"""
        print("\n" + "="*70)
        print("📊 إحصائيات القواعد")
        print("="*70)

        stats = {}

        # قاعدة السور
        conn = sqlite3.connect(self.db_paths['surahs'])
        cursor = conn.cursor()

        surah_count = cursor.execute("SELECT COUNT(*) FROM surahs").fetchone()[0]
        meccan = cursor.execute(
            "SELECT COUNT(*) FROM surahs WHERE revelation_type='Meccan'"
        ).fetchone()[0]
        medinan = cursor.execute(
            "SELECT COUNT(*) FROM surahs WHERE revelation_type='Medinan'"
        ).fetchone()[0]

        stats['surahs'] = {
            'total': surah_count,
            'meccan': meccan,
            'medinan': medinan
        }

        conn.close()

        # قاعدة الآيات
        conn = sqlite3.connect(self.db_paths['ayahs'])
        cursor = conn.cursor()

        ayah_count = cursor.execute("SELECT COUNT(*) FROM ayahs").fetchone()[0]

        stats['ayahs'] = {
            'total': ayah_count
        }

        conn.close()

        # عرض الإحصائيات
        print(f"\n🕌 السور:")
        print(f"   • المجموع: {stats['surahs']['total']}")
        print(f"   • المكية: {stats['surahs']['meccan']}")
        print(f"   • المدنية: {stats['surahs']['medinan']}")

        print(f"\n📖 الآيات:")
        print(f"   • المجموع: {stats['ayahs']['total']}")

        return stats


def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description="استيراد البيانات القرآنية إلى القواعد",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
    python3 import_data.py --all         # استيراد كل شيء
    python3 import_data.py --surahs      # استيراد السور فقط
    python3 import_data.py --ayahs       # استيراد الآيات فقط
    python3 import_data.py --stats       # عرض الإحصائيات
        """
    )

    parser.add_argument('--all', action='store_true', help='استيراد كل شيء')
    parser.add_argument('--surahs', action='store_true', help='استيراد السور')
    parser.add_argument('--ayahs', action='store_true', help='استيراد الآيات')
    parser.add_argument('--stats', action='store_true', help='عرض الإحصائيات')

    parser.add_argument(
        '--db-dir',
        default='databases',
        help='مجلد قواعد البيانات'
    )

    parser.add_argument(
        '--source-dir',
        default='data/sources',
        help='مجلد البيانات المصدرية'
    )

    args = parser.parse_args()

    try:
        importer = QuranDataImporter(
            db_dir=args.db_dir,
            source_dir=args.source_dir
        )

        # إذا لم يحدد المستخدم خياراً، استورد كل شيء
        if not any([args.all, args.surahs, args.ayahs, args.stats]):
            args.all = True

        success = True

        if args.all or args.surahs:
            success = importer.import_surahs() and success

        if args.all or args.ayahs:
            success = importer.import_ayahs_from_tanzil() and success

        if args.all or args.stats:
            importer.get_statistics()

        if success:
            print("\n" + "="*70)
            print("🎉 اكتمل الاستيراد بنجاح!")
            print("="*70)
            print("\n💡 الخطوات التالية:")
            print("   1. python3 scripts/verify_data.py  # للتحقق من البيانات")
            print("   2. python3 app.py                   # لتشغيل الواجهة")

        return 0 if success else 1

    except Exception as e:
        print(f"\n❌ خطأ: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

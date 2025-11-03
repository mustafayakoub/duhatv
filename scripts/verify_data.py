#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت التحقق من دقة البيانات القرآنية
==========================================

يتحقق من:
1. عدد السور = 114
2. عدد الآيات (حسب العد الكوفي)
3. صحة العلاقات بين الجداول
4. عدم وجود بيانات فارغة أو null
5. عدد الكلمات المتوقع = 77,432

الاستخدام:
    python3 verify_data.py
    python3 verify_data.py --detailed
    python3 verify_data.py --fix

المؤلف: مشروع القرآن الرقمي
التاريخ: 3 نوفمبر 2025
"""

import os
import sys
import sqlite3
import argparse
from pathlib import Path


class QuranDataVerifier:
    """محقق البيانات القرآنية"""

    def __init__(self, db_dir="databases"):
        """
        Args:
            db_dir: مجلد قواعد البيانات
        """
        self.db_dir = Path(db_dir)

        # مسارات القواعد
        self.db_paths = {
            'surahs': self.db_dir / "SURAHS_DATABASE.db",
            'ayahs': self.db_dir / "AYAHS_DATABASE.db",
            'words': self.db_dir / "WORDS_DATABASE.db",
            'letters': self.db_dir / "LETTERS_DATABASE.db"
        }

        # الأرقام الصحيحة
        self.expected = {
            'surahs_total': 114,
            'surahs_meccan': 86,
            'surahs_medinan': 28,
            'ayahs_total': 6236,  # العد الكوفي
            'words_total': 77432,  # العدد الدقيق
            'letters_total': 320000  # تقريبي
        }

        # نتائج الفحص
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }

    def verify_surahs(self):
        """التحقق من قاعدة السور"""
        print("\n" + "="*70)
        print("🕌 فحص قاعدة السور")
        print("="*70)

        conn = sqlite3.connect(self.db_paths['surahs'])
        cursor = conn.cursor()

        # 1. عدد السور
        count = cursor.execute("SELECT COUNT(*) FROM surahs").fetchone()[0]
        self._check("عدد السور", count, self.expected['surahs_total'])

        # 2. عدد السور المكية
        meccan = cursor.execute(
            "SELECT COUNT(*) FROM surahs WHERE revelation_type='Meccan'"
        ).fetchone()[0]
        self._check("السور المكية", meccan, self.expected['surahs_meccan'])

        # 3. عدد السور المدنية
        medinan = cursor.execute(
            "SELECT COUNT(*) FROM surahs WHERE revelation_type='Medinan'"
        ).fetchone()[0]
        self._check("السور المدنية", medinan, self.expected['surahs_medinan'])

        # 4. التحقق من الأسماء العربية
        null_names = cursor.execute(
            "SELECT COUNT(*) FROM surahs WHERE name_arabic IS NULL OR name_arabic=''"
        ).fetchone()[0]

        if null_names == 0:
            self.results['passed'].append("✅ جميع السور لها أسماء عربية")
            print("   ✅ جميع السور لها أسماء عربية")
        else:
            self.results['failed'].append(f"❌ {null_names} سورة بدون أسماء عربية")
            print(f"   ❌ {null_names} سورة بدون أسماء عربية")

        # 5. التحقق من عدد الآيات
        zero_ayahs = cursor.execute(
            "SELECT COUNT(*) FROM surahs WHERE ayah_count = 0 OR ayah_count IS NULL"
        ).fetchone()[0]

        if zero_ayahs == 0:
            self.results['passed'].append("✅ جميع السور لها عدد آيات صحيح")
            print("   ✅ جميع السور لها عدد آيات صحيح")
        else:
            self.results['failed'].append(f"❌ {zero_ayahs} سورة بدون عدد آيات")
            print(f"   ❌ {zero_ayahs} سورة بدون عدد آيات")

        # 6. التحقق من ترتيب السور (1-114)
        missing_ids = []
        for i in range(1, 115):
            exists = cursor.execute(
                "SELECT COUNT(*) FROM surahs WHERE surah_id=?", (i,)
            ).fetchone()[0]
            if exists == 0:
                missing_ids.append(i)

        if not missing_ids:
            self.results['passed'].append("✅ جميع أرقام السور موجودة (1-114)")
            print("   ✅ جميع أرقام السور موجودة (1-114)")
        else:
            self.results['failed'].append(f"❌ سور مفقودة: {missing_ids}")
            print(f"   ❌ سور مفقودة: {missing_ids}")

        conn.close()

    def verify_ayahs(self):
        """التحقق من قاعدة الآيات"""
        print("\n" + "="*70)
        print("📖 فحص قاعدة الآيات")
        print("="*70)

        conn = sqlite3.connect(self.db_paths['ayahs'])
        cursor = conn.cursor()

        # 1. عدد الآيات الإجمالي
        count = cursor.execute("SELECT COUNT(*) FROM ayahs").fetchone()[0]
        self._check("عدد الآيات الإجمالي", count, self.expected['ayahs_total'])

        # 2. التحقق من النصوص الفارغة
        empty_text = cursor.execute(
            "SELECT COUNT(*) FROM ayahs WHERE ayah_text IS NULL OR ayah_text=''"
        ).fetchone()[0]

        if empty_text == 0:
            self.results['passed'].append("✅ جميع الآيات لها نص")
            print("   ✅ جميع الآيات لها نص")
        else:
            self.results['warnings'].append(f"⚠️  {empty_text} آية بدون نص")
            print(f"   ⚠️  {empty_text} آية بدون نص")

        # 3. التحقق من أرقام السور (1-114)
        invalid_surah = cursor.execute(
            "SELECT COUNT(*) FROM ayahs WHERE surah_id < 1 OR surah_id > 114"
        ).fetchone()[0]

        if invalid_surah == 0:
            self.results['passed'].append("✅ جميع الآيات لها أرقام سور صحيحة")
            print("   ✅ جميع الآيات لها أرقام سور صحيحة")
        else:
            self.results['failed'].append(f"❌ {invalid_surah} آية بأرقام سور خاطئة")
            print(f"   ❌ {invalid_surah} آية بأرقام سور خاطئة")

        # 4. التحقق من أرقام الآيات
        invalid_ayah_num = cursor.execute(
            "SELECT COUNT(*) FROM ayahs WHERE ayah_number < 1"
        ).fetchone()[0]

        if invalid_ayah_num == 0:
            self.results['passed'].append("✅ جميع الآيات لها أرقام صحيحة")
            print("   ✅ جميع الآيات لها أرقام صحيحة")
        else:
            self.results['failed'].append(f"❌ {invalid_ayah_num} آية بأرقام خاطئة")
            print(f"   ❌ {invalid_ayah_num} آية بأرقام خاطئة")

        conn.close()

    def verify_relations(self):
        """التحقق من العلاقات بين القواعد"""
        print("\n" + "="*70)
        print("🔗 فحص العلاقات بين القواعد")
        print("="*70)

        # الاتصال بالقاعدتين
        conn_surahs = sqlite3.connect(self.db_paths['surahs'])
        conn_ayahs = sqlite3.connect(self.db_paths['ayahs'])

        cursor_surahs = conn_surahs.cursor()
        cursor_ayahs = conn_ayahs.cursor()

        # التحقق من تطابق عدد الآيات
        surahs = cursor_surahs.execute(
            "SELECT surah_id, ayah_count FROM surahs ORDER BY surah_id"
        ).fetchall()

        mismatches = []

        for surah_id, expected_count in surahs:
            actual_count = cursor_ayahs.execute(
                "SELECT COUNT(*) FROM ayahs WHERE surah_id=?", (surah_id,)
            ).fetchone()[0]

            if actual_count != expected_count:
                mismatches.append((surah_id, expected_count, actual_count))

        if not mismatches:
            self.results['passed'].append("✅ عدد الآيات متطابق مع جدول السور")
            print("   ✅ عدد الآيات متطابق مع جدول السور")
        else:
            msg = f"❌ {len(mismatches)} سورة بعدد آيات غير متطابق"
            self.results['failed'].append(msg)
            print(f"   {msg}")

            # عرض أول 5 اختلافات
            for surah_id, expected, actual in mismatches[:5]:
                print(f"      • سورة {surah_id}: متوقع {expected}، وُجد {actual}")

        conn_surahs.close()
        conn_ayahs.close()

    def verify_words(self):
        """التحقق من قاعدة الكلمات (إن وُجدت بيانات)"""
        print("\n" + "="*70)
        print("📝 فحص قاعدة الكلمات")
        print("="*70)

        conn = sqlite3.connect(self.db_paths['words'])
        cursor = conn.cursor()

        count = cursor.execute("SELECT COUNT(*) FROM words").fetchone()[0]

        if count == 0:
            self.results['warnings'].append("⚠️  قاعدة الكلمات فارغة - تحتاج استيراد")
            print("   ⚠️  قاعدة الكلمات فارغة - تحتاج استيراد")
        else:
            self._check("عدد الكلمات", count, self.expected['words_total'], warning_only=True)

        conn.close()

    def _check(self, name, actual, expected, warning_only=False):
        """فحص قيمة مع القيمة المتوقعة"""
        if actual == expected:
            msg = f"✅ {name}: {actual:,}"
            self.results['passed'].append(msg)
            print(f"   {msg}")
        else:
            if warning_only:
                msg = f"⚠️  {name}: {actual:,} (متوقع: {expected:,})"
                self.results['warnings'].append(msg)
            else:
                msg = f"❌ {name}: {actual:,} (متوقع: {expected:,})"
                self.results['failed'].append(msg)
            print(f"   {msg}")

    def verify_all(self):
        """تشغيل جميع الفحوصات"""
        print("="*70)
        print("🔍 بدء التحقق من دقة البيانات القرآنية")
        print("="*70)

        self.verify_surahs()
        self.verify_ayahs()
        self.verify_relations()
        self.verify_words()

        # عرض التقرير النهائي
        self.print_summary()

    def print_summary(self):
        """عرض ملخص النتائج"""
        print("\n" + "="*70)
        print("📊 ملخص نتائج الفحص")
        print("="*70)

        print(f"\n✅ النجاحات: {len(self.results['passed'])}")
        for result in self.results['passed']:
            print(f"   {result}")

        if self.results['warnings']:
            print(f"\n⚠️  التحذيرات: {len(self.results['warnings'])}")
            for result in self.results['warnings']:
                print(f"   {result}")

        if self.results['failed']:
            print(f"\n❌ الأخطاء: {len(self.results['failed'])}")
            for result in self.results['failed']:
                print(f"   {result}")

        # النتيجة النهائية
        print("\n" + "="*70)

        if not self.results['failed']:
            print("🎉 جميع الفحوصات نجحت!")
            if self.results['warnings']:
                print("⚠️  يوجد تحذيرات - راجعها أعلاه")
            print("="*70)
            return True
        else:
            print("❌ فشل بعض الفحوصات - راجع الأخطاء أعلاه")
            print("="*70)
            return False

    def get_detailed_stats(self):
        """عرض إحصائيات تفصيلية"""
        print("\n" + "="*70)
        print("📈 إحصائيات تفصيلية")
        print("="*70)

        # قاعدة السور
        conn = sqlite3.connect(self.db_paths['surahs'])
        cursor = conn.cursor()

        print("\n🕌 السور:")
        total = cursor.execute('SELECT COUNT(*) FROM surahs').fetchone()[0]
        meccan = cursor.execute("SELECT COUNT(*) FROM surahs WHERE revelation_type='Meccan'").fetchone()[0]
        medinan = cursor.execute("SELECT COUNT(*) FROM surahs WHERE revelation_type='Medinan'").fetchone()[0]
        print(f"   • المجموع: {total}")
        print(f"   • المكية: {meccan}")
        print(f"   • المدنية: {medinan}")

        # أطول وأقصر سورة
        longest = cursor.execute(
            "SELECT name_arabic, ayah_count FROM surahs ORDER BY ayah_count DESC LIMIT 1"
        ).fetchone()
        shortest = cursor.execute(
            "SELECT name_arabic, ayah_count FROM surahs ORDER BY ayah_count ASC LIMIT 1"
        ).fetchone()

        print(f"   • أطول سورة: {longest[0]} ({longest[1]} آية)")
        print(f"   • أقصر سورة: {shortest[0]} ({shortest[1]} آية)")

        conn.close()

        # قاعدة الآيات
        conn = sqlite3.connect(self.db_paths['ayahs'])
        cursor = conn.cursor()

        print("\n📖 الآيات:")
        ayah_count = cursor.execute('SELECT COUNT(*) FROM ayahs').fetchone()[0]
        print(f"   • المجموع: {ayah_count:,}")

        # متوسط عدد الآيات
        avg_per_surah = ayah_count / 114
        print(f"   • المتوسط لكل سورة: {avg_per_surah:.1f}")

        conn.close()

        # قاعدة الكلمات
        conn = sqlite3.connect(self.db_paths['words'])
        cursor = conn.cursor()

        word_count = cursor.execute('SELECT COUNT(*) FROM words').fetchone()[0]

        print("\n📝 الكلمات:")
        if word_count > 0:
            print(f"   • المجموع: {word_count:,}")
        else:
            print("   • لم يتم استيرادها بعد")

        conn.close()


def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description="التحقق من دقة البيانات القرآنية",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
    python3 verify_data.py              # فحص أساسي
    python3 verify_data.py --detailed   # مع إحصائيات تفصيلية
        """
    )

    parser.add_argument(
        '--detailed',
        action='store_true',
        help='عرض إحصائيات تفصيلية'
    )

    parser.add_argument(
        '--db-dir',
        default='databases',
        help='مجلد قواعد البيانات'
    )

    args = parser.parse_args()

    try:
        verifier = QuranDataVerifier(db_dir=args.db_dir)

        # تشغيل الفحوصات
        success = verifier.verify_all()

        # إحصائيات تفصيلية
        if args.detailed:
            verifier.get_detailed_stats()

        return 0 if success else 1

    except Exception as e:
        print(f"\n❌ خطأ: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

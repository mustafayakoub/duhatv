#!/usr/bin/env python3
"""
استيراد بيانات القرآن الكريم من ملف hafs_smart_v8.json
Import Quran Data from hafs_smart_v8.json

هذا السكريبت يقوم بـ:
1. قراءة ملف JSON الذي يحتوي على كل بيانات القرآن (سور، آيات، أجزاء، صفحات)
2. معالجة البيانات وتنظيمها
3. استيرادها إلى قاعدة بيانات PostgreSQL

المتطلبات:
- Python 3.8+
- psycopg2 or psycopg2-binary
- python-dotenv

الاستخدام:
    python import_hafs_data.py --input hafs_smart_v8.json --db-url postgresql://user:pass@localhost/quran_db
"""

import json
import argparse
import sys
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

try:
    import psycopg2
    from psycopg2.extras import execute_batch
    from psycopg2 import sql
except ImportError:
    print("❌ Error: psycopg2 not installed")
    print("📦 Install it using: pip install psycopg2-binary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  Warning: python-dotenv not installed (optional)")
    print("📦 Install it using: pip install python-dotenv")


class QuranDataImporter:
    """مستورد بيانات القرآن الكريم"""

    def __init__(self, db_url: str, verbose: bool = True):
        """
        Initialize the importer

        Args:
            db_url: Database connection URL (postgresql://user:pass@host:port/dbname)
            verbose: Print detailed logs
        """
        self.db_url = db_url
        self.verbose = verbose
        self.conn = None
        self.cursor = None

        # إحصائيات
        self.stats = {
            'surahs_imported': 0,
            'ayahs_imported': 0,
            'errors': 0,
            'start_time': datetime.now()
        }

    def log(self, message: str, level: str = "INFO"):
        """طباعة رسالة"""
        if self.verbose:
            icons = {
                "INFO": "ℹ️ ",
                "SUCCESS": "✅",
                "ERROR": "❌",
                "WARNING": "⚠️ ",
                "PROGRESS": "⏳"
            }
            icon = icons.get(level, "  ")
            print(f"{icon} {message}")

    def connect(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.log(f"Connecting to database...", "PROGRESS")
            self.conn = psycopg2.connect(self.db_url)
            self.cursor = self.conn.cursor()
            self.log("Connected successfully!", "SUCCESS")

            # اختبار الاتصال
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()[0]
            self.log(f"PostgreSQL version: {version[:50]}...", "INFO")

        except Exception as e:
            self.log(f"Failed to connect: {e}", "ERROR")
            raise

    def disconnect(self):
        """قطع الاتصال"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.log("Disconnected from database", "INFO")

    def load_json(self, file_path: str) -> List[Dict[str, Any]]:
        """
        تحميل ملف JSON

        Args:
            file_path: مسار ملف JSON

        Returns:
            قائمة بالآيات
        """
        self.log(f"Loading JSON file: {file_path}", "PROGRESS")

        if not os.path.exists(file_path):
            self.log(f"File not found: {file_path}", "ERROR")
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.log(f"Loaded {len(data)} records", "SUCCESS")
            return data

        except json.JSONDecodeError as e:
            self.log(f"Invalid JSON: {e}", "ERROR")
            raise
        except Exception as e:
            self.log(f"Error loading file: {e}", "ERROR")
            raise

    def extract_surahs(self, data: List[Dict]) -> List[Dict]:
        """
        استخراج معلومات السور من البيانات

        Args:
            data: قائمة الآيات من JSON

        Returns:
            قائمة السور
        """
        self.log("Extracting Surahs info...", "PROGRESS")

        surahs_dict = {}

        for ayah in data:
            surah_no = ayah.get('sura_no')
            if surah_no and surah_no not in surahs_dict:
                surahs_dict[surah_no] = {
                    'number': surah_no,
                    'name_arabic': ayah.get('sura_name_ar', ''),
                    'name_transliteration': ayah.get('sura_name_en', ''),
                    'ayah_count': 0,  # سنحسبها لاحقاً
                    'metadata': {}
                }

        # حساب عدد الآيات لكل سورة
        for ayah in data:
            surah_no = ayah.get('sura_no')
            if surah_no and surah_no in surahs_dict:
                surahs_dict[surah_no]['ayah_count'] += 1

        surahs = sorted(surahs_dict.values(), key=lambda x: x['number'])

        self.log(f"Extracted {len(surahs)} surahs", "SUCCESS")
        return surahs

    def import_surahs(self, surahs: List[Dict]):
        """
        استيراد السور إلى قاعدة البيانات

        Args:
            surahs: قائمة السور
        """
        self.log("Importing Surahs...", "PROGRESS")

        try:
            # حذف البيانات القديمة (اختياري)
            # self.cursor.execute("TRUNCATE TABLE surahs CASCADE;")

            insert_query = """
                INSERT INTO surahs (number, name_arabic, name_transliteration, ayah_count, metadata)
                VALUES (%(number)s, %(name_arabic)s, %(name_transliteration)s, %(ayah_count)s, %(metadata)s)
                ON CONFLICT (number) DO UPDATE SET
                    name_arabic = EXCLUDED.name_arabic,
                    name_transliteration = EXCLUDED.name_transliteration,
                    ayah_count = EXCLUDED.ayah_count,
                    updated_at = NOW()
                RETURNING id;
            """

            surah_ids = {}
            for surah in surahs:
                self.cursor.execute(insert_query, {
                    'number': surah['number'],
                    'name_arabic': surah['name_arabic'],
                    'name_transliteration': surah['name_transliteration'],
                    'ayah_count': surah['ayah_count'],
                    'metadata': json.dumps(surah.get('metadata', {}))
                })
                surah_id = self.cursor.fetchone()[0]
                surah_ids[surah['number']] = surah_id
                self.stats['surahs_imported'] += 1

            self.conn.commit()
            self.log(f"Imported {self.stats['surahs_imported']} surahs", "SUCCESS")

            return surah_ids

        except Exception as e:
            self.conn.rollback()
            self.log(f"Error importing surahs: {e}", "ERROR")
            raise

    def import_ayahs(self, data: List[Dict], surah_ids: Dict[int, int]):
        """
        استيراد الآيات إلى قاعدة البيانات

        Args:
            data: قائمة الآيات من JSON
            surah_ids: словарь معرفات السور {surah_number: surah_id}
        """
        self.log(f"Importing {len(data)} Ayahs...", "PROGRESS")

        try:
            insert_query = """
                INSERT INTO ayahs (
                    surah_id, ayah_number, global_ayah_number,
                    text_uthmani, text_simple, text_imlaei,
                    juz_number, page_number,
                    metadata
                )
                VALUES (
                    %(surah_id)s, %(ayah_number)s, %(global_ayah_number)s,
                    %(text_uthmani)s, %(text_simple)s, %(text_imlaei)s,
                    %(juz_number)s, %(page_number)s,
                    %(metadata)s
                )
                ON CONFLICT (surah_id, ayah_number) DO UPDATE SET
                    text_uthmani = EXCLUDED.text_uthmani,
                    text_simple = EXCLUDED.text_simple,
                    text_imlaei = EXCLUDED.text_imlaei,
                    juz_number = EXCLUDED.juz_number,
                    page_number = EXCLUDED.page_number,
                    metadata = EXCLUDED.metadata
                RETURNING id;
            """

            batch_size = 100
            batch = []

            for ayah in data:
                surah_no = ayah.get('sura_no')
                surah_id = surah_ids.get(surah_no)

                if not surah_id:
                    self.log(f"Surah {surah_no} not found, skipping ayah", "WARNING")
                    continue

                ayah_data = {
                    'surah_id': surah_id,
                    'ayah_number': ayah.get('aya_no'),
                    'global_ayah_number': ayah.get('id'),
                    'text_uthmani': ayah.get('aya_text', ''),
                    'text_simple': ayah.get('aya_text', ''),  # نفس النص الآن
                    'text_imlaei': ayah.get('aya_text_emlaey', ''),
                    'juz_number': ayah.get('jozz'),
                    'page_number': ayah.get('page'),
                    'metadata': json.dumps({
                        'line_start': ayah.get('line_start'),
                        'line_end': ayah.get('line_end')
                    })
                }

                batch.append(ayah_data)

                # استيراد Batch
                if len(batch) >= batch_size:
                    execute_batch(self.cursor, insert_query, batch)
                    self.conn.commit()
                    self.stats['ayahs_imported'] += len(batch)
                    self.log(f"Imported {self.stats['ayahs_imported']} ayahs...", "PROGRESS")
                    batch = []

            # استيراد الباقي
            if batch:
                execute_batch(self.cursor, insert_query, batch)
                self.conn.commit()
                self.stats['ayahs_imported'] += len(batch)

            self.log(f"Imported total {self.stats['ayahs_imported']} ayahs", "SUCCESS")

        except Exception as e:
            self.conn.rollback()
            self.log(f"Error importing ayahs: {e}", "ERROR")
            raise

    def print_stats(self):
        """طباعة الإحصائيات"""
        duration = datetime.now() - self.stats['start_time']

        print("\n" + "="*60)
        print("📊 Import Statistics / إحصائيات الاستيراد")
        print("="*60)
        print(f"✅ Surahs imported:  {self.stats['surahs_imported']}")
        print(f"✅ Ayahs imported:   {self.stats['ayahs_imported']}")
        print(f"❌ Errors:           {self.stats['errors']}")
        print(f"⏱️  Duration:         {duration}")
        print("="*60 + "\n")

    def run(self, json_file: str):
        """
        تشغيل عملية الاستيراد الكاملة

        Args:
            json_file: مسار ملف JSON
        """
        try:
            # 1. الاتصال بقاعدة البيانات
            self.connect()

            # 2. تحميل البيانات
            data = self.load_json(json_file)

            # 3. استخراج السور
            surahs = self.extract_surahs(data)

            # 4. استيراد السور
            surah_ids = self.import_surahs(surahs)

            # 5. استيراد الآيات
            self.import_ayahs(data, surah_ids)

            # 6. طباعة الإحصائيات
            self.print_stats()

            self.log("Import completed successfully! 🎉", "SUCCESS")

        except Exception as e:
            self.stats['errors'] += 1
            self.log(f"Import failed: {e}", "ERROR")
            raise

        finally:
            self.disconnect()


def main():
    """البرنامج الرئيسي"""
    parser = argparse.ArgumentParser(
        description="استيراد بيانات القرآن الكريم من hafs_smart_v8.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
مثال الاستخدام:
  python import_hafs_data.py \\
      --input /path/to/hafs_smart_v8.json \\
      --db-url "postgresql://quran:password@localhost:5432/quran_db"

أو استخدام متغيرات البيئة:
  export DATABASE_URL="postgresql://quran:password@localhost:5432/quran_db"
  python import_hafs_data.py --input /path/to/hafs_smart_v8.json
        """
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='مسار ملف JSON (hafs_smart_v8.json)'
    )

    parser.add_argument(
        '-d', '--db-url',
        default=os.getenv('DATABASE_URL'),
        help='Database URL (أو استخدم DATABASE_URL env variable)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=True,
        help='طباعة تفاصيل أكثر'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='عدم طباعة التفاصيل'
    )

    args = parser.parse_args()

    # التحقق من وجود DATABASE_URL
    if not args.db_url:
        print("❌ Error: Database URL is required")
        print("   Use --db-url argument or set DATABASE_URL environment variable")
        sys.exit(1)

    # التحقق من وجود الملف
    if not os.path.exists(args.input):
        print(f"❌ Error: File not found: {args.input}")
        sys.exit(1)

    # تشغيل الاستيراد
    verbose = args.verbose and not args.quiet
    importer = QuranDataImporter(args.db_url, verbose=verbose)

    try:
        importer.run(args.input)
    except KeyboardInterrupt:
        print("\n\n⚠️  Import cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Import failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

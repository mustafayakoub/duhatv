#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
📥 استيراد متقدم من SQLite إلى PostgreSQL
Advanced SQLite to PostgreSQL Import Tool
═══════════════════════════════════════════════════════════════
"""

import sqlite3
import psycopg2
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse

# ═══════════════════════════════════════════════════════════════
# الألوان
# ═══════════════════════════════════════════════════════════════

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ═══════════════════════════════════════════════════════════════
# فئة الاستيراد
# ═══════════════════════════════════════════════════════════════

class QuranDataImporter:
    """مستورد بيانات القرآن المتقدم"""

    def __init__(self, config_path: str):
        """تهيئة المستورد"""
        self.config = self.load_config(config_path)
        self.sqlite_conn = None
        self.pg_conn = None
        self.stats = {
            'total_imported': 0,
            'total_skipped': 0,
            'total_errors': 0,
            'tables': {}
        }

    def load_config(self, config_path: str) -> Dict:
        """تحميل ملف التكوين"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"{Colors.GREEN}✅ تم تحميل التكوين من: {config_path}{Colors.END}\n")
            return config
        except FileNotFoundError:
            print(f"{Colors.RED}❌ ملف التكوين غير موجود: {config_path}{Colors.END}")
            print(f"{Colors.YELLOW}💡 استخدم import_config.template.json كنموذج{Colors.END}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"{Colors.RED}❌ خطأ في JSON: {e}{Colors.END}")
            sys.exit(1)

    def connect_sqlite(self) -> sqlite3.Connection:
        """الاتصال بـ SQLite"""
        db_path = self.config['sqlite']['database_path']

        if not Path(db_path).exists():
            print(f"{Colors.RED}❌ قاعدة SQLite غير موجودة: {db_path}{Colors.END}")
            sys.exit(1)

        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            print(f"{Colors.GREEN}✅ اتصال SQLite: {db_path}{Colors.END}")
            return conn
        except Exception as e:
            print(f"{Colors.RED}❌ فشل الاتصال بـ SQLite: {e}{Colors.END}")
            sys.exit(1)

    def connect_postgresql(self) -> psycopg2.extensions.connection:
        """الاتصال بـ PostgreSQL"""
        pg_config = self.config['postgresql']

        # طلب كلمة المرور إذا لم تكن موجودة
        if not pg_config.get('password'):
            import getpass
            pg_config['password'] = getpass.getpass("🔐 كلمة مرور PostgreSQL: ")

        try:
            conn = psycopg2.connect(
                host=pg_config['host'],
                port=pg_config['port'],
                database=pg_config['database'],
                user=pg_config['user'],
                password=pg_config['password']
            )
            print(f"{Colors.GREEN}✅ اتصال PostgreSQL: {pg_config['database']}{Colors.END}\n")
            return conn
        except Exception as e:
            print(f"{Colors.RED}❌ فشل الاتصال بـ PostgreSQL: {e}{Colors.END}")
            sys.exit(1)

    def validate_record(self, table_name: str, record: Dict) -> bool:
        """التحقق من صحة السجل"""
        if 'validation_rules' not in self.config:
            return True

        rules = self.config['validation_rules'].get(table_name, {})

        for field, constraints in rules.items():
            value = record.get(field)

            # التحقق من الحقول المطلوبة
            if constraints.get('required') and not value:
                print(f"{Colors.YELLOW}⚠️  حقل مطلوب فارغ: {field}{Colors.END}")
                return False

            if value is not None:
                # التحقق من النطاق الرقمي
                if 'min' in constraints and value < constraints['min']:
                    return False
                if 'max' in constraints and value > constraints['max']:
                    return False

                # التحقق من طول النص
                if isinstance(value, str):
                    if 'min_length' in constraints and len(value) < constraints['min_length']:
                        return False
                    if 'max_length' in constraints and len(value) > constraints['max_length']:
                        return False

        return True

    def transform_value(self, value: Any, field_type: str) -> Any:
        """تحويل القيم حسب القواعد المحددة"""
        if value is None:
            return None

        transformations = self.config.get('data_transformations', {})

        # تحويل نوع الوحي
        if field_type == 'revelation_type' and value in transformations.get('revelation_type', {}):
            return transformations['revelation_type'][value]

        # تحويل رموز اللغات
        if field_type == 'language_code' and value in transformations.get('language_codes', {}):
            return transformations['language_codes'][value]

        return value

    def import_table(self, table_name: str, mapping: Dict) -> int:
        """استيراد جدول واحد"""
        if not mapping.get('enabled', False):
            print(f"{Colors.YELLOW}⏭️  تخطي {table_name} (معطّل في التكوين){Colors.END}\n")
            return 0

        print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 60}")
        print(f"📦 استيراد {table_name}")
        print(f"{'═' * 60}{Colors.END}\n")

        source_table = mapping['source_table']
        column_mapping = mapping.get('column_mapping', {})

        # التحقق من وجود الجدول المصدر
        sqlite_cur = self.sqlite_conn.cursor()
        try:
            sqlite_cur.execute(f"SELECT * FROM {source_table} LIMIT 1")
        except sqlite3.OperationalError:
            print(f"{Colors.RED}❌ الجدول المصدر غير موجود: {source_table}{Colors.END}\n")
            return 0

        # عد السجلات
        sqlite_cur.execute(f"SELECT COUNT(*) FROM {source_table}")
        total_count = sqlite_cur.fetchone()[0]
        print(f"📊 إجمالي السجلات: {total_count:,}\n")

        # قراءة البيانات
        source_columns = list(column_mapping.keys())
        target_columns = list(column_mapping.values())

        sqlite_cur.execute(f"SELECT * FROM {source_table}")

        pg_cur = self.pg_conn.cursor()
        imported = 0
        skipped = 0
        errors = 0

        batch_size = self.config['import_options'].get('batch_size', 100)

        while True:
            batch = sqlite_cur.fetchmany(batch_size)
            if not batch:
                break

            for row in batch:
                try:
                    row_dict = dict(row)

                    # إنشاء سجل مُعاد تعيينه
                    mapped_record = {}
                    for src_col, tgt_col in column_mapping.items():
                        value = row_dict.get(src_col)
                        # تطبيق التحويلات
                        if src_col in ['revelation_type', 'type']:
                            value = self.transform_value(value, 'revelation_type')
                        elif src_col in ['language', 'lang']:
                            value = self.transform_value(value, 'language_code')
                        mapped_record[tgt_col] = value

                    # إضافة القيم الافتراضية
                    defaults = mapping.get('defaults', {})
                    for key, value in defaults.items():
                        if key not in mapped_record or mapped_record[key] is None:
                            mapped_record[key] = value

                    # التحقق من الصحة
                    if not self.validate_record(table_name, mapped_record):
                        skipped += 1
                        continue

                    # بناء استعلام الإدراج
                    schema = 'quran' if table_name not in ['users', 'bookmarks', 'annotations'] else 'community'
                    full_table_name = f"{schema}.{table_name}"

                    columns_str = ', '.join(target_columns)
                    placeholders = ', '.join(['%s'] * len(target_columns))
                    values = [mapped_record.get(col) for col in target_columns]

                    skip_existing = self.config['import_options'].get('skip_existing', True)
                    on_conflict = "ON CONFLICT DO NOTHING" if skip_existing else ""

                    query = f"""
                        INSERT INTO {full_table_name} ({columns_str})
                        VALUES ({placeholders})
                        {on_conflict}
                    """

                    pg_cur.execute(query, values)
                    imported += 1

                    if imported % 500 == 0:
                        print(f"   ... {imported:,} سجل")
                        self.pg_conn.commit()

                except Exception as e:
                    errors += 1
                    if errors <= 10:  # عرض أول 10 أخطاء فقط
                        print(f"{Colors.YELLOW}⚠️  خطأ: {e}{Colors.END}")

            self.pg_conn.commit()

        # الإحصائيات
        self.stats['tables'][table_name] = {
            'imported': imported,
            'skipped': skipped,
            'errors': errors
        }

        print(f"\n{Colors.GREEN}✅ {table_name}:")
        print(f"   تم الاستيراد: {imported:,}")
        if skipped > 0:
            print(f"   تم التخطي: {skipped:,}")
        if errors > 0:
            print(f"   أخطاء: {errors:,}")
        print(f"{Colors.END}")

        return imported

    def run(self):
        """تشغيل عملية الاستيراد الكاملة"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 70}")
        print("📥 بدء الاستيراد المتقدم من SQLite إلى PostgreSQL")
        print(f"{'═' * 70}{Colors.END}\n")

        start_time = datetime.now()

        # الاتصال بالقواعد
        self.sqlite_conn = self.connect_sqlite()
        self.pg_conn = self.connect_postgresql()

        # استيراد الجداول
        table_mappings = self.config.get('table_mappings', {})

        # ترتيب الاستيراد (الأهم أولاً)
        import_order = ['surahs', 'ayahs', 'words', 'translations', 'tafsir', 'reciters', 'recitations']

        for table_name in import_order:
            if table_name in table_mappings:
                self.import_table(table_name, table_mappings[table_name])

        # إغلاق الاتصالات
        self.sqlite_conn.close()
        self.pg_conn.close()

        # النتيجة النهائية
        duration = (datetime.now() - start_time).total_seconds()

        print(f"\n{Colors.BOLD}{Colors.GREEN}{'═' * 70}")
        print("🎉 تم الاستيراد بنجاح!")
        print(f"{'═' * 70}{Colors.END}\n")

        print(f"{Colors.CYAN}⏱️  المدة: {duration:.2f} ثانية{Colors.END}\n")

        print(f"{Colors.BOLD}📊 الإحصائيات التفصيلية:{Colors.END}\n")
        for table_name, stats in self.stats['tables'].items():
            print(f"  {table_name}:")
            print(f"    ✅ مستورد: {stats['imported']:,}")
            if stats['skipped'] > 0:
                print(f"    ⏭️  متخطى: {stats['skipped']:,}")
            if stats['errors'] > 0:
                print(f"    ❌ أخطاء: {stats['errors']:,}")

        total_imported = sum(s['imported'] for s in self.stats['tables'].values())
        print(f"\n{Colors.GREEN}{Colors.BOLD}  إجمالي السجلات المستوردة: {total_imported:,}{Colors.END}\n")

# ═══════════════════════════════════════════════════════════════
# البرنامج الرئيسي
# ═══════════════════════════════════════════════════════════════

def main():
    """البرنامج الرئيسي"""
    parser = argparse.ArgumentParser(
        description='📥 استيراد متقدم من SQLite إلى PostgreSQL',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-c', '--config',
        default='import_config.json',
        help='ملف التكوين (افتراضي: import_config.json)'
    )

    args = parser.parse_args()

    # إنشاء المستورد وتشغيله
    importer = QuranDataImporter(args.config)
    importer.run()

if __name__ == "__main__":
    main()

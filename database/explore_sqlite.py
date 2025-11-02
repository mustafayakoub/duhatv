#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
🔍 أداة استكشاف قواعد بيانات SQLite
SQLite Database Explorer Tool
═══════════════════════════════════════════════════════════════
تستكشف هذه الأداة بنية قاعدة بيانات SQLite وتعرض جميع الجداول
والأعمدة والإحصائيات لمساعدتك في تخطيط عملية الاستيراد
"""

import sqlite3
import sys
import json
from pathlib import Path
from typing import List, Dict, Any
import argparse

# ═══════════════════════════════════════════════════════════════
# الألوان للطباعة
# ═══════════════════════════════════════════════════════════════

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ═══════════════════════════════════════════════════════════════
# دوال الاتصال
# ═══════════════════════════════════════════════════════════════

def connect_database(db_path: str) -> sqlite3.Connection:
    """الاتصال بقاعدة بيانات SQLite"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print(f"{Colors.GREEN}✅ اتصال ناجح بـ: {db_path}{Colors.END}\n")
        return conn
    except Exception as e:
        print(f"{Colors.RED}❌ فشل الاتصال: {e}{Colors.END}")
        sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# استكشاف البنية
# ═══════════════════════════════════════════════════════════════

def get_all_tables(conn: sqlite3.Connection) -> List[str]:
    """الحصول على جميع أسماء الجداول"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    return [row[0] for row in cursor.fetchall()]

def get_table_info(conn: sqlite3.Connection, table_name: str) -> Dict[str, Any]:
    """الحصول على معلومات تفصيلية عن جدول"""
    cursor = conn.cursor()

    # معلومات الأعمدة
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = []
    for row in cursor.fetchall():
        columns.append({
            'cid': row[0],
            'name': row[1],
            'type': row[2],
            'notnull': row[3],
            'default': row[4],
            'pk': row[5]
        })

    # عدد السجلات
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
    except:
        count = 0

    # حجم الجدول التقريبي
    try:
        cursor.execute(f"SELECT SUM(pgsize) FROM dbstat WHERE name='{table_name}'")
        size_result = cursor.fetchone()[0]
        size = size_result if size_result else 0
    except:
        size = 0

    # الفهارس
    cursor.execute(f"PRAGMA index_list({table_name})")
    indexes = [row[1] for row in cursor.fetchall()]

    return {
        'name': table_name,
        'columns': columns,
        'row_count': count,
        'size_bytes': size,
        'indexes': indexes
    }

def get_sample_data(conn: sqlite3.Connection, table_name: str, limit: int = 3) -> List[Dict]:
    """الحصول على عينة من البيانات"""
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        return []

def detect_quran_tables(conn: sqlite3.Connection) -> Dict[str, str]:
    """كشف جداول القرآن المحتملة"""
    cursor = conn.cursor()
    tables = get_all_tables(conn)

    quran_tables = {
        'surahs': None,
        'ayahs': None,
        'words': None,
        'translations': None,
        'tafsir': None,
        'reciters': None,
        'recitations': None
    }

    # أسماء محتملة لكل نوع جدول
    patterns = {
        'surahs': ['sura', 'surah', 'suras', 'surahs', 'chapter', 'chapters'],
        'ayahs': ['quran', 'quran_text', 'aya', 'ayah', 'ayat', 'ayahs', 'verse', 'verses'],
        'words': ['word', 'words', 'kalima', 'kalimat'],
        'translations': ['translation', 'translations', 'tarjama', 'tarjamat'],
        'tafsir': ['tafsir', 'tafseer', 'commentary', 'interpretation'],
        'reciters': ['reciter', 'reciters', 'qari', 'qurra'],
        'recitations': ['recitation', 'recitations', 'tilawa', 'audio']
    }

    for table_type, possible_names in patterns.items():
        for name in possible_names:
            # بحث دقيق أو جزئي
            matching = [t for t in tables if name in t.lower()]
            if matching:
                quran_tables[table_type] = matching[0]
                break

    return {k: v for k, v in quran_tables.items() if v is not None}

# ═══════════════════════════════════════════════════════════════
# عرض التقارير
# ═══════════════════════════════════════════════════════════════

def print_header(text: str):
    """طباعة عنوان رئيسي"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 70}")
    print(f"  {text}")
    print(f"{'═' * 70}{Colors.END}\n")

def print_database_overview(db_path: str, tables: List[str]):
    """عرض نظرة عامة على القاعدة"""
    print_header("📊 نظرة عامة على قاعدة البيانات")

    path = Path(db_path)
    size_mb = path.stat().st_size / 1024 / 1024

    print(f"{Colors.CYAN}📂 المسار:{Colors.END} {db_path}")
    print(f"{Colors.CYAN}📦 الحجم:{Colors.END} {size_mb:.2f} MB")
    print(f"{Colors.CYAN}📋 عدد الجداول:{Colors.END} {len(tables)}")
    print()

def print_table_details(table_info: Dict[str, Any], show_sample: bool = False, sample_data: List[Dict] = None):
    """عرض تفاصيل جدول"""
    print(f"{Colors.BOLD}{Colors.GREEN}📌 {table_info['name']}{Colors.END}")
    print(f"   السجلات: {Colors.YELLOW}{table_info['row_count']:,}{Colors.END}")

    if table_info['size_bytes'] > 0:
        size_kb = table_info['size_bytes'] / 1024
        print(f"   الحجم: {size_kb:.2f} KB")

    print(f"   الأعمدة ({len(table_info['columns'])}):")

    for col in table_info['columns']:
        pk_marker = f"{Colors.YELLOW}🔑{Colors.END}" if col['pk'] else "  "
        nn_marker = "NOT NULL" if col['notnull'] else ""
        print(f"      {pk_marker} {col['name']:<30} {col['type']:<15} {nn_marker}")

    if table_info['indexes']:
        print(f"   الفهارس ({len(table_info['indexes'])}):")
        for idx in table_info['indexes']:
            print(f"      📇 {idx}")

    if show_sample and sample_data:
        print(f"\n   {Colors.CYAN}عينة من البيانات:{Colors.END}")
        for i, row in enumerate(sample_data, 1):
            print(f"      السجل {i}:")
            for key, value in row.items():
                value_str = str(value)[:50] + "..." if value and len(str(value)) > 50 else value
                print(f"         {key}: {value_str}")

    print()

def print_quran_detection_results(quran_tables: Dict[str, str]):
    """عرض نتائج كشف جداول القرآن"""
    print_header("🔍 كشف جداول القرآن")

    if not quran_tables:
        print(f"{Colors.YELLOW}⚠️  لم يتم اكتشاف أي جداول قرآنية معروفة{Colors.END}\n")
        return

    print(f"{Colors.GREEN}✅ تم اكتشاف الجداول التالية:{Colors.END}\n")

    icons = {
        'surahs': '📖',
        'ayahs': '📜',
        'words': '🔤',
        'translations': '🌍',
        'tafsir': '📚',
        'reciters': '🎤',
        'recitations': '🔊'
    }

    for table_type, table_name in quran_tables.items():
        icon = icons.get(table_type, '📋')
        print(f"   {icon} {table_type.title():<15} → {Colors.CYAN}{table_name}{Colors.END}")

    print()

def export_schema_to_json(tables_info: List[Dict[str, Any]], output_file: str):
    """تصدير البنية إلى ملف JSON"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tables_info, f, ensure_ascii=False, indent=2)
        print(f"{Colors.GREEN}✅ تم تصدير البنية إلى: {output_file}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ فشل التصدير: {e}{Colors.END}")

# ═══════════════════════════════════════════════════════════════
# البرنامج الرئيسي
# ═══════════════════════════════════════════════════════════════

def main():
    """البرنامج الرئيسي"""
    parser = argparse.ArgumentParser(
        description='🔍 استكشاف قاعدة بيانات SQLite',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('database', help='مسار قاعدة بيانات SQLite')
    parser.add_argument('-s', '--sample', action='store_true', help='عرض عينة من البيانات')
    parser.add_argument('-e', '--export', metavar='FILE', help='تصدير البنية إلى JSON')
    parser.add_argument('-t', '--table', metavar='TABLE', help='عرض تفاصيل جدول معين فقط')

    args = parser.parse_args()

    # التحقق من وجود الملف
    if not Path(args.database).exists():
        print(f"{Colors.RED}❌ الملف غير موجود: {args.database}{Colors.END}")
        sys.exit(1)

    # الاتصال بالقاعدة
    conn = connect_database(args.database)

    # الحصول على الجداول
    tables = get_all_tables(conn)

    if not tables:
        print(f"{Colors.YELLOW}⚠️  القاعدة فارغة (لا توجد جداول){Colors.END}")
        sys.exit(0)

    # عرض النظرة العامة
    print_database_overview(args.database, tables)

    # كشف جداول القرآن
    quran_tables = detect_quran_tables(conn)
    print_quran_detection_results(quran_tables)

    # عرض تفاصيل الجداول
    print_header("📋 تفاصيل الجداول")

    tables_info = []

    if args.table:
        # عرض جدول معين فقط
        if args.table in tables:
            table_info = get_table_info(conn, args.table)
            sample_data = get_sample_data(conn, args.table, 5) if args.sample else None
            print_table_details(table_info, args.sample, sample_data)
            tables_info.append(table_info)
        else:
            print(f"{Colors.RED}❌ الجدول غير موجود: {args.table}{Colors.END}")
    else:
        # عرض جميع الجداول
        for table_name in tables:
            table_info = get_table_info(conn, table_name)
            sample_data = get_sample_data(conn, table_name) if args.sample else None
            print_table_details(table_info, args.sample, sample_data)
            tables_info.append(table_info)

    # تصدير إلى JSON إذا طُلب
    if args.export:
        export_schema_to_json(tables_info, args.export)

    # إغلاق الاتصال
    conn.close()

    # ملخص نهائي
    print_header("📊 الملخص")
    total_rows = sum(t['row_count'] for t in tables_info)
    total_columns = sum(len(t['columns']) for t in tables_info)

    print(f"{Colors.GREEN}✅ تم استكشاف {len(tables_info)} جدول{Colors.END}")
    print(f"   إجمالي السجلات: {total_rows:,}")
    print(f"   إجمالي الأعمدة: {total_columns}")

    if quran_tables:
        print(f"\n{Colors.CYAN}💡 الخطوة التالية:{Colors.END}")
        print(f"   استخدم import_from_sqlite.py لاستيراد البيانات إلى PostgreSQL")

    print()

if __name__ == "__main__":
    main()

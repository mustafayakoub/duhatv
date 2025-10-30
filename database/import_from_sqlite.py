#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
📥 استيراد البيانات من SQLite إلى PostgreSQL
═══════════════════════════════════════════════════════════════
"""

import sqlite3
import psycopg2
import sys
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# الإعدادات - عدّلها حسب بيئتك
# ═══════════════════════════════════════════════════════════════

# مسار قاعدة SQLite
SQLITE_DB_PATH = r"C:\quran7\quran_ultimate_final.db"

# إعدادات PostgreSQL
PG_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'quran_hierarchical_db',
    'user': 'postgres',
    'password': ''  # أدخل كلمة المرور هنا
}

# ═══════════════════════════════════════════════════════════════
# دوال الاتصال
# ═══════════════════════════════════════════════════════════════

def connect_sqlite(db_path):
    """الاتصال بقاعدة SQLite"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print(f"✅ اتصال SQLite: {db_path}")
        return conn
    except Exception as e:
        print(f"❌ فشل الاتصال بـ SQLite: {e}")
        sys.exit(1)

def connect_postgresql():
    """الاتصال بقاعدة PostgreSQL"""
    # اسأل عن كلمة المرور إذا لم تكن مُعرّفة
    if not PG_CONFIG['password']:
        import getpass
        PG_CONFIG['password'] = getpass.getpass("🔐 كلمة مرور PostgreSQL: ")

    try:
        conn = psycopg2.connect(**PG_CONFIG)
        print(f"✅ اتصال PostgreSQL: {PG_CONFIG['database']}")
        return conn
    except Exception as e:
        print(f"❌ فشل الاتصال بـ PostgreSQL: {e}")
        sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# استكشاف قاعدة SQLite
# ═══════════════════════════════════════════════════════════════

def explore_sqlite_schema(sqlite_conn):
    """استكشاف بنية قاعدة SQLite"""
    print("\n" + "="*60)
    print("📊 استكشاف قاعدة SQLite")
    print("="*60 + "\n")

    cursor = sqlite_conn.cursor()

    # قراءة جميع الجداول
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    """)

    tables = [row[0] for row in cursor.fetchall()]
    print(f"📋 عدد الجداول: {len(tables)}\n")

    # عرض كل جدول مع عدد السجلات
    for table_name in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]

            # قراءة أسماء الأعمدة
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]

            print(f"📌 {table_name}:")
            print(f"   السجلات: {count:,}")
            print(f"   الأعمدة: {', '.join(columns[:5])}")
            if len(columns) > 5:
                print(f"           ... و {len(columns)-5} عمود آخر")
            print()
        except Exception as e:
            print(f"⚠️  تعذر قراءة جدول {table_name}: {e}\n")

    return tables

# ═══════════════════════════════════════════════════════════════
# استيراد السور
# ═══════════════════════════════════════════════════════════════

def import_surahs(sqlite_conn, pg_conn):
    """استيراد جدول السور"""
    print("\n" + "="*60)
    print("📖 استيراد السور (surahs)")
    print("="*60 + "\n")

    sqlite_cur = sqlite_conn.cursor()
    pg_cur = pg_conn.cursor()

    # محاولة إيجاد جدول السور
    possible_names = ['suras', 'surah', 'surahs', 'chapters']
    sura_table = None

    for name in possible_names:
        try:
            sqlite_cur.execute(f"SELECT * FROM {name} LIMIT 1")
            sura_table = name
            print(f"✅ تم العثور على جدول السور: {name}")
            break
        except:
            continue

    if not sura_table:
        print("❌ لم يتم العثور على جدول السور")
        return

    # قراءة السور من SQLite
    sqlite_cur.execute(f"SELECT * FROM {sura_table} ORDER BY sura")
    suras = sqlite_cur.fetchall()

    print(f"📊 عدد السور: {len(suras)}")

    # استيراد السور إلى PostgreSQL
    imported = 0
    for sura in suras:
        try:
            # تكييف أسماء الأعمدة
            sura_dict = dict(sura)

            pg_cur.execute("""
                INSERT INTO quran.surahs (
                    sur_id, sur_name_ar, sur_name_en,
                    sur_ayah_count, sur_revelation_type
                ) VALUES (
                    %(sura)s, %(name_arabic)s, %(name_english)s,
                    %(ayas_count)s, %(revelation_type)s
                )
                ON CONFLICT (sur_id) DO NOTHING
            """, {
                'sura': sura_dict.get('sura') or sura_dict.get('id'),
                'name_arabic': sura_dict.get('name_arabic') or sura_dict.get('name'),
                'name_english': sura_dict.get('name_english') or sura_dict.get('english_name'),
                'ayas_count': sura_dict.get('ayas_count') or sura_dict.get('ayah_count'),
                'revelation_type': (sura_dict.get('revelation_type') or 'meccan').lower()
            })
            imported += 1
        except Exception as e:
            print(f"⚠️  خطأ في السورة {sura_dict.get('sura', '?')}: {e}")

    pg_conn.commit()
    print(f"✅ تم استيراد {imported} سورة بنجاح!\n")

# ═══════════════════════════════════════════════════════════════
# استيراد الآيات
# ═══════════════════════════════════════════════════════════════

def import_ayahs(sqlite_conn, pg_conn):
    """استيراد جدول الآيات"""
    print("\n" + "="*60)
    print("📜 استيراد الآيات (ayahs)")
    print("="*60 + "\n")

    sqlite_cur = sqlite_conn.cursor()
    pg_cur = pg_conn.cursor()

    # محاولة إيجاد جدول الآيات
    possible_names = ['quran', 'quran_text', 'ayat', 'verses', 'ayahs']
    aya_table = None

    for name in possible_names:
        try:
            sqlite_cur.execute(f"SELECT * FROM {name} LIMIT 1")
            aya_table = name
            print(f"✅ تم العثور على جدول الآيات: {name}")
            break
        except:
            continue

    if not aya_table:
        print("❌ لم يتم العثور على جدول الآيات")
        return

    # عرض أسماء الأعمدة
    sqlite_cur.execute(f"PRAGMA table_info({aya_table})")
    columns = [col[1] for col in sqlite_cur.fetchall()]
    print(f"📋 الأعمدة المتاحة: {', '.join(columns[:10])}")
    if len(columns) > 10:
        print(f"    ... و {len(columns)-10} عمود آخر")
    print()

    # قراءة الآيات
    print("🔄 جاري استيراد الآيات...")
    sqlite_cur.execute(f"""
        SELECT * FROM {aya_table}
        ORDER BY sura, aya
    """)

    imported = 0
    global_id = 1

    while True:
        batch = sqlite_cur.fetchmany(100)
        if not batch:
            break

        for aya in batch:
            try:
                aya_dict = dict(aya)

                # استخراج البيانات مع التكييف
                sura = aya_dict.get('sura') or aya_dict.get('surah') or aya_dict.get('sura_number')
                aya_num = aya_dict.get('aya') or aya_dict.get('ayah') or aya_dict.get('aya_number')

                # النصوص
                text_uthmani = (
                    aya_dict.get('text_uthmani') or
                    aya_dict.get('text') or
                    aya_dict.get('aya_text')
                )

                text_simple = (
                    aya_dict.get('text_simple') or
                    aya_dict.get('text_imlaei') or
                    text_uthmani
                )

                pg_cur.execute("""
                    INSERT INTO quran.ayahs (
                        aya_global_id, aya_sur_id, aya_number,
                        aya_text_uthmani, aya_text_simple,
                        aya_juz, aya_page
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (aya_global_id) DO NOTHING
                """, (
                    global_id, sura, aya_num,
                    text_uthmani, text_simple,
                    aya_dict.get('juz'), aya_dict.get('page')
                ))

                imported += 1
                global_id += 1

                if imported % 500 == 0:
                    print(f"   ... {imported} آية")
                    pg_conn.commit()

            except Exception as e:
                print(f"⚠️  خطأ في آية {sura}:{aya_num}: {e}")

        pg_conn.commit()

    print(f"\n✅ تم استيراد {imported} آية بنجاح!\n")

# ═══════════════════════════════════════════════════════════════
# البرنامج الرئيسي
# ═══════════════════════════════════════════════════════════════

def main():
    """البرنامج الرئيسي"""
    print("\n" + "="*60)
    print("📥 استيراد البيانات من SQLite إلى PostgreSQL")
    print("="*60 + "\n")

    # التحقق من وجود ملف SQLite
    sqlite_path = Path(SQLITE_DB_PATH)
    if not sqlite_path.exists():
        print(f"❌ الملف غير موجود: {SQLITE_DB_PATH}")
        print(f"\n💡 يرجى تعديل المسار في السكريبت:")
        print(f"   SQLITE_DB_PATH = r'YOUR_PATH_HERE'\n")
        sys.exit(1)

    print(f"📂 ملف SQLite: {SQLITE_DB_PATH}")
    print(f"📦 حجم الملف: {sqlite_path.stat().st_size / 1024 / 1024:.2f} MB\n")

    # الاتصال بالقواعد
    sqlite_conn = connect_sqlite(SQLITE_DB_PATH)
    pg_conn = connect_postgresql()

    # استكشاف البنية
    tables = explore_sqlite_schema(sqlite_conn)

    # تأكيد
    print("\n" + "="*60)
    response = input("⚠️  هل تريد المتابعة مع الاستيراد؟ (نعم/لا): ")
    if response.lower() not in ['نعم', 'yes', 'y']:
        print("❌ تم الإلغاء")
        return

    # الاستيراد
    start_time = datetime.now()

    import_surahs(sqlite_conn, pg_conn)
    import_ayahs(sqlite_conn, pg_conn)

    # إغلاق الاتصالات
    sqlite_conn.close()
    pg_conn.close()

    # النتيجة
    duration = (datetime.now() - start_time).total_seconds()

    print("\n" + "="*60)
    print("🎉 تم الاستيراد بنجاح!")
    print("="*60)
    print(f"⏱️  المدة: {duration:.2f} ثانية")
    print(f"📊 للتحقق:")
    print(f"   psql -U postgres -d quran_hierarchical_db")
    print(f"   SELECT COUNT(*) FROM quran.surahs;")
    print(f"   SELECT COUNT(*) FROM quran.ayahs;")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════
Quran Modern Stack - Database Migration Script
سكريبت نقل البيانات من القواعد الثلاث إلى قاعدة PostgreSQL الموحدة

يقوم بـ:
1. قراءة البيانات من 3 قواعد SQLite
2. دمجها وتنظيمها
3. إدخالها في PostgreSQL

═══════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import sqlite3
import psycopg2
from psycopg2.extras import execute_batch
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import json

# ═══════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# مسارات قواعد البيانات
SOURCE_DB_1 = os.getenv('SOURCE_DB_1', '/source-dbs/quran_ultimate_final.db')
SOURCE_DB_2 = os.getenv('SOURCE_DB_2', '/source-dbs/surah_database_app_v32.db')
SOURCE_DB_3 = os.getenv('SOURCE_DB_3', '/source-dbs/Quran_Crystalline.db')

TARGET_DB_URL = os.getenv('TARGET_DB_URL', 'postgresql://quran:quran_secure_pass_2025@postgres:5432/quran_db')

# ═══════════════════════════════════════════════════════════════════════════
# Database Connection Helpers
# ═══════════════════════════════════════════════════════════════════════════

def connect_sqlite(db_path: str) -> sqlite3.Connection:
    """الاتصال بقاعدة SQLite"""
    logger.info(f"Connecting to SQLite: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def connect_postgres() -> psycopg2.extensions.connection:
    """الاتصال بقاعدة PostgreSQL"""
    logger.info(f"Connecting to PostgreSQL: {TARGET_DB_URL}")
    return psycopg2.connect(TARGET_DB_URL)

# ═══════════════════════════════════════════════════════════════════════════
# Migration Functions
# ═══════════════════════════════════════════════════════════════════════════

class QuranMigration:
    """فئة رئيسية لنقل البيانات"""

    def __init__(self):
        self.db1 = None
        self.db2 = None
        self.db3 = None
        self.target = None
        self.cursor = None

    def connect_all(self):
        """الاتصال بكل القواعد"""
        try:
            logger.info("=" * 70)
            logger.info("  بدء الاتصال بقواعد البيانات")
            logger.info("=" * 70)

            self.db1 = connect_sqlite(SOURCE_DB_1)
            logger.info(f"✅ Connected to DB1: quran_ultimate_final.db")

            self.db2 = connect_sqlite(SOURCE_DB_2)
            logger.info(f"✅ Connected to DB2: surah_database_app_v32.db")

            self.db3 = connect_sqlite(SOURCE_DB_3)
            logger.info(f"✅ Connected to DB3: Quran_Crystalline.db")

            self.target = connect_postgres()
            self.cursor = self.target.cursor()
            logger.info(f"✅ Connected to PostgreSQL")

        except Exception as e:
            logger.error(f"❌ خطأ في الاتصال: {e}")
            sys.exit(1)

    def migrate_surahs(self):
        """نقل السور (114 سورة)"""
        logger.info("\n" + "=" * 70)
        logger.info("  📚 نقل السور (Surahs)")
        logger.info("=" * 70)

        try:
            # القراءة من DB3 (Crystalline - الأكثر تنظيماً)
            cursor3 = self.db3.cursor()
            cursor3.execute("""
                SELECT
                    surah_id,
                    name_ar,
                    revelation_type,
                    revelation_order,
                    ayah_count
                FROM Surahs
                ORDER BY surah_id
            """)

            surahs = []
            for row in cursor3.fetchall():
                surah = {
                    'number': row['surah_id'],
                    'name_arabic': row['name_ar'],
                    'revelation_type': row['revelation_type'],
                    'revelation_order': row['revelation_order'],
                    'ayah_count': row['ayah_count']
                }
                surahs.append(surah)

            # الإدخال في PostgreSQL
            insert_query = """
                INSERT INTO surahs (
                    number, name_arabic, revelation_type,
                    revelation_order, ayah_count
                )
                VALUES (%(number)s, %(name_arabic)s, %(revelation_type)s,
                        %(revelation_order)s, %(ayah_count)s)
                ON CONFLICT (number) DO NOTHING
            """

            execute_batch(self.cursor, insert_query, surahs, page_size=100)
            self.target.commit()

            logger.info(f"✅ تم نقل {len(surahs)} سورة")

        except Exception as e:
            logger.error(f"❌ خطأ في نقل السور: {e}")
            self.target.rollback()
            raise

    def migrate_ayahs(self):
        """نقل الآيات (6,236 آية)"""
        logger.info("\n" + "=" * 70)
        logger.info("  📖 نقل الآيات (Ayahs)")
        logger.info("=" * 70)

        try:
            # القراءة من DB3 (Crystalline)
            cursor3 = self.db3.cursor()
            cursor3.execute("""
                SELECT
                    ayah_global_id,
                    surah_id,
                    ayah_num_in_surah,
                    juz_id,
                    hizb_id,
                    page_num,
                    revelation_order_global,
                    sajda_type
                FROM Ayat
                ORDER BY ayah_global_id
            """)

            # النص القرآني من DB3
            cursor3_text = self.db3.cursor()
            cursor3_text.execute("""
                SELECT
                    ayah_global_id,
                    text_type_id,
                    text
                FROM QuranicText
            """)

            # تنظيم النصوص حسب الآية
            texts = {}
            for row in cursor3_text.fetchall():
                ayah_id = row['ayah_global_id']
                if ayah_id not in texts:
                    texts[ayah_id] = {}
                # 1 = Uthmani, 2 = Simple
                if row['text_type_id'] == 1:
                    texts[ayah_id]['uthmani'] = row['text']
                elif row['text_type_id'] == 2:
                    texts[ayah_id]['simple'] = row['text']

            ayahs = []
            for row in cursor3.fetchall():
                global_id = row['ayah_global_id']
                ayah = {
                    'surah_id': row['surah_id'],
                    'ayah_number': row['ayah_num_in_surah'],
                    'global_ayah_number': global_id,
                    'text_uthmani': texts.get(global_id, {}).get('uthmani', ''),
                    'text_simple': texts.get(global_id, {}).get('simple', ''),
                    'juz_number': row['juz_id'],
                    'hizb_number': row['hizb_id'],
                    'page_number': row['page_num'],
                    'sajda_type': row['sajda_type'],
                    'revelation_order_global': row['revelation_order_global']
                }
                ayahs.append(ayah)

            # الإدخال في PostgreSQL
            insert_query = """
                INSERT INTO ayahs (
                    surah_id, ayah_number, global_ayah_number,
                    text_uthmani, text_simple,
                    juz_number, hizb_number, page_number,
                    sajda_type, revelation_order_global
                )
                VALUES (
                    %(surah_id)s, %(ayah_number)s, %(global_ayah_number)s,
                    %(text_uthmani)s, %(text_simple)s,
                    %(juz_number)s, %(hizb_number)s, %(page_number)s,
                    %(sajda_type)s, %(revelation_order_global)s
                )
                ON CONFLICT (global_ayah_number) DO NOTHING
            """

            execute_batch(self.cursor, insert_query, ayahs, page_size=500)
            self.target.commit()

            logger.info(f"✅ تم نقل {len(ayahs)} آية")

        except Exception as e:
            logger.error(f"❌ خطأ في نقل الآيات: {e}")
            self.target.rollback()
            raise

    def migrate_roots(self):
        """نقل الجذور (1,775 جذر)"""
        logger.info("\n" + "=" * 70)
        logger.info("  🌱 نقل الجذور (Roots)")
        logger.info("=" * 70)

        try:
            # القراءة من DB3 (Crystalline)
            cursor3 = self.db3.cursor()
            cursor3.execute("""
                SELECT
                    root_id,
                    root_text
                FROM Roots
                ORDER BY root_id
            """)

            roots = []
            for row in cursor3.fetchall():
                root = {
                    'id': row['root_id'],
                    'root_text': row['root_text']
                }
                roots.append(root)

            # الإدخال في PostgreSQL
            insert_query = """
                INSERT INTO roots (id, root_text)
                VALUES (%(id)s, %(root_text)s)
                ON CONFLICT (root_text) DO NOTHING
            """

            execute_batch(self.cursor, insert_query, roots, page_size=500)
            self.target.commit()

            logger.info(f"✅ تم نقل {len(roots)} جذر")

        except Exception as e:
            logger.error(f"❌ خطأ في نقل الجذور: {e}")
            self.target.rollback()
            raise

    def migrate_words(self):
        """نقل الكلمات (77,430 كلمة)"""
        logger.info("\n" + "=" * 70)
        logger.info("  🔤 نقل الكلمات (Words)")
        logger.info("=" * 70)

        try:
            # القراءة من DB3 (Crystalline)
            cursor3 = self.db3.cursor()
            cursor3.execute("""
                SELECT
                    word_id,
                    ayah_global_id,
                    word_num_in_ayah,
                    text_uthmani,
                    root_id
                FROM Words
                ORDER BY word_id
                LIMIT 10000  -- دفعة تجريبية
            """)

            words = []
            for row in cursor3.fetchall():
                word = {
                    'id': row['word_id'],
                    'ayah_id': row['ayah_global_id'],
                    'word_number': row['word_num_in_ayah'],
                    'global_word_number': row['word_id'],
                    'text_uthmani': row['text_uthmani'] or '',
                    'text_simple': row['text_uthmani'] or '',  # نبسطه لاحقاً
                    'root_id': row['root_id']
                }
                words.append(word)

            # الإدخال في PostgreSQL
            insert_query = """
                INSERT INTO words (
                    global_word_number, ayah_id, word_number,
                    text_uthmani, text_simple, root_id
                )
                VALUES (
                    %(global_word_number)s, %(ayah_id)s, %(word_number)s,
                    %(text_uthmani)s, %(text_simple)s, %(root_id)s
                )
                ON CONFLICT (global_word_number) DO NOTHING
            """

            execute_batch(self.cursor, insert_query, words, page_size=1000)
            self.target.commit()

            logger.info(f"✅ تم نقل {len(words)} كلمة (دفعة تجريبية)")

        except Exception as e:
            logger.error(f"❌ خطأ في نقل الكلمات: {e}")
            self.target.rollback()
            raise

    def migrate_sources(self):
        """نقل المصادر (293 مصدر)"""
        logger.info("\n" + "=" * 70)
        logger.info("  📚 نقل المصادر (Sources)")
        logger.info("=" * 70)

        try:
            # القراءة من DB3 (Crystalline)
            cursor3 = self.db3.cursor()
            cursor3.execute("""
                SELECT
                    source_id,
                    title,
                    author,
                    year_hijri,
                    type,
                    language,
                    description
                FROM Sources
                ORDER BY source_id
            """)

            sources = []
            for row in cursor3.fetchall():
                source = {
                    'title': row['title'],
                    'author': row['author'],
                    'year_hijri': row['year_hijri'],
                    'source_type': row['type'],
                    'language': row['language'],
                    'description': row['description']
                }
                sources.append(source)

            # الإدخال في PostgreSQL
            insert_query = """
                INSERT INTO sources (
                    title, author, year_hijri,
                    source_type, language, description
                )
                VALUES (
                    %(title)s, %(author)s, %(year_hijri)s,
                    %(source_type)s, %(language)s, %(description)s
                )
                ON CONFLICT DO NOTHING
            """

            execute_batch(self.cursor, insert_query, sources, page_size=100)
            self.target.commit()

            logger.info(f"✅ تم نقل {len(sources)} مصدر")

        except Exception as e:
            logger.error(f"❌ خطأ في نقل المصادر: {e}")
            self.target.rollback()
            raise

    def run_migration(self):
        """تشغيل كل عمليات النقل"""
        start_time = datetime.now()

        logger.info("\n" + "═" * 70)
        logger.info("  بدء نقل البيانات - Quran Modern Stack Migration")
        logger.info("═" * 70)

        try:
            self.connect_all()

            # نقل البيانات الأساسية
            self.migrate_surahs()
            self.migrate_ayahs()
            self.migrate_roots()
            self.migrate_words()
            self.migrate_sources()

            # TODO: نقل باقي البيانات
            # self.migrate_tafseer()
            # self.migrate_translations()
            # self.migrate_irab()
            # self.migrate_sarf()
            # ... إلخ

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info("\n" + "═" * 70)
            logger.info(f"  ✅ تم النقل بنجاح في {duration:.2f} ثانية")
            logger.info("═" * 70)

        except Exception as e:
            logger.error(f"\n❌ فشل النقل: {e}")
            sys.exit(1)

        finally:
            # إغلاق كل الاتصالات
            if self.db1:
                self.db1.close()
            if self.db2:
                self.db2.close()
            if self.db3:
                self.db3.close()
            if self.target:
                self.target.close()

# ═══════════════════════════════════════════════════════════════════════════
# Main Entry Point
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    migration = QuranMigration()
    migration.run_migration()

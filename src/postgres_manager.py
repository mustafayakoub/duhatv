#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
📊 مدير قاعدة بيانات PostgreSQL - تطبيق القرآن الكريم Pro
═══════════════════════════════════════════════════════════════
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json

from config import *


class PostgresQuranDatabase:
    """مدير قاعدة بيانات PostgreSQL للقرآن الكريم"""

    def __init__(self, host='localhost', port=5432, database='quran_hierarchical_db',
                 user='postgres', password=''):
        """
        تهيئة الاتصال بقاعدة PostgreSQL

        Args:
            host: عنوان الخادم
            port: المنفذ
            database: اسم القاعدة
            user: اسم المستخدم
            password: كلمة المرور
        """
        self.config = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }

        try:
            self.conn = psycopg2.connect(**self.config)
            self.conn.set_client_encoding('UTF8')
            print(f"✅ تم الاتصال بـ PostgreSQL: {database}")
        except psycopg2.Error as e:
            raise ConnectionError(f"❌ فشل الاتصال بـ PostgreSQL: {e}")

    def cursor(self, dict_cursor=True):
        """إنشاء cursor"""
        if dict_cursor:
            return self.conn.cursor(cursor_factory=RealDictCursor)
        return self.conn.cursor()

    # ═══════════════════════════════════════════════════════════════
    # معلومات السور
    # ═══════════════════════════════════════════════════════════════

    def get_sura_info(self, sura_num: int) -> Dict[str, Any]:
        """الحصول على معلومات سورة"""
        query = """
        SELECT
            sur_id as sura,
            sur_name_ar as name,
            sur_name_en as name_english,
            sur_ayah_count as ayas_count,
            sur_revelation_type as revelation_type,
            sur_revelation_order
        FROM quran.surahs
        WHERE sur_id = %s
        """

        with self.cursor() as cur:
            cur.execute(query, (sura_num,))
            row = cur.fetchone()

            if row:
                info = dict(row)
                # تحويل نوع الوحي
                type_map = {
                    'meccan': 'مكية',
                    'medinan': 'مدنية'
                }
                info['type_full'] = type_map.get(info.get('revelation_type', 'meccan'), 'مكية')
                return info

        # إذا لم توجد
        return {
            'sura': sura_num,
            'name': f'السورة {sura_num}',
            'name_english': f'Sura {sura_num}',
            'ayas_count': 0,
            'type_full': 'مكية'
        }

    def get_sura_name(self, sura_num: int) -> str:
        """الحصول على اسم السورة"""
        info = self.get_sura_info(sura_num)
        return info['name']

    def get_all_suras(self) -> List[Dict[str, Any]]:
        """الحصول على كل السور"""
        query = """
        SELECT
            sur_id as sura,
            sur_name_ar as name,
            sur_name_en as name_english,
            sur_ayah_count as ayas_count,
            sur_revelation_type as revelation_type
        FROM quran.surahs
        ORDER BY sur_id
        """

        with self.cursor() as cur:
            cur.execute(query)
            return [dict(row) for row in cur.fetchall()]

    # ═══════════════════════════════════════════════════════════════
    # الآيات
    # ═══════════════════════════════════════════════════════════════

    def get_aya(self, sura: int, aya: int, rasm_type: str = 'uthmani') -> Optional[Dict[str, Any]]:
        """الحصول على آية واحدة"""
        # اختيار العمود المناسب حسب نوع الرسم
        text_column = 'aya_text_uthmani' if rasm_type == 'uthmani' else 'aya_text_simple'

        query = f"""
        SELECT
            aya_id,
            aya_sur_id as sura,
            aya_number as aya,
            {text_column} as text,
            aya_text_simple as text_simple,
            aya_juz as juz,
            aya_page as page,
            aya_hizb as hizb,
            aya_word_count
        FROM quran.ayahs
        WHERE aya_sur_id = %s AND aya_number = %s
        """

        with self.cursor() as cur:
            cur.execute(query, (sura, aya))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_sura_ayas(self, sura_num: int, rasm_type: str = 'uthmani') -> List[Dict[str, Any]]:
        """الحصول على كل آيات سورة"""
        text_column = 'aya_text_uthmani' if rasm_type == 'uthmani' else 'aya_text_simple'

        query = f"""
        SELECT
            aya_sur_id as sura,
            aya_number as aya,
            {text_column} as text,
            aya_juz as juz,
            aya_page as page
        FROM quran.ayahs
        WHERE aya_sur_id = %s
        ORDER BY aya_number
        """

        with self.cursor() as cur:
            cur.execute(query, (sura_num,))
            return [dict(row) for row in cur.fetchall()]

    def get_page_ayas(self, page_num: int, rasm_type: str = 'uthmani') -> List[Dict[str, Any]]:
        """الحصول على آيات صفحة"""
        text_column = 'aya_text_uthmani' if rasm_type == 'uthmani' else 'aya_text_simple'

        query = f"""
        SELECT
            aya_sur_id as sura,
            aya_number as aya,
            {text_column} as text,
            aya_juz as juz,
            aya_page as page
        FROM quran.ayahs
        WHERE aya_page = %s
        ORDER BY aya_global_id
        """

        with self.cursor() as cur:
            cur.execute(query, (page_num,))
            return [dict(row) for row in cur.fetchall()]

    def get_juz_ayas(self, juz_num: int, rasm_type: str = 'uthmani') -> List[Dict[str, Any]]:
        """الحصول على آيات جزء"""
        text_column = 'aya_text_uthmani' if rasm_type == 'uthmani' else 'aya_text_simple'

        query = f"""
        SELECT
            aya_sur_id as sura,
            aya_number as aya,
            {text_column} as text,
            aya_juz as juz,
            aya_page as page
        FROM quran.ayahs
        WHERE aya_juz = %s
        ORDER BY aya_global_id
        """

        with self.cursor() as cur:
            cur.execute(query, (juz_num,))
            return [dict(row) for row in cur.fetchall()]

    # ═══════════════════════════════════════════════════════════════
    # البحث
    # ═══════════════════════════════════════════════════════════════

    def search_text(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """البحث في نص القرآن"""
        query = """
        SELECT
            aya_sur_id as sura,
            aya_number as aya,
            aya_text_simple as text,
            aya_page as page,
            aya_juz as juz,
            ts_rank(aya_text_search, query) as rank
        FROM quran.ayahs,
             to_tsquery('arabic', %s) query
        WHERE aya_text_search @@ query
        ORDER BY rank DESC, aya_global_id
        LIMIT %s
        """

        # تجهيز نص البحث للـ tsquery
        search_query = ' | '.join(search_term.split())

        with self.cursor() as cur:
            try:
                cur.execute(query, (search_query, limit))
                return [dict(row) for row in cur.fetchall()]
            except psycopg2.Error:
                # إذا فشل البحث المتقدم، نستخدم LIKE
                return self.search_text_simple(search_term, limit)

    def search_text_simple(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """بحث بسيط باستخدام LIKE"""
        query = """
        SELECT
            aya_sur_id as sura,
            aya_number as aya,
            aya_text_simple as text,
            aya_page as page,
            aya_juz as juz
        FROM quran.ayahs
        WHERE aya_text_simple LIKE %s
        ORDER BY aya_global_id
        LIMIT %s
        """

        with self.cursor() as cur:
            cur.execute(query, (f'%{search_term}%', limit))
            return [dict(row) for row in cur.fetchall()]

    # ═══════════════════════════════════════════════════════════════
    # إحصائيات
    # ═══════════════════════════════════════════════════════════════

    def get_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات القاعدة"""
        stats = {}

        with self.cursor() as cur:
            # عدد السور
            cur.execute("SELECT COUNT(*) as count FROM quran.surahs")
            stats['total_suras'] = cur.fetchone()['count']

            # عدد الآيات
            cur.execute("SELECT COUNT(*) as count FROM quran.ayahs")
            stats['total_ayahs'] = cur.fetchone()['count']

            # عدد الكلمات
            cur.execute("SELECT COUNT(*) as count FROM quran.words")
            stats['total_words'] = cur.fetchone()['count']

        return stats

    def get_database_info(self) -> Dict[str, Any]:
        """معلومات عن قاعدة البيانات"""
        info = {
            'type': 'PostgreSQL',
            'database': self.config['database'],
            'host': self.config['host'],
            'version': None
        }

        with self.cursor() as cur:
            # إصدار PostgreSQL
            cur.execute("SELECT version()")
            version = cur.fetchone()['version']
            info['version'] = version.split(',')[0]

            # الامتدادات المفعلة
            cur.execute("SELECT extname FROM pg_extension ORDER BY extname")
            info['extensions'] = [row['extname'] for row in cur.fetchall()]

        return info

    # ═══════════════════════════════════════════════════════════════
    # إغلاق الاتصال
    # ═══════════════════════════════════════════════════════════════

    def close(self):
        """إغلاق الاتصال"""
        if self.conn:
            self.conn.close()
            print("✅ تم إغلاق الاتصال بـ PostgreSQL")

    def __del__(self):
        """تنظيف عند الحذف"""
        self.close()

    def __enter__(self):
        """دعم context manager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """إغلاق عند الخروج من context"""
        self.close()

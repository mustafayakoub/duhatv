#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
📊 مدير قاعدة البيانات - تطبيق القرآن الكريم Pro
═══════════════════════════════════════════════════════════════
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json

from config import *


class QuranDatabase:
    """مدير قاعدة بيانات القرآن الكريم"""

    def __init__(self, db_path: Path = None):
        """
        تهيئة الاتصال بقاعدة البيانات

        Args:
            db_path: مسار قاعدة البيانات (اختياري)
        """
        self.db_path = db_path or DB_PATH

        if not self.db_path.exists():
            raise FileNotFoundError(
                f"❌ قاعدة البيانات غير موجودة: {self.db_path}\n"
                f"الرجاء وضع الملف quran_ultimate_final.db في مجلد data"
            )

        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row  # للوصول للأعمدة بالاسم
        self.cursor = self.conn.cursor()

        print(f"✅ تم الاتصال بقاعدة البيانات: {self.db_path.name}")

        # كشف البنية
        self.detect_schema()

    def detect_schema(self):
        """كشف بنية قاعدة البيانات تلقائياً"""
        # قراءة أسماء الجداول
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        self.tables = [row[0] for row in self.cursor.fetchall()]
        print(f"📊 عدد الجداول: {len(self.tables)}")

        # قراءة أسماء الأعمدة في جدول القرآن
        self.cursor.execute("PRAGMA table_info(quran)")
        self.quran_columns = {row[1]: row[2] for row in self.cursor.fetchall()}
        print(f"📋 أعمدة جدول القرآن: {list(self.quran_columns.keys())}")

    # ═══════════════════════════════════════════════════════════════
    # معلومات السور
    # ═══════════════════════════════════════════════════════════════

    def get_sura_info(self, sura_num: int) -> Dict[str, Any]:
        """الحصول على معلومات سورة"""
        query = """
        SELECT
            sura,
            name_arabic as name,
            name_english,
            name_transliteration,
            revelation_type,
            revelation_place,
            ayas_count
        FROM suras
        WHERE sura = ?
        """

        self.cursor.execute(query, (sura_num,))
        row = self.cursor.fetchone()

        if row:
            info = dict(row)
            # نوع السورة
            type_map = {
                'meccan': 'مكية',
                'medinan': 'مدنية',
                'Meccan': 'مكية',
                'Medinan': 'مدنية'
            }
            info['type_full'] = type_map.get(info.get('revelation_type', ''), 'مكية')
            return info

        # إذا لم توجد، نستخدم معلومات افتراضية
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
        query = "SELECT * FROM suras ORDER BY sura"
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]

    # ═══════════════════════════════════════════════════════════════
    # الآيات
    # ═══════════════════════════════════════════════════════════════

    def get_aya(self, sura: int, aya: int, rasm_type: str = 'uthmani') -> Optional[Dict[str, Any]]:
        """الحصول على آية واحدة"""
        rasm_col = RASM_TYPES[rasm_type]['column']

        # البحث عن العمود المناسب
        if rasm_col not in self.quran_columns:
            # محاولة البحث عن أعمدة بديلة
            alternatives = {
                'text_uthmani': ['text', 'aya_text', 'aya_text_uthmani'],
                'text_simple': ['text_imlaei', 'text', 'simple'],
                'text_simple_clean': ['text_simple', 'text'],
                'text_imlaei': ['text_simple', 'text']
            }

            for alt_col in alternatives.get(rasm_col, ['text']):
                if alt_col in self.quran_columns:
                    rasm_col = alt_col
                    break

        query = f"""
        SELECT
            sura, aya, {rasm_col} as text,
            juz, page, manzil, ruku, hizb_quarter
        FROM quran
        WHERE sura = ? AND aya = ?
        """

        self.cursor.execute(query, (sura, aya))
        row = self.cursor.fetchone()

        return dict(row) if row else None

    def get_sura_ayas(self, sura: int, rasm_type: str = 'uthmani') -> List[Dict[str, Any]]:
        """الحصول على كل آيات سورة"""
        rasm_col = RASM_TYPES[rasm_type]['column']

        # البحث عن العمود المناسب
        if rasm_col not in self.quran_columns:
            alternatives = {
                'text_uthmani': ['text', 'aya_text', 'aya_text_uthmani'],
                'text_simple': ['text_imlaei', 'text', 'simple'],
                'text_simple_clean': ['text_simple', 'text'],
                'text_imlaei': ['text_simple', 'text']
            }

            for alt_col in alternatives.get(rasm_col, ['text']):
                if alt_col in self.quran_columns:
                    rasm_col = alt_col
                    break

        query = f"""
        SELECT
            sura, aya, {rasm_col} as text,
            juz, page, manzil, ruku, hizb_quarter
        FROM quran
        WHERE sura = ?
        ORDER BY aya
        """

        self.cursor.execute(query, (sura,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_suras_in_juz(self, juz: int) -> List[Dict[str, Any]]:
        """الحصول على السور في جزء معين"""
        query = """
        SELECT DISTINCT sura
        FROM quran
        WHERE juz = ?
        ORDER BY sura
        """

        self.cursor.execute(query, (juz,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_page_ayas(self, page: int) -> List[Dict[str, Any]]:
        """الحصول على آيات صفحة معينة"""
        query = """
        SELECT sura, aya
        FROM quran
        WHERE page = ?
        ORDER BY sura, aya
        """

        self.cursor.execute(query, (page,))
        return [dict(row) for row in self.cursor.fetchall()]

    # ═══════════════════════════════════════════════════════════════
    # التفاسير
    # ═══════════════════════════════════════════════════════════════

    def get_tafsir_muyassar(self, sura: int) -> List[Dict[str, Any]]:
        """تفسير ميسر"""
        return self._get_tafsir('tafsir_muyassar', sura)

    def get_tafsir_jalalayn(self, sura: int) -> List[Dict[str, Any]]:
        """تفسير الجلالين"""
        return self._get_tafsir('tafsir_jalalayn', sura)

    def get_historical_all_sura(self, sura: int) -> List[Dict[str, Any]]:
        """التفاسير التاريخية (الطبري وغيره)"""
        if 'tafsir_tabari' in self.tables:
            return self._get_tafsir('tafsir_tabari', sura)
        elif 'historical_tafsirs' in self.tables:
            query = """
            SELECT sura, aya, text, source
            FROM historical_tafsirs
            WHERE sura = ?
            ORDER BY aya
            """
            self.cursor.execute(query, (sura,))
            return [dict(row) for row in self.cursor.fetchall()]
        return []

    def _get_tafsir(self, table_name: str, sura: int) -> List[Dict[str, Any]]:
        """دالة عامة للحصول على التفسير"""
        if table_name not in self.tables:
            return []

        query = f"""
        SELECT sura, aya, text
        FROM {table_name}
        WHERE sura = ?
        ORDER BY aya
        """

        self.cursor.execute(query, (sura,))
        return [dict(row) for row in self.cursor.fetchall()]

    # ═══════════════════════════════════════════════════════════════
    # الترجمات
    # ═══════════════════════════════════════════════════════════════

    def get_available_languages(self) -> List[Tuple[str, str]]:
        """الحصول على اللغات المتاحة"""
        if 'translations' not in self.tables:
            return []

        query = """
        SELECT DISTINCT language, language_name
        FROM translations
        ORDER BY language_name
        """

        try:
            self.cursor.execute(query)
            return [(row[0], row[1]) for row in self.cursor.fetchall()]
        except:
            # في حالة عدم وجود عمود language_name
            query = "SELECT DISTINCT language FROM translations"
            self.cursor.execute(query)
            return [(row[0], row[0].title()) for row in self.cursor.fetchall()]

    def get_sura_translations(self, sura: int, language: str) -> List[Dict[str, Any]]:
        """الحصول على ترجمة سورة"""
        if 'translations' not in self.tables:
            return []

        query = """
        SELECT sura, aya, text
        FROM translations
        WHERE sura = ? AND language = ?
        ORDER BY aya
        """

        self.cursor.execute(query, (sura, language))
        return [dict(row) for row in self.cursor.fetchall()]

    # ═══════════════════════════════════════════════════════════════
    # البحث
    # ═══════════════════════════════════════════════════════════════

    def search_text(self, query: str, places: List[str]) -> List[Dict[str, Any]]:
        """بحث نصي"""
        results = []
        search_pattern = f"%{query}%"

        # البحث في القرآن
        if 'quran' in places:
            sql = """
            SELECT
                q.sura, q.aya, q.text,
                s.name_arabic as sura_name,
                'quran' as source
            FROM quran q
            JOIN suras s ON q.sura = s.sura
            WHERE q.text LIKE ?
            ORDER BY q.sura, q.aya
            LIMIT ?
            """

            self.cursor.execute(sql, (search_pattern, SEARCH_SETTINGS['max_results']))
            results.extend([dict(row) for row in self.cursor.fetchall()])

        # البحث في التفاسير
        if 'tafsir' in places:
            for table in ['tafsir_muyassar', 'tafsir_jalalayn', 'tafsir_tabari']:
                if table in self.tables:
                    sql = f"""
                    SELECT
                        t.sura, t.aya, t.text,
                        s.name_arabic as sura_name,
                        'tafsir' as source
                    FROM {table} t
                    JOIN suras s ON t.sura = s.sura
                    WHERE t.text LIKE ?
                    ORDER BY t.sura, t.aya
                    LIMIT ?
                    """

                    self.cursor.execute(sql, (search_pattern, SEARCH_SETTINGS['max_results'] // 3))
                    results.extend([dict(row) for row in self.cursor.fetchall()])

        # البحث في الترجمات
        if 'translation' in places and 'translations' in self.tables:
            sql = """
            SELECT
                t.sura, t.aya, t.text,
                s.name_arabic as sura_name,
                'translation' as source
            FROM translations t
            JOIN suras s ON t.sura = s.sura
            WHERE t.text LIKE ?
            ORDER BY t.sura, t.aya
            LIMIT ?
            """

            self.cursor.execute(sql, (search_pattern, SEARCH_SETTINGS['max_results']))
            results.extend([dict(row) for row in self.cursor.fetchall()])

        return results[:SEARCH_SETTINGS['max_results']]

    def search_by_root(self, root: str, places: List[str]) -> List[Dict[str, Any]]:
        """البحث بالجذر"""
        if 'morphology' not in self.tables:
            # إذا لم يكن هناك جدول morphology، نستخدم البحث النصي
            return self.search_text(root, places)

        query = """
        SELECT
            q.sura, q.aya, q.text,
            s.name_arabic as sura_name,
            m.root,
            'root' as source
        FROM morphology m
        JOIN quran q ON m.sura = q.sura AND m.aya = q.aya
        JOIN suras s ON q.sura = s.sura
        WHERE m.root = ?
        ORDER BY q.sura, q.aya
        LIMIT ?
        """

        self.cursor.execute(query, (root, SEARCH_SETTINGS['max_results']))
        return [dict(row) for row in self.cursor.fetchall()]

    def search_by_pattern(self, pattern: str, places: List[str]) -> List[Dict[str, Any]]:
        """البحث بالنمط الصرفي"""
        if 'morphology' not in self.tables:
            return self.search_text(pattern, places)

        query = """
        SELECT
            q.sura, q.aya, q.text,
            s.name_arabic as sura_name,
            m.pattern,
            'pattern' as source
        FROM morphology m
        JOIN quran q ON m.sura = q.sura AND m.aya = q.aya
        JOIN suras s ON q.sura = s.sura
        WHERE m.pattern LIKE ?
        ORDER BY q.sura, q.aya
        LIMIT ?
        """

        self.cursor.execute(query, (f"%{pattern}%", SEARCH_SETTINGS['max_results']))
        return [dict(row) for row in self.cursor.fetchall()]

    def search_by_topic(self, topic: str, places: List[str]) -> List[Dict[str, Any]]:
        """البحث بالموضوع"""
        if 'topics' not in self.tables:
            return self.search_text(topic, places)

        query = """
        SELECT
            q.sura, q.aya, q.text,
            s.name_arabic as sura_name,
            t.topic_name,
            'topic' as source
        FROM topics t
        JOIN quran q ON t.sura = q.sura AND t.aya = q.aya
        JOIN suras s ON q.sura = s.sura
        WHERE t.topic_name LIKE ?
        ORDER BY q.sura, q.aya
        LIMIT ?
        """

        self.cursor.execute(query, (f"%{topic}%", SEARCH_SETTINGS['max_results']))
        return [dict(row) for row in self.cursor.fetchall()]

    # ═══════════════════════════════════════════════════════════════
    # علوم القرآن
    # ═══════════════════════════════════════════════════════════════

    def get_sajda_ayas(self) -> List[Dict[str, Any]]:
        """الحصول على آيات السجدة"""
        if 'sajdas' in self.tables:
            query = """
            SELECT
                s.sura, s.aya, s.type,
                su.name_arabic as sura_name,
                q.text
            FROM sajdas s
            JOIN suras su ON s.sura = su.sura
            JOIN quran q ON s.sura = q.sura AND s.aya = q.aya
            ORDER BY s.sura, s.aya
            """

            self.cursor.execute(query)
            return [dict(row) for row in self.cursor.fetchall()]

        return []

    def get_statistics(self) -> Dict[str, Any]:
        """إحصائيات عامة"""
        stats = {}

        # عدد السور
        self.cursor.execute("SELECT COUNT(*) FROM suras")
        stats['suras_count'] = self.cursor.fetchone()[0]

        # عدد الآيات
        self.cursor.execute("SELECT COUNT(*) FROM quran")
        stats['ayas_count'] = self.cursor.fetchone()[0]

        # عدد الأجزاء
        self.cursor.execute("SELECT MAX(juz) FROM quran")
        stats['juz_count'] = self.cursor.fetchone()[0]

        # عدد الصفحات
        self.cursor.execute("SELECT MAX(page) FROM quran")
        stats['pages_count'] = self.cursor.fetchone()[0]

        return stats

    # ═══════════════════════════════════════════════════════════════
    # العلامات المرجعية
    # ═══════════════════════════════════════════════════════════════

    def add_bookmark(self, sura: int, aya: int, note: str = ""):
        """إضافة علامة مرجعية"""
        # التحقق من وجود جدول العلامات
        if 'bookmarks' not in self.tables:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sura INTEGER NOT NULL,
                aya INTEGER NOT NULL,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(sura, aya)
            )
            """)
            self.tables.append('bookmarks')

        query = """
        INSERT OR REPLACE INTO bookmarks (sura, aya, note, created_at)
        VALUES (?, ?, ?, ?)
        """

        self.cursor.execute(query, (sura, aya, note, datetime.now()))
        self.conn.commit()

    def get_bookmarks(self) -> List[Dict[str, Any]]:
        """الحصول على العلامات المرجعية"""
        if 'bookmarks' not in self.tables:
            return []

        query = """
        SELECT
            b.id, b.sura, b.aya, b.note, b.created_at,
            s.name_arabic as sura_name
        FROM bookmarks b
        JOIN suras s ON b.sura = s.sura
        ORDER BY b.created_at DESC
        """

        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]

    def remove_bookmark(self, bookmark_id: int):
        """حذف علامة مرجعية"""
        if 'bookmarks' in self.tables:
            self.cursor.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
            self.conn.commit()

    # ═══════════════════════════════════════════════════════════════
    # إدارة الاتصال
    # ═══════════════════════════════════════════════════════════════

    def close(self):
        """إغلاق الاتصال"""
        if self.conn:
            self.conn.close()
            print("✅ تم إغلاق الاتصال بقاعدة البيانات")

    def __del__(self):
        """التنظيف عند الحذف"""
        self.close()

    def __enter__(self):
        """دعم context manager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """إغلاق عند الخروج"""
        self.close()


# ═══════════════════════════════════════════════════════════════
# نهاية الملف
# ═══════════════════════════════════════════════════════════════

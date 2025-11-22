"""
🗄️ محرك قاعدة البيانات العصبية - دُحى TV
===========================================
نظام إدارة قاعدة البيانات مع دعم:
- البحث الفوري FTS5
- الربط العصبي
- التخزين المؤقت الذكي
- الأداء العالي
"""

import sqlite3
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from functools import lru_cache
from contextlib import contextmanager
import threading


class NeuralDatabase:
    """محرك قاعدة البيانات العصبية"""

    def __init__(self, db_path: str = "data/duhatv.db"):
        """
        تهيئة قاعدة البيانات

        Args:
            db_path: مسار ملف قاعدة البيانات
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Thread-local storage للاتصالات
        self._local = threading.local()

        # إنشاء قاعدة البيانات
        self._initialize_database()

        # إحصائيات الأداء
        self.stats = {
            'queries': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'avg_query_time': 0.0
        }

    @property
    def connection(self) -> sqlite3.Connection:
        """الحصول على اتصال خاص بالـ thread الحالي"""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = self._create_connection()
        return self._local.conn

    def _create_connection(self) -> sqlite3.Connection:
        """إنشاء اتصال جديد بقاعدة البيانات"""
        conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=30.0
        )
        conn.row_factory = sqlite3.Row

        # تحسينات الأداء
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute("PRAGMA temp_store = MEMORY")
        conn.execute("PRAGMA cache_size = -64000")  # 64MB

        return conn

    @contextmanager
    def transaction(self):
        """Context manager للمعاملات"""
        conn = self.connection
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

    def _initialize_database(self):
        """تهيئة قاعدة البيانات بإنشاء الجداول"""
        schema_path = Path(__file__).parent.parent.parent / "database" / "smart_search_schema.sql"

        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = f.read()

            with self.transaction() as conn:
                conn.executescript(schema)
            print("✅ تم تهيئة قاعدة البيانات بنجاح")
        else:
            print("⚠️ ملف المخطط غير موجود، إنشاء جداول أساسية...")
            self._create_basic_tables()

    def _create_basic_tables(self):
        """إنشاء الجداول الأساسية"""
        with self.transaction() as conn:
            # جدول السور
            conn.execute("""
                CREATE TABLE IF NOT EXISTS surahs (
                    surah_id INTEGER PRIMARY KEY,
                    surah_name_arabic TEXT NOT NULL,
                    verses_count INTEGER NOT NULL,
                    revelation_type TEXT
                )
            """)

            # جدول الآيات
            conn.execute("""
                CREATE TABLE IF NOT EXISTS verses (
                    verse_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surah_id INTEGER NOT NULL,
                    verse_number INTEGER NOT NULL,
                    text_othmani TEXT NOT NULL,
                    text_simplified TEXT,
                    FOREIGN KEY (surah_id) REFERENCES surahs(surah_id)
                )
            """)

    # =====================================================
    # 🔍 وظائف البحث الذكي
    # =====================================================

    def search_quran(
        self,
        query: str,
        limit: int = 100,
        use_fts: bool = True
    ) -> List[Dict[str, Any]]:
        """
        البحث في القرآن الكريم

        Args:
            query: نص البحث
            limit: عدد النتائج
            use_fts: استخدام FTS5 للبحث السريع

        Returns:
            قائمة الآيات المطابقة
        """
        start_time = time.time()

        if use_fts:
            results = self._search_quran_fts(query, limit)
        else:
            results = self._search_quran_like(query, limit)

        # تحديث الإحصائيات
        elapsed = time.time() - start_time
        self._update_stats(elapsed)

        return results

    def _search_quran_fts(self, query: str, limit: int) -> List[Dict]:
        """البحث باستخدام FTS5"""
        # إزالة التشكيل من الاستعلام
        query_clean = self._remove_tashkeel(query)

        sql = """
            SELECT
                v.verse_id,
                v.surah_id,
                v.verse_number,
                v.page_number,
                v.juz_number,
                v.text_othmani,
                v.text_simplified,
                s.surah_name_arabic,
                s.revelation_type,
                fts.rank
            FROM quran_fts fts
            JOIN verses v ON fts.verse_id = v.verse_id
            JOIN surahs s ON v.surah_id = s.surah_id
            WHERE quran_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """

        cursor = self.connection.execute(sql, (query_clean, limit))
        return [dict(row) for row in cursor.fetchall()]

    def _search_quran_like(self, query: str, limit: int) -> List[Dict]:
        """البحث باستخدام LIKE"""
        sql = """
            SELECT
                v.verse_id,
                v.surah_id,
                v.verse_number,
                v.text_othmani,
                s.surah_name_arabic
            FROM verses v
            JOIN surahs s ON v.surah_id = s.surah_id
            WHERE v.text_simplified LIKE ?
            LIMIT ?
        """

        cursor = self.connection.execute(sql, (f"%{query}%", limit))
        return [dict(row) for row in cursor.fetchall()]

    def search_words(
        self,
        query: str,
        search_type: str = "text",
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        البحث في الكلمات

        Args:
            query: نص البحث
            search_type: نوع البحث (text, root, stem)
            limit: عدد النتائج
        """
        if search_type == "root":
            column = "root"
        elif search_type == "stem":
            column = "stem"
        else:
            column = "word_no_tashkeel"

        sql = f"""
            SELECT
                w.word_id,
                w.verse_id,
                w.word_text,
                w.root,
                w.stem,
                w.grammar_type,
                v.surah_id,
                v.verse_number,
                v.text_othmani
            FROM words w
            JOIN verses v ON w.verse_id = v.verse_id
            WHERE w.{column} LIKE ?
            LIMIT ?
        """

        cursor = self.connection.execute(sql, (f"%{query}%", limit))
        return [dict(row) for row in cursor.fetchall()]

    def search_tafseer(
        self,
        query: str,
        book_ids: Optional[List[int]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        البحث في التفاسير

        Args:
            query: نص البحث
            book_ids: أرقام الكتب المحددة (None = كل الكتب)
            limit: عدد النتائج
        """
        if book_ids:
            book_filter = f"AND t.book_id IN ({','.join(map(str, book_ids))})"
        else:
            book_filter = ""

        sql = f"""
            SELECT
                t.tafseer_id,
                t.book_id,
                t.verse_id,
                t.tafseer_text,
                b.book_name_arabic,
                b.author_name,
                v.surah_id,
                v.verse_number,
                v.text_othmani
            FROM tafseer_fts fts
            JOIN tafseer_texts t ON fts.tafseer_id = t.tafseer_id
            JOIN tafseer_books b ON t.book_id = b.book_id
            JOIN verses v ON t.verse_id = v.verse_id
            WHERE tafseer_fts MATCH ?
            {book_filter}
            ORDER BY fts.rank
            LIMIT ?
        """

        cursor = self.connection.execute(sql, (query, limit))
        return [dict(row) for row in cursor.fetchall()]

    def search_topics(
        self,
        query: str,
        level: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        البحث في الموضوعات

        Args:
            query: نص البحث
            level: المستوى (1,2,3,4) أو None لكل المستويات
        """
        level_filter = f"AND level = {level}" if level else ""

        sql = f"""
            SELECT
                t.topic_id,
                t.topic_name,
                t.parent_id,
                t.level,
                t.description,
                fts.rank
            FROM topics_fts fts
            JOIN topics t ON fts.topic_id = t.topic_id
            WHERE topics_fts MATCH ?
            {level_filter}
            ORDER BY fts.rank
        """

        cursor = self.connection.execute(sql, (query,))
        return [dict(row) for row in cursor.fetchall()]

    def search_all(
        self,
        query: str,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        البحث الشامل في كل شيء

        Args:
            query: نص البحث
            filters: فلاتر إضافية

        Returns:
            قاموس يحتوي على نتائج من كل المصادر
        """
        results = {
            'quran': [],
            'words': [],
            'tafseer': [],
            'topics': [],
            'translations': [],
            'total': 0
        }

        # البحث في القرآن
        if not filters or filters.get('quran', True):
            results['quran'] = self.search_quran(query, limit=50)

        # البحث في الكلمات
        if not filters or filters.get('words', True):
            results['words'] = self.search_words(query, limit=50)

        # البحث في التفاسير
        if not filters or filters.get('tafseer', True):
            book_ids = filters.get('tafseer_books') if filters else None
            results['tafseer'] = self.search_tafseer(query, book_ids, limit=50)

        # البحث في الموضوعات
        if not filters or filters.get('topics', True):
            results['topics'] = self.search_topics(query)

        # حساب الإجمالي
        results['total'] = sum(len(v) for k, v in results.items() if k != 'total')

        return results

    # =====================================================
    # 🔗 وظائف الربط العصبي
    # =====================================================

    def get_neural_links(
        self,
        source_type: str,
        source_id: int,
        target_type: Optional[str] = None,
        relation_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        جلب الروابط العصبية

        Args:
            source_type: نوع المصدر (verse, word, topic)
            source_id: رقم المصدر
            target_type: نوع الهدف (اختياري)
            relation_type: نوع العلاقة (اختياري)
            limit: عدد النتائج
        """
        filters = ["source_type = ?", "source_id = ?"]
        params = [source_type, source_id]

        if target_type:
            filters.append("target_type = ?")
            params.append(target_type)

        if relation_type:
            filters.append("relation_type = ?")
            params.append(relation_type)

        params.append(limit)

        sql = f"""
            SELECT *
            FROM neural_links
            WHERE {' AND '.join(filters)}
            ORDER BY weight DESC
            LIMIT ?
        """

        cursor = self.connection.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def add_neural_link(
        self,
        source_type: str,
        source_id: int,
        target_type: str,
        target_id: int,
        relation_type: str,
        weight: float = 1.0,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        إضافة رابط عصبي جديد

        Returns:
            رقم الرابط الجديد
        """
        metadata_json = json.dumps(metadata) if metadata else None

        sql = """
            INSERT OR REPLACE INTO neural_links
            (source_type, source_id, target_type, target_id, relation_type, weight, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        with self.transaction() as conn:
            cursor = conn.execute(
                sql,
                (source_type, source_id, target_type, target_id, relation_type, weight, metadata_json)
            )
            return cursor.lastrowid

    def get_linked_data(self, verse_id: int) -> Dict[str, Any]:
        """
        جلب كل البيانات المرتبطة بآية معينة

        Args:
            verse_id: رقم الآية

        Returns:
            قاموس يحتوي على كل البيانات المرتبطة
        """
        return {
            'verse': self.get_verse(verse_id),
            'words': self.get_verse_words(verse_id),
            'tafseer': self.get_verse_tafseer(verse_id),
            'translations': self.get_verse_translations(verse_id),
            'topics': self.get_verse_topics(verse_id),
            'related_verses': self.get_related_verses(verse_id),
            'sciences': self.get_verse_sciences(verse_id)
        }

    # =====================================================
    # 📖 وظائف الاستعلام الأساسية
    # =====================================================

    @lru_cache(maxsize=500)
    def get_verse(self, verse_id: int) -> Optional[Dict[str, Any]]:
        """جلب آية بالرقم"""
        sql = """
            SELECT
                v.*,
                s.surah_name_arabic,
                s.revelation_type,
                s.verses_count
            FROM verses v
            JOIN surahs s ON v.surah_id = s.surah_id
            WHERE v.verse_id = ?
        """

        cursor = self.connection.execute(sql, (verse_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    @lru_cache(maxsize=200)
    def get_surah(self, surah_id: int) -> Optional[Dict[str, Any]]:
        """جلب سورة بالرقم"""
        sql = "SELECT * FROM surahs WHERE surah_id = ?"
        cursor = self.connection.execute(sql, (surah_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_surah_verses(
        self,
        surah_id: int,
        verse_start: int = 1,
        verse_end: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """جلب آيات سورة"""
        if verse_end:
            where = "surah_id = ? AND verse_number BETWEEN ? AND ?"
            params = (surah_id, verse_start, verse_end)
        else:
            where = "surah_id = ? AND verse_number >= ?"
            params = (surah_id, verse_start)

        sql = f"""
            SELECT * FROM verses
            WHERE {where}
            ORDER BY verse_number
        """

        cursor = self.connection.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_verse_words(self, verse_id: int) -> List[Dict[str, Any]]:
        """جلب كلمات آية"""
        sql = """
            SELECT * FROM words
            WHERE verse_id = ?
            ORDER BY word_position
        """

        cursor = self.connection.execute(sql, (verse_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_verse_tafseer(
        self,
        verse_id: int,
        book_ids: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """جلب تفاسير آية"""
        if book_ids:
            book_filter = f"AND t.book_id IN ({','.join(map(str, book_ids))})"
        else:
            book_filter = ""

        sql = f"""
            SELECT
                t.*,
                b.book_name_arabic,
                b.author_name,
                b.category
            FROM tafseer_texts t
            JOIN tafseer_books b ON t.book_id = b.book_id
            WHERE t.verse_id = ?
            {book_filter}
        """

        cursor = self.connection.execute(sql, (verse_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_verse_translations(
        self,
        verse_id: int,
        language_codes: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """جلب ترجمات آية"""
        if language_codes:
            lang_filter = f"AND b.language_code IN ({','.join(repr(l) for l in language_codes)})"
        else:
            lang_filter = ""

        sql = f"""
            SELECT
                t.*,
                b.book_name,
                b.translator_name,
                b.language_code,
                b.language_name
            FROM translation_texts t
            JOIN translation_books b ON t.book_id = b.book_id
            WHERE t.verse_id = ?
            {lang_filter}
        """

        cursor = self.connection.execute(sql, (verse_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_verse_topics(self, verse_id: int) -> List[Dict[str, Any]]:
        """جلب موضوعات آية"""
        sql = """
            SELECT
                t.*,
                vt.relevance_score
            FROM verse_topics vt
            JOIN topics t ON vt.topic_id = t.topic_id
            WHERE vt.verse_id = ?
            ORDER BY vt.relevance_score DESC
        """

        cursor = self.connection.execute(sql, (verse_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_verse_sciences(self, verse_id: int) -> List[Dict[str, Any]]:
        """جلب علوم القرآن لآية"""
        sql = """
            SELECT * FROM quran_sciences
            WHERE verse_id = ?
        """

        cursor = self.connection.execute(sql, (verse_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_related_verses(self, verse_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """جلب الآيات المرتبطة"""
        sql = """
            SELECT
                v.*,
                nl.relation_type,
                nl.weight
            FROM neural_links nl
            JOIN verses v ON nl.target_id = v.verse_id
            WHERE nl.source_type = 'verse'
            AND nl.source_id = ?
            AND nl.target_type = 'verse'
            ORDER BY nl.weight DESC
            LIMIT ?
        """

        cursor = self.connection.execute(sql, (verse_id, limit))
        return [dict(row) for row in cursor.fetchall()]

    # =====================================================
    # 📚 وظائف الموضوعات
    # =====================================================

    def get_topics_tree(self, parent_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """جلب شجرة الموضوعات"""
        if parent_id is None:
            where = "parent_id IS NULL"
            params = ()
        else:
            where = "parent_id = ?"
            params = (parent_id,)

        sql = f"""
            SELECT * FROM topics
            WHERE {where}
            ORDER BY sort_order, topic_name
        """

        cursor = self.connection.execute(sql, params)
        topics = [dict(row) for row in cursor.fetchall()]

        # جلب الموضوعات الفرعية بشكل تكراري
        for topic in topics:
            topic['children'] = self.get_topics_tree(topic['topic_id'])

        return topics

    def get_topic_verses(self, topic_id: int) -> List[Dict[str, Any]]:
        """جلب آيات موضوع"""
        sql = """
            SELECT
                v.*,
                s.surah_name_arabic,
                vt.relevance_score
            FROM verse_topics vt
            JOIN verses v ON vt.verse_id = v.verse_id
            JOIN surahs s ON v.surah_id = s.surah_id
            WHERE vt.topic_id = ?
            ORDER BY v.surah_id, v.verse_number
        """

        cursor = self.connection.execute(sql, (topic_id,))
        return [dict(row) for row in cursor.fetchall()]

    # =====================================================
    # 📊 وظائف الإحصائيات
    # =====================================================

    def get_search_stats(self) -> Dict[str, Any]:
        """جلب إحصائيات البحث"""
        return self.stats.copy()

    def get_database_stats(self) -> Dict[str, Any]:
        """جلب إحصائيات قاعدة البيانات"""
        sql = """
            SELECT
                (SELECT COUNT(*) FROM surahs) as total_surahs,
                (SELECT COUNT(*) FROM verses) as total_verses,
                (SELECT COUNT(*) FROM words) as total_words,
                (SELECT COUNT(*) FROM tafseer_texts) as total_tafseer,
                (SELECT COUNT(*) FROM topics) as total_topics,
                (SELECT COUNT(*) FROM neural_links) as total_links
        """

        cursor = self.connection.execute(sql)
        row = cursor.fetchone()
        return dict(row) if row else {}

    def _update_stats(self, query_time: float):
        """تحديث الإحصائيات"""
        self.stats['queries'] += 1

        # حساب المتوسط المتحرك
        n = self.stats['queries']
        old_avg = self.stats['avg_query_time']
        self.stats['avg_query_time'] = (old_avg * (n - 1) + query_time) / n

    # =====================================================
    # 🛠️ وظائف مساعدة
    # =====================================================

    @staticmethod
    def _remove_tashkeel(text: str) -> str:
        """إزالة التشكيل من النص"""
        tashkeel = ['ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ّ', 'ْ', 'ٰ', 'ۡ', 'ۢ', 'ۣ']
        for mark in tashkeel:
            text = text.replace(mark, '')
        return text

    def close(self):
        """إغلاق الاتصالات"""
        if hasattr(self._local, 'conn') and self._local.conn:
            self._local.conn.close()
            self._local.conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# =====================================================
# 🧪 اختبار سريع
# =====================================================

if __name__ == "__main__":
    # إنشاء قاعدة البيانات
    db = NeuralDatabase("test_duhatv.db")

    print("✅ تم إنشاء قاعدة البيانات")

    # جلب الإحصائيات
    stats = db.get_database_stats()
    print(f"📊 إحصائيات قاعدة البيانات: {stats}")

    # إغلاق
    db.close()
    print("✅ تم الإغلاق بنجاح")

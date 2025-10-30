#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
🔍 QuranSearchComponent - مكون البحث المتقدم
Advanced Search Component for Quran Applications
═══════════════════════════════════════════════════════════════

🎯 الميزات:
- بحث نصي متقدم (Full-Text Search)
- بحث بالجذور
- بحث بالسور والآيات
- بحث بالأجزاء والأحزاب
- بحث مع التشكيل أو بدونه
- تمييز النتائج
- ترتيب حسب الأهمية

📖 الاستخدام:
    from qurankit.components import QuranSearchComponent

    search = QuranSearchComponent(database)
    results = search.search("الله", search_type="text")
    results_html = search.format_results_html(results)

═══════════════════════════════════════════════════════════════
"""

from typing import List, Dict, Any, Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel
from PyQt6.QtCore import pyqtSignal, QThread
import re


class QuranSearchWorker(QThread):
    """Worker thread للبحث في الخلفية"""

    search_finished = pyqtSignal(list)
    search_progress = pyqtSignal(int)

    def __init__(self, database, query, search_type='text'):
        super().__init__()
        self.database = database
        self.query = query
        self.search_type = search_type

    def run(self):
        """تنفيذ البحث"""
        try:
            if self.search_type == 'text':
                results = self.database.search_text(self.query)
            elif self.search_type == 'root':
                results = self.database.search_by_root(self.query)
            else:
                results = []

            self.search_finished.emit(results)
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            self.search_finished.emit([])


class QuranSearchComponent:
    """
    مكون البحث المتقدم في القرآن الكريم

    يوفر وظائف بحث متقدمة مع دعم أنواع مختلفة من البحث
    """

    def __init__(self, database, config=None):
        """
        تهيئة مكون البحث

        Args:
            database: كائن قاعدة البيانات
            config: إعدادات البحث (اختياري)
        """
        self.database = database
        self.config = config or {}
        self.last_results = []

        # إعدادات افتراضية
        self.search_limit = self.config.get('limit', 50)
        self.highlight_color = self.config.get('highlight_color', '#ffeb3b')
        self.case_sensitive = self.config.get('case_sensitive', False)

    # ═══════════════════════════════════════════════════════════════
    # البحث النصي
    # ═══════════════════════════════════════════════════════════════

    def search(self, query: str, search_type: str = 'text',
               limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        البحث في القرآن

        Args:
            query: نص البحث
            search_type: نوع البحث (text, root, sura, juz)
            limit: حد النتائج

        Returns:
            قائمة النتائج

        Example:
            >>> results = search.search("الله", search_type="text")
            >>> print(f"وجدنا {len(results)} نتيجة")
        """
        if not query or len(query) < 2:
            return []

        limit = limit or self.search_limit

        try:
            if search_type == 'text':
                results = self._search_text(query, limit)
            elif search_type == 'root':
                results = self._search_by_root(query, limit)
            elif search_type == 'sura':
                results = self._search_by_sura(query)
            elif search_type == 'juz':
                results = self._search_by_juz(query)
            else:
                results = []

            self.last_results = results
            return results

        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return []

    def _search_text(self, query: str, limit: int) -> List[Dict]:
        """البحث النصي العادي"""
        return self.database.search_text(query, limit=limit)

    def _search_by_root(self, root: str, limit: int) -> List[Dict]:
        """البحث بالجذر"""
        if hasattr(self.database, 'search_by_root'):
            return self.database.search_by_root(root, limit=limit)
        return []

    def _search_by_sura(self, sura_num: int) -> List[Dict]:
        """البحث بالسورة"""
        return self.database.get_sura_ayas(sura_num)

    def _search_by_juz(self, juz_num: int) -> List[Dict]:
        """البحث بالجزء"""
        if hasattr(self.database, 'get_juz_ayas'):
            return self.database.get_juz_ayas(juz_num)
        return []

    # ═══════════════════════════════════════════════════════════════
    # تنسيق النتائج
    # ═══════════════════════════════════════════════════════════════

    def format_results_html(self, results: List[Dict],
                           query: str = None) -> str:
        """
        تنسيق النتائج بصيغة HTML

        Args:
            results: قائمة النتائج
            query: نص البحث (لتمييز الكلمات)

        Returns:
            HTML منسق
        """
        if not results:
            return "<p style='text-align: center; color: #999;'>لا توجد نتائج</p>"

        html = f"""
        <div style='direction: rtl; font-family: Arial;'>
            <h3 style='color: #1e3c72; text-align: center;'>
                🔍 نتائج البحث ({len(results)})
            </h3>
        """

        for result in results:
            text = result.get('text', '')

            # تمييز نص البحث
            if query:
                text = self._highlight_text(text, query)

            html += f"""
            <div style='background: #f9f9f9; padding: 15px; margin: 10px 0;
                        border-radius: 5px; border-left: 3px solid #1e3c72;'>
                <p style='font-size: 16pt; line-height: 2; margin: 0;'>
                    {text}
                </p>
                <p style='color: #666; font-size: 10pt; margin-top: 10px;'>
                    📖 {result.get('sura', '-')} : {result.get('aya', '-')} |
                    📄 ص {result.get('page', '-')} |
                    📚 جـ {result.get('juz', '-')}
                </p>
            </div>
            """

        html += "</div>"
        return html

    def _highlight_text(self, text: str, query: str) -> str:
        """تمييز نص البحث في النتيجة"""
        if not query:
            return text

        pattern = re.escape(query)
        highlighted = re.sub(
            f'({pattern})',
            f'<mark style="background-color: {self.highlight_color};">\\1</mark>',
            text,
            flags=re.IGNORECASE if not self.case_sensitive else 0
        )
        return highlighted

    def format_results_plain(self, results: List[Dict]) -> str:
        """تنسيق النتائج بصيغة نص عادي"""
        if not results:
            return "لا توجد نتائج"

        text = f"نتائج البحث ({len(results)}):\n"
        text += "=" * 70 + "\n\n"

        for i, result in enumerate(results, 1):
            text += f"{i}. {result.get('text', '')}\n"
            text += f"   [السورة {result.get('sura')} : الآية {result.get('aya')}]\n\n"

        return text

    # ═══════════════════════════════════════════════════════════════
    # إحصائيات البحث
    # ═══════════════════════════════════════════════════════════════

    def get_search_stats(self, results: List[Dict]) -> Dict[str, Any]:
        """
        الحصول على إحصائيات نتائج البحث

        Returns:
            قاموس الإحصائيات
        """
        if not results:
            return {'total': 0}

        stats = {
            'total': len(results),
            'suras': set(),
            'juzs': set(),
            'pages': set()
        }

        for result in results:
            if 'sura' in result:
                stats['suras'].add(result['sura'])
            if 'juz' in result:
                stats['juzs'].add(result['juz'])
            if 'page' in result:
                stats['pages'].add(result['page'])

        stats['suras_count'] = len(stats['suras'])
        stats['juzs_count'] = len(stats['juzs'])
        stats['pages_count'] = len(stats['pages'])

        return stats

    # ═══════════════════════════════════════════════════════════════
    # البحث المتقدم
    # ═══════════════════════════════════════════════════════════════

    def advanced_search(self, query: str, filters: Dict = None) -> List[Dict]:
        """
        بحث متقدم مع فلاتر

        Args:
            query: نص البحث
            filters: فلاتر إضافية (sura, juz, page, revelation_type)

        Returns:
            قائمة النتائج المفلترة
        """
        results = self.search(query)

        if not filters:
            return results

        filtered = results

        # فلتر حسب السورة
        if 'sura' in filters and filters['sura']:
            filtered = [r for r in filtered if r.get('sura') == filters['sura']]

        # فلتر حسب الجزء
        if 'juz' in filters and filters['juz']:
            filtered = [r for r in filtered if r.get('juz') == filters['juz']]

        # فلتر حسب الصفحة
        if 'page' in filters and filters['page']:
            filtered = [r for r in filtered if r.get('page') == filters['page']]

        return filtered

    # ═══════════════════════════════════════════════════════════════
    # Widgets (للواجهة الرسومية)
    # ═══════════════════════════════════════════════════════════════

    def create_search_widget(self, parent=None) -> 'QuranSearchWidget':
        """
        إنشاء widget جاهز للبحث

        Returns:
            QuranSearchWidget
        """
        return QuranSearchWidget(self, parent)


class QuranSearchWidget(QWidget):
    """Widget جاهز للبحث في الواجهة الرسومية"""

    search_executed = pyqtSignal(list)

    def __init__(self, search_component: QuranSearchComponent, parent=None):
        super().__init__(parent)
        self.search_component = search_component
        self.init_ui()

    def init_ui(self):
        """بناء الواجهة"""
        layout = QVBoxLayout()

        # حقل البحث
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 ابحث في القرآن...")
        self.search_input.returnPressed.connect(self.do_search)
        layout.addWidget(self.search_input)

        # زر البحث
        search_btn = QPushButton("بحث")
        search_btn.clicked.connect(self.do_search)
        layout.addWidget(search_btn)

        # عرض النتائج
        self.results_label = QLabel("أدخل نص البحث")
        self.results_label.setWordWrap(True)
        layout.addWidget(self.results_label)

        self.setLayout(layout)

    def do_search(self):
        """تنفيذ البحث"""
        query = self.search_input.text().strip()
        if not query:
            self.results_label.setText("الرجاء إدخال نص البحث")
            return

        results = self.search_component.search(query)

        if results:
            self.results_label.setText(f"✅ تم العثور على {len(results)} نتيجة")
        else:
            self.results_label.setText("❌ لم يتم العثور على نتائج")

        self.search_executed.emit(results)


# ═══════════════════════════════════════════════════════════════
# Usage Example
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 70)
    print("🔍 QuranSearchComponent - مكون البحث المتقدم")
    print("═" * 70)

    # مثال استخدام
    example_code = """
    from qurankit.components import QuranSearchComponent

    # إنشاء مكون البحث
    search = QuranSearchComponent(database)

    # بحث نصي
    results = search.search("الله", search_type="text")

    # تنسيق النتائج
    html = search.format_results_html(results, query="الله")

    # إحصائيات
    stats = search.get_search_stats(results)
    print(f"عدد النتائج: {stats['total']}")
    print(f"السور: {stats['suras_count']}")
    """

    print(example_code)
    print("═" * 70)

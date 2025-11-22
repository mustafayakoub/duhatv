"""
🔍 محرك البحث الذكي الفوري - دُحى TV
=========================================
بحث فوري وذكي مع فلاتر ديناميكية متعددة المستويات
- بحث فوري بمجرد كتابة حرف (< 100ms)
- فلاتر قابلة للإضافة والإزالة
- autocomplete ذكي
- ربط عصبي للنتائج
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QScrollArea, QFrame,
    QCompleter, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QStringListModel, QThread, QObject
from PyQt6.QtGui import QFont, QColor
from typing import List, Dict, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import time


class FilterType(Enum):
    """أنواع الفلاتر"""
    SOURCE = "source"              # المصدر (قرآن، تفاسير...)
    RASM = "rasm"                  # الرسم
    TASHKEEL = "tashkeel"          # التشكيل
    GRAMMAR = "grammar"            # النحو
    BOOK = "book"                  # الكتاب
    SURAH = "surah"                # السورة
    JUZ = "juz"                    # الجزء
    PAGE = "page"                  # الصفحة
    TOPIC = "topic"                # الموضوع
    LANGUAGE = "language"          # اللغة


@dataclass
class SearchFilter:
    """فلتر بحث"""
    filter_id: str
    filter_type: FilterType
    filter_value: Any
    display_name: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'id': self.filter_id,
            'type': self.filter_type.value,
            'value': self.filter_value,
            'name': self.display_name
        }


class FilterChip(QWidget):
    """
    فلتر Chip قابل للإزالة
    مثل الموقع الباحث القرآني
    """
    removed = pyqtSignal(str)  # إشارة الإزالة

    def __init__(self, filter_obj: SearchFilter, parent=None):
        super().__init__(parent)

        self.filter_obj = filter_obj

        # التصميم
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

        # النص
        label = QLabel(filter_obj.display_name)
        label.setFont(QFont("Arial", 10))
        label.setStyleSheet("color: white;")

        # زر الإزالة
        remove_btn = QPushButton("×")
        remove_btn.setFixedSize(20, 20)
        remove_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        remove_btn.clicked.connect(self.on_remove)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.3);
                border: none;
                border-radius: 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.5);
            }
        """)

        layout.addWidget(label)
        layout.addWidget(remove_btn)

        # الستايل العام
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea,
                    stop:1 #764ba2
                );
                border-radius: 15px;
            }
        """)

    def on_remove(self):
        """معالج الإزالة"""
        self.removed.emit(self.filter_obj.filter_id)
        self.deleteLater()


class SearchWorker(QObject):
    """Worker للبحث في thread منفصل"""
    search_completed = pyqtSignal(dict)
    suggestions_ready = pyqtSignal(list)

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.current_query = ""
        self.current_filters = []

    def search(self, query: str, filters: List[SearchFilter]):
        """تنفيذ البحث"""
        self.current_query = query
        self.current_filters = filters

        start_time = time.time()

        # تحويل الفلاتر إلى قاموس
        filters_dict = self._filters_to_dict(filters)

        # البحث
        results = self.db.search_all(query, filters_dict)

        # حساب الوقت
        elapsed = time.time() - start_time
        results['search_time'] = elapsed

        # إرسال النتائج
        self.search_completed.emit(results)

    def get_suggestions(self, query: str):
        """جلب اقتراحات الإكمال التلقائي"""
        if len(query) < 1:
            return

        suggestions = []

        # البحث في الكلمات الشائعة
        try:
            # من جدول الكلمات
            cursor = self.db.connection.execute("""
                SELECT DISTINCT word_no_tashkeel
                FROM words
                WHERE word_no_tashkeel LIKE ?
                LIMIT 10
            """, (f"{query}%",))

            suggestions = [row[0] for row in cursor.fetchall()]

        except Exception as e:
            print(f"خطأ في جلب الاقتراحات: {e}")

        self.suggestions_ready.emit(suggestions)

    def _filters_to_dict(self, filters: List[SearchFilter]) -> Dict:
        """تحويل الفلاتر إلى قاموس"""
        filters_dict = {}

        for f in filters:
            if f.filter_type == FilterType.SOURCE:
                filters_dict[f.filter_value] = True

            elif f.filter_type == FilterType.BOOK:
                if 'tafseer_books' not in filters_dict:
                    filters_dict['tafseer_books'] = []
                filters_dict['tafseer_books'].append(f.filter_value)

            elif f.filter_type == FilterType.SURAH:
                filters_dict['surah_id'] = f.filter_value

            # يمكن إضافة المزيد من أنواع الفلاتر

        return filters_dict


class SmartSearchEngine(QWidget):
    """
    محرك البحث الذكي الفوري

    Features:
    - بحث فوري (live search)
    - autocomplete
    - فلاتر ديناميكية
    - نتائج فورية
    """

    # الإشارات
    search_triggered = pyqtSignal(str, list)  # (query, filters)
    results_ready = pyqtSignal(dict)          # النتائج
    filter_added = pyqtSignal(SearchFilter)   # فلتر مضاف
    filter_removed = pyqtSignal(str)          # فلتر محذوف

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)

        self.db = db_manager
        self.active_filters: List[SearchFilter] = []
        self.last_query = ""
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._perform_search)

        # Worker Thread
        self.search_thread = QThread()
        self.search_worker = SearchWorker(db_manager)
        self.search_worker.moveToThread(self.search_thread)
        self.search_worker.search_completed.connect(self._on_search_completed)
        self.search_worker.suggestions_ready.connect(self._on_suggestions_ready)
        self.search_thread.start()

        # إحصائيات
        self.stats = {
            'total_searches': 0,
            'avg_time': 0.0,
            'last_results_count': 0
        }

        # إعداد الواجهة
        self._setup_ui()

    def _setup_ui(self):
        """إعداد واجهة المستخدم"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # =====================================================
        # 1️⃣ صندوق البحث الرئيسي
        # =====================================================

        search_container = QFrame()
        search_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 5px;
            }
            QFrame:focus-within {
                border-color: #667eea;
            }
        """)

        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(15, 10, 15, 10)

        # أيقونة البحث
        search_icon = QLabel("🔍")
        search_icon.setFont(QFont("Arial", 16))

        # حقل البحث
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("أدخل كلمات البحث أو أضف قيداً...")
        self.search_input.setFont(QFont("Amiri", 14))
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: none;
                background: transparent;
                padding: 5px;
            }
        """)
        self.search_input.textChanged.connect(self._on_search_text_changed)

        # زر الفلتر
        self.filter_btn = QPushButton("🔽")
        self.filter_btn.setFixedSize(35, 35)
        self.filter_btn.setFont(QFont("Arial", 14))
        self.filter_btn.clicked.connect(self._toggle_filter_panel)
        self.filter_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: none;
                border-radius: 17px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)

        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(self.filter_btn)

        layout.addWidget(search_container)

        # =====================================================
        # 2️⃣ منطقة الفلاتر النشطة (Chips)
        # =====================================================

        self.filters_container = QWidget()
        filters_layout = QHBoxLayout(self.filters_container)
        filters_layout.setContentsMargins(5, 5, 5, 5)
        filters_layout.setSpacing(8)
        filters_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.filters_area = QScrollArea()
        self.filters_area.setWidget(self.filters_container)
        self.filters_area.setWidgetResizable(True)
        self.filters_area.setMaximumHeight(60)
        self.filters_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.filters_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlways)
        self.filters_area.setStyleSheet("""
            QScrollArea {
                background-color: #f9f9f9;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)
        self.filters_area.hide()  # مخفي في البداية

        layout.addWidget(self.filters_area)

        # =====================================================
        # 3️⃣ لوحة الفلاتر المنسدلة
        # =====================================================

        self.filter_panel = QFrame()
        self.filter_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.filter_panel.hide()

        filter_panel_layout = QVBoxLayout(self.filter_panel)

        # عنوان
        title = QLabel("الفلاتر")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        filter_panel_layout.addWidget(title)

        # أزرار الفلاتر السريعة
        quick_filters_layout = QHBoxLayout()

        # فلاتر المصدر
        self._add_quick_filter(quick_filters_layout, "القرآن", FilterType.SOURCE, "quran")
        self._add_quick_filter(quick_filters_layout, "التفاسير", FilterType.SOURCE, "tafseer")
        self._add_quick_filter(quick_filters_layout, "الترجمات", FilterType.SOURCE, "translations")
        self._add_quick_filter(quick_filters_layout, "الموضوعات", FilterType.SOURCE, "topics")

        filter_panel_layout.addLayout(quick_filters_layout)

        # فلاتر النحو
        grammar_layout = QHBoxLayout()
        grammar_label = QLabel("نوع الكلمة:")
        grammar_layout.addWidget(grammar_label)

        self._add_quick_filter(grammar_layout, "اسم", FilterType.GRAMMAR, "noun")
        self._add_quick_filter(grammar_layout, "فعل", FilterType.GRAMMAR, "verb")
        self._add_quick_filter(grammar_layout, "حرف", FilterType.GRAMMAR, "particle")

        filter_panel_layout.addLayout(grammar_layout)

        layout.addWidget(self.filter_panel)

        # =====================================================
        # 4️⃣ شريط الإحصائيات
        # =====================================================

        self.stats_label = QLabel("")
        self.stats_label.setFont(QFont("Arial", 9))
        self.stats_label.setStyleSheet("color: #6c757d; padding: 5px;")
        layout.addWidget(self.stats_label)

        # Completer للاقتراحات
        self.completer = QCompleter()
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.search_input.setCompleter(self.completer)

    def _add_quick_filter(
        self,
        layout: QHBoxLayout,
        text: str,
        filter_type: FilterType,
        value: Any
    ):
        """إضافة زر فلتر سريع"""
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setFont(QFont("Arial", 10))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
            QPushButton:checked {
                background-color: #667eea;
                color: white;
                border-color: #667eea;
            }
        """)
        btn.clicked.connect(
            lambda checked: self._on_quick_filter_clicked(text, filter_type, value, checked)
        )

        layout.addWidget(btn)

    # =====================================================
    # 🔍 معالجات البحث
    # =====================================================

    def _on_search_text_changed(self, text: str):
        """معالج تغيير نص البحث"""
        # تأخير البحث لـ 300ms (debounce)
        self.search_timer.stop()
        self.search_timer.start(300)

        # جلب الاقتراحات
        if len(text) >= 1:
            self.search_worker.get_suggestions(text)

    def _perform_search(self):
        """تنفيذ البحث"""
        query = self.search_input.text().strip()

        if len(query) < 1:
            return

        self.last_query = query
        self.stats['total_searches'] += 1

        # إرسال إشارة
        self.search_triggered.emit(query, self.active_filters)

        # البحث في thread منفصل
        self.search_worker.search(query, self.active_filters)

    def _on_search_completed(self, results: Dict):
        """معالج اكتمال البحث"""
        # تحديث الإحصائيات
        search_time = results.get('search_time', 0)
        total_count = results.get('total', 0)

        self.stats['last_results_count'] = total_count

        # تحديث متوسط الوقت
        n = self.stats['total_searches']
        old_avg = self.stats['avg_time']
        self.stats['avg_time'] = (old_avg * (n - 1) + search_time) / n

        # تحديث الشريط
        self._update_stats_label(results)

        # إرسال النتائج
        self.results_ready.emit(results)

    def _on_suggestions_ready(self, suggestions: List[str]):
        """معالج جاهزية الاقتراحات"""
        model = QStringListModel(suggestions)
        self.completer.setModel(model)

    def _update_stats_label(self, results: Dict):
        """تحديث شريط الإحصائيات"""
        total = results.get('total', 0)
        quran_count = len(results.get('quran', []))
        tafseer_count = len(results.get('tafseer', []))
        topics_count = len(results.get('topics', []))
        search_time = results.get('search_time', 0)

        text = f"📊 النتائج: {total} | "
        text += f"قرآن: {quran_count} | "
        text += f"تفاسير: {tafseer_count} | "
        text += f"موضوعات: {topics_count} | "
        text += f"⏱️ {search_time*1000:.1f}ms"

        self.stats_label.setText(text)

    # =====================================================
    # 🎯 معالجات الفلاتر
    # =====================================================

    def _toggle_filter_panel(self):
        """إظهار/إخفاء لوحة الفلاتر"""
        self.filter_panel.setVisible(not self.filter_panel.isVisible())

    def _on_quick_filter_clicked(
        self,
        text: str,
        filter_type: FilterType,
        value: Any,
        checked: bool
    ):
        """معالج الضغط على فلتر سريع"""
        filter_id = f"{filter_type.value}_{value}"

        if checked:
            # إضافة الفلتر
            self.add_filter(filter_type, value, text)
        else:
            # إزالة الفلتر
            self.remove_filter(filter_id)

    def add_filter(
        self,
        filter_type: FilterType,
        filter_value: Any,
        display_name: str,
        metadata: Optional[Dict] = None
    ):
        """
        إضافة فلتر

        Args:
            filter_type: نوع الفلتر
            filter_value: قيمة الفلتر
            display_name: الاسم المعروض
            metadata: بيانات إضافية
        """
        filter_id = f"{filter_type.value}_{filter_value}"

        # التحقق من عدم وجوده
        if any(f.filter_id == filter_id for f in self.active_filters):
            return

        # إنشاء الفلتر
        filter_obj = SearchFilter(
            filter_id=filter_id,
            filter_type=filter_type,
            filter_value=filter_value,
            display_name=display_name,
            metadata=metadata or {}
        )

        # إضافة إلى القائمة
        self.active_filters.append(filter_obj)

        # إنشاء Chip
        chip = FilterChip(filter_obj)
        chip.removed.connect(self.remove_filter)

        # إضافة إلى الواجهة
        self.filters_container.layout().addWidget(chip)

        # إظهار منطقة الفلاتر
        self.filters_area.show()

        # إرسال إشارة
        self.filter_added.emit(filter_obj)

        # إعادة البحث
        if self.last_query:
            self._perform_search()

    def remove_filter(self, filter_id: str):
        """
        إزالة فلتر

        Args:
            filter_id: معرف الفلتر
        """
        # حذف من القائمة
        self.active_filters = [
            f for f in self.active_filters
            if f.filter_id != filter_id
        ]

        # إخفاء المنطقة إذا لم يكن هناك فلاتر
        if not self.active_filters:
            self.filters_area.hide()

        # إرسال إشارة
        self.filter_removed.emit(filter_id)

        # إعادة البحث
        if self.last_query:
            self._perform_search()

    def clear_filters(self):
        """مسح كل الفلاتر"""
        # حذف كل الـ chips
        for i in reversed(range(self.filters_container.layout().count())):
            widget = self.filters_container.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # مسح القائمة
        self.active_filters.clear()

        # إخفاء المنطقة
        self.filters_area.hide()

        # إعادة البحث
        if self.last_query:
            self._perform_search()

    def get_active_filters(self) -> List[SearchFilter]:
        """جلب الفلاتر النشطة"""
        return self.active_filters.copy()

    # =====================================================
    # 🛠️ وظائف مساعدة
    # =====================================================

    def set_search_text(self, text: str):
        """تعيين نص البحث"""
        self.search_input.setText(text)

    def get_search_text(self) -> str:
        """جلب نص البحث"""
        return self.search_input.text()

    def clear_search(self):
        """مسح البحث"""
        self.search_input.clear()
        self.clear_filters()
        self.stats_label.clear()

    def get_stats(self) -> Dict:
        """جلب الإحصائيات"""
        return self.stats.copy()

    def closeEvent(self, event):
        """عند الإغلاق"""
        self.search_thread.quit()
        self.search_thread.wait()
        super().closeEvent(event)


# =====================================================
# 🧪 اختبار سريع
# =====================================================

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    # محاكاة مدير قاعدة البيانات
    class MockDB:
        def __init__(self):
            self.connection = None

        def search_all(self, query, filters):
            return {
                'quran': [],
                'tafseer': [],
                'topics': [],
                'total': 0
            }

    engine = SmartSearchEngine(MockDB())
    engine.resize(800, 400)
    engine.show()

    sys.exit(app.exec())

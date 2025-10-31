"""
🖥️ نافذة البحث الذكي الرئيسية - دُحى TV
==========================================
الواجهة الرئيسية التي تجمع:
- الشجرة الديناميكية
- محرك البحث الذكي
- منطقة العرض
- الربط العصبي بين كل المكونات
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTabWidget, QTextBrowser, QLabel,
    QToolBar, QPushButton, QStatusBar, QFrame,
    QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QSettings
from PyQt6.QtGui import QFont, QColor, QAction, QIcon
from typing import Dict, Any, Optional, List
from pathlib import Path
import sys

# استيراد المكونات
sys.path.append(str(Path(__file__).parent.parent))

from database.neural_database import NeuralDatabase
from widgets.smart_search_tree import SmartSearchTree
from search.smart_search_engine import SmartSearchEngine


class DisplayArea(QWidget):
    """
    منطقة العرض الرئيسية
    تعرض: القرآن، التفاسير، الترجمات، إلخ
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._setup_ui()

    def _setup_ui(self):
        """إعداد الواجهة"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # =====================================================
        # التابات
        # =====================================================

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 5px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-bottom: none;
                border-radius: 5px 5px 0 0;
                padding: 8px 20px;
                margin-right: 2px;
                font-size: 11pt;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #667eea;
            }
            QTabBar::tab:hover {
                background-color: #e9ecef;
            }
        """)

        layout.addWidget(self.tabs)

        # =====================================================
        # 1️⃣ تاب القرآن
        # =====================================================

        self.quran_display = QTextBrowser()
        self.quran_display.setFont(QFont("Amiri", 18))
        self.quran_display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.quran_display.setStyleSheet("""
            QTextBrowser {
                background-color: #fffef7;
                border: none;
                padding: 20px;
                line-height: 1.8;
            }
        """)
        self.tabs.addTab(self.quran_display, "📖 القرآن الكريم")

        # =====================================================
        # 2️⃣ تاب التفاسير
        # =====================================================

        self.tafseer_display = QTextBrowser()
        self.tafseer_display.setFont(QFont("Arial", 12))
        self.tafseer_display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.tafseer_display.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                border: none;
                padding: 20px;
            }
        """)
        self.tabs.addTab(self.tafseer_display, "📚 التفاسير")

        # =====================================================
        # 3️⃣ تاب الترجمات
        # =====================================================

        self.translation_display = QTextBrowser()
        self.translation_display.setFont(QFont("Arial", 12))
        self.translation_display.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                border: none;
                padding: 20px;
            }
        """)
        self.tabs.addTab(self.translation_display, "🌍 الترجمات")

        # =====================================================
        # 4️⃣ تاب علوم القرآن
        # =====================================================

        self.sciences_display = QTextBrowser()
        self.sciences_display.setFont(QFont("Arial", 12))
        self.sciences_display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.sciences_display.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                border: none;
                padding: 20px;
            }
        """)
        self.tabs.addTab(self.sciences_display, "🔬 علوم القرآن")

    def display_verse(self, verse_data: Dict):
        """عرض آية"""
        verse_text = verse_data.get('text_othmani', '')
        surah_name = verse_data.get('surah_name_arabic', '')
        verse_number = verse_data.get('verse_number', '')

        html = f"""
        <div style="direction: rtl; text-align: right; line-height: 2.0;">
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #667eea; margin: 0;">سورة {surah_name} - الآية {verse_number}</h3>
            </div>
            <div style="font-size: 24pt; color: #2c3e50; padding: 20px; background-color: #fffef7; border-right: 4px solid #667eea; border-radius: 5px;">
                {verse_text}
            </div>
        </div>
        """

        self.quran_display.setHtml(html)

    def display_tafseer(self, tafseer_list: List[Dict]):
        """عرض التفاسير"""
        html = '<div style="direction: rtl; text-align: right;">'

        for tafseer in tafseer_list:
            book_name = tafseer.get('book_name_arabic', '')
            author = tafseer.get('author_name', '')
            text = tafseer.get('tafseer_text', '')

            html += f"""
            <div style="margin-bottom: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
                <h4 style="color: #667eea; margin-top: 0;">
                    📖 {book_name}
                    <span style="color: #6c757d; font-size: 10pt;">({author})</span>
                </h4>
                <p style="color: #2c3e50; line-height: 1.8; font-size: 12pt;">
                    {text}
                </p>
            </div>
            """

        html += '</div>'
        self.tafseer_display.setHtml(html)

    def display_translations(self, translation_list: List[Dict]):
        """عرض الترجمات"""
        html = '<div style="direction: ltr; text-align: left;">'

        for trans in translation_list:
            book_name = trans.get('book_name', '')
            language = trans.get('language_name', '')
            text = trans.get('translation_text', '')

            html += f"""
            <div style="margin-bottom: 25px; padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
                <h5 style="color: #667eea; margin-top: 0;">
                    🌍 {book_name} ({language})
                </h5>
                <p style="color: #2c3e50; line-height: 1.6;">
                    {text}
                </p>
            </div>
            """

        html += '</div>'
        self.translation_display.setHtml(html)

    def display_sciences(self, sciences_list: List[Dict]):
        """عرض علوم القرآن"""
        html = '<div style="direction: rtl; text-align: right;">'

        for science in sciences_list:
            science_type = science.get('science_type', '')
            text = science.get('science_text', '')
            source = science.get('source', '')

            html += f"""
            <div style="margin-bottom: 25px; padding: 15px; background-color: #e7f3ff; border-right: 4px solid #2196f3; border-radius: 5px;">
                <h5 style="color: #1976d2; margin-top: 0;">
                    🔬 {science_type}
                </h5>
                <p style="color: #37474f; line-height: 1.7;">
                    {text}
                </p>
                {f'<small style="color: #78909c;">المصدر: {source}</small>' if source else ''}
            </div>
            """

        html += '</div>'
        self.sciences_display.setHtml(html)

    def display_topic(self, topic_data: Dict, verses: List[Dict]):
        """عرض موضوع مع آياته"""
        topic_name = topic_data.get('topic_name', '')
        description = topic_data.get('description', '')

        html = f"""
        <div style="direction: rtl; text-align: right;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h2 style="color: white; margin: 0;">{topic_name}</h2>
                {f'<p style="color: rgba(255,255,255,0.9); margin-top: 10px;">{description}</p>' if description else ''}
            </div>
        """

        for verse in verses:
            surah_name = verse.get('surah_name_arabic', '')
            verse_number = verse.get('verse_number', '')
            text = verse.get('text_othmani', '')

            html += f"""
            <div style="margin-bottom: 20px; padding: 15px; background-color: #f8f9fa; border-right: 3px solid #667eea; border-radius: 5px;">
                <div style="color: #667eea; font-weight: bold; margin-bottom: 10px;">
                    [{surah_name}: {verse_number}]
                </div>
                <div style="font-size: 16pt; color: #2c3e50; line-height: 1.8;">
                    {text}
                </div>
            </div>
            """

        html += '</div>'
        self.quran_display.setHtml(html)

    def clear_display(self):
        """مسح العرض"""
        self.quran_display.clear()
        self.tafseer_display.clear()
        self.translation_display.clear()
        self.sciences_display.clear()


class SmartSearchWindow(QMainWindow):
    """
    النافذة الرئيسية للبحث الذكي

    المكونات:
    - محرك البحث (أعلى)
    - الشجرة الديناميكية (يمين)
    - منطقة العرض (وسط)
    - شريط المعلومات (أسفل)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # قاعدة البيانات
        self.db = NeuralDatabase()

        # الإعدادات
        self.settings = QSettings("DuhaTV", "SmartSearch")

        # إعداد النافذة
        self.setWindowTitle("البحث الذكي - دُحى TV")
        self.setMinimumSize(1200, 800)

        # إعداد الواجهة
        self._setup_ui()

        # إعداد الاتصالات
        self._setup_connections()

        # تحميل الإعدادات
        self._load_settings()

    def _setup_ui(self):
        """إعداد واجهة المستخدم"""
        # الـ Widget الرئيسي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # =====================================================
        # 1️⃣ شريط الأدوات العلوي
        # =====================================================

        toolbar = self._create_toolbar()
        self.addToolBar(toolbar)

        # =====================================================
        # 2️⃣ محرك البحث
        # =====================================================

        self.search_engine = SmartSearchEngine(self.db)
        main_layout.addWidget(self.search_engine)

        # =====================================================
        # 3️⃣ المحتوى الرئيسي (Splitter)
        # =====================================================

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #dee2e6;
                width: 2px;
            }
            QSplitter::handle:hover {
                background-color: #667eea;
            }
        """)

        # الشجرة (يمين)
        self.tree = SmartSearchTree(self.db)
        self.tree.setMinimumWidth(300)

        # منطقة العرض (وسط)
        self.display_area = DisplayArea()

        # إضافة إلى الـ Splitter (RTL: الشجرة يمين، العرض يسار)
        main_splitter.addWidget(self.display_area)  # العرض أولاً
        main_splitter.addWidget(self.tree)          # ثم الشجرة

        # النسب الافتراضية: 70% عرض، 30% شجرة
        main_splitter.setSizes([700, 300])

        main_layout.addWidget(main_splitter, 1)

        # =====================================================
        # 4️⃣ شريط الحالة السفلي
        # =====================================================

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.info_label = QLabel("مرحباً بك في البحث الذكي")
        self.info_label.setFont(QFont("Arial", 10))
        self.status_bar.addPermanentWidget(self.info_label)

    def _create_toolbar(self) -> QToolBar:
        """إنشاء شريط الأدوات"""
        toolbar = QToolBar("أدوات")
        toolbar.setIconSize(Qt.GlobalColor.black)
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                spacing: 5px;
                padding: 5px;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                border-radius: 5px;
                padding: 8px;
                margin: 2px;
            }
            QToolButton:hover {
                background-color: #e9ecef;
            }
            QToolButton:pressed {
                background-color: #dee2e6;
            }
        """)

        # زر السابق
        prev_action = QAction("⮜ السابق", self)
        prev_action.setShortcut("Alt+Right")
        prev_action.triggered.connect(self.tree.navigate_previous)
        toolbar.addAction(prev_action)

        # زر التالي
        next_action = QAction("التالي ⮞", self)
        next_action.setShortcut("Alt+Left")
        next_action.triggered.connect(self.tree.navigate_next)
        toolbar.addAction(next_action)

        toolbar.addSeparator()

        # زر مسح البحث
        clear_action = QAction("🗑️ مسح", self)
        clear_action.triggered.connect(self.clear_all)
        toolbar.addAction(clear_action)

        # زر التحديث
        refresh_action = QAction("🔄 تحديث", self)
        refresh_action.triggered.connect(self.tree.refresh_tree)
        toolbar.addAction(refresh_action)

        toolbar.addSeparator()

        # زر الإعدادات
        settings_action = QAction("⚙️ الإعدادات", self)
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)

        return toolbar

    def _setup_connections(self):
        """إعداد الاتصالات بين المكونات"""
        # عند اختيار آية من الشجرة
        self.tree.verse_selected.connect(self.on_verse_selected)

        # عند اختيار سورة
        self.tree.surah_selected.connect(self.on_surah_selected)

        # عند اختيار موضوع
        self.tree.topic_selected.connect(self.on_topic_selected)

        # عند جاهزية نتائج البحث
        self.search_engine.results_ready.connect(self.on_search_results_ready)

        # عند اختيار عنصر من الشجرة
        self.tree.item_selected.connect(self.on_tree_item_selected)

    # =====================================================
    # 🔗 معالجات الاتصالات (Slots)
    # =====================================================

    @pyqtSlot(int)
    def on_verse_selected(self, verse_id: int):
        """معالج اختيار آية"""
        try:
            # جلب البيانات المرتبطة
            linked_data = self.db.get_linked_data(verse_id)

            # عرض الآية
            verse = linked_data.get('verse')
            if verse:
                self.display_area.display_verse(verse)

            # عرض التفاسير
            tafseer = linked_data.get('tafseer', [])
            if tafseer:
                self.display_area.display_tafseer(tafseer)

            # عرض الترجمات
            translations = linked_data.get('translations', [])
            if translations:
                self.display_area.display_translations(translations)

            # عرض علوم القرآن
            sciences = linked_data.get('sciences', [])
            if sciences:
                self.display_area.display_sciences(sciences)

            # تحديث شريط الحالة
            surah_name = verse.get('surah_name_arabic', '') if verse else ''
            verse_number = verse.get('verse_number', '') if verse else ''
            page = verse.get('page_number', '') if verse else ''
            juz = verse.get('juz_number', '') if verse else ''

            info = f"سورة {surah_name}: {verse_number}"
            if page:
                info += f" | الصفحة: {page}"
            if juz:
                info += f" | الجزء: {juz}"

            self.info_label.setText(info)

        except Exception as e:
            print(f"❌ خطأ في عرض الآية: {e}")
            self.info_label.setText(f"خطأ: {e}")

    @pyqtSlot(int)
    def on_surah_selected(self, surah_id: int):
        """معالج اختيار سورة"""
        try:
            surah = self.db.get_surah(surah_id)
            if surah:
                name = surah.get('surah_name_arabic', '')
                verses_count = surah.get('verses_count', 0)
                revelation_type = surah.get('revelation_type', '')

                self.info_label.setText(
                    f"سورة {name} | {revelation_type} | {verses_count} آية"
                )

        except Exception as e:
            print(f"❌ خطأ في عرض السورة: {e}")

    @pyqtSlot(int)
    def on_topic_selected(self, topic_id: int):
        """معالج اختيار موضوع"""
        try:
            # جلب معلومات الموضوع
            topic = self.db.connection.execute(
                "SELECT * FROM topics WHERE topic_id = ?",
                (topic_id,)
            ).fetchone()

            if topic:
                topic_data = dict(topic)

                # جلب الآيات المرتبطة
                verses = self.db.get_topic_verses(topic_id)

                # عرض الموضوع والآيات
                self.display_area.display_topic(topic_data, verses)

                # تحديث شريط الحالة
                topic_name = topic_data.get('topic_name', '')
                verses_count = len(verses)

                self.info_label.setText(
                    f"الموضوع: {topic_name} | {verses_count} آية"
                )

        except Exception as e:
            print(f"❌ خطأ في عرض الموضوع: {e}")

    @pyqtSlot(dict)
    def on_search_results_ready(self, results: Dict):
        """معالج جاهزية نتائج البحث"""
        try:
            # تحديث الشجرة بالنتائج
            query = self.search_engine.get_search_text()
            self.tree.update_from_search(results, query)

            # تحديث شريط الحالة
            total = results.get('total', 0)
            self.info_label.setText(f"عدد النتائج: {total}")

        except Exception as e:
            print(f"❌ خطأ في عرض النتائج: {e}")

    @pyqtSlot(dict)
    def on_tree_item_selected(self, data: Dict):
        """معالج اختيار عنصر من الشجرة"""
        item_type = data.get('type')
        item_data = data.get('data', {})

        # معالجة حسب النوع
        # يمكن إضافة معالجات إضافية هنا

    # =====================================================
    # 🛠️ وظائف مساعدة
    # =====================================================

    def clear_all(self):
        """مسح كل شيء"""
        self.search_engine.clear_search()
        self.display_area.clear_display()
        self.tree.clear_tree()
        self.info_label.setText("تم المسح")

    def show_settings(self):
        """عرض نافذة الإعدادات"""
        # يمكن إضافة نافذة إعدادات منفصلة
        self.info_label.setText("الإعدادات قريباً...")

    def _load_settings(self):
        """تحميل الإعدادات المحفوظة"""
        # حجم النافذة
        if self.settings.contains("window/size"):
            self.resize(self.settings.value("window/size"))

        # موضع النافذة
        if self.settings.contains("window/position"):
            self.move(self.settings.value("window/position"))

    def _save_settings(self):
        """حفظ الإعدادات"""
        self.settings.setValue("window/size", self.size())
        self.settings.setValue("window/position", self.pos())

    def closeEvent(self, event):
        """عند إغلاق النافذة"""
        self._save_settings()
        self.db.close()
        event.accept()


# =====================================================
# 🧪 اختبار سريع
# =====================================================

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    # تطبيق الخطوط العربية
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    window = SmartSearchWindow()
    window.show()

    sys.exit(app.exec())

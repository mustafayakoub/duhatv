#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📖 QuranKit - مثال تطبيق بسيط
Simple Example Application using QuranKit Components
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# استيراد قاعدة البيانات الموجودة
sys.path.insert(0, str(Path(__file__).parent / "src"))
from db_manager import QuranDatabase

# استيراد QuranKit
from qurankit import (
    QuranSearchComponent,
    QuranTreeComponent,
    QuranTreeWidget,
    QuranDisplayComponent,
    QuranBookmarksComponent,
    QuranThemeComponent,
    QuranAudioComponent
)


class QuranKitExampleApp(QMainWindow):
    """تطبيق مثال باستخدام QuranKit"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("📖 QuranKit - تطبيق مثال")
        self.setGeometry(100, 100, 1400, 900)

        # قاعدة البيانات
        try:
            self.db = QuranDatabase()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل الاتصال بقاعدة البيانات:\n{e}")
            sys.exit(1)

        # إعداد المكونات
        self.setup_components()

        # بناء الواجهة
        self.setup_ui()

        # تحميل سورة الفاتحة افتراضياً
        self.load_sura(1)

    def setup_components(self):
        """إعداد مكونات QuranKit"""

        # مكون البحث
        self.search_component = QuranSearchComponent(
            database=self.db,
            config={'max_results': 50}
        )

        # مكون الشجرة
        self.tree_component = QuranTreeComponent(
            database=self.db,
            config={'mode': 'juz'}
        )

        # مكون العرض
        self.display_component = QuranDisplayComponent(
            config={
                'arabic_font': 'Arial',
                'font_size': 18,
                'primary_color': '#1e3c72',
                'secondary_color': '#2a5298'
            }
        )

        # مكون الإشارات
        self.bookmarks_component = QuranBookmarksComponent(
            database=self.db,
            config={}
        )

        # مكون المظاهر
        self.theme_component = QuranThemeComponent(theme_name='light')

        print("✅ تم إعداد كل مكونات QuranKit بنجاح!")

    def setup_ui(self):
        """بناء واجهة المستخدم"""

        # القائمة الرئيسية
        self.create_menu()

        # الواجهة الرئيسية
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # شريط البحث العلوي
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 ابحث في القرآن الكريم...")
        self.search_input.returnPressed.connect(self.perform_search)
        search_layout.addWidget(self.search_input)

        btn_search = QPushButton("بحث")
        btn_search.clicked.connect(self.perform_search)
        search_layout.addWidget(btn_search)

        btn_clear = QPushButton("مسح")
        btn_clear.clicked.connect(self.clear_search)
        search_layout.addWidget(btn_clear)

        main_layout.addLayout(search_layout)

        # المنطقة الرئيسية (شجرة + عرض)
        content_splitter = QSplitter(Qt.Orientation.Horizontal)

        # شجرة التصفح على اليسار
        self.tree_widget = QuranTreeWidget(self.tree_component)
        self.tree_widget.item_selected.connect(self.on_tree_item_selected)
        content_splitter.addWidget(self.tree_widget)

        # منطقة العرض على اليمين
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # معلومات السورة
        self.info_label = QLabel()
        self.info_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3c72, stop:1 #2a5298);
                color: white;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.info_label)

        # متصفح النصوص
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(False)
        self.text_browser.setReadOnly(True)
        self.text_browser.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        right_layout.addWidget(self.text_browser)

        # أزرار الإجراءات
        actions_layout = QHBoxLayout()

        btn_bookmark = QPushButton("🔖 إضافة إشارة")
        btn_bookmark.clicked.connect(self.add_bookmark)
        actions_layout.addWidget(btn_bookmark)

        btn_view_bookmarks = QPushButton("📚 عرض الإشارات")
        btn_view_bookmarks.clicked.connect(self.show_bookmarks)
        actions_layout.addWidget(btn_view_bookmarks)

        actions_layout.addStretch()

        right_layout.addLayout(actions_layout)

        content_splitter.addWidget(right_panel)

        # تحديد النسب
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 3)

        main_layout.addWidget(content_splitter)

        # شريط الحالة
        self.statusBar().showMessage("✅ جاهز - QuranKit Example")

        # تطبيق الثيم
        self.apply_current_theme()

    def create_menu(self):
        """إنشاء القائمة الرئيسية"""
        menubar = self.menuBar()

        # قائمة عرض
        view_menu = menubar.addMenu("عرض")

        # اختيار الثيم
        theme_menu = view_menu.addMenu("🎨 المظهر")
        themes = self.theme_component.get_available_themes()

        for theme_id, theme_name in themes.items():
            action = theme_menu.addAction(theme_name)
            action.triggered.connect(lambda checked, tid=theme_id: self.change_theme(tid))

        # قائمة أدوات
        tools_menu = menubar.addMenu("أدوات")

        search_action = tools_menu.addAction("🔍 بحث متقدم")
        search_action.triggered.connect(self.show_advanced_search)

        bookmarks_action = tools_menu.addAction("🔖 الإشارات المرجعية")
        bookmarks_action.triggered.connect(self.show_bookmarks)

        stats_action = tools_menu.addAction("📊 إحصائيات")
        stats_action.triggered.connect(self.show_statistics)

        # قائمة مساعدة
        help_menu = menubar.addMenu("مساعدة")

        about_action = help_menu.addAction("ℹ️ حول")
        about_action.triggered.connect(self.show_about)

    def on_tree_item_selected(self, data):
        """عند اختيار عنصر من الشجرة"""
        item_type = data.get('type')

        if item_type == 'sura':
            sura = data.get('sura')
            self.load_sura(sura)
        elif item_type == 'juz':
            juz = data.get('juz')
            self.load_juz(juz)

    def load_sura(self, sura_num: int):
        """تحميل سورة"""
        try:
            # معلومات السورة
            sura_info = self.db.get_sura_info(sura_num)

            # الآيات
            ayas = self.db.get_sura(sura_num)

            # تحديث معلومات السورة
            self.info_label.setText(
                f"سورة {sura_info['name']} • "
                f"{sura_info.get('type_full', 'مكية')} • "
                f"{sura_info['ayas_count']} آية"
            )

            # عرض السورة
            html = self.display_component.format_sura_html(sura_info, ayas)
            self.text_browser.setHtml(html)

            self.current_sura = sura_num
            self.statusBar().showMessage(f"✅ تم تحميل سورة {sura_info['name']}")

        except Exception as e:
            QMessageBox.warning(self, "خطأ", f"فشل تحميل السورة: {e}")

    def load_juz(self, juz_num: int):
        """تحميل جزء"""
        self.info_label.setText(f"الجزء {juz_num}")
        self.text_browser.setHtml(f"<h2>عرض الجزء {juz_num} قيد التطوير...</h2>")
        self.statusBar().showMessage(f"تم اختيار الجزء {juz_num}")

    def perform_search(self):
        """تنفيذ البحث"""
        query = self.search_input.text().strip()

        if len(query) < 2:
            QMessageBox.warning(self, "تنبيه", "أدخل كلمة البحث (حرفان على الأقل)")
            return

        try:
            # البحث
            results = self.search_component.search(query, search_type='text', limit=50)

            if not results:
                self.text_browser.setHtml("<h2>لا توجد نتائج</h2>")
                self.statusBar().showMessage("❌ لا توجد نتائج")
                return

            # عرض النتائج
            html = self.display_component.format_search_results_html(results, query)
            self.text_browser.setHtml(html)

            self.info_label.setText(f"نتائج البحث عن: {query} ({len(results)} نتيجة)")
            self.statusBar().showMessage(f"✅ تم العثور على {len(results)} نتيجة")

        except Exception as e:
            QMessageBox.warning(self, "خطأ", f"فشل البحث: {e}")

    def clear_search(self):
        """مسح البحث"""
        self.search_input.clear()
        if hasattr(self, 'current_sura'):
            self.load_sura(self.current_sura)
        else:
            self.load_sura(1)

    def add_bookmark(self):
        """إضافة إشارة مرجعية"""
        if not hasattr(self, 'current_sura'):
            QMessageBox.warning(self, "تنبيه", "اختر سورة أولاً")
            return

        note, ok = QInputDialog.getText(
            self,
            "إضافة إشارة",
            "ملاحظة (اختياري):",
        )

        if ok:
            success = self.bookmarks_component.add_bookmark(
                sura=self.current_sura,
                ayah=1,
                note=note
            )

            if success:
                QMessageBox.information(self, "نجح", "تمت إضافة الإشارة المرجعية!")
            else:
                QMessageBox.warning(self, "تنبيه", "الإشارة موجودة مسبقاً")

    def show_bookmarks(self):
        """عرض الإشارات المرجعية"""
        bookmarks = self.bookmarks_component.get_all_bookmarks()

        if not bookmarks:
            QMessageBox.information(self, "الإشارات", "لا توجد إشارات مرجعية")
            return

        # عرض في نافذة بسيطة
        dialog = QDialog(self)
        dialog.setWindowTitle("🔖 الإشارات المرجعية")
        dialog.resize(600, 400)

        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        for bookmark in bookmarks:
            item_text = f"{bookmark['sura_name']}:{bookmark['ayah']}"
            if bookmark.get('note'):
                item_text += f" - {bookmark['note']}"
            list_widget.addItem(item_text)

        layout.addWidget(list_widget)

        btn_close = QPushButton("إغلاق")
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)

        dialog.exec()

    def show_advanced_search(self):
        """بحث متقدم"""
        QMessageBox.information(self, "قريباً", "البحث المتقدم قيد التطوير...")

    def show_statistics(self):
        """عرض الإحصائيات"""
        stats = self.db.get_statistics()
        bookmark_stats = self.bookmarks_component.get_statistics()

        msg = f"""
📊 إحصائيات القرآن الكريم:

📖 عدد السور: {stats.get('suras_count', 114)}
📄 عدد الآيات: {stats.get('ayas_count', 6236)}
📚 عدد الأجزاء: {stats.get('juz_count', 30)}
📃 عدد الصفحات: {stats.get('pages_count', 604)}

🔖 الإشارات المرجعية:
• إجمالي الإشارات: {bookmark_stats['total_bookmarks']}
• سور محفوظة: {bookmark_stats['suras_bookmarked']}
        """

        QMessageBox.information(self, "📊 الإحصائيات", msg)

    def change_theme(self, theme_id: str):
        """تغيير المظهر"""
        self.theme_component.set_theme(theme_id)
        self.apply_current_theme()
        self.statusBar().showMessage(f"✅ تم تطبيق مظهر: {theme_id}")

    def apply_current_theme(self):
        """تطبيق المظهر الحالي"""
        stylesheet = self.theme_component.apply_theme_to_stylesheet(self)
        self.setStyleSheet(stylesheet)

    def show_about(self):
        """حول التطبيق"""
        about_text = """
<div dir="rtl" style="text-align: center;">
<h2>📖 QuranKit - مثال تطبيق</h2>
<p><b>نسخة 1.0</b></p>
<p>تطبيق مثال يوضح استخدام مكتبة QuranKit</p>
<hr>
<h3>المكونات المستخدمة:</h3>
<ul style="text-align: right;">
<li>🔍 QuranSearchComponent - البحث المتقدم</li>
<li>🌳 QuranTreeComponent - شجرة التصفح</li>
<li>📺 QuranDisplayComponent - عرض منسق</li>
<li>🔖 QuranBookmarksComponent - الإشارات</li>
<li>🎨 QuranThemeComponent - المظاهر</li>
</ul>
<hr>
<p>المطور: Mustafa Yakoub<br>
Email: duhatv@gmail.com<br>
Website: duhatv.net</p>
</div>
        """

        QMessageBox.about(self, "ℹ️ حول البرنامج", about_text)


def main():
    """نقطة الدخول الرئيسية"""
    app = QApplication(sys.argv)

    # إعداد الخط العربي
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # إنشاء التطبيق
    window = QuranKitExampleApp()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

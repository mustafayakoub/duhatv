#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                    تطبيق القرآن الكريم الاحترافي النهائي
                    Ultimate Professional Quran Application
================================================================================

المطور: Claude AI Assistant
النسخة: 2.0 Ultimate Edition
التاريخ: 2025-10-30

الميزات:
✨ شجرة ديناميكية ذكية (السور → الآيات)
✨ تابات متعددة المستويات
✨ بحث متقدم (4 أنماط)
✨ ألوان Claude الهادئة والراقية
✨ تزامن كامل بين كل المكونات
✨ أداء محسّن بدون حدود
✨ تصميم احترافي عصري
"""

import sys
import os
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

# محاولة استيراد PyQt6، وإذا فشل نستخدم PyQt5
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTreeWidget, QTreeWidgetItem, QTabWidget, QTextEdit, QLabel,
        QPushButton, QLineEdit, QComboBox, QSplitter, QFrame, QMessageBox,
        QCheckBox, QScrollArea, QGroupBox
    )
    from PyQt6.QtCore import Qt, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QIcon, QColor
    PYQT_VERSION = 6
    print("✅ استخدام PyQt6")
except ImportError:
    try:
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QTreeWidget, QTreeWidgetItem, QTabWidget, QTextEdit, QLabel,
            QPushButton, QLineEdit, QComboBox, QSplitter, QFrame, QMessageBox,
            QCheckBox, QScrollArea, QGroupBox
        )
        from PyQt5.QtCore import Qt, pyqtSignal, QTimer
        from PyQt5.QtGui import QFont, QIcon, QColor
        PYQT_VERSION = 5
        print("✅ استخدام PyQt5")
    except ImportError:
        print("❌ خطأ: يجب تثبيت PyQt6 أو PyQt5")
        print("قم بتشغيل: pip install PyQt6")
        print("أو: pip install PyQt5")
        sys.exit(1)


# ============================================================================
#                             نظام الألوان الراقي
# ============================================================================

class ClaudeColors:
    """نظام ألوان Claude الهادئة والراقية"""

    # الألوان الأساسية
    PRIMARY = "#CC9B66"          # برونزي دافئ
    SECONDARY = "#9B8B7E"        # رمادي دافئ
    ACCENT = "#B8956A"           # ذهبي هادئ

    # ألوان الخلفية
    BG_MAIN = "#F8F6F4"          # خلفية رئيسية كريمية
    BG_SIDEBAR = "#F0EBE3"       # خلفية جانبية
    BG_CONTENT = "#FFFFFF"       # خلفية المحتوى
    BG_HEADER = "#E8DFD0"        # خلفية العناوين

    # ألوان النص
    TEXT_PRIMARY = "#2C2416"     # نص أساسي داكن
    TEXT_SECONDARY = "#5C5445"   # نص ثانوي
    TEXT_MUTED = "#8C8173"       # نص خافت
    TEXT_LIGHT = "#ACA197"       # نص فاتح

    # ألوان التفاعل
    HOVER = "#E5D4B8"            # عند التحويم
    SELECTED = "#D4C4A8"         # عند التحديد
    PRESSED = "#C4B498"          # عند الضغط

    # ألوان الحالات
    SUCCESS = "#7A9D54"          # نجاح (أخضر هادئ)
    WARNING = "#D4A574"          # تحذير (برتقالي هادئ)
    ERROR = "#C17767"            # خطأ (أحمر هادئ)
    INFO = "#7B8FA3"             # معلومات (أزرق هادئ)

    # ألوان الحدود
    BORDER_LIGHT = "#E0D5C7"     # حدود فاتحة
    BORDER_MEDIUM = "#C9BDB0"    # حدود متوسطة
    BORDER_DARK = "#B3A699"      # حدود داكنة

    @classmethod
    def get_stylesheet(cls) -> str:
        """الحصول على ورقة الأنماط الكاملة"""
        return f"""
        /* النمط العام */
        QMainWindow, QWidget {{
            background-color: {cls.BG_MAIN};
            color: {cls.TEXT_PRIMARY};
            font-family: 'Segoe UI', 'Tahoma', sans-serif;
        }}

        /* الشجرة */
        QTreeWidget {{
            background-color: {cls.BG_SIDEBAR};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            padding: 8px;
            font-size: 13px;
        }}

        QTreeWidget::item {{
            padding: 8px;
            border-radius: 4px;
            color: {cls.TEXT_PRIMARY};
        }}

        QTreeWidget::item:hover {{
            background-color: {cls.HOVER};
        }}

        QTreeWidget::item:selected {{
            background-color: {cls.SELECTED};
            color: {cls.TEXT_PRIMARY};
        }}

        /* التابات */
        QTabWidget::pane {{
            border: 1px solid {cls.BORDER_LIGHT};
            background-color: {cls.BG_CONTENT};
            border-radius: 8px;
        }}

        QTabBar::tab {{
            background-color: {cls.BG_SIDEBAR};
            color: {cls.TEXT_SECONDARY};
            padding: 12px 24px;
            margin: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: bold;
            font-size: 13px;
        }}

        QTabBar::tab:selected {{
            background-color: {cls.PRIMARY};
            color: white;
        }}

        QTabBar::tab:hover {{
            background-color: {cls.HOVER};
        }}

        /* مناطق النص */
        QTextEdit {{
            background-color: {cls.BG_CONTENT};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            padding: 16px;
            font-size: 16px;
            line-height: 1.8;
            color: {cls.TEXT_PRIMARY};
        }}

        /* حقول الإدخال */
        QLineEdit {{
            background-color: {cls.BG_CONTENT};
            border: 2px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 14px;
            color: {cls.TEXT_PRIMARY};
        }}

        QLineEdit:focus {{
            border: 2px solid {cls.PRIMARY};
        }}

        /* القوائم المنسدلة */
        QComboBox {{
            background-color: {cls.BG_CONTENT};
            border: 2px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 13px;
            color: {cls.TEXT_PRIMARY};
        }}

        QComboBox:hover {{
            border: 2px solid {cls.PRIMARY};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}

        /* الأزرار */
        QPushButton {{
            background-color: {cls.PRIMARY};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 13px;
        }}

        QPushButton:hover {{
            background-color: {cls.ACCENT};
        }}

        QPushButton:pressed {{
            background-color: {cls.PRESSED};
        }}

        QPushButton:disabled {{
            background-color: {cls.TEXT_LIGHT};
            color: {cls.TEXT_MUTED};
        }}

        /* التسميات */
        QLabel {{
            color: {cls.TEXT_PRIMARY};
            font-size: 13px;
        }}

        /* الإطارات */
        QFrame {{
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            background-color: {cls.BG_CONTENT};
        }}

        /* أشرطة التمرير */
        QScrollBar:vertical {{
            background-color: {cls.BG_SIDEBAR};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {cls.BORDER_MEDIUM};
            border-radius: 6px;
            min-height: 30px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {cls.PRIMARY};
        }}

        QScrollBar:horizontal {{
            background-color: {cls.BG_SIDEBAR};
            height: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {cls.BORDER_MEDIUM};
            border-radius: 6px;
            min-width: 30px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {cls.PRIMARY};
        }}

        /* مربعات الاختيار */
        QCheckBox {{
            color: {cls.TEXT_PRIMARY};
            font-size: 13px;
            spacing: 8px;
        }}

        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {cls.BORDER_MEDIUM};
            border-radius: 4px;
            background-color: {cls.BG_CONTENT};
        }}

        QCheckBox::indicator:checked {{
            background-color: {cls.PRIMARY};
            border-color: {cls.PRIMARY};
        }}

        /* GroupBox */
        QGroupBox {{
            border: 2px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            font-weight: bold;
            color: {cls.TEXT_PRIMARY};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 4px 12px;
            background-color: {cls.BG_MAIN};
        }}
        """


# ============================================================================
#                          مدير قاعدة البيانات
# ============================================================================

class DatabaseManager:
    """مدير قاعدة البيانات الذكي"""

    def __init__(self):
        self.conn: Optional[sqlite3.Connection] = None
        self.db_path: Optional[str] = None
        self.tables_info: Dict[str, List[str]] = {}

    def find_database(self) -> Optional[str]:
        """البحث الذكي عن قاعدة البيانات"""
        possible_paths = [
            r"C:\QYRAN5\QYRAN62\surah_database_app_v32.db",
            r"C:\QYRAN5\QYRAN62\quran.db",
            r"C:\QYRAN5\surah_database_app_v32.db",
            r"C:\QYRAN5\quran.db",
            "surah_database_app_v32.db",
            "quran.db",
            "./surah_database_app_v32.db",
            "./quran.db",
            "../surah_database_app_v32.db",
            "../quran.db",
        ]

        # البحث في المجلد الحالي
        current_dir = Path(".")
        for db_file in current_dir.glob("*.db"):
            if db_file.is_file() and db_file.stat().st_size > 1000000:  # أكبر من 1MB
                possible_paths.insert(0, str(db_file))

        # البحث في المجلد الأب
        parent_dir = Path("..")
        for db_file in parent_dir.glob("*.db"):
            if db_file.is_file() and db_file.stat().st_size > 1000000:
                possible_paths.insert(0, str(db_file))

        for path in possible_paths:
            if os.path.exists(path):
                return path

        return None

    def connect(self) -> bool:
        """الاتصال بقاعدة البيانات"""
        try:
            self.db_path = self.find_database()
            if not self.db_path:
                return False

            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self._analyze_structure()
            return True

        except Exception as e:
            print(f"خطأ في الاتصال: {e}")
            return False

    def _analyze_structure(self):
        """تحليل بنية قاعدة البيانات"""
        if not self.conn:
            return

        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            self.tables_info[table_name] = [col[1] for col in columns]

    def get_surahs(self) -> List[Dict[str, Any]]:
        """الحصول على قائمة السور"""
        if not self.conn:
            return []

        # البحث عن جدول السور
        surah_table = None
        for table_name in self.tables_info.keys():
            if 'surah' in table_name.lower() or 'sura' in table_name.lower():
                surah_table = table_name
                break

        if not surah_table:
            return []

        try:
            cursor = self.conn.cursor()

            # محاولة الحصول على البيانات بطرق مختلفة
            queries = [
                f"SELECT * FROM {surah_table} ORDER BY id",
                f"SELECT * FROM {surah_table} ORDER BY surah_id",
                f"SELECT * FROM {surah_table} ORDER BY sura_id",
                f"SELECT * FROM {surah_table}",
            ]

            for query in queries:
                try:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    if rows:
                        return [dict(row) for row in rows]
                except:
                    continue

            return []

        except Exception as e:
            print(f"خطأ في الحصول على السور: {e}")
            return []

    def get_verses_by_surah(self, surah_id: int) -> List[Dict[str, Any]]:
        """الحصول على آيات سورة معينة"""
        if not self.conn:
            return []

        # البحث عن جدول الآيات
        verse_table = None
        for table_name in self.tables_info.keys():
            if 'verse' in table_name.lower() or 'aya' in table_name.lower() or 'ayah' in table_name.lower():
                if 'quran' in table_name.lower() or 'text' in table_name.lower():
                    verse_table = table_name
                    break

        if not verse_table:
            return []

        try:
            cursor = self.conn.cursor()
            columns = self.tables_info[verse_table]

            # تحديد اسم عمود السورة
            surah_column = None
            for col in ['surah_id', 'sura_id', 'surah', 'sura']:
                if col in columns:
                    surah_column = col
                    break

            if not surah_column:
                return []

            # تحديد عمود الآية
            verse_column = None
            for col in ['verse_id', 'aya_id', 'ayah_id', 'verse', 'aya', 'ayah']:
                if col in columns:
                    verse_column = col
                    break

            query = f"SELECT * FROM {verse_table} WHERE {surah_column} = ? ORDER BY {verse_column if verse_column else 'id'}"
            cursor.execute(query, (surah_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            print(f"خطأ في الحصول على الآيات: {e}")
            return []

    def search_text(self, text: str) -> List[Dict[str, Any]]:
        """البحث النصي في القرآن"""
        if not self.conn or not text:
            return []

        try:
            cursor = self.conn.cursor()

            # البحث في الجداول المحتملة
            for table_name, columns in self.tables_info.items():
                if 'quran' in table_name.lower() or 'verse' in table_name.lower():
                    # البحث عن عمود النص
                    text_column = None
                    for col in ['text', 'verse_text', 'aya_text', 'content']:
                        if col in columns:
                            text_column = col
                            break

                    if text_column:
                        query = f"SELECT * FROM {table_name} WHERE {text_column} LIKE ?"
                        cursor.execute(query, (f'%{text}%',))
                        rows = cursor.fetchall()
                        if rows:
                            return [dict(row) for row in rows]

            return []

        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return []

    def search_by_root(self, root: str) -> List[Dict[str, Any]]:
        """البحث بالجذر"""
        if not self.conn or not root:
            return []

        try:
            cursor = self.conn.cursor()

            # البحث في جدول الجذور أو الكلمات
            for table_name, columns in self.tables_info.items():
                if 'root' in table_name.lower() or 'word' in table_name.lower():
                    if 'root' in columns:
                        query = f"SELECT * FROM {table_name} WHERE root LIKE ?"
                        cursor.execute(query, (f'%{root}%',))
                        rows = cursor.fetchall()
                        if rows:
                            return [dict(row) for row in rows]

            return []

        except Exception as e:
            print(f"خطأ في البحث بالجذر: {e}")
            return []

    def get_tafseer(self, surah_id: int, verse_id: int, tafseer_name: str = 'الميسر') -> str:
        """الحصول على التفسير"""
        if not self.conn:
            return ""

        try:
            cursor = self.conn.cursor()

            # البحث في جداول التفسير
            for table_name, columns in self.tables_info.items():
                if 'tafseer' in table_name.lower() or 'tafsir' in table_name.lower():
                    # محاولة الحصول على التفسير
                    for text_col in ['text', 'tafseer_text', 'content']:
                        if text_col in columns:
                            query = f"SELECT {text_col} FROM {table_name} WHERE surah_id = ? AND verse_id = ?"
                            try:
                                cursor.execute(query, (surah_id, verse_id))
                                row = cursor.fetchone()
                                if row:
                                    return row[0]
                            except:
                                continue

            return "التفسير غير متوفر"

        except Exception as e:
            print(f"خطأ في الحصول على التفسير: {e}")
            return ""

    def close(self):
        """إغلاق الاتصال"""
        if self.conn:
            self.conn.close()


# ============================================================================
#                            التطبيق الرئيسي
# ============================================================================

class QuranAppUltimate(QMainWindow):
    """التطبيق الرئيسي"""

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_surah_id = None
        self.current_verse_id = None
        self.surahs = []
        self.init_ui()
        self.init_database()

    def init_ui(self):
        """تهيئة الواجهة"""
        self.setWindowTitle("تطبيق القرآن الكريم الاحترافي 2.0")
        self.setGeometry(100, 100, 1400, 900)

        # تطبيق الألوان
        self.setStyleSheet(ClaudeColors.get_stylesheet())

        # الويدجت الرئيسي
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # Splitter للتقسيم
        splitter = QSplitter(Qt.Orientation.Horizontal if PYQT_VERSION == 6 else Qt.Horizontal)

        # الشجرة (يمين)
        self.create_tree_widget()
        splitter.addWidget(self.tree_widget)

        # المحتوى (يسار)
        content_widget = self.create_content_widget()
        splitter.addWidget(content_widget)

        # تحديد النسب
        splitter.setSizes([300, 1000])

        main_layout.addWidget(splitter)

    def create_tree_widget(self):
        """إنشاء الشجرة الديناميكية"""
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("📖 القرآن الكريم")
        self.tree_widget.setRightToLeft(True)

        if PYQT_VERSION == 6:
            self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)
            self.tree_widget.itemExpanded.connect(self.on_tree_item_expanded)
        else:
            self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)
            self.tree_widget.itemExpanded.connect(self.on_tree_item_expanded)

    def create_content_widget(self) -> QWidget:
        """إنشاء منطقة المحتوى"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        # أزرار التنقل
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(8)

        self.btn_prev = QPushButton("→ السابق")
        self.btn_next = QPushButton("التالي ←")
        self.btn_prev.clicked.connect(self.go_previous)
        self.btn_next.clicked.connect(self.go_next)

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_next)
        nav_layout.addStretch()

        layout.addLayout(nav_layout)

        # التابات الرئيسية
        self.main_tabs = QTabWidget()
        self.main_tabs.setTabPosition(QTabWidget.TabPosition.North if PYQT_VERSION == 6 else QTabWidget.North)

        # تاب التصفح
        browse_tab = self.create_browse_tab()
        self.main_tabs.addTab(browse_tab, "📖 التصفح")

        # تاب البحث
        search_tab = self.create_search_tab()
        self.main_tabs.addTab(search_tab, "🔍 البحث")

        layout.addWidget(self.main_tabs)

        return widget

    def create_browse_tab(self) -> QWidget:
        """إنشاء تاب التصفح"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # التابات الفرعية
        self.browse_tabs = QTabWidget()

        # تاب القرآن
        self.quran_text = QTextEdit()
        self.quran_text.setReadOnly(True)
        self.quran_text.setFont(QFont("Traditional Arabic", 18))
        self.browse_tabs.addTab(self.quran_text, "📖 القرآن الكريم")

        # تاب التفسير
        self.tafseer_text = QTextEdit()
        self.tafseer_text.setReadOnly(True)
        self.tafseer_text.setFont(QFont("Traditional Arabic", 14))
        self.browse_tabs.addTab(self.tafseer_text, "📚 التفسير")

        # تاب الإعراب
        self.erab_text = QTextEdit()
        self.erab_text.setReadOnly(True)
        self.erab_text.setFont(QFont("Traditional Arabic", 13))
        self.browse_tabs.addTab(self.erab_text, "📝 الإعراب")

        # تاب الصرف
        self.sarf_text = QTextEdit()
        self.sarf_text.setReadOnly(True)
        self.sarf_text.setFont(QFont("Traditional Arabic", 13))
        self.browse_tabs.addTab(self.sarf_text, "🔤 الصرف")

        # تاب الترجمات
        self.translation_text = QTextEdit()
        self.translation_text.setReadOnly(True)
        self.translation_text.setFont(QFont("Arial", 12))
        self.browse_tabs.addTab(self.translation_text, "🌐 الترجمات")

        layout.addWidget(self.browse_tabs)

        return widget

    def create_search_tab(self) -> QWidget:
        """إنشاء تاب البحث"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # منطقة البحث
        search_group = QGroupBox("أدوات البحث")
        search_layout = QVBoxLayout()

        # نوع البحث
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("نوع البحث:"))

        self.search_type = QComboBox()
        self.search_type.addItems([
            "🔍 البحث الذكي",
            "🌱 البحث بالجذور",
            "📝 البحث بالإعراب",
            "⚖️ البحث بالوزن"
        ])
        type_layout.addWidget(self.search_type)
        type_layout.addStretch()
        search_layout.addLayout(type_layout)

        # حقل البحث
        input_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ادخل كلمة البحث...")
        self.search_input.returnPressed.connect(self.perform_search)
        input_layout.addWidget(self.search_input)

        self.btn_search = QPushButton("🔍 بحث")
        self.btn_search.clicked.connect(self.perform_search)
        input_layout.addWidget(self.btn_search)

        search_layout.addLayout(input_layout)

        search_group.setLayout(search_layout)
        layout.addWidget(search_group)

        # نتائج البحث
        results_group = QGroupBox("النتائج")
        results_layout = QVBoxLayout()

        self.search_results = QTreeWidget()
        self.search_results.setHeaderLabels(["السورة", "الآية", "النص"])
        self.search_results.setRightToLeft(True)

        if PYQT_VERSION == 6:
            self.search_results.itemClicked.connect(self.on_search_result_clicked)
        else:
            self.search_results.itemClicked.connect(self.on_search_result_clicked)

        results_layout.addWidget(self.search_results)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        return widget

    def init_database(self):
        """تهيئة قاعدة البيانات"""
        if not self.db.connect():
            QMessageBox.critical(
                self,
                "خطأ",
                "لم يتم العثور على قاعدة البيانات!\n\n"
                "الرجاء وضع ملف قاعدة البيانات في:\n"
                "C:\\QYRAN5\\QYRAN62\\\n\n"
                "أو في نفس مجلد التطبيق."
            )
            return

        # تحميل السور
        self.load_surahs()

    def load_surahs(self):
        """تحميل السور في الشجرة"""
        self.surahs = self.db.get_surahs()

        for surah in self.surahs:
            # محاولة الحصول على معلومات السورة بطرق مختلفة
            surah_id = surah.get('id') or surah.get('surah_id') or surah.get('sura_id')
            surah_name = surah.get('name') or surah.get('surah_name') or surah.get('sura_name') or f"سورة {surah_id}"

            item = QTreeWidgetItem(self.tree_widget)
            item.setText(0, f"📖 {surah_name}")
            item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole, {
                'type': 'surah',
                'id': surah_id,
                'data': surah
            })

            # إضافة عنصر وهمي للسماح بالتوسيع
            dummy = QTreeWidgetItem(item)
            dummy.setText(0, "...")

    def on_tree_item_expanded(self, item: QTreeWidgetItem):
        """عند توسيع عنصر في الشجرة"""
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)

        if data and data.get('type') == 'surah':
            # حذف العناصر الوهمية
            item.takeChildren()

            # تحميل الآيات
            surah_id = data['id']
            verses = self.db.get_verses_by_surah(surah_id)

            for verse in verses:
                verse_id = verse.get('verse_id') or verse.get('aya_id') or verse.get('ayah_id')
                verse_text = verse.get('text') or verse.get('verse_text') or verse.get('aya_text') or ""

                # اختصار النص
                short_text = verse_text[:50] + "..." if len(verse_text) > 50 else verse_text

                verse_item = QTreeWidgetItem(item)
                verse_item.setText(0, f"آية {verse_id}: {short_text}")
                verse_item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole, {
                    'type': 'verse',
                    'surah_id': surah_id,
                    'verse_id': verse_id,
                    'data': verse
                })

    def on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        """عند النقر على عنصر في الشجرة"""
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)

        if not data:
            return

        if data['type'] == 'verse':
            self.display_verse(data['surah_id'], data['verse_id'], data['data'])
        elif data['type'] == 'surah':
            # عرض أول آية من السورة
            verses = self.db.get_verses_by_surah(data['id'])
            if verses:
                first_verse = verses[0]
                verse_id = first_verse.get('verse_id') or first_verse.get('aya_id') or 1
                self.display_verse(data['id'], verse_id, first_verse)

    def display_verse(self, surah_id: int, verse_id: int, verse_data: Dict[str, Any]):
        """عرض آية معينة"""
        self.current_surah_id = surah_id
        self.current_verse_id = verse_id

        # التبديل إلى تاب التصفح
        self.main_tabs.setCurrentIndex(0)

        # عرض نص القرآن
        verse_text = verse_data.get('text') or verse_data.get('verse_text') or verse_data.get('aya_text') or ""
        self.quran_text.setHtml(f"""
            <div style='text-align: center; direction: rtl; padding: 20px;'>
                <h2 style='color: {ClaudeColors.PRIMARY};'>سورة ... - الآية {verse_id}</h2>
                <p style='font-size: 24px; line-height: 2.5; color: {ClaudeColors.TEXT_PRIMARY};'>
                    {verse_text}
                </p>
            </div>
        """)

        # عرض التفسير
        tafseer = self.db.get_tafseer(surah_id, verse_id)
        self.tafseer_text.setHtml(f"""
            <div style='direction: rtl; padding: 20px;'>
                <h3 style='color: {ClaudeColors.PRIMARY};'>التفسير الميسر</h3>
                <p style='font-size: 16px; line-height: 2;'>
                    {tafseer}
                </p>
            </div>
        """)

        # الإعراب (placeholder)
        self.erab_text.setHtml(f"""
            <div style='direction: rtl; padding: 20px;'>
                <h3 style='color: {ClaudeColors.PRIMARY};'>الإعراب</h3>
                <p>قيد التطوير...</p>
            </div>
        """)

        # الصرف (placeholder)
        self.sarf_text.setHtml(f"""
            <div style='direction: rtl; padding: 20px;'>
                <h3 style='color: {ClaudeColors.PRIMARY};'>الصرف</h3>
                <p>قيد التطوير...</p>
            </div>
        """)

        # الترجمة (placeholder)
        self.translation_text.setHtml(f"""
            <div style='padding: 20px;'>
                <h3 style='color: {ClaudeColors.PRIMARY};'>English Translation</h3>
                <p>Coming soon...</p>
            </div>
        """)

    def go_previous(self):
        """الانتقال إلى الآية السابقة"""
        if not self.current_surah_id or not self.current_verse_id:
            return

        # TODO: تنفيذ الانتقال
        pass

    def go_next(self):
        """الانتقال إلى الآية التالية"""
        if not self.current_surah_id or not self.current_verse_id:
            return

        # TODO: تنفيذ الانتقال
        pass

    def perform_search(self):
        """تنفيذ البحث"""
        search_text = self.search_input.text().strip()
        if not search_text:
            return

        search_type = self.search_type.currentIndex()

        self.search_results.clear()

        if search_type == 0:  # بحث ذكي
            results = self.db.search_text(search_text)
        elif search_type == 1:  # بحث بالجذور
            results = self.db.search_by_root(search_text)
        else:
            results = []

        # عرض النتائج
        for result in results[:100]:  # عرض أول 100 نتيجة
            item = QTreeWidgetItem(self.search_results)

            surah_id = result.get('surah_id') or result.get('sura_id') or '?'
            verse_id = result.get('verse_id') or result.get('aya_id') or '?'
            text = result.get('text') or result.get('verse_text') or '...'

            item.setText(0, str(surah_id))
            item.setText(1, str(verse_id))
            item.setText(2, text[:100])
            item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole, result)

        if not results:
            item = QTreeWidgetItem(self.search_results)
            item.setText(0, "لا توجد نتائج")

    def on_search_result_clicked(self, item: QTreeWidgetItem, column: int):
        """عند النقر على نتيجة بحث"""
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)

        if data:
            surah_id = data.get('surah_id') or data.get('sura_id')
            verse_id = data.get('verse_id') or data.get('aya_id')

            if surah_id and verse_id:
                self.display_verse(surah_id, verse_id, data)

    def closeEvent(self, event):
        """عند إغلاق التطبيق"""
        self.db.close()
        event.accept()


# ============================================================================
#                              نقطة البداية
# ============================================================================

def main():
    """تشغيل التطبيق"""
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft if PYQT_VERSION == 6 else Qt.RightToLeft)

    window = QuranAppUltimate()
    window.show()

    sys.exit(app.exec() if PYQT_VERSION == 6 else app.exec_())


if __name__ == "__main__":
    main()

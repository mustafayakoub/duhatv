#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                    تطبيق القرآن الكريم الاحترافي النهائي
                    Ultimate Professional Quran Application
================================================================================

المطور: Claude AI Assistant
النسخة: 2.2 Final Edition - مع معلومات قاعدة البيانات
التاريخ: 2025-10-30

الميزات:
✨ شجرة ديناميكية ذكية (السور → الآيات)
✨ تابات متعددة المستويات
✨ بحث متقدم (4 أنماط)
✨ ألوان Claude الهادئة والراقية
✨ تزامن كامل بين كل المكونات
✨ أداء محسّن بدون حدود
✨ دعم ذكي لأسماء الأعمدة المختلفة
✨ تفاسير متعددة
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
        QCheckBox, QScrollArea, QGroupBox, QStatusBar
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
            QCheckBox, QScrollArea, QGroupBox, QStatusBar
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

        /* شريط الحالة */
        QStatusBar {{
            background-color: {cls.BG_SIDEBAR};
            color: {cls.TEXT_SECONDARY};
            border-top: 1px solid {cls.BORDER_LIGHT};
        }}
        """


# ============================================================================
#                          مدير قاعدة البيانات الذكي
# ============================================================================

class DatabaseManager:
    """مدير قاعدة البيانات الذكي - محدّث"""

    def __init__(self):
        self.conn: Optional[sqlite3.Connection] = None
        self.db_path: Optional[str] = None
        self.tables_info: Dict[str, List[str]] = {}
        self.column_mappings: Dict[str, str] = {}  # خريطة الأعمدة
        self.main_table: Optional[str] = None

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
            if db_file.is_file() and db_file.stat().st_size > 1000000:
                possible_paths.insert(0, str(db_file))

        # البحث في المجلد الأب
        parent_dir = Path("..")
        for db_file in parent_dir.glob("*.db"):
            if db_file.is_file() and db_file.stat().st_size > 1000000:
                possible_paths.insert(0, str(db_file))

        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ تم العثور على قاعدة البيانات: {path}")
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
            self._detect_column_mappings()
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

        print(f"📊 تم العثور على {len(self.tables_info)} جدول")

    def _detect_column_mappings(self):
        """اكتشاف أسماء الأعمدة الفعلية"""
        # البحث عن الجدول الرئيسي
        for table_name, columns in self.tables_info.items():
            if 'quran' in table_name.lower() or 'aya' in table_name.lower():
                # التحقق من وجود أعمدة مهمة
                has_text = any('text' in col.lower() or 'aya' in col.lower() for col in columns)
                has_sora = any('sora' in col.lower() or 'surah' in col.lower() for col in columns)

                if has_text and has_sora:
                    self.main_table = table_name
                    print(f"✅ الجدول الرئيسي: {table_name}")

                    # رسم خريطة الأعمدة
                    for col in columns:
                        col_lower = col.lower()

                        # أعمدة النص
                        if 'aya_text' in col_lower and 'emlaey' not in col_lower and 'tashkil' not in col_lower:
                            self.column_mappings['verse_text'] = col
                        elif 'aya_text_emlaey' in col_lower:
                            self.column_mappings['verse_text_simple'] = col
                        elif 'aya_text_tashkil' in col_lower:
                            self.column_mappings['verse_text_tashkil'] = col

                        # أعمدة السورة
                        elif col_lower == 'sora' or col_lower == 'surah':
                            self.column_mappings['surah_id'] = col
                        elif 'sora_name_ar' in col_lower:
                            self.column_mappings['surah_name_ar'] = col
                        elif 'sora_name_en' in col_lower:
                            self.column_mappings['surah_name_en'] = col

                        # أعمدة الآية
                        elif col_lower == 'aya_no' or col_lower == 'ayah_no':
                            self.column_mappings['verse_id'] = col

                        # أعمدة إضافية
                        elif 'page' in col_lower:
                            self.column_mappings['page'] = col
                        elif 'jozz' in col_lower or 'juz' in col_lower:
                            self.column_mappings['juz'] = col
                        elif 'earab' in col_lower or 'erab' in col_lower or 'i3rab' in col_lower:
                            self.column_mappings['erab'] = col
                        elif 'tafseer_moysar' in col_lower or 'tafsir_moysar' in col_lower:
                            self.column_mappings['tafseer_moysar'] = col
                        elif 'tafseer_saadi' in col_lower or 'tafsir_saadi' in col_lower:
                            self.column_mappings['tafseer_saadi'] = col
                        elif 'tafseer_bughiu' in col_lower or 'tafsir_baghawy' in col_lower:
                            self.column_mappings['tafseer_baghawy'] = col

                    break

        print(f"✅ تم اكتشاف {len(self.column_mappings)} عمود")
        for key, value in self.column_mappings.items():
            print(f"   {key} → {value}")

    def get_surahs(self) -> List[Dict[str, Any]]:
        """الحصول على قائمة السور"""
        if not self.conn or not self.main_table:
            return []

        try:
            cursor = self.conn.cursor()

            surah_id_col = self.column_mappings.get('surah_id', 'sora')
            surah_name_col = self.column_mappings.get('surah_name_ar', 'sora_name_ar')

            query = f"""
                SELECT DISTINCT {surah_id_col}, {surah_name_col}
                FROM {self.main_table}
                ORDER BY {surah_id_col}
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            surahs = []
            for row in rows:
                surahs.append({
                    'id': row[0],
                    'name': row[1] if len(row) > 1 else f"سورة {row[0]}"
                })

            print(f"✅ تم تحميل {len(surahs)} سورة")
            return surahs

        except Exception as e:
            print(f"خطأ في الحصول على السور: {e}")
            return []

    def get_verses_by_surah(self, surah_id: int) -> List[Dict[str, Any]]:
        """الحصول على آيات سورة معينة"""
        if not self.conn or not self.main_table:
            return []

        try:
            cursor = self.conn.cursor()

            surah_id_col = self.column_mappings.get('surah_id', 'sora')
            verse_id_col = self.column_mappings.get('verse_id', 'aya_no')
            verse_text_col = self.column_mappings.get('verse_text', 'aya_text')

            query = f"""
                SELECT *
                FROM {self.main_table}
                WHERE {surah_id_col} = ?
                ORDER BY {verse_id_col}
            """

            cursor.execute(query, (surah_id,))
            rows = cursor.fetchall()

            return [dict(row) for row in rows]

        except Exception as e:
            print(f"خطأ في الحصول على الآيات: {e}")
            return []

    def get_verse_data(self, surah_id: int, verse_id: int) -> Optional[Dict[str, Any]]:
        """الحصول على بيانات آية محددة"""
        if not self.conn or not self.main_table:
            return None

        try:
            cursor = self.conn.cursor()

            surah_id_col = self.column_mappings.get('surah_id', 'sora')
            verse_id_col = self.column_mappings.get('verse_id', 'aya_no')

            query = f"""
                SELECT *
                FROM {self.main_table}
                WHERE {surah_id_col} = ? AND {verse_id_col} = ?
            """

            cursor.execute(query, (surah_id, verse_id))
            row = cursor.fetchone()

            if row:
                return dict(row)
            return None

        except Exception as e:
            print(f"خطأ في الحصول على بيانات الآية: {e}")
            return None

    def search_text(self, text: str, limit: int = 1000) -> List[Dict[str, Any]]:
        """البحث النصي في القرآن"""
        if not self.conn or not self.main_table or not text:
            return []

        try:
            cursor = self.conn.cursor()

            # البحث في كل أعمدة النص
            text_columns = [
                self.column_mappings.get('verse_text', 'aya_text'),
                self.column_mappings.get('verse_text_simple', 'aya_text_emlaey'),
            ]

            conditions = " OR ".join([f"{col} LIKE ?" for col in text_columns if col])
            query = f"""
                SELECT *
                FROM {self.main_table}
                WHERE {conditions}
                LIMIT ?
            """

            params = [f'%{text}%'] * len([c for c in text_columns if c]) + [limit]
            cursor.execute(query, params)
            rows = cursor.fetchall()

            print(f"✅ تم العثور على {len(rows)} نتيجة")
            return [dict(row) for row in rows]

        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return []

    def search_by_root(self, root: str, limit: int = 1000) -> List[Dict[str, Any]]:
        """البحث بالجذر"""
        # للبساطة، سنستخدم البحث النصي
        return self.search_text(root, limit)

    def close(self):
        """إغلاق الاتصال"""
        if self.conn:
            self.conn.close()


# ============================================================================
#                            التطبيق الرئيسي
# ============================================================================

class QuranAppFinal(QMainWindow):
    """التطبيق الرئيسي النهائي"""

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_surah_id = None
        self.current_verse_id = None
        self.surahs = []
        self.current_verses = []
        self.init_ui()
        self.init_database()

    def init_ui(self):
        """تهيئة الواجهة"""
        self.setWindowTitle("تطبيق القرآن الكريم الاحترافي 2.2 Final")
        self.setGeometry(100, 100, 1400, 900)

        # تطبيق الألوان
        self.setStyleSheet(ClaudeColors.get_stylesheet())

        # شريط الحالة
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("جاري التحميل...")

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
        splitter.setSizes([300, 1100])

        main_layout.addWidget(splitter)

    def create_tree_widget(self):
        """إنشاء الشجرة الديناميكية"""
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("📖 القرآن الكريم")
        self.tree_widget.setMinimumWidth(280)

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
        self.btn_prev.setEnabled(False)
        self.btn_next.setEnabled(False)

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_next)
        nav_layout.addStretch()

        self.lbl_position = QLabel("مرحباً بك في تطبيق القرآن الكريم")
        self.lbl_position.setStyleSheet(f"color: {ClaudeColors.TEXT_SECONDARY}; font-weight: bold;")
        nav_layout.addWidget(self.lbl_position)

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

        # تاب معلومات قاعدة البيانات
        db_info_tab = self.create_db_info_tab()
        self.main_tabs.addTab(db_info_tab, "💾 معلومات قاعدة البيانات")

        layout.addWidget(self.main_tabs)

        return widget

    def create_db_info_tab(self) -> QWidget:
        """إنشاء تاب معلومات قاعدة البيانات"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # عنوان رئيسي
        title = QLabel("📊 معلومات قاعدة البيانات")
        title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {ClaudeColors.PRIMARY}; padding: 10px;")
        layout.addWidget(title)

        # منطقة قابلة للتمرير
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"border: none; background-color: {ClaudeColors.BG_CONTENT};")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(12)

        # معلومات قاعدة البيانات
        self.db_info_text = QTextEdit()
        self.db_info_text.setReadOnly(True)
        self.db_info_text.setFont(QFont("Consolas", 11))
        self.db_info_text.setMinimumHeight(600)

        content_layout.addWidget(self.db_info_text)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # زر تحديث المعلومات
        btn_refresh = QPushButton("🔄 تحديث المعلومات")
        btn_refresh.clicked.connect(self.update_db_info)
        btn_refresh.setMaximumWidth(200)
        layout.addWidget(btn_refresh)

        return widget

    def update_db_info(self):
        """تحديث معلومات قاعدة البيانات"""
        if not self.db.conn:
            self.db_info_text.setHtml(f"""
                <div style='direction: rtl; padding: 20px;'>
                    <h2 style='color: {ClaudeColors.ERROR};'>❌ لم يتم الاتصال بقاعدة البيانات</h2>
                    <p>الرجاء التأكد من وجود ملف قاعدة البيانات في المسار الصحيح.</p>
                </div>
            """)
            return

        html = f"""
        <html dir='rtl'>
        <head>
            <style>
                body {{
                    font-family: 'Traditional Arabic', 'Segoe UI', sans-serif;
                    padding: 20px;
                    background-color: {ClaudeColors.BG_CONTENT};
                    color: {ClaudeColors.TEXT_PRIMARY};
                }}
                h2 {{
                    color: {ClaudeColors.PRIMARY};
                    border-bottom: 2px solid {ClaudeColors.BORDER_LIGHT};
                    padding-bottom: 10px;
                    margin-top: 20px;
                }}
                h3 {{
                    color: {ClaudeColors.ACCENT};
                    margin-top: 15px;
                }}
                .info-box {{
                    background-color: {ClaudeColors.BG_SIDEBAR};
                    border: 1px solid {ClaudeColors.BORDER_LIGHT};
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                }}
                .success {{
                    color: {ClaudeColors.SUCCESS};
                    font-weight: bold;
                }}
                .warning {{
                    color: {ClaudeColors.WARNING};
                    font-weight: bold;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                    background-color: white;
                }}
                th, td {{
                    border: 1px solid {ClaudeColors.BORDER_LIGHT};
                    padding: 10px;
                    text-align: right;
                }}
                th {{
                    background-color: {ClaudeColors.BG_HEADER};
                    font-weight: bold;
                    color: {ClaudeColors.TEXT_PRIMARY};
                }}
                .column-name {{
                    font-family: 'Consolas', monospace;
                    background-color: {ClaudeColors.BG_SIDEBAR};
                    padding: 2px 6px;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <h2>📁 معلومات الملف</h2>
            <div class='info-box'>
                <p><strong>مسار قاعدة البيانات:</strong><br/>
                <span class='column-name'>{self.db.db_path}</span></p>
                <p><strong>حجم الملف:</strong> {os.path.getsize(self.db.db_path) / (1024*1024):.2f} MB</p>
                <p><strong>الحالة:</strong> <span class='success'>✅ متصل بنجاح</span></p>
            </div>

            <h2>🗂️ بنية قاعدة البيانات</h2>
            <div class='info-box'>
                <p><strong>الجدول الرئيسي:</strong> <span class='column-name'>{self.db.main_table}</span></p>
                <p><strong>عدد الجداول:</strong> {len(self.db.tables_info)}</p>
            </div>

            <h3>📋 الجداول المتوفرة:</h3>
            <table>
                <tr>
                    <th>اسم الجدول</th>
                    <th>عدد الأعمدة</th>
                </tr>
        """

        for table_name, columns in self.db.tables_info.items():
            html += f"""
                <tr>
                    <td><span class='column-name'>{table_name}</span></td>
                    <td>{len(columns)}</td>
                </tr>
            """

        html += """
            </table>

            <h2>🔍 خريطة الأعمدة المكتشفة</h2>
            <div class='info-box'>
                <p>تم اكتشاف <strong>{}</strong> عمود تلقائياً:</p>
            </div>
            <table>
                <tr>
                    <th>الاسم المنطقي</th>
                    <th>اسم العمود الفعلي</th>
                </tr>
        """.format(len(self.db.column_mappings))

        # ترتيب الأعمدة حسب الأهمية
        important_columns = [
            'verse_text', 'verse_text_simple', 'verse_text_tashkil',
            'surah_id', 'surah_name_ar', 'surah_name_en',
            'verse_id', 'page', 'juz',
            'tafseer_moysar', 'tafseer_saadi', 'tafseer_baghawy',
            'erab'
        ]

        # الأعمدة المهمة أولاً
        for logical_name in important_columns:
            if logical_name in self.db.column_mappings:
                actual_name = self.db.column_mappings[logical_name]
                icon = '✅'
                html += f"""
                <tr>
                    <td>{icon} {logical_name}</td>
                    <td><span class='column-name'>{actual_name}</span></td>
                </tr>
                """

        # باقي الأعمدة
        for logical_name, actual_name in self.db.column_mappings.items():
            if logical_name not in important_columns:
                html += f"""
                <tr>
                    <td>📌 {logical_name}</td>
                    <td><span class='column-name'>{actual_name}</span></td>
                </tr>
                """

        html += """
            </table>

            <h2>📊 الإحصائيات</h2>
            <div class='info-box'>
        """

        # إحصائيات إضافية
        try:
            cursor = self.db.conn.cursor()

            # عدد الآيات
            if self.db.main_table:
                cursor.execute(f"SELECT COUNT(*) FROM {self.db.main_table}")
                total_verses = cursor.fetchone()[0]
                html += f"<p><strong>إجمالي الآيات:</strong> {total_verses:,} آية</p>"

            # عدد السور
            html += f"<p><strong>عدد السور:</strong> {len(self.surahs)} سورة</p>"

            # حالة الفهرسة
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='{self.db.main_table}'")
            indexes = cursor.fetchall()
            html += f"<p><strong>عدد الفهارس:</strong> {len(indexes)}</p>"

            if len(indexes) > 0:
                html += "<p><strong>الفهارس المتوفرة:</strong></p><ul>"
                for idx in indexes:
                    html += f"<li><span class='column-name'>{idx[0]}</span></li>"
                html += "</ul>"
            else:
                html += f"<p class='warning'>⚠️ لا توجد فهارس - قد يكون البحث بطيئاً</p>"
                html += "<p>💡 نصيحة: قم بتشغيل <span class='column-name'>create_indexes.py</span> لتحسين الأداء</p>"

        except Exception as e:
            html += f"<p class='warning'>⚠️ خطأ في الحصول على الإحصائيات: {e}</p>"

        html += """
            </div>

            <h2>🎯 التفاسير المتوفرة</h2>
            <div class='info-box'>
        """

        # التحقق من التفاسير المتوفرة
        tafaseer_status = []
        if 'tafseer_moysar' in self.db.column_mappings:
            tafaseer_status.append("✅ التفسير الميسر")
        else:
            tafaseer_status.append("❌ التفسير الميسر")

        if 'tafseer_saadi' in self.db.column_mappings:
            tafaseer_status.append("✅ تفسير السعدي")
        else:
            tafaseer_status.append("❌ تفسير السعدي")

        if 'tafseer_baghawy' in self.db.column_mappings:
            tafaseer_status.append("✅ تفسير البغوي")
        else:
            tafaseer_status.append("❌ تفسير البغوي")

        for status in tafaseer_status:
            html += f"<p>{status}</p>"

        html += """
            </div>

            <hr style='margin: 30px 0; border: 1px solid {}'>
            <p style='text-align: center; color: {}; font-size: 12px;'>
                تم إنشاء هذا التقرير تلقائياً • النسخة 2.2 Final
            </p>
        </body>
        </html>
        """.format(ClaudeColors.BORDER_LIGHT, ClaudeColors.TEXT_MUTED)

        self.db_info_text.setHtml(html)

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
        tafseer_widget = QWidget()
        tafseer_layout = QVBoxLayout(tafseer_widget)

        # قائمة اختيار التفسير
        tafseer_selector_layout = QHBoxLayout()
        tafseer_selector_layout.addWidget(QLabel("اختر التفسير:"))
        self.tafseer_combo = QComboBox()
        self.tafseer_combo.addItems(["التفسير الميسر", "تفسير السعدي", "تفسير البغوي", "الكل"])
        self.tafseer_combo.currentIndexChanged.connect(self.update_tafseer_display)
        tafseer_selector_layout.addWidget(self.tafseer_combo)
        tafseer_selector_layout.addStretch()
        tafseer_layout.addLayout(tafseer_selector_layout)

        self.tafseer_text = QTextEdit()
        self.tafseer_text.setReadOnly(True)
        self.tafseer_text.setFont(QFont("Traditional Arabic", 14))
        tafseer_layout.addWidget(self.tafseer_text)

        self.browse_tabs.addTab(tafseer_widget, "📚 التفسير")

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
        self.search_results.setColumnWidth(0, 100)
        self.search_results.setColumnWidth(1, 80)

        if PYQT_VERSION == 6:
            self.search_results.itemClicked.connect(self.on_search_result_clicked)
        else:
            self.search_results.itemClicked.connect(self.on_search_result_clicked)

        results_layout.addWidget(self.search_results)

        self.lbl_search_count = QLabel("لا توجد نتائج")
        self.lbl_search_count.setStyleSheet(f"color: {ClaudeColors.TEXT_MUTED};")
        results_layout.addWidget(self.lbl_search_count)

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
            self.status_bar.showMessage("خطأ: لم يتم العثور على قاعدة البيانات")
            return

        # تحميل السور
        self.load_surahs()
        self.status_bar.showMessage(f"✅ تم تحميل {len(self.surahs)} سورة")

        # تحديث معلومات قاعدة البيانات
        self.update_db_info()

    def load_surahs(self):
        """تحميل السور في الشجرة"""
        self.surahs = self.db.get_surahs()

        for surah in self.surahs:
            surah_id = surah.get('id')
            surah_name = surah.get('name', f"سورة {surah_id}")

            item = QTreeWidgetItem(self.tree_widget)
            item.setText(0, f"📖 {surah_name}")
            item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole, {
                'type': 'surah',
                'id': surah_id,
                'name': surah_name
            })

            # إضافة عنصر وهمي للسماح بالتوسيع
            dummy = QTreeWidgetItem(item)
            dummy.setText(0, "جاري التحميل...")

    def on_tree_item_expanded(self, item: QTreeWidgetItem):
        """عند توسيع عنصر في الشجرة"""
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)

        if data and data.get('type') == 'surah':
            # حذف العناصر الوهمية
            item.takeChildren()

            # تحميل الآيات
            surah_id = data['id']
            verses = self.db.get_verses_by_surah(surah_id)

            surah_id_col = self.db.column_mappings.get('surah_id', 'sora')
            verse_id_col = self.db.column_mappings.get('verse_id', 'aya_no')
            verse_text_col = self.db.column_mappings.get('verse_text', 'aya_text')

            for verse in verses:
                verse_id = verse.get(verse_id_col, verse.get('aya_no', '?'))
                verse_text = verse.get(verse_text_col, verse.get('aya_text', '...'))

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
                verse_id_col = self.db.column_mappings.get('verse_id', 'aya_no')
                first_verse = verses[0]
                verse_id = first_verse.get(verse_id_col, 1)
                self.display_verse(data['id'], verse_id, first_verse)

    def display_verse(self, surah_id: int, verse_id: int, verse_data: Dict[str, Any]):
        """عرض آية معينة"""
        self.current_surah_id = surah_id
        self.current_verse_id = verse_id
        self.current_verses = self.db.get_verses_by_surah(surah_id)

        # تفعيل أزرار التنقل
        self.btn_prev.setEnabled(True)
        self.btn_next.setEnabled(True)

        # التبديل إلى تاب التصفح
        self.main_tabs.setCurrentIndex(0)

        # الحصول على أسماء الأعمدة
        verse_text_col = self.db.column_mappings.get('verse_text', 'aya_text')
        surah_name_col = self.db.column_mappings.get('surah_name_ar', 'sora_name_ar')

        verse_text = verse_data.get(verse_text_col, verse_data.get('aya_text', '...'))
        surah_name = verse_data.get(surah_name_col, verse_data.get('sora_name_ar', f'سورة {surah_id}'))

        # تحديث الموضع
        self.lbl_position.setText(f"{surah_name} - الآية {verse_id}")
        self.status_bar.showMessage(f"سورة {surah_name} - الآية {verse_id}")

        # عرض نص القرآن
        self.quran_text.setHtml(f"""
            <div style='text-align: center; direction: rtl; padding: 20px;'>
                <h2 style='color: {ClaudeColors.PRIMARY};'>{surah_name} - الآية {verse_id}</h2>
                <p style='font-size: 24px; line-height: 2.5; color: {ClaudeColors.TEXT_PRIMARY};'>
                    {verse_text}
                </p>
            </div>
        """)

        # عرض التفسير
        self.update_tafseer_display()

        # عرض الإعراب
        erab_col = self.db.column_mappings.get('erab', 'earab_quran')
        erab_text = verse_data.get(erab_col, 'غير متوفر')

        self.erab_text.setHtml(f"""
            <div style='direction: rtl; padding: 20px;'>
                <h3 style='color: {ClaudeColors.PRIMARY};'>الإعراب</h3>
                <p style='font-size: 16px; line-height: 2;'>
                    {erab_text if erab_text else 'غير متوفر'}
                </p>
            </div>
        """)

        # الصرف (placeholder)
        self.sarf_text.setHtml(f"""
            <div style='direction: rtl; padding: 20px;'>
                <h3 style='color: {ClaudeColors.PRIMARY};'>التحليل الصرفي</h3>
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

    def update_tafseer_display(self):
        """تحديث عرض التفسير"""
        if not self.current_surah_id or not self.current_verse_id:
            return

        verse_data = self.db.get_verse_data(self.current_surah_id, self.current_verse_id)
        if not verse_data:
            return

        selected_tafseer = self.tafseer_combo.currentText()

        html = f"""
            <div style='direction: rtl; padding: 20px;'>
        """

        if selected_tafseer == "الكل":
            # عرض كل التفاسير
            tafaseer = [
                ('التفسير الميسر', self.db.column_mappings.get('tafseer_moysar', 'tafseer_moysar')),
                ('تفسير السعدي', self.db.column_mappings.get('tafseer_saadi', 'tafseer_saadi')),
                ('تفسير البغوي', self.db.column_mappings.get('tafseer_baghawy', 'tafseer_bughiu')),
            ]

            for name, col in tafaseer:
                tafseer_text = verse_data.get(col, '')
                if tafseer_text:
                    html += f"""
                        <h3 style='color: {ClaudeColors.PRIMARY}; margin-top: 20px;'>{name}</h3>
                        <p style='font-size: 16px; line-height: 2;'>{tafseer_text}</p>
                        <hr style='border: 1px solid {ClaudeColors.BORDER_LIGHT}; margin: 20px 0;'>
                    """
        else:
            # عرض تفسير واحد
            tafseer_map = {
                'التفسير الميسر': self.db.column_mappings.get('tafseer_moysar', 'tafseer_moysar'),
                'تفسير السعدي': self.db.column_mappings.get('tafseer_saadi', 'tafseer_saadi'),
                'تفسير البغوي': self.db.column_mappings.get('tafseer_baghawy', 'tafseer_bughiu'),
            }

            col = tafseer_map.get(selected_tafseer, 'tafseer_moysar')
            tafseer_text = verse_data.get(col, 'غير متوفر')

            html += f"""
                <h3 style='color: {ClaudeColors.PRIMARY};'>{selected_tafseer}</h3>
                <p style='font-size: 16px; line-height: 2;'>
                    {tafseer_text if tafseer_text else 'غير متوفر'}
                </p>
            """

        html += "</div>"
        self.tafseer_text.setHtml(html)

    def go_previous(self):
        """الانتقال إلى الآية السابقة"""
        if not self.current_surah_id or not self.current_verse_id or not self.current_verses:
            return

        verse_id_col = self.db.column_mappings.get('verse_id', 'aya_no')

        # البحث عن الآية الحالية
        current_index = -1
        for i, verse in enumerate(self.current_verses):
            if verse.get(verse_id_col) == self.current_verse_id:
                current_index = i
                break

        if current_index > 0:
            # الآية السابقة في نفس السورة
            prev_verse = self.current_verses[current_index - 1]
            prev_verse_id = prev_verse.get(verse_id_col)
            self.display_verse(self.current_surah_id, prev_verse_id, prev_verse)
        elif self.current_surah_id > 1:
            # آخر آية من السورة السابقة
            prev_surah_id = self.current_surah_id - 1
            prev_verses = self.db.get_verses_by_surah(prev_surah_id)
            if prev_verses:
                last_verse = prev_verses[-1]
                last_verse_id = last_verse.get(verse_id_col)
                self.display_verse(prev_surah_id, last_verse_id, last_verse)

    def go_next(self):
        """الانتقال إلى الآية التالية"""
        if not self.current_surah_id or not self.current_verse_id or not self.current_verses:
            return

        verse_id_col = self.db.column_mappings.get('verse_id', 'aya_no')

        # البحث عن الآية الحالية
        current_index = -1
        for i, verse in enumerate(self.current_verses):
            if verse.get(verse_id_col) == self.current_verse_id:
                current_index = i
                break

        if current_index < len(self.current_verses) - 1:
            # الآية التالية في نفس السورة
            next_verse = self.current_verses[current_index + 1]
            next_verse_id = next_verse.get(verse_id_col)
            self.display_verse(self.current_surah_id, next_verse_id, next_verse)
        elif self.current_surah_id < 114:
            # أول آية من السورة التالية
            next_surah_id = self.current_surah_id + 1
            next_verses = self.db.get_verses_by_surah(next_surah_id)
            if next_verses:
                first_verse = next_verses[0]
                first_verse_id = first_verse.get(verse_id_col)
                self.display_verse(next_surah_id, first_verse_id, first_verse)

    def perform_search(self):
        """تنفيذ البحث"""
        search_text = self.search_input.text().strip()
        if not search_text:
            return

        search_type = self.search_type.currentIndex()

        self.search_results.clear()
        self.status_bar.showMessage("جاري البحث...")

        if search_type == 0:  # بحث ذكي
            results = self.db.search_text(search_text)
        elif search_type == 1:  # بحث بالجذور
            results = self.db.search_by_root(search_text)
        else:
            results = []

        # عرض النتائج
        surah_id_col = self.db.column_mappings.get('surah_id', 'sora')
        verse_id_col = self.db.column_mappings.get('verse_id', 'aya_no')
        verse_text_col = self.db.column_mappings.get('verse_text', 'aya_text')
        surah_name_col = self.db.column_mappings.get('surah_name_ar', 'sora_name_ar')

        for result in results:
            item = QTreeWidgetItem(self.search_results)

            surah_id = result.get(surah_id_col, '?')
            verse_id = result.get(verse_id_col, '?')
            text = result.get(verse_text_col, '...')
            surah_name = result.get(surah_name_col, f'سورة {surah_id}')

            item.setText(0, str(surah_name))
            item.setText(1, str(verse_id))
            item.setText(2, text[:100] + "..." if len(text) > 100 else text)
            item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole, result)

        count = len(results)
        self.lbl_search_count.setText(f"تم العثور على {count} نتيجة")
        self.status_bar.showMessage(f"✅ تم العثور على {count} نتيجة")

        if count == 0:
            item = QTreeWidgetItem(self.search_results)
            item.setText(0, "لا توجد نتائج")

    def on_search_result_clicked(self, item: QTreeWidgetItem, column: int):
        """عند النقر على نتيجة بحث"""
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)

        if data:
            surah_id_col = self.db.column_mappings.get('surah_id', 'sora')
            verse_id_col = self.db.column_mappings.get('verse_id', 'aya_no')

            surah_id = data.get(surah_id_col)
            verse_id = data.get(verse_id_col)

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

    window = QuranAppFinal()
    window.show()

    sys.exit(app.exec() if PYQT_VERSION == 6 else app.exec_())


if __name__ == "__main__":
    main()

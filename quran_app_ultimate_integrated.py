#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                تطبيق القرآن الكريم المتكامل النهائي
            Ultimate Integrated Quran Application
================================================================================

المطور: Claude AI Assistant
النسخة: 3.0 Ultimate Integrated Edition
التاريخ: 2025-10-31

الميزات الجديدة:
✨ دعم 3 قواعد بيانات متكاملة
✨ نظام الموضوعات القرآنية (Topics)
✨ التصفح الذكي والمرن
✨ بحث متقدم عبر كل القواعد
✨ تكامل كامل بين الموديلات
✨ واجهة موحدة وجميلة
✨ أداء محسّن للغاية
"""

import sys
import os
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from collections import defaultdict

# محاولة استيراد PyQt6، وإذا فشل نستخدم PyQt5
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTreeWidget, QTreeWidgetItem, QTabWidget, QTextEdit, QLabel,
        QPushButton, QLineEdit, QComboBox, QSplitter, QFrame, QMessageBox,
        QCheckBox, QScrollArea, QGroupBox, QStatusBar, QTableWidget,
        QTableWidgetItem, QHeaderView
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
            QCheckBox, QScrollArea, QGroupBox, QStatusBar, QTableWidget,
            QTableWidgetItem, QHeaderView
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

        /* الجداول */
        QTableWidget {{
            background-color: {cls.BG_CONTENT};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            gridline-color: {cls.BORDER_LIGHT};
        }}

        QTableWidget::item {{
            padding: 8px;
            color: {cls.TEXT_PRIMARY};
        }}

        QTableWidget::item:selected {{
            background-color: {cls.SELECTED};
        }}

        QHeaderView::section {{
            background-color: {cls.BG_HEADER};
            color: {cls.TEXT_PRIMARY};
            padding: 8px;
            border: 1px solid {cls.BORDER_LIGHT};
            font-weight: bold;
        }}

        /* شريط الحالة */
        QStatusBar {{
            background-color: {cls.BG_SIDEBAR};
            color: {cls.TEXT_SECONDARY};
            border-top: 1px solid {cls.BORDER_LIGHT};
        }}
        """


# ============================================================================
#                    مدير قواعد البيانات المتعددة المتكامل
# ============================================================================

class MultiDatabaseManager:
    """مدير ذكي لقواعد بيانات متعددة"""

    def __init__(self):
        self.databases: Dict[str, sqlite3.Connection] = {}
        self.primary_db: Optional[str] = None
        self.db_info: Dict[str, Dict[str, Any]] = {}
        self.column_mappings: Dict[str, Dict[str, str]] = {}

    def connect_databases(self) -> bool:
        """الاتصال بجميع قواعد البيانات المتوفرة"""

        # المسارات المحتملة لقواعد البيانات
        possible_paths = {
            'primary': [
                r"C:\quran9\quran_ultimate_final.db",
                "quran_ultimate_final.db",
                "./quran_ultimate_final.db",
            ],
            'secondary': [
                r"C:\quran9\surah_database_app_v32.db",
                "surah_database_app_v32.db",
                "./surah_database_app_v32.db",
            ],
            'crystalline': [
                r"C:\quran9\Quran_Crystalline.db",
                "Quran_Crystalline.db",
                "./Quran_Crystalline.db",
            ]
        }

        # البحث في المجلد الحالي عن أي ملفات .db
        current_dir = Path(".")
        for db_file in current_dir.glob("*.db"):
            if db_file.is_file() and db_file.stat().st_size > 100000:
                db_name = db_file.stem.lower()
                if 'ultimate' in db_name or 'final' in db_name:
                    possible_paths['primary'].insert(0, str(db_file))
                elif 'crystalline' in db_name:
                    possible_paths['crystalline'].insert(0, str(db_file))
                else:
                    possible_paths['secondary'].insert(0, str(db_file))

        # محاولة الاتصال بكل قاعدة
        connected_count = 0
        for db_key, paths in possible_paths.items():
            for path in paths:
                if os.path.exists(path):
                    try:
                        conn = sqlite3.connect(path)
                        conn.row_factory = sqlite3.Row
                        self.databases[db_key] = conn

                        # تحليل البنية
                        self._analyze_database(db_key, conn)

                        print(f"✅ [{db_key}] متصل: {path}")
                        connected_count += 1

                        # تعيين القاعدة الأساسية
                        if db_key == 'primary' or self.primary_db is None:
                            self.primary_db = db_key

                        break
                    except Exception as e:
                        print(f"⚠️ خطأ في الاتصال بـ {path}: {e}")

        if connected_count == 0:
            print("❌ لم يتم العثور على أي قاعدة بيانات!")
            return False

        print(f"\n✅ تم الاتصال بـ {connected_count} قاعدة بيانات")
        print(f"📊 القاعدة الأساسية: {self.primary_db}")
        return True

    def _analyze_database(self, db_key: str, conn: sqlite3.Connection):
        """تحليل بنية قاعدة بيانات واحدة"""
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        self.db_info[db_key] = {
            'tables': {},
            'main_table': None
        }

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            self.db_info[db_key]['tables'][table_name] = column_names

            # تحديد الجدول الرئيسي
            if 'quran' in table_name.lower() or 'aya' in table_name.lower():
                has_text = any('text' in col.lower() for col in column_names)
                has_sora = any('sora' in col.lower() or 'surah' in col.lower() for col in column_names)

                if has_text and has_sora:
                    self.db_info[db_key]['main_table'] = table_name
                    self._detect_columns(db_key, table_name, column_names)

    def _detect_columns(self, db_key: str, table_name: str, columns: List[str]):
        """اكتشاف تطابق الأعمدة"""
        self.column_mappings[db_key] = {}

        for col in columns:
            col_lower = col.lower()

            # أعمدة النص
            if 'aya_text' in col_lower and 'emlaey' not in col_lower:
                self.column_mappings[db_key]['verse_text'] = col
            elif 'aya_text_emlaey' in col_lower:
                self.column_mappings[db_key]['verse_text_simple'] = col

            # أعمدة السورة والآية
            elif col_lower in ['sora', 'surah']:
                self.column_mappings[db_key]['surah_id'] = col
            elif col_lower in ['aya_no', 'ayah_no']:
                self.column_mappings[db_key]['verse_id'] = col
            elif 'sora_name_ar' in col_lower:
                self.column_mappings[db_key]['surah_name'] = col

            # أعمدة إضافية
            elif 'tafseer' in col_lower or 'tafsir' in col_lower:
                if 'moysar' in col_lower:
                    self.column_mappings[db_key]['tafseer_moysar'] = col
                elif 'saadi' in col_lower:
                    self.column_mappings[db_key]['tafseer_saadi'] = col
            elif 'earab' in col_lower or 'erab' in col_lower:
                self.column_mappings[db_key]['erab'] = col

    def get_surahs(self) -> List[Dict[str, Any]]:
        """الحصول على قائمة السور من القاعدة الأساسية"""
        if not self.primary_db or self.primary_db not in self.databases:
            return []

        conn = self.databases[self.primary_db]
        main_table = self.db_info[self.primary_db]['main_table']

        if not main_table:
            return []

        try:
            cursor = conn.cursor()
            mappings = self.column_mappings.get(self.primary_db, {})

            surah_id_col = mappings.get('surah_id', 'sora')
            surah_name_col = mappings.get('surah_name', 'sora_name_ar')

            query = f"""
                SELECT DISTINCT {surah_id_col}, {surah_name_col}
                FROM {main_table}
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

            return surahs

        except Exception as e:
            print(f"خطأ في الحصول على السور: {e}")
            return []

    def get_verses_by_surah(self, surah_id: int, db_key: Optional[str] = None) -> List[Dict[str, Any]]:
        """الحصول على آيات سورة من قاعدة معينة"""
        if db_key is None:
            db_key = self.primary_db

        if db_key not in self.databases:
            return []

        conn = self.databases[db_key]
        main_table = self.db_info[db_key]['main_table']

        if not main_table:
            return []

        try:
            cursor = conn.cursor()
            mappings = self.column_mappings.get(db_key, {})

            surah_id_col = mappings.get('surah_id', 'sora')
            verse_id_col = mappings.get('verse_id', 'aya_no')

            query = f"""
                SELECT *
                FROM {main_table}
                WHERE {surah_id_col} = ?
                ORDER BY {verse_id_col}
            """

            cursor.execute(query, (surah_id,))
            rows = cursor.fetchall()

            return [dict(row) for row in rows]

        except Exception as e:
            print(f"خطأ في الحصول على الآيات: {e}")
            return []

    def search_across_all(self, text: str, limit: int = 500) -> Dict[str, List[Dict[str, Any]]]:
        """البحث عبر جميع قواعد البيانات"""
        results = {}

        for db_key, conn in self.databases.items():
            main_table = self.db_info[db_key]['main_table']
            if not main_table:
                continue

            try:
                cursor = conn.cursor()
                mappings = self.column_mappings.get(db_key, {})

                verse_text_col = mappings.get('verse_text', 'aya_text')
                verse_simple_col = mappings.get('verse_text_simple', 'aya_text_emlaey')

                query = f"""
                    SELECT *
                    FROM {main_table}
                    WHERE {verse_text_col} LIKE ? OR {verse_simple_col} LIKE ?
                    LIMIT ?
                """

                cursor.execute(query, (f'%{text}%', f'%{text}%', limit))
                rows = cursor.fetchall()

                results[db_key] = [dict(row) for row in rows]

            except Exception as e:
                print(f"خطأ في البحث في {db_key}: {e}")
                results[db_key] = []

        return results

    def get_topics(self) -> List[Dict[str, Any]]:
        """الحصول على الموضوعات القرآنية (مصطنعة مؤقتاً)"""
        # يمكن توسيعها لاحقاً من قاعدة بيانات حقيقية
        topics = [
            {"id": 1, "name": "العقيدة والإيمان", "keywords": ["آمن", "كفر", "توحيد", "الله"]},
            {"id": 2, "name": "العبادات", "keywords": ["صلاة", "صيام", "زكاة", "حج"]},
            {"id": 3, "name": "الأخلاق والآداب", "keywords": ["خلق", "صبر", "شكر", "تواضع"]},
            {"id": 4, "name": "القصص القرآني", "keywords": ["موسى", "عيسى", "نوح", "إبراهيم"]},
            {"id": 5, "name": "الأحكام الشرعية", "keywords": ["حكم", "حلال", "حرام", "فرض"]},
            {"id": 6, "name": "الجنة والنار", "keywords": ["جنة", "نار", "جزاء", "عذاب"]},
            {"id": 7, "name": "الرحمة والمغفرة", "keywords": ["رحمة", "غفر", "توب", "عفو"]},
            {"id": 8, "name": "الدعاء والذكر", "keywords": ["دعا", "ذكر", "سبح", "استغفر"]},
        ]
        return topics

    def search_by_topic(self, topic: Dict[str, Any]) -> List[Dict[str, Any]]:
        """البحث بالموضوع"""
        all_results = []

        for keyword in topic['keywords']:
            results = self.search_across_all(keyword, limit=50)
            for db_key, verses in results.items():
                all_results.extend(verses)

        # إزالة التكرار
        unique_results = []
        seen = set()
        for result in all_results:
            key = (result.get('sora', 0), result.get('aya_no', 0))
            if key not in seen:
                seen.add(key)
                unique_results.append(result)

        return unique_results[:100]  # حد أقصى 100 نتيجة

    def close_all(self):
        """إغلاق جميع الاتصالات"""
        for conn in self.databases.values():
            conn.close()


# ============================================================================
#                         التطبيق الرئيسي المتكامل
# ============================================================================

class QuranAppIntegrated(QMainWindow):
    """التطبيق المتكامل النهائي"""

    def __init__(self):
        super().__init__()
        self.db_manager = MultiDatabaseManager()
        self.current_surah_id = None
        self.current_verse_id = None
        self.surahs = []
        self.current_verses = []

        self.init_ui()
        self.init_databases()

    def init_ui(self):
        """تهيئة الواجهة"""
        self.setWindowTitle("🕌 تطبيق القرآن الكريم المتكامل v3.0 - Ultimate Integrated")
        self.setGeometry(100, 100, 1400, 900)

        # تطبيق نظام الألوان
        self.setStyleSheet(ClaudeColors.get_stylesheet())

        # الويدجت الرئيسي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # إنشاء المكونات الرئيسية
        self.create_sidebar()
        self.create_main_area()

        # إضافة إلى التخطيط
        splitter = QSplitter(Qt.Orientation.Horizontal if PYQT_VERSION == 6 else Qt.Horizontal)
        splitter.addWidget(self.sidebar_widget)
        splitter.addWidget(self.main_area_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        main_layout.addWidget(splitter)

        # شريط الحالة
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("مرحباً بك في تطبيق القرآن الكريم المتكامل ✨")

    def create_sidebar(self):
        """إنشاء الشريط الجانبي"""
        self.sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar_widget)

        # عنوان
        title_label = QLabel("📖 التصفح")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold if PYQT_VERSION == 6 else QFont.Bold))
        sidebar_layout.addWidget(title_label)

        # الشجرة
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("السور والآيات")
        self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)
        self.tree_widget.itemExpanded.connect(self.on_tree_item_expanded)
        sidebar_layout.addWidget(self.tree_widget)

    def create_main_area(self):
        """إنشاء المنطقة الرئيسية"""
        self.main_area_widget = QWidget()
        main_layout = QVBoxLayout(self.main_area_widget)

        # التابات الرئيسية
        self.main_tabs = QTabWidget()

        # تاب التصفح
        self.browse_tab = self.create_browse_tab()
        self.main_tabs.addTab(self.browse_tab, "📖 التصفح")

        # تاب البحث
        self.search_tab = self.create_search_tab()
        self.main_tabs.addTab(self.search_tab, "🔍 البحث")

        # تاب الموضوعات
        self.topics_tab = self.create_topics_tab()
        self.main_tabs.addTab(self.topics_tab, "📚 الموضوعات")

        main_layout.addWidget(self.main_tabs)

    def create_browse_tab(self) -> QWidget:
        """إنشاء تاب التصفح"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # أزرار التنقل
        nav_layout = QHBoxLayout()

        self.prev_btn = QPushButton("← السابق")
        self.prev_btn.clicked.connect(self.go_previous)
        nav_layout.addWidget(self.prev_btn)

        self.position_label = QLabel("اختر آية للبدء")
        self.position_label.setFont(QFont("Arial", 12, QFont.Weight.Bold if PYQT_VERSION == 6 else QFont.Bold))
        self.position_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        nav_layout.addWidget(self.position_label)

        self.next_btn = QPushButton("التالي →")
        self.next_btn.clicked.connect(self.go_next)
        nav_layout.addWidget(self.next_btn)

        layout.addLayout(nav_layout)

        # التابات الفرعية
        self.content_tabs = QTabWidget()

        # تاب القرآن
        self.quran_text = QTextEdit()
        self.quran_text.setReadOnly(True)
        self.quran_text.setFont(QFont("Arial", 18))
        self.content_tabs.addTab(self.quran_text, "📜 القرآن")

        # تاب التفسير
        self.tafseer_combo = QComboBox()
        self.tafseer_combo.addItems(["التفسير الميسر", "تفسير السعدي", "عرض الكل"])
        self.tafseer_combo.currentTextChanged.connect(self.update_tafseer)

        tafseer_widget = QWidget()
        tafseer_layout = QVBoxLayout(tafseer_widget)
        tafseer_layout.addWidget(self.tafseer_combo)

        self.tafseer_text = QTextEdit()
        self.tafseer_text.setReadOnly(True)
        self.tafseer_text.setFont(QFont("Arial", 14))
        tafseer_layout.addWidget(self.tafseer_text)

        self.content_tabs.addTab(tafseer_widget, "📖 التفسير")

        # تاب الإعراب
        self.erab_text = QTextEdit()
        self.erab_text.setReadOnly(True)
        self.erab_text.setFont(QFont("Arial", 14))
        self.content_tabs.addTab(self.erab_text, "🔤 الإعراب")

        layout.addWidget(self.content_tabs)

        return widget

    def create_search_tab(self) -> QWidget:
        """إنشاء تاب البحث"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # شريط البحث
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث في القرآن الكريم...")
        self.search_input.returnPressed.connect(self.perform_search)
        search_layout.addWidget(self.search_input)

        search_btn = QPushButton("🔍 بحث")
        search_btn.clicked.connect(self.perform_search)
        search_layout.addWidget(search_btn)

        layout.addLayout(search_layout)

        # نوع البحث
        search_type_layout = QHBoxLayout()
        search_type_layout.addWidget(QLabel("نوع البحث:"))

        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems(["بحث نصي", "بحث في كل القواعد", "بحث متقدم"])
        search_type_layout.addWidget(self.search_type_combo)
        search_type_layout.addStretch()

        layout.addLayout(search_type_layout)

        # جدول النتائج
        self.search_results_table = QTableWidget()
        self.search_results_table.setColumnCount(4)
        self.search_results_table.setHorizontalHeaderLabels(["السورة", "الآية", "النص", "القاعدة"])
        self.search_results_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch if PYQT_VERSION == 6 else QHeaderView.Stretch
        )
        self.search_results_table.cellClicked.connect(self.on_search_result_clicked)
        layout.addWidget(self.search_results_table)

        return widget

    def create_topics_tab(self) -> QWidget:
        """إنشاء تاب الموضوعات"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # عنوان
        title = QLabel("📚 الموضوعات القرآنية")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold if PYQT_VERSION == 6 else QFont.Bold))
        layout.addWidget(title)

        # قائمة الموضوعات
        topics_layout = QHBoxLayout()

        self.topics_list = QTableWidget()
        self.topics_list.setColumnCount(2)
        self.topics_list.setHorizontalHeaderLabels(["الموضوع", "الكلمات المفتاحية"])
        self.topics_list.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch if PYQT_VERSION == 6 else QHeaderView.Stretch
        )
        self.topics_list.cellClicked.connect(self.on_topic_clicked)
        topics_layout.addWidget(self.topics_list)

        layout.addLayout(topics_layout)

        # نتائج الموضوع
        self.topic_results_text = QTextEdit()
        self.topic_results_text.setReadOnly(True)
        self.topic_results_text.setFont(QFont("Arial", 14))
        layout.addWidget(self.topic_results_text)

        return widget

    def init_databases(self):
        """تهيئة قواعد البيانات"""
        if not self.db_manager.connect_databases():
            QMessageBox.critical(
                self,
                "خطأ",
                "❌ لم يتم العثور على أي قاعدة بيانات!\n\n"
                "يرجى وضع أحد الملفات التالية في نفس المجلد:\n"
                "• quran_ultimate_final.db\n"
                "• surah_database_app_v32.db\n"
                "• Quran_Crystalline.db"
            )
            sys.exit(1)

        # تحميل السور
        self.surahs = self.db_manager.get_surahs()
        self.populate_tree()

        # تحميل الموضوعات
        self.load_topics()

        self.status_bar.showMessage(f"✅ تم تحميل {len(self.surahs)} سورة من {len(self.db_manager.databases)} قاعدة بيانات")

    def populate_tree(self):
        """ملء الشجرة بالسور"""
        self.tree_widget.clear()

        for surah in self.surahs:
            item = QTreeWidgetItem([f"📖 {surah['name']}"])
            item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole, {
                'type': 'surah',
                'id': surah['id'],
                'name': surah['name']
            })
            self.tree_widget.addTopLevelItem(item)

    def on_tree_item_expanded(self, item: QTreeWidgetItem):
        """عند توسيع عنصر في الشجرة"""
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)

        if data and data['type'] == 'surah' and item.childCount() == 0:
            # تحميل الآيات
            verses = self.db_manager.get_verses_by_surah(data['id'])

            for verse in verses:
                verse_id = verse.get('aya_no', verse.get('ayah_no', 0))
                verse_item = QTreeWidgetItem([f"آية {verse_id}"])
                verse_item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole, {
                    'type': 'verse',
                    'surah_id': data['id'],
                    'verse_id': verse_id,
                    'data': verse
                })
                item.addChild(verse_item)

    def on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        """عند النقر على عنصر في الشجرة"""
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)

        if not data:
            return

        if data['type'] == 'surah':
            # عرض أول آية
            verses = self.db_manager.get_verses_by_surah(data['id'])
            if verses:
                self.display_verse(verses[0])

        elif data['type'] == 'verse':
            self.display_verse(data['data'])

    def display_verse(self, verse_data: Dict[str, Any]):
        """عرض آية"""
        self.current_surah_id = verse_data.get('sora', verse_data.get('surah', 1))
        self.current_verse_id = verse_data.get('aya_no', verse_data.get('ayah_no', 1))

        # عرض النص
        verse_text = verse_data.get('aya_text', verse_data.get('verse_text', 'لا يوجد نص'))
        self.quran_text.setHtml(f"""
            <div dir="rtl" style="text-align: center; padding: 20px;">
                <h2 style="color: {ClaudeColors.PRIMARY};">﴿ {verse_text} ﴾</h2>
            </div>
        """)

        # عرض التفسير
        self.update_tafseer()

        # عرض الإعراب
        erab = verse_data.get('earab_quran', verse_data.get('erab', 'غير متوفر'))
        self.erab_text.setHtml(f"""
            <div dir="rtl" style="padding: 20px;">
                <p style="font-size: 14px; line-height: 2;">{erab}</p>
            </div>
        """)

        # تحديث المؤشر
        surah_name = next((s['name'] for s in self.surahs if s['id'] == self.current_surah_id), "")
        self.position_label.setText(f"{surah_name} - آية {self.current_verse_id}")

        self.status_bar.showMessage(f"📖 {surah_name} - الآية {self.current_verse_id}")

    def update_tafseer(self):
        """تحديث التفسير"""
        if not self.current_surah_id or not self.current_verse_id:
            return

        verses = self.db_manager.get_verses_by_surah(self.current_surah_id)
        current_verse = next((v for v in verses if v.get('aya_no', v.get('ayah_no', 0)) == self.current_verse_id), None)

        if not current_verse:
            return

        tafseer_type = self.tafseer_combo.currentText()

        html_content = '<div dir="rtl" style="padding: 20px; line-height: 2;">'

        if tafseer_type == "عرض الكل":
            # عرض كل التفاسير
            tafseer_moysar = current_verse.get('tafseer_moysar', '')
            tafseer_saadi = current_verse.get('tafseer_saadi', '')

            if tafseer_moysar:
                html_content += f'<h3 style="color: {ClaudeColors.PRIMARY};">التفسير الميسر:</h3><p>{tafseer_moysar}</p><hr>'
            if tafseer_saadi:
                html_content += f'<h3 style="color: {ClaudeColors.PRIMARY};">تفسير السعدي:</h3><p>{tafseer_saadi}</p>'

        elif tafseer_type == "التفسير الميسر":
            tafseer = current_verse.get('tafseer_moysar', 'غير متوفر')
            html_content += f'<p>{tafseer}</p>'

        elif tafseer_type == "تفسير السعدي":
            tafseer = current_verse.get('tafseer_saadi', 'غير متوفر')
            html_content += f'<p>{tafseer}</p>'

        html_content += '</div>'
        self.tafseer_text.setHtml(html_content)

    def go_previous(self):
        """الانتقال للآية السابقة"""
        if not self.current_surah_id or not self.current_verse_id:
            return

        verses = self.db_manager.get_verses_by_surah(self.current_surah_id)
        current_index = next((i for i, v in enumerate(verses) if v.get('aya_no', v.get('ayah_no', 0)) == self.current_verse_id), None)

        if current_index is not None and current_index > 0:
            self.display_verse(verses[current_index - 1])
        elif self.current_surah_id > 1:
            # الانتقال لآخر آية من السورة السابقة
            prev_verses = self.db_manager.get_verses_by_surah(self.current_surah_id - 1)
            if prev_verses:
                self.display_verse(prev_verses[-1])

    def go_next(self):
        """الانتقال للآية التالية"""
        if not self.current_surah_id or not self.current_verse_id:
            return

        verses = self.db_manager.get_verses_by_surah(self.current_surah_id)
        current_index = next((i for i, v in enumerate(verses) if v.get('aya_no', v.get('ayah_no', 0)) == self.current_verse_id), None)

        if current_index is not None and current_index < len(verses) - 1:
            self.display_verse(verses[current_index + 1])
        elif self.current_surah_id < 114:
            # الانتقال لأول آية من السورة التالية
            next_verses = self.db_manager.get_verses_by_surah(self.current_surah_id + 1)
            if next_verses:
                self.display_verse(next_verses[0])

    def perform_search(self):
        """تنفيذ البحث"""
        query = self.search_input.text().strip()

        if not query:
            return

        search_type = self.search_type_combo.currentText()

        self.search_results_table.setRowCount(0)

        if search_type == "بحث في كل القواعد":
            results = self.db_manager.search_across_all(query)

            row = 0
            for db_key, verses in results.items():
                for verse in verses:
                    self.search_results_table.insertRow(row)

                    surah_id = verse.get('sora', verse.get('surah', ''))
                    verse_id = verse.get('aya_no', verse.get('ayah_no', ''))
                    verse_text = verse.get('aya_text', verse.get('verse_text', ''))[:100]

                    surah_name = next((s['name'] for s in self.surahs if s['id'] == surah_id), str(surah_id))

                    self.search_results_table.setItem(row, 0, QTableWidgetItem(surah_name))
                    self.search_results_table.setItem(row, 1, QTableWidgetItem(str(verse_id)))
                    self.search_results_table.setItem(row, 2, QTableWidgetItem(verse_text))
                    self.search_results_table.setItem(row, 3, QTableWidgetItem(db_key))

                    # حفظ البيانات
                    self.search_results_table.item(row, 0).setData(
                        Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole,
                        verse
                    )

                    row += 1

        else:
            # بحث عادي في القاعدة الأساسية
            results = self.db_manager.search_across_all(query)
            primary_results = results.get(self.db_manager.primary_db, [])

            for row, verse in enumerate(primary_results):
                self.search_results_table.insertRow(row)

                surah_id = verse.get('sora', verse.get('surah', ''))
                verse_id = verse.get('aya_no', verse.get('ayah_no', ''))
                verse_text = verse.get('aya_text', verse.get('verse_text', ''))[:100]

                surah_name = next((s['name'] for s in self.surahs if s['id'] == surah_id), str(surah_id))

                self.search_results_table.setItem(row, 0, QTableWidgetItem(surah_name))
                self.search_results_table.setItem(row, 1, QTableWidgetItem(str(verse_id)))
                self.search_results_table.setItem(row, 2, QTableWidgetItem(verse_text))
                self.search_results_table.setItem(row, 3, QTableWidgetItem(self.db_manager.primary_db))

                self.search_results_table.item(row, 0).setData(
                    Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole,
                    verse
                )

        total = self.search_results_table.rowCount()
        self.status_bar.showMessage(f"🔍 تم العثور على {total} نتيجة")

    def on_search_result_clicked(self, row: int, column: int):
        """عند النقر على نتيجة بحث"""
        item = self.search_results_table.item(row, 0)
        if item:
            verse_data = item.data(Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)
            if verse_data:
                self.display_verse(verse_data)
                self.main_tabs.setCurrentIndex(0)  # الانتقال لتاب التصفح

    def load_topics(self):
        """تحميل الموضوعات"""
        topics = self.db_manager.get_topics()

        self.topics_list.setRowCount(len(topics))

        for row, topic in enumerate(topics):
            self.topics_list.setItem(row, 0, QTableWidgetItem(topic['name']))
            self.topics_list.setItem(row, 1, QTableWidgetItem(", ".join(topic['keywords'])))

            self.topics_list.item(row, 0).setData(
                Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole,
                topic
            )

    def on_topic_clicked(self, row: int, column: int):
        """عند النقر على موضوع"""
        item = self.topics_list.item(row, 0)
        if item:
            topic = item.data(Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)
            if topic:
                results = self.db_manager.search_by_topic(topic)

                html_content = f'<div dir="rtl" style="padding: 20px;">'
                html_content += f'<h2 style="color: {ClaudeColors.PRIMARY};">موضوع: {topic["name"]}</h2>'
                html_content += f'<p style="color: {ClaudeColors.TEXT_SECONDARY};">عدد النتائج: {len(results)}</p><hr>'

                for verse in results[:50]:  # أول 50 نتيجة
                    surah_id = verse.get('sora', verse.get('surah', ''))
                    verse_id = verse.get('aya_no', verse.get('ayah_no', ''))
                    verse_text = verse.get('aya_text', verse.get('verse_text', ''))

                    surah_name = next((s['name'] for s in self.surahs if s['id'] == surah_id), str(surah_id))

                    html_content += f'''
                        <div style="margin: 15px 0; padding: 15px; background-color: {ClaudeColors.BG_SIDEBAR}; border-radius: 8px;">
                            <p style="font-size: 12px; color: {ClaudeColors.TEXT_SECONDARY};">{surah_name} - الآية {verse_id}</p>
                            <p style="font-size: 16px; font-weight: bold;">{verse_text}</p>
                        </div>
                    '''

                html_content += '</div>'
                self.topic_results_text.setHtml(html_content)

                self.status_bar.showMessage(f"📚 موضوع: {topic['name']} - {len(results)} نتيجة")

    def closeEvent(self, event):
        """عند إغلاق التطبيق"""
        self.db_manager.close_all()
        event.accept()


# ============================================================================
#                                نقطة الدخول
# ============================================================================

def main():
    """نقطة الدخول الرئيسية"""
    app = QApplication(sys.argv)

    # إعدادات التطبيق
    app.setApplicationName("تطبيق القرآن الكريم المتكامل")
    app.setApplicationVersion("3.0")

    # تشغيل التطبيق
    window = QuranAppIntegrated()
    window.show()

    sys.exit(app.exec() if PYQT_VERSION == 6 else app.exec_())


if __name__ == "__main__":
    main()

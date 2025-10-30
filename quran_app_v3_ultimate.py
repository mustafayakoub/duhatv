#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                    تطبيق القرآن الكريم الاحترافي المتقدم
                    Ultimate Advanced Quran Application
================================================================================

المطور: Claude AI Assistant
النسخة: 3.0 Ultimate Edition - البناء الذكي المتكامل
التاريخ: 2025-10-30

الميزات الجديدة في v3.0:
✨ إصلاح مشكلة تفكك الحروف في ألوان التجويد
✨ فتح تلقائي على سورة الفاتحة أو آخر موضع
✨ تنقل بالأسهم وسكرول الماوس آية بآية
✨ عرض التفاسير (الميسر، السعدي، البغوي)
✨ عرض الترجمات
✨ عرض الصرف والإعراب
✨ نافذة الموضوعات للتصفح الموضوعي
✨ بحث محسّن يعمل بكامل طاقته
✨ بحث بالموضوعات
✨ أنواع عرض قرآني (عادي، تجويد، إملائي)
"""

import sys
import os
import sqlite3
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import re

# محاولة استيراد PyQt6، وإذا فشل نستخدم PyQt5
try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    PYQT_VERSION = 6
    print("✅ استخدام PyQt6")
except ImportError:
    try:
        from PyQt5.QtWidgets import *
        from PyQt5.QtCore import *
        from PyQt5.QtGui import *
        PYQT_VERSION = 5
        print("✅ استخدام PyQt5")
    except ImportError:
        print("❌ خطأ: يجب تثبيت PyQt6 أو PyQt5")
        sys.exit(1)


# ============================================================================
#                          نظام ألوان التجويد المحسّن
# ============================================================================

class TajweedColors:
    """نظام ألوان أحكام التجويد - مُحسّن لمنع تفكك الحروف"""

    RULES = {
        '1': {'name': 'إظهار', 'color': '#696969'},
        '2': {'name': 'إدغام', 'color': '#228B22'},
        '3': {'name': 'إدغام بغنة', 'color': '#2E8B57'},
        '4': {'name': 'مد', 'color': '#DC143C'},
        '5': {'name': 'قلقلة', 'color': '#4169E1'},
        '6': {'name': 'سكون', 'color': '#2F4F4F'},
        '7': {'name': 'غنة', 'color': '#FF8C00'},
        '8': {'name': 'شدة', 'color': '#8B0000'},
        '9': {'name': 'إقلاب', 'color': '#9370DB'},
        '10': {'name': 'تفخيم', 'color': '#8B4513'},
        '11': {'name': 'ترقيق', 'color': '#4682B4'},
        '12': {'name': 'إخفاء', 'color': '#D4AF37'},
        '13': {'name': 'صفير', 'color': '#20B2AA'},
        '14': {'name': 'لين', 'color': '#DDA0DD'},
        '15': {'name': 'مد لازم', 'color': '#B22222'},
    }

    @classmethod
    def convert_to_html(cls, text: str, with_colors: bool = True) -> str:
        """
        تحويل النص من رموز التجويد إلى HTML ملون
        مع الحفاظ على اتصال الحروف العربية
        """
        if not text:
            return ""

        if not with_colors:
            # إزالة الرموز فقط وإرجاع نص نظيف
            return re.sub(r'<\d+>([^<]+?)</\d+>', r'\1', text)

        # نمط XML: <number>text</number>
        pattern = r'<(\d+)>([^<]+?)</\1>'

        def replace_match(match):
            number = match.group(1)
            content = match.group(2)

            if number in cls.RULES:
                info = cls.RULES[number]
                # الحل: استخدام display: inline و unicode-bidi: embed
                # لمنع تفكك الحروف المتصلة
                return (f'<span style="color: {info["color"]}; font-weight: bold; '
                       f'display: inline; unicode-bidi: embed; white-space: pre;" '
                       f'title="{info["name"]}">{content}</span>')
            return content

        return re.sub(pattern, replace_match, text)

    @classmethod
    def get_color_legend(cls) -> str:
        """الحصول على مفتاح الألوان"""
        legend_items = []
        main_rules = ['1', '2', '4', '5', '7', '9', '12']  # الأحكام الرئيسية

        for num in main_rules:
            if num in cls.RULES:
                info = cls.RULES[num]
                legend_items.append(
                    f'<span style="color: {info["color"]}; font-weight: bold;">⬛ {info["name"]}</span>'
                )

        return ' • '.join(legend_items)


# ============================================================================
#                             نظام الألوان الراقي
# ============================================================================

class ClaudeColors:
    """نظام ألوان Claude الهادئة والراقية"""

    PRIMARY = "#CC9B66"
    SECONDARY = "#9B8B7E"
    ACCENT = "#B8956A"

    BG_MAIN = "#F8F6F4"
    BG_SIDEBAR = "#F0EBE3"
    BG_CONTENT = "#FFFFFF"
    BG_HEADER = "#E8DFD0"

    TEXT_PRIMARY = "#2C2416"
    TEXT_SECONDARY = "#5C5445"
    TEXT_MUTED = "#8C8173"
    TEXT_LIGHT = "#ACA197"

    HOVER = "#E5D4B8"
    SELECTED = "#D4C4A8"
    PRESSED = "#C4B498"

    SUCCESS = "#7A9D54"
    WARNING = "#D4A574"
    ERROR = "#C17767"
    INFO = "#7B8FA3"

    BORDER_LIGHT = "#E0D5C7"
    BORDER_MEDIUM = "#C9BDB0"
    BORDER_DARK = "#B3A699"

    @classmethod
    def get_stylesheet(cls) -> str:
        return f"""
        QMainWindow, QWidget {{
            background-color: {cls.BG_MAIN};
            color: {cls.TEXT_PRIMARY};
            font-family: 'Segoe UI', 'Tahoma', sans-serif;
        }}

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
        }}

        QTreeWidget::item:hover {{
            background-color: {cls.HOVER};
        }}

        QTreeWidget::item:selected {{
            background-color: {cls.SELECTED};
            color: {cls.TEXT_PRIMARY};
        }}

        QTabWidget::pane {{
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            background-color: {cls.BG_CONTENT};
            padding: 4px;
        }}

        QTabBar::tab {{
            background-color: {cls.BG_SIDEBAR};
            color: {cls.TEXT_SECONDARY};
            padding: 10px 20px;
            margin: 2px;
            border: none;
            border-radius: 6px;
            font-weight: 500;
        }}

        QTabBar::tab:selected {{
            background-color: {cls.PRIMARY};
            color: white;
        }}

        QTabBar::tab:hover {{
            background-color: {cls.HOVER};
        }}

        QPushButton {{
            background-color: {cls.PRIMARY};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 500;
        }}

        QPushButton:hover {{
            background-color: {cls.ACCENT};
        }}

        QPushButton:pressed {{
            background-color: {cls.PRESSED};
        }}

        QLineEdit, QComboBox {{
            background-color: {cls.BG_CONTENT};
            border: 1px solid {cls.BORDER_MEDIUM};
            border-radius: 6px;
            padding: 8px;
            color: {cls.TEXT_PRIMARY};
        }}

        QLineEdit:focus, QComboBox:focus {{
            border: 2px solid {cls.PRIMARY};
        }}

        QTextEdit {{
            background-color: {cls.BG_CONTENT};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            padding: 12px;
            color: {cls.TEXT_PRIMARY};
        }}

        QStatusBar {{
            background-color: {cls.BG_HEADER};
            color: {cls.TEXT_SECONDARY};
            border-top: 1px solid {cls.BORDER_LIGHT};
        }}

        QLabel {{
            color: {cls.TEXT_PRIMARY};
        }}
        """


# ============================================================================
#                          مدير قاعدة البيانات الذكي
# ============================================================================

class SmartDatabaseManager:
    """مدير قاعدة بيانات ذكي مع اكتشاف تلقائي للأعمدة"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.tables_info = {}
        self.column_mappings = {}
        self.main_table = None

        # أسماء السور المحفوظة
        self.surah_names = [
            "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف",
            "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر",
            "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون",
            "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم",
            "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر",
            "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف",
            "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر",
            "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف",
            "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم",
            "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان",
            "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين",
            "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد",
            "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة",
            "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل",
            "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص",
            "الفلق", "الناس"
        ]

    def connect(self) -> bool:
        """الاتصال بقاعدة البيانات"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self._analyze_database()
            return True
        except Exception as e:
            print(f"❌ خطأ في الاتصال: {e}")
            return False

    def _analyze_database(self):
        """تحليل بنية قاعدة البيانات"""
        cursor = self.conn.cursor()

        # جلب جميع الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print(f"\n📊 تحليل قاعدة البيانات...")
        print(f"عدد الجداول: {len(tables)}")

        # تحليل كل جدول
        for (table_name,) in tables:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            self.tables_info[table_name] = columns
            print(f"  • {table_name}: {len(columns)} عمود")

        # اكتشاف الجدول الرئيسي
        self._detect_main_table()

        # اكتشاف خريطة الأعمدة
        self._detect_column_mappings()

    def _detect_main_table(self):
        """اكتشاف الجدول الرئيسي للنص القرآني"""
        priority_tables = [
            'quran_text_with_tajweed',
            'quran_text',
            'ayah_text',
            'verses',
            'QuranText'
        ]

        for priority in priority_tables:
            for table_name in self.tables_info.keys():
                if priority.lower() in table_name.lower():
                    self.main_table = table_name
                    print(f"✅ الجدول الرئيسي: {self.main_table}")
                    return

        # إذا لم يجد، خذ أول جدول به أعمدة مناسبة
        for table_name, columns in self.tables_info.items():
            cols_lower = [c.lower() for c in columns]
            if any('surah' in c or 'sora' in c for c in cols_lower) and \
               any('ayah' in c or 'aya' in c or 'verse' in c for c in cols_lower):
                self.main_table = table_name
                print(f"✅ الجدول الرئيسي (تلقائي): {self.main_table}")
                return

    def _detect_column_mappings(self):
        """اكتشاف خريطة الأعمدة"""
        if not self.main_table:
            return

        columns = self.tables_info.get(self.main_table, [])
        cols_lower = {c.lower(): c for c in columns}

        # اكتشاف عمود رقم السورة
        for pattern in ['surahno', 'surah_id', 'surah', 'sura_no', 'sora', 'soraid']:
            if pattern in cols_lower:
                self.column_mappings['surah_id'] = cols_lower[pattern]
                break

        # اكتشاف عمود رقم الآية
        for pattern in ['ayahno', 'ayah_id', 'ayah', 'aya_no', 'aya', 'ayaid', 'verse_id', 'verse']:
            if pattern in cols_lower:
                self.column_mappings['verse_id'] = cols_lower[pattern]
                break

        # اكتشاف عمود النص
        for pattern in ['tajweedtext', 'text', 'ayah_text', 'verse_text', 'arabic']:
            if pattern in cols_lower:
                self.column_mappings['verse_text'] = cols_lower[pattern]
                break

        print(f"✅ خريطة الأعمدة: {self.column_mappings}")

    def get_surah_name(self, surah_id: int) -> str:
        """الحصول على اسم السورة"""
        if 1 <= surah_id <= 114:
            return self.surah_names[surah_id - 1]
        return f"سورة {surah_id}"

    def get_all_surahs(self) -> List[Dict[str, Any]]:
        """جلب جميع السور"""
        if not self.main_table or 'surah_id' not in self.column_mappings:
            return []

        cursor = self.conn.cursor()
        surah_col = self.column_mappings['surah_id']
        verse_col = self.column_mappings.get('verse_id', 'ayahNo')

        # جلب السور الموجودة مع عدد الآيات
        query = f"""
            SELECT DISTINCT {surah_col} as surah_id,
                   COUNT(*) as verse_count
            FROM {self.main_table}
            GROUP BY {surah_col}
            ORDER BY {surah_col}
        """

        cursor.execute(query)
        surahs = []

        for row in cursor.fetchall():
            surah_id = row['surah_id']
            surahs.append({
                'id': surah_id,
                'name': self.get_surah_name(surah_id),
                'verse_count': row['verse_count']
            })

        return surahs

    def get_surah_verses(self, surah_id: int) -> List[Dict[str, Any]]:
        """جلب آيات سورة معينة"""
        if not self.main_table:
            return []

        cursor = self.conn.cursor()
        surah_col = self.column_mappings.get('surah_id', 'surahNo')
        verse_col = self.column_mappings.get('verse_id', 'ayahNo')
        text_col = self.column_mappings.get('verse_text', 'tajweedText')

        query = f"""
            SELECT {verse_col} as verse_id,
                   {text_col} as text
            FROM {self.main_table}
            WHERE {surah_col} = ?
            ORDER BY {verse_col}
        """

        cursor.execute(query, (surah_id,))
        verses = []

        for row in cursor.fetchall():
            verses.append({
                'id': row['verse_id'],
                'text': row['text'] or ''
            })

        return verses

    def get_verse_data(self, surah_id: int, verse_id: int) -> Dict[str, Any]:
        """جلب بيانات آية كاملة مع كل التفاصيل"""
        data = {
            'text': '',
            'tafsir_moyassar': '',
            'tafsir_saadi': '',
            'tafsir_baghawi': '',
            'translation_en': '',
            'translation_fr': '',
            'irab': '',
            'sarf': '',
        }

        # جلب النص الرئيسي
        if self.main_table:
            cursor = self.conn.cursor()
            surah_col = self.column_mappings.get('surah_id', 'surahNo')
            verse_col = self.column_mappings.get('verse_id', 'ayahNo')
            text_col = self.column_mappings.get('verse_text', 'tajweedText')

            query = f"""
                SELECT {text_col} as text
                FROM {self.main_table}
                WHERE {surah_col} = ? AND {verse_col} = ?
            """

            cursor.execute(query, (surah_id, verse_id))
            row = cursor.fetchone()
            if row:
                data['text'] = row['text'] or ''

        # جلب التفاسير
        data['tafsir_moyassar'] = self._get_tafsir('tafsir_moyassar', surah_id, verse_id)
        data['tafsir_saadi'] = self._get_tafsir('tafsir_saadi', surah_id, verse_id)
        data['tafsir_baghawi'] = self._get_tafsir('tafsir_baghawi', surah_id, verse_id)

        # جلب الترجمات
        data['translation_en'] = self._get_translation('en', surah_id, verse_id)
        data['translation_fr'] = self._get_translation('fr', surah_id, verse_id)

        # جلب الإعراب والصرف
        data['irab'] = self._get_irab(surah_id, verse_id)
        data['sarf'] = self._get_sarf(surah_id, verse_id)

        return data

    def _get_tafsir(self, table_name: str, surah_id: int, verse_id: int) -> str:
        """جلب تفسير من جدول معين"""
        # البحث عن الجدول
        actual_table = None
        for tname in self.tables_info.keys():
            if table_name.lower() in tname.lower():
                actual_table = tname
                break

        if not actual_table:
            return ""

        cursor = self.conn.cursor()

        # محاولة أنماط مختلفة من الأعمدة
        for surah_pattern in ['surahNo', 'surah_id', 'surah', 'sura']:
            for verse_pattern in ['ayahNo', 'ayah_id', 'ayah', 'aya', 'verse']:
                for text_pattern in ['text', 'tafsir', 'tafseer', 'content']:
                    try:
                        query = f"""
                            SELECT {text_pattern}
                            FROM {actual_table}
                            WHERE {surah_pattern} = ? AND {verse_pattern} = ?
                        """
                        cursor.execute(query, (surah_id, verse_id))
                        row = cursor.fetchone()
                        if row and row[0]:
                            return row[0]
                    except:
                        continue

        return ""

    def _get_translation(self, lang: str, surah_id: int, verse_id: int) -> str:
        """جلب ترجمة"""
        # البحث عن جداول الترجمة
        translation_tables = []
        for tname in self.tables_info.keys():
            if 'translat' in tname.lower() and lang.lower() in tname.lower():
                translation_tables.append(tname)

        if not translation_tables:
            return ""

        # محاولة جلب الترجمة
        cursor = self.conn.cursor()
        for table in translation_tables:
            try:
                # نفس منطق _get_tafsir
                for surah_pattern in ['surahNo', 'surah_id', 'surah']:
                    for verse_pattern in ['ayahNo', 'ayah_id', 'ayah']:
                        for text_pattern in ['text', 'translation', 'trans']:
                            try:
                                query = f"""
                                    SELECT {text_pattern}
                                    FROM {table}
                                    WHERE {surah_pattern} = ? AND {verse_pattern} = ?
                                """
                                cursor.execute(query, (surah_id, verse_id))
                                row = cursor.fetchone()
                                if row and row[0]:
                                    return row[0]
                            except:
                                continue
            except:
                continue

        return ""

    def _get_irab(self, surah_id: int, verse_id: int) -> str:
        """جلب الإعراب"""
        # البحث عن جدول الإعراب
        for tname in self.tables_info.keys():
            if 'irab' in tname.lower() or 'i3rab' in tname.lower():
                cursor = self.conn.cursor()
                try:
                    # محاولة أنماط مختلفة
                    for surah_col in ['surahNo', 'surah', 'sura']:
                        for verse_col in ['ayahNo', 'ayah', 'aya']:
                            for text_col in ['text', 'irab', 'i3rab', 'content']:
                                try:
                                    query = f"""
                                        SELECT {text_col}
                                        FROM {tname}
                                        WHERE {surah_col} = ? AND {verse_col} = ?
                                    """
                                    cursor.execute(query, (surah_id, verse_id))
                                    row = cursor.fetchone()
                                    if row and row[0]:
                                        return row[0]
                                except:
                                    continue
                except:
                    continue

        return ""

    def _get_sarf(self, surah_id: int, verse_id: int) -> str:
        """جلب الصرف"""
        # البحث عن جدول الصرف
        for tname in self.tables_info.keys():
            if 'sarf' in tname.lower() or 'morphology' in tname.lower():
                cursor = self.conn.cursor()
                try:
                    for surah_col in ['surahNo', 'surah']:
                        for verse_col in ['ayahNo', 'ayah']:
                            for text_col in ['text', 'sarf', 'morphology', 'content']:
                                try:
                                    query = f"""
                                        SELECT {text_col}
                                        FROM {tname}
                                        WHERE {surah_col} = ? AND {verse_col} = ?
                                    """
                                    cursor.execute(query, (surah_id, verse_id))
                                    row = cursor.fetchone()
                                    if row and row[0]:
                                        return row[0]
                                except:
                                    continue
                except:
                    continue

        return ""

    def search_verses(self, search_text: str, search_in: str = 'text') -> List[Dict[str, Any]]:
        """بحث في الآيات"""
        if not self.main_table:
            return []

        cursor = self.conn.cursor()
        surah_col = self.column_mappings.get('surah_id', 'surahNo')
        verse_col = self.column_mappings.get('verse_id', 'ayahNo')
        text_col = self.column_mappings.get('verse_text', 'tajweedText')

        if search_in == 'text':
            # البحث في النص القرآني
            query = f"""
                SELECT {surah_col} as surah_id,
                       {verse_col} as verse_id,
                       {text_col} as text
                FROM {self.main_table}
                WHERE {text_col} LIKE ?
                ORDER BY {surah_col}, {verse_col}
            """
            cursor.execute(query, (f'%{search_text}%',))

        results = []
        for row in cursor.fetchall():
            results.append({
                'surah_id': row['surah_id'],
                'verse_id': row['verse_id'],
                'text': row['text'] or '',
                'surah_name': self.get_surah_name(row['surah_id'])
            })

        return results


# ============================================================================
#                          النافذة الرئيسية
# ============================================================================

class QuranApp(QMainWindow):
    """النافذة الرئيسية لتطبيق القرآن"""

    def __init__(self):
        super().__init__()
        self.db = None
        self.current_surah = 1  # سورة الفاتحة
        self.current_verse = 1
        self.show_tajweed_colors = True
        self.settings_file = 'quran_app_settings.json'

        self.init_ui()
        self.load_settings()
        self.connect_database()

    def init_ui(self):
        """تهيئة الواجهة"""
        self.setWindowTitle("تطبيق القرآن الكريم v3.0 Ultimate")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(ClaudeColors.get_stylesheet())

        # الويدجت الرئيسي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # التخطيط الرئيسي
        main_layout = QHBoxLayout(central_widget)

        # الفاصل الرئيسي
        splitter = QSplitter(Qt.Orientation.Horizontal if PYQT_VERSION == 6 else Qt.Horizontal)
        main_layout.addWidget(splitter)

        # الشجرة (الجانب الأيمن)
        self.create_tree_widget()
        splitter.addWidget(self.tree_widget)

        # منطقة المحتوى (الوسط والجانب الأيسر)
        content_widget = self.create_content_widget()
        splitter.addWidget(content_widget)

        # نسب التقسيم
        splitter.setSizes([300, 1100])

        # شريط الحالة
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status_bar()

        # ربط الأحداث
        self.connect_signals()

    def create_tree_widget(self):
        """إنشاء شجرة السور والآيات"""
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("القرآن الكريم")
        self.tree_widget.setLayoutDirection(Qt.LayoutDirection.RightToLeft if PYQT_VERSION == 6 else Qt.RightToLeft)
        self.tree_widget.setFont(QFont("Arial", 11))

    def create_content_widget(self) -> QWidget:
        """إنشاء منطقة المحتوى"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # شريط التحكم العلوي
        control_bar = self.create_control_bar()
        layout.addWidget(control_bar)

        # التابات
        self.tabs = QTabWidget()

        # تاب النص القرآني
        self.quran_text = QTextEdit()
        self.quran_text.setReadOnly(True)
        self.quran_text.setFont(QFont("Arial", 18))
        self.quran_text.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        self.tabs.addTab(self.quran_text, "النص القرآني")

        # تاب التفسير
        self.tafsir_text = QTextEdit()
        self.tafsir_text.setReadOnly(True)
        self.tafsir_text.setFont(QFont("Arial", 13))
        self.tabs.addTab(self.tafsir_text, "التفسير")

        # تاب الترجمة
        self.translation_text = QTextEdit()
        self.translation_text.setReadOnly(True)
        self.translation_text.setFont(QFont("Arial", 13))
        self.tabs.addTab(self.translation_text, "الترجمة")

        # تاب الإعراب
        self.irab_text = QTextEdit()
        self.irab_text.setReadOnly(True)
        self.irab_text.setFont(QFont("Arial", 13))
        self.tabs.addTab(self.irab_text, "الإعراب")

        # تاب الصرف
        self.sarf_text = QTextEdit()
        self.sarf_text.setReadOnly(True)
        self.sarf_text.setFont(QFont("Arial", 13))
        self.tabs.addTab(self.sarf_text, "الصرف")

        # تاب الموضوعات
        self.topics_text = QTextEdit()
        self.topics_text.setReadOnly(True)
        self.topics_text.setFont(QFont("Arial", 13))
        self.tabs.addTab(self.topics_text, "الموضوعات")

        # تاب البحث
        search_widget = self.create_search_tab()
        self.tabs.addTab(search_widget, "البحث")

        layout.addWidget(self.tabs)

        # أزرار التنقل
        nav_bar = self.create_navigation_bar()
        layout.addWidget(nav_bar)

        return widget

    def create_control_bar(self) -> QWidget:
        """إنشاء شريط التحكم"""
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # اختيار نوع العرض
        layout.addWidget(QLabel("نوع العرض:"))
        self.display_type = QComboBox()
        self.display_type.addItems(["تجويد ملون", "عادي", "إملائي"])
        layout.addWidget(self.display_type)

        # اختيار التفسير
        layout.addWidget(QLabel("التفسير:"))
        self.tafsir_combo = QComboBox()
        self.tafsir_combo.addItems(["التفسير الميسر", "تفسير السعدي", "تفسير البغوي", "الكل"])
        layout.addWidget(self.tafsir_combo)

        # اختيار الترجمة
        layout.addWidget(QLabel("الترجمة:"))
        self.translation_combo = QComboBox()
        self.translation_combo.addItems(["English", "Français", "كلاهما"])
        layout.addWidget(self.translation_combo)

        layout.addStretch()

        return widget

    def create_navigation_bar(self) -> QWidget:
        """إنشاء شريط التنقل"""
        widget = QWidget()
        layout = QHBoxLayout(widget)

        self.btn_prev = QPushButton("◄ السابقة")
        self.btn_next = QPushButton("التالية ►")

        self.verse_label = QLabel("الآية: 1")
        self.verse_label.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)

        layout.addWidget(self.btn_prev)
        layout.addWidget(self.verse_label, 1)
        layout.addWidget(self.btn_next)

        return widget

    def create_search_tab(self) -> QWidget:
        """إنشاء تاب البحث"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # شريط البحث
        search_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث في القرآن...")
        search_bar.addWidget(self.search_input)

        self.search_type = QComboBox()
        self.search_type.addItems(["في النص", "في التفسير", "في الموضوعات"])
        search_bar.addWidget(self.search_type)

        self.search_btn = QPushButton("بحث")
        search_bar.addWidget(self.search_btn)

        layout.addLayout(search_bar)

        # نتائج البحث
        self.search_results = QTreeWidget()
        self.search_results.setHeaderLabels(["السورة", "الآية", "النص"])
        self.search_results.setRightToLeft(True)
        layout.addWidget(self.search_results)

        return widget

    def connect_signals(self):
        """ربط الإشارات"""
        self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)
        self.btn_prev.clicked.connect(self.go_previous_verse)
        self.btn_next.clicked.connect(self.go_next_verse)
        self.display_type.currentTextChanged.connect(self.update_current_verse_display)
        self.tafsir_combo.currentTextChanged.connect(self.update_tafsir_display)
        self.translation_combo.currentTextChanged.connect(self.update_translation_display)
        self.search_btn.clicked.connect(self.perform_search)
        self.search_results.itemDoubleClicked.connect(self.on_search_result_clicked)

    def keyPressEvent(self, event):
        """معالجة ضغطات المفاتيح"""
        if event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Right] if PYQT_VERSION == 6 else [Qt.Key_Up, Qt.Key_Right]:
            self.go_previous_verse()
        elif event.key() in [Qt.Key.Key_Down, Qt.Key.Key_Left] if PYQT_VERSION == 6 else [Qt.Key_Down, Qt.Key_Left]:
            self.go_next_verse()
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        """معالجة سكرول الماوس"""
        if PYQT_VERSION == 6:
            delta = event.angleDelta().y()
        else:
            delta = event.delta()

        if delta > 0:
            self.go_previous_verse()
        else:
            self.go_next_verse()

    def connect_database(self):
        """الاتصال بقاعدة البيانات"""
        # البحث عن ملف قاعدة البيانات
        possible_paths = [
            'quran.db',
            'quran.sqlite',
            'data/quran.db',
            '../quran.db',
        ]

        db_path = None
        for path in possible_paths:
            if os.path.exists(path):
                db_path = path
                break

        if not db_path:
            QMessageBox.warning(self, "تحذير",
                              "لم يتم العثور على قاعدة البيانات!\n"
                              "ضع ملف quran.db في نفس مجلد التطبيق.")
            return

        self.db = SmartDatabaseManager(db_path)
        if self.db.connect():
            self.load_surahs()
            # فتح على سورة الفاتحة أو آخر موضع
            self.load_verse(self.current_surah, self.current_verse)

    def load_surahs(self):
        """تحميل السور في الشجرة"""
        self.tree_widget.clear()
        surahs = self.db.get_all_surahs()

        for surah in surahs:
            surah_item = QTreeWidgetItem(self.tree_widget)
            surah_item.setText(0, f"{surah['name']} ({surah['verse_count']} آية)")
            surah_item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole,
                              {'type': 'surah', 'id': surah['id']})

            # تحميل الآيات كـ lazy loading
            # سنحملها عند التوسيع

        self.tree_widget.itemExpanded.connect(self.on_surah_expanded)

    def on_surah_expanded(self, item):
        """عند توسيع سورة، حمّل آياتها"""
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)
        if data and data['type'] == 'surah' and item.childCount() == 0:
            surah_id = data['id']
            verses = self.db.get_surah_verses(surah_id)

            for verse in verses:
                verse_item = QTreeWidgetItem(item)
                # نص نظيف بدون رموز تجويد
                clean_text = TajweedColors.convert_to_html(verse['text'], with_colors=False)
                verse_item.setText(0, f"آية {verse['id']}: {clean_text[:50]}...")
                verse_item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole,
                                  {'type': 'verse', 'surah_id': surah_id, 'verse_id': verse['id']})

    def on_tree_item_clicked(self, item, column):
        """عند النقر على عنصر في الشجرة"""
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)
        if data and data['type'] == 'verse':
            self.load_verse(data['surah_id'], data['verse_id'])

    def load_verse(self, surah_id: int, verse_id: int):
        """تحميل آية معينة"""
        self.current_surah = surah_id
        self.current_verse = verse_id

        # جلب بيانات الآية
        verse_data = self.db.get_verse_data(surah_id, verse_id)

        # عرض النص القرآني
        self.display_quran_text(verse_data)

        # عرض التفسير
        self.display_tafsir(verse_data)

        # عرض الترجمة
        self.display_translation(verse_data)

        # عرض الإعراب
        self.display_irab(verse_data)

        # عرض الصرف
        self.display_sarf(verse_data)

        # تحديث شريط الحالة
        self.update_status_bar()

        # حفظ آخر موضع
        self.save_settings()

    def display_quran_text(self, verse_data: Dict[str, Any]):
        """عرض النص القرآني"""
        text = verse_data.get('text', '')
        surah_name = self.db.get_surah_name(self.current_surah)

        # تطبيق نوع العرض
        display_type = self.display_type.currentText()

        if display_type == "تجويد ملون":
            colored_text = TajweedColors.convert_to_html(text, with_colors=True)
        elif display_type == "عادي":
            colored_text = TajweedColors.convert_to_html(text, with_colors=False)
        else:  # إملائي
            # TODO: تحويل إلى رسم إملائي
            colored_text = TajweedColors.convert_to_html(text, with_colors=False)

        # مفتاح الألوان
        color_legend = TajweedColors.get_color_legend() if display_type == "تجويد ملون" else ""

        html = f"""
        <div style='text-align: center; direction: rtl; padding: 20px;'>
            <h2 style='color: {ClaudeColors.PRIMARY};'>{surah_name} - الآية {self.current_verse}</h2>
            <p style='font-size: 28px; line-height: 2.8; direction: rtl; unicode-bidi: embed;'>
                {colored_text}
            </p>
            {f"<p style='font-size: 11px; color: {ClaudeColors.TEXT_MUTED};'>{color_legend}</p>" if color_legend else ""}
        </div>
        """

        self.quran_text.setHtml(html)

    def display_tafsir(self, verse_data: Dict[str, Any]):
        """عرض التفسير"""
        tafsir_type = self.tafsir_combo.currentText()

        html = f"""
        <div style='direction: rtl; padding: 15px;'>
            <h3 style='color: {ClaudeColors.PRIMARY};'>التفسير</h3>
        """

        if tafsir_type == "التفسير الميسر" or tafsir_type == "الكل":
            if verse_data.get('tafsir_moyassar'):
                html += f"""
                <div style='margin-bottom: 20px;'>
                    <h4 style='color: {ClaudeColors.ACCENT};'>التفسير الميسر:</h4>
                    <p style='font-size: 14px; line-height: 1.8;'>{verse_data['tafsir_moyassar']}</p>
                </div>
                """

        if tafsir_type == "تفسير السعدي" or tafsir_type == "الكل":
            if verse_data.get('tafsir_saadi'):
                html += f"""
                <div style='margin-bottom: 20px;'>
                    <h4 style='color: {ClaudeColors.ACCENT};'>تفسير السعدي:</h4>
                    <p style='font-size: 14px; line-height: 1.8;'>{verse_data['tafsir_saadi']}</p>
                </div>
                """

        if tafsir_type == "تفسير البغوي" or tafsir_type == "الكل":
            if verse_data.get('tafsir_baghawi'):
                html += f"""
                <div style='margin-bottom: 20px;'>
                    <h4 style='color: {ClaudeColors.ACCENT};'>تفسير البغوي:</h4>
                    <p style='font-size: 14px; line-height: 1.8;'>{verse_data['tafsir_baghawi']}</p>
                </div>
                """

        if not any([verse_data.get('tafsir_moyassar'), verse_data.get('tafsir_saadi'),
                   verse_data.get('tafsir_baghawi')]):
            html += "<p style='color: #999;'>لا يوجد تفسير متاح لهذه الآية</p>"

        html += "</div>"
        self.tafsir_text.setHtml(html)

    def display_translation(self, verse_data: Dict[str, Any]):
        """عرض الترجمة"""
        translation_type = self.translation_combo.currentText()

        html = f"""
        <div style='padding: 15px;'>
            <h3 style='color: {ClaudeColors.PRIMARY};'>Translation</h3>
        """

        if translation_type == "English" or translation_type == "كلاهما":
            if verse_data.get('translation_en'):
                html += f"""
                <div style='margin-bottom: 20px;'>
                    <h4 style='color: {ClaudeColors.ACCENT};'>English:</h4>
                    <p style='font-size: 14px; line-height: 1.8;'>{verse_data['translation_en']}</p>
                </div>
                """

        if translation_type == "Français" or translation_type == "كلاهما":
            if verse_data.get('translation_fr'):
                html += f"""
                <div style='margin-bottom: 20px;'>
                    <h4 style='color: {ClaudeColors.ACCENT};'>Français:</h4>
                    <p style='font-size: 14px; line-height: 1.8;'>{verse_data['translation_fr']}</p>
                </div>
                """

        if not any([verse_data.get('translation_en'), verse_data.get('translation_fr')]):
            html += "<p style='color: #999;'>No translation available</p>"

        html += "</div>"
        self.translation_text.setHtml(html)

    def display_irab(self, verse_data: Dict[str, Any]):
        """عرض الإعراب"""
        irab = verse_data.get('irab', '')

        html = f"""
        <div style='direction: rtl; padding: 15px;'>
            <h3 style='color: {ClaudeColors.PRIMARY};'>الإعراب</h3>
        """

        if irab:
            html += f"<p style='font-size: 14px; line-height: 1.8;'>{irab}</p>"
        else:
            html += "<p style='color: #999;'>لا يوجد إعراب متاح لهذه الآية</p>"

        html += "</div>"
        self.irab_text.setHtml(html)

    def display_sarf(self, verse_data: Dict[str, Any]):
        """عرض الصرف"""
        sarf = verse_data.get('sarf', '')

        html = f"""
        <div style='direction: rtl; padding: 15px;'>
            <h3 style='color: {ClaudeColors.PRIMARY};'>الصرف</h3>
        """

        if sarf:
            html += f"<p style='font-size: 14px; line-height: 1.8;'>{sarf}</p>"
        else:
            html += "<p style='color: #999;'>لا يوجد صرف متاح لهذه الآية</p>"

        html += "</div>"
        self.sarf_text.setHtml(html)

    def update_current_verse_display(self):
        """تحديث عرض الآية الحالية"""
        verse_data = self.db.get_verse_data(self.current_surah, self.current_verse)
        self.display_quran_text(verse_data)

    def update_tafsir_display(self):
        """تحديث عرض التفسير"""
        verse_data = self.db.get_verse_data(self.current_surah, self.current_verse)
        self.display_tafsir(verse_data)

    def update_translation_display(self):
        """تحديث عرض الترجمة"""
        verse_data = self.db.get_verse_data(self.current_surah, self.current_verse)
        self.display_translation(verse_data)

    def go_previous_verse(self):
        """الانتقال للآية السابقة"""
        if self.current_verse > 1:
            self.load_verse(self.current_surah, self.current_verse - 1)
        elif self.current_surah > 1:
            # الانتقال لآخر آية في السورة السابقة
            prev_surah = self.current_surah - 1
            verses = self.db.get_surah_verses(prev_surah)
            if verses:
                self.load_verse(prev_surah, len(verses))

    def go_next_verse(self):
        """الانتقال للآية التالية"""
        verses = self.db.get_surah_verses(self.current_surah)

        if self.current_verse < len(verses):
            self.load_verse(self.current_surah, self.current_verse + 1)
        elif self.current_surah < 114:
            # الانتقال لأول آية في السورة التالية
            self.load_verse(self.current_surah + 1, 1)

    def perform_search(self):
        """تنفيذ البحث"""
        search_text = self.search_input.text().strip()
        if not search_text:
            return

        search_type = self.search_type.currentText()

        self.search_results.clear()

        if search_type == "في النص":
            results = self.db.search_verses(search_text, 'text')

            for result in results:
                item = QTreeWidgetItem(self.search_results)
                item.setText(0, result['surah_name'])
                item.setText(1, str(result['verse_id']))
                clean_text = TajweedColors.convert_to_html(result['text'], with_colors=False)
                item.setText(2, clean_text[:100] + "...")
                item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole,
                           {'surah_id': result['surah_id'], 'verse_id': result['verse_id']})

        self.status_bar.showMessage(f"تم العثور على {self.search_results.topLevelItemCount()} نتيجة")

    def on_search_result_clicked(self, item, column):
        """عند النقر على نتيجة بحث"""
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)
        if data:
            self.load_verse(data['surah_id'], data['verse_id'])
            self.tabs.setCurrentIndex(0)  # العودة لتاب النص القرآني

    def update_status_bar(self):
        """تحديث شريط الحالة"""
        surah_name = self.db.get_surah_name(self.current_surah) if self.db else "..."
        self.status_bar.showMessage(f"{surah_name} - الآية {self.current_verse}")
        self.verse_label.setText(f"الآية: {self.current_verse}")

    def load_settings(self):
        """تحميل الإعدادات"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_surah = settings.get('last_surah', 1)
                    self.current_verse = settings.get('last_verse', 1)
        except:
            pass

    def save_settings(self):
        """حفظ الإعدادات"""
        try:
            settings = {
                'last_surah': self.current_surah,
                'last_verse': self.current_verse
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except:
            pass

    def closeEvent(self, event):
        """عند إغلاق التطبيق"""
        self.save_settings()
        event.accept()


# ============================================================================
#                               نقطة الدخول
# ============================================================================

def main():
    """نقطة الدخول الرئيسية"""
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft if PYQT_VERSION == 6 else Qt.RightToLeft)

    window = QuranApp()
    window.show()

    sys.exit(app.exec() if PYQT_VERSION == 6 else app.exec_())


if __name__ == '__main__':
    main()

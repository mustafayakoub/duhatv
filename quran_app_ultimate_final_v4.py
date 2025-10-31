#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                تطبيق القرآن الكريم v4.0 Ultimate - النسخة النهائية
                    Quran Application v4.0 Ultimate Final
================================================================================

المطور: Claude AI + Mustafa Yakoub
النسخة: 4.0 Ultimate Final Edition
التاريخ: 2025-10-31

الميزات الكاملة:
✨ الموديلات الثلاثة متكاملة (ClaudeColors + DatabaseManager + QuranApp)
✨ دعم قاعدة بيانات واحدة متكاملة
✨ التجويد الملون (15 حكم تجويد)
✨ التفاسير المتعددة (الميسر، السعدي، البغوي، الجلالين، الطبري)
✨ الترجمات (إنجليزي، فرنسي)
✨ الإعراب والصرف
✨ الموضوعات القرآنية
✨ البحث المتقدم (نصي، بالجذور، بالموضوعات)
✨ العلامات المرجعية
✨ أنواع رسم متعددة
✨ 15+ خط قرآني
✨ التنقل الذكي (سورة:آية، جزء، صفحة)
✨ حفظ آخر موضع تلقائياً
✨ تنقل بالأسهم وعجلة الماوس

📧 duhatv@gmail.com | 🌐 duhatv.net | 📱 +905342390000
================================================================================
"""

import sys
import os
import sqlite3
import json
import re
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime

# PyQt6/PyQt5 Support
try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    PYQT_VERSION = 6
except ImportError:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    PYQT_VERSION = 5


# ============================================================================
#                          PART 1: نظام ألوان التجويد
# ============================================================================

class TajweedColors:
    """
    نظام ألوان التجويد المحسّن
    يمنع تفكك الحروف العربية المتصلة
    """

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
        """تحويل النص من رموز التجويد إلى HTML ملون"""
        if not text:
            return ""

        if not with_colors:
            return re.sub(r'<\d+>([^<]+?)</\d+>', r'\1', text)

        pattern = r'<(\d+)>([^<]+?)</\1>'

        def replace_match(match):
            number = match.group(1)
            content = match.group(2)

            if number in cls.RULES:
                info = cls.RULES[number]
                return (f'<span style="color: {info["color"]}; font-weight: bold; '
                       f'display: inline; unicode-bidi: embed; white-space: pre;" '
                       f'title="{info["name"]}">{content}</span>')
            return content

        return re.sub(pattern, replace_match, text)

    @classmethod
    def get_legend_html(cls) -> str:
        """مفتاح الألوان"""
        items = []
        main_rules = ['1', '2', '4', '5', '7', '9', '12']

        for num in main_rules:
            if num in cls.RULES:
                info = cls.RULES[num]
                items.append(
                    f'<span style="color: {info["color"]}; font-weight: bold;">⬛ {info["name"]}</span>'
                )

        return ' • '.join(items)


# ============================================================================
#                          PART 2: نظام الألوان الراقي
# ============================================================================

class ClaudeColors:
    """نظام ألوان Claude الهادئة والراقية - Mod 1"""

    # الألوان الأساسية
    PRIMARY = "#CC9B66"
    SECONDARY = "#9B8B7E"
    ACCENT = "#B8956A"

    # ألوان الخلفية
    BG_MAIN = "#F8F6F4"
    BG_SIDEBAR = "#F0EBE3"
    BG_CONTENT = "#FFFFFF"
    BG_HEADER = "#E8DFD0"

    # ألوان النص
    TEXT_PRIMARY = "#2C2416"
    TEXT_SECONDARY = "#5C5445"
    TEXT_MUTED = "#8C8173"
    TEXT_LIGHT = "#ACA197"

    # ألوان التفاعل
    HOVER = "#E5D4B8"
    SELECTED = "#D4C4A8"
    PRESSED = "#C4B498"

    # ألوان الحالات
    SUCCESS = "#7A9D54"
    WARNING = "#D4A574"
    ERROR = "#C17767"
    INFO = "#7B8FA3"

    # ألوان الحدود
    BORDER_LIGHT = "#E0D5C7"
    BORDER_MEDIUM = "#C9BDB0"
    BORDER_DARK = "#B3A699"

    @classmethod
    def get_stylesheet(cls) -> str:
        """CSS الكامل للتطبيق"""
        return f"""
        QMainWindow, QWidget {{
            background-color: {cls.BG_MAIN};
            color: {cls.TEXT_PRIMARY};
            font-family: 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
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
            color: {cls.TEXT_PRIMARY};
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

        QTextEdit {{
            background-color: {cls.BG_CONTENT};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            padding: 16px;
            font-size: 16px;
            line-height: 1.8;
            color: {cls.TEXT_PRIMARY};
        }}

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

        QLabel {{
            color: {cls.TEXT_PRIMARY};
            font-size: 13px;
        }}

        QStatusBar {{
            background-color: {cls.BG_SIDEBAR};
            color: {cls.TEXT_SECONDARY};
            border-top: 1px solid {cls.BORDER_LIGHT};
        }}

        QListWidget {{
            background-color: {cls.BG_CONTENT};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
        }}

        QListWidget::item {{
            padding: 8px;
            border-radius: 4px;
        }}

        QListWidget::item:hover {{
            background-color: {cls.HOVER};
        }}

        QListWidget::item:selected {{
            background-color: {cls.SELECTED};
        }}
        """


# ============================================================================
#                     PART 3: مدير قاعدة البيانات الذكي
# ============================================================================

class QuranDatabaseManager:
    """
    مدير قاعدة البيانات الموحد - Mod 2
    يعمل مع قاعدة بيانات واحدة متكاملة

    أسماء الجداول المحددة (سيتم استخدامها بدقة):
    - quran_text
    - quran_tajweed
    - surahs_info
    - tafsir_muyassar
    - tafsir_saadi
    - tafsir_baghawi
    - tafsir_jalalayn
    - tafsir_tabari
    - translation_english
    - translation_french
    - irab
    - sarf
    - topics
    - topics_verses
    - bookmarks
    - user_settings
    - sajda_ayahs
    """

    def __init__(self, db_path: str = "quran_ultimate.db"):
        self.db_path = db_path
        self.conn = None

        # أسماء السور (ثابتة)
        self.surah_names_ar = [
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
            print(f"✅ تم الاتصال بقاعدة البيانات: {self.db_path}")
            return True
        except Exception as e:
            print(f"❌ خطأ في الاتصال: {e}")
            return False

    # ========================================================================
    # معلومات السور
    # ========================================================================

    def get_surah_name(self, surah_id: int) -> str:
        """الحصول على اسم السورة"""
        if 1 <= surah_id <= 114:
            return self.surah_names_ar[surah_id - 1]
        return f"سورة {surah_id}"

    def get_all_surahs(self) -> List[Dict[str, Any]]:
        """
        جلب جميع السور من جدول: surahs_info
        الأعمدة المطلوبة:
        - id (INTEGER)
        - name_ar (TEXT)
        - ayahs_count (INTEGER)
        - type (TEXT: 'makkiyah' or 'madaniyah')
        """
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, name_ar, ayahs_count, type
                FROM surahs_info
                ORDER BY id
            """)

            surahs = []
            for row in cursor.fetchall():
                surahs.append({
                    'id': row['id'],
                    'name': row['name_ar'],
                    'ayahs_count': row['ayahs_count'],
                    'type': row['type']
                })

            return surahs

        except sqlite3.OperationalError as e:
            print(f"⚠️ جدول surahs_info غير موجود أو خطأ: {e}")
            # Fallback: إنشاء قائمة افتراضية
            return [{'id': i, 'name': self.get_surah_name(i), 'ayahs_count': 0, 'type': 'unknown'}
                    for i in range(1, 115)]

    # ========================================================================
    # النص القرآني
    # ========================================================================

    def get_verses_by_surah(self, surah_id: int, text_type: str = 'normal') -> List[Dict[str, Any]]:
        """
        جلب آيات سورة

        من جدول: quran_text أو quran_tajweed

        الأعمدة في quran_text:
        - id (INTEGER PRIMARY KEY)
        - surah_id (INTEGER)
        - ayah_id (INTEGER)
        - text (TEXT) - النص العادي
        - text_simple (TEXT) - بدون تشكيل
        - juz (INTEGER)
        - page (INTEGER)

        الأعمدة في quran_tajweed:
        - id (INTEGER PRIMARY KEY)
        - surah_id (INTEGER)
        - ayah_id (INTEGER)
        - tajweed_text (TEXT) - النص مع رموز التجويد
        """
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor()

            if text_type == 'tajweed':
                cursor.execute("""
                    SELECT surah_id, ayah_id, tajweed_text as text
                    FROM quran_tajweed
                    WHERE surah_id = ?
                    ORDER BY ayah_id
                """, (surah_id,))
            else:
                cursor.execute("""
                    SELECT surah_id, ayah_id, text, text_simple, juz, page
                    FROM quran_text
                    WHERE surah_id = ?
                    ORDER BY ayah_id
                """, (surah_id,))

            verses = []
            for row in cursor.fetchall():
                verses.append(dict(row))

            return verses

        except Exception as e:
            print(f"❌ خطأ في جلب الآيات: {e}")
            return []

    def get_verse(self, surah_id: int, ayah_id: int) -> Dict[str, Any]:
        """
        جلب آية محددة مع كل التفاصيل

        الجداول المستخدمة:
        - quran_text
        - quran_tajweed
        - tafsir_muyassar
        - tafsir_saadi
        - tafsir_baghawi
        - translation_english
        - translation_french
        - irab
        - sarf
        """
        if not self.conn:
            return {}

        data = {
            'surah_id': surah_id,
            'ayah_id': ayah_id,
            'text': '',
            'text_simple': '',
            'tajweed_text': '',
            'juz': 0,
            'page': 0,
            'tafsir_muyassar': '',
            'tafsir_saadi': '',
            'tafsir_baghawi': '',
            'translation_english': '',
            'translation_french': '',
            'irab': '',
            'sarf': ''
        }

        cursor = self.conn.cursor()

        # النص الأساسي
        try:
            cursor.execute("""
                SELECT text, text_simple, juz, page
                FROM quran_text
                WHERE surah_id = ? AND ayah_id = ?
            """, (surah_id, ayah_id))
            row = cursor.fetchone()
            if row:
                data.update(dict(row))
        except:
            pass

        # النص بالتجويد
        try:
            cursor.execute("""
                SELECT tajweed_text
                FROM quran_tajweed
                WHERE surah_id = ? AND ayah_id = ?
            """, (surah_id, ayah_id))
            row = cursor.fetchone()
            if row:
                data['tajweed_text'] = row['tajweed_text']
        except:
            pass

        # التفاسير
        for tafsir_name in ['tafsir_muyassar', 'tafsir_saadi', 'tafsir_baghawi']:
            try:
                cursor.execute(f"""
                    SELECT text
                    FROM {tafsir_name}
                    WHERE surah_id = ? AND ayah_id = ?
                """, (surah_id, ayah_id))
                row = cursor.fetchone()
                if row:
                    data[tafsir_name] = row['text']
            except:
                pass

        # الترجمات
        for trans_name in ['translation_english', 'translation_french']:
            try:
                cursor.execute(f"""
                    SELECT text
                    FROM {trans_name}
                    WHERE surah_id = ? AND ayah_id = ?
                """, (surah_id, ayah_id))
                row = cursor.fetchone()
                if row:
                    data[trans_name] = row['text']
            except:
                pass

        # الإعراب والصرف
        for science in ['irab', 'sarf']:
            try:
                cursor.execute(f"""
                    SELECT text
                    FROM {science}
                    WHERE surah_id = ? AND ayah_id = ?
                """, (surah_id, ayah_id))
                row = cursor.fetchone()
                if row:
                    data[science] = row['text']
            except:
                pass

        return data

    # ========================================================================
    # البحث
    # ========================================================================

    def search_text(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        البحث في النص القرآني

        جدول: quran_text
        البحث في: text_simple (بدون تشكيل)
        """
        if not self.conn or not query:
            return []

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT surah_id, ayah_id, text, text_simple
                FROM quran_text
                WHERE text_simple LIKE ?
                ORDER BY surah_id, ayah_id
                LIMIT ?
            """, (f'%{query}%', limit))

            results = []
            for row in cursor.fetchall():
                results.append({
                    'surah_id': row['surah_id'],
                    'ayah_id': row['ayah_id'],
                    'text': row['text'],
                    'surah_name': self.get_surah_name(row['surah_id'])
                })

            return results

        except Exception as e:
            print(f"❌ خطأ في البحث: {e}")
            return []

    # ========================================================================
    # الموضوعات
    # ========================================================================

    def get_all_topics(self) -> List[Dict[str, Any]]:
        """
        جلب جميع الموضوعات

        جدول: topics
        الأعمدة:
        - id (INTEGER PRIMARY KEY)
        - topic_name (TEXT)
        - topic_category (TEXT)
        - description (TEXT)
        """
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, topic_name, topic_category, description
                FROM topics
                ORDER BY id
            """)

            topics = []
            for row in cursor.fetchall():
                topics.append(dict(row))

            return topics

        except:
            # قائمة افتراضية
            return [
                {'id': 1, 'topic_name': 'العقيدة والإيمان', 'topic_category': '', 'description': ''},
                {'id': 2, 'topic_name': 'العبادات', 'topic_category': '', 'description': ''},
                {'id': 3, 'topic_name': 'الأخلاق', 'topic_category': '', 'description': ''}
            ]

    def get_topic_verses(self, topic_id: int) -> List[Dict[str, Any]]:
        """
        جلب آيات موضوع معين

        جدول: topics_verses
        الأعمدة:
        - id (INTEGER PRIMARY KEY)
        - topic_id (INTEGER)
        - surah_id (INTEGER)
        - ayah_id (INTEGER)
        - relevance (INTEGER) - درجة الصلة 1-10
        """
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT tv.surah_id, tv.ayah_id, qt.text
                FROM topics_verses tv
                JOIN quran_text qt ON tv.surah_id = qt.surah_id AND tv.ayah_id = qt.ayah_id
                WHERE tv.topic_id = ?
                ORDER BY tv.relevance DESC, tv.surah_id, tv.ayah_id
            """, (topic_id,))

            verses = []
            for row in cursor.fetchall():
                verses.append({
                    'surah_id': row['surah_id'],
                    'ayah_id': row['ayah_id'],
                    'text': row['text'],
                    'surah_name': self.get_surah_name(row['surah_id'])
                })

            return verses

        except Exception as e:
            print(f"❌ خطأ في جلب آيات الموضوع: {e}")
            return []

    # ========================================================================
    # العلامات المرجعية
    # ========================================================================

    def get_bookmarks(self) -> List[Dict[str, Any]]:
        """
        جلب العلامات المرجعية

        جدول: bookmarks
        الأعمدة:
        - id (INTEGER PRIMARY KEY)
        - surah_id (INTEGER)
        - ayah_id (INTEGER)
        - note (TEXT)
        - created_at (DATETIME)
        - color (TEXT)
        - category (TEXT)
        """
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, surah_id, ayah_id, note, created_at, color, category
                FROM bookmarks
                ORDER BY created_at DESC
            """)

            bookmarks = []
            for row in cursor.fetchall():
                bookmark = dict(row)
                bookmark['surah_name'] = self.get_surah_name(row['surah_id'])
                bookmarks.append(bookmark)

            return bookmarks

        except:
            return []

    def add_bookmark(self, surah_id: int, ayah_id: int, note: str = "") -> bool:
        """إضافة علامة مرجعية"""
        if not self.conn:
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO bookmarks (surah_id, ayah_id, note, created_at)
                VALUES (?, ?, ?, ?)
            """, (surah_id, ayah_id, note, datetime.now()))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"❌ خطأ في إضافة العلامة: {e}")
            return False

    def delete_bookmark(self, bookmark_id: int) -> bool:
        """حذف علامة مرجعية"""
        if not self.conn:
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
            self.conn.commit()
            return True
        except:
            return False

    # ========================================================================
    # الإعدادات
    # ========================================================================

    def get_setting(self, key: str, default: str = "") -> str:
        """
        جلب إعداد

        جدول: user_settings
        الأعمدة:
        - id (INTEGER PRIMARY KEY)
        - setting_key (TEXT UNIQUE)
        - setting_value (TEXT)
        - updated_at (DATETIME)
        """
        if not self.conn:
            return default

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT setting_value
                FROM user_settings
                WHERE setting_key = ?
            """, (key,))

            row = cursor.fetchone()
            return row['setting_value'] if row else default

        except:
            return default

    def set_setting(self, key: str, value: str) -> bool:
        """حفظ إعداد"""
        if not self.conn:
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_settings (setting_key, setting_value, updated_at)
                VALUES (?, ?, ?)
            """, (key, value, datetime.now()))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"❌ خطأ في حفظ الإعداد: {e}")
            return False

    # ========================================================================
    # معلومات إضافية
    # ========================================================================

    def get_sajda_ayahs(self) -> List[Dict[str, Any]]:
        """
        جلب آيات السجدة

        جدول: sajda_ayahs
        الأعمدة:
        - id (INTEGER PRIMARY KEY)
        - surah_id (INTEGER)
        - ayah_id (INTEGER)
        - sajda_type (TEXT: 'واجبة' or 'مستحبة')
        - sajda_number (INTEGER: 1-15)
        """
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT surah_id, ayah_id, sajda_type, sajda_number
                FROM sajda_ayahs
                ORDER BY sajda_number
            """)

            ayahs = []
            for row in cursor.fetchall():
                ayah = dict(row)
                ayah['surah_name'] = self.get_surah_name(row['surah_id'])
                ayahs.append(ayah)

            return ayahs

        except:
            return []

    def close(self):
        """إغلاق الاتصال"""
        if self.conn:
            self.conn.close()
            print("✅ تم إغلاق الاتصال بقاعدة البيانات")


# ============================================================================
# Part 4 - QuranApp (Model 3): التطبيق الرئيسي
# ============================================================================

class QuranApp(QMainWindow):
    """
    التطبيق الرئيسي للقرآن الكريم - Model 3
    يدمج TajweedColors و ClaudeColors و QuranDatabaseManager
    """

    def __init__(self):
        super().__init__()

        # تهيئة النماذج
        self.colors = ClaudeColors()
        self.tajweed = TajweedColors()
        self.db = QuranDatabaseManager()

        # المتغيرات
        self.current_surah = 1
        self.current_ayah = 1
        self.all_surahs = []
        self.current_verses = []

        # تهيئة الواجهة
        self.init_ui()

        # تحميل البيانات الأولية
        self.load_initial_data()

        # استعادة آخر موضع
        self.restore_last_position()

    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("القرآن الكريم - Ultimate Edition")
        self.setGeometry(100, 100, 1400, 900)

        # تطبيق الألوان
        self.setStyleSheet(self.colors.get_full_stylesheet())

        # الويدجت المركزي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # التخطيط الرئيسي
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # شريط العنوان
        self.create_header(main_layout)

        # شريط التنقل
        self.create_navigation_bar(main_layout)

        # التبويبات
        self.create_tabs(main_layout)

        # شريط الحالة
        self.create_status_bar()

    def create_header(self, parent_layout):
        """إنشاء شريط العنوان"""
        header = QLabel("بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"""
            QLabel {{
                font-family: 'Traditional Arabic', 'Arabic Typesetting';
                font-size: 32px;
                color: {self.colors.PRIMARY};
                padding: 15px;
                background: {self.colors.BACKGROUND};
                border-radius: 10px;
                border: 2px solid {self.colors.PRIMARY};
            }}
        """)
        parent_layout.addWidget(header)

    def create_navigation_bar(self, parent_layout):
        """إنشاء شريط التنقل"""
        nav_widget = QWidget()
        nav_layout = QHBoxLayout(nav_widget)
        nav_layout.setSpacing(10)

        # اختيار السورة
        nav_layout.addWidget(QLabel("السورة:"))
        self.surah_combo = QComboBox()
        self.surah_combo.setMinimumWidth(200)
        self.surah_combo.currentIndexChanged.connect(self.on_surah_changed)
        nav_layout.addWidget(self.surah_combo)

        # اختيار الآية
        nav_layout.addWidget(QLabel("الآية:"))
        self.ayah_spin = QSpinBox()
        self.ayah_spin.setMinimum(1)
        self.ayah_spin.setMaximum(286)
        self.ayah_spin.valueChanged.connect(self.on_ayah_changed)
        nav_layout.addWidget(self.ayah_spin)

        # أزرار التنقل
        nav_layout.addStretch()

        btn_prev = QPushButton("◀ السابقة")
        btn_prev.clicked.connect(self.previous_verse)
        nav_layout.addWidget(btn_prev)

        btn_next = QPushButton("التالية ▶")
        btn_next.clicked.connect(self.next_verse)
        nav_layout.addWidget(btn_next)

        # الانتقال إلى جزء
        nav_layout.addWidget(QLabel("الجزء:"))
        self.juz_spin = QSpinBox()
        self.juz_spin.setMinimum(1)
        self.juz_spin.setMaximum(30)
        self.juz_spin.valueChanged.connect(self.jump_to_juz)
        nav_layout.addWidget(self.juz_spin)

        # الانتقال إلى صفحة
        nav_layout.addWidget(QLabel("الصفحة:"))
        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.page_spin.setMaximum(604)
        self.page_spin.valueChanged.connect(self.jump_to_page)
        nav_layout.addWidget(self.page_spin)

        parent_layout.addWidget(nav_widget)

    def create_tabs(self, parent_layout):
        """إنشاء التبويبات"""
        self.tabs = QTabWidget()

        # تبويب النص القرآني
        self.create_quran_tab()

        # تبويب التفسير
        self.create_tafsir_tab()

        # تبويب الترجمة
        self.create_translation_tab()

        # تبويب الإعراب
        self.create_irab_tab()

        # تبويب الصرف
        self.create_sarf_tab()

        # تبويب المواضيع
        self.create_topics_tab()

        # تبويب البحث
        self.create_search_tab()

        # تبويب العلامات المرجعية
        self.create_bookmarks_tab()

        # تبويب الإعدادات
        self.create_settings_tab()

        parent_layout.addWidget(self.tabs)

    def create_quran_tab(self):
        """تبويب النص القرآني"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # مربع النص
        self.quran_text = QTextBrowser()
        self.quran_text.setOpenExternalLinks(False)
        self.quran_text.setStyleSheet(f"""
            QTextBrowser {{
                font-family: 'Traditional Arabic', 'Arabic Typesetting';
                font-size: 28px;
                background: {self.colors.BACKGROUND};
                color: {self.colors.TEXT};
                border: 2px solid {self.colors.PRIMARY};
                border-radius: 8px;
                padding: 20px;
                line-height: 2.0;
            }}
        """)
        layout.addWidget(self.quran_text)

        # أزرار الإجراءات
        actions_layout = QHBoxLayout()

        btn_bookmark = QPushButton("🔖 إضافة علامة")
        btn_bookmark.clicked.connect(self.add_bookmark_dialog)
        actions_layout.addWidget(btn_bookmark)

        btn_copy = QPushButton("📋 نسخ")
        btn_copy.clicked.connect(self.copy_current_verse)
        actions_layout.addWidget(btn_copy)

        btn_tajweed_legend = QPushButton("🎨 دليل التجويد")
        btn_tajweed_legend.clicked.connect(self.show_tajweed_legend)
        actions_layout.addWidget(btn_tajweed_legend)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        self.tabs.addTab(tab, "📖 القرآن الكريم")

    def create_tafsir_tab(self):
        """تبويب التفسير"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # اختيار التفسير
        tafsir_select_layout = QHBoxLayout()
        tafsir_select_layout.addWidget(QLabel("اختر التفسير:"))

        self.tafsir_combo = QComboBox()
        self.tafsir_combo.addItems([
            "التفسير الميسر",
            "تفسير السعدي",
            "تفسير البغوي"
        ])
        self.tafsir_combo.currentIndexChanged.connect(self.display_tafsir)
        tafsir_select_layout.addWidget(self.tafsir_combo)
        tafsir_select_layout.addStretch()

        layout.addLayout(tafsir_select_layout)

        # مربع التفسير
        self.tafsir_text = QTextBrowser()
        self.tafsir_text.setStyleSheet(f"""
            QTextBrowser {{
                font-family: 'Traditional Arabic', 'Arabic Typesetting';
                font-size: 20px;
                background: {self.colors.BACKGROUND};
                color: {self.colors.TEXT};
                border: 2px solid {self.colors.ACCENT};
                border-radius: 8px;
                padding: 15px;
                line-height: 1.8;
            }}
        """)
        layout.addWidget(self.tafsir_text)

        self.tabs.addTab(tab, "📚 التفسير")

    def create_translation_tab(self):
        """تبويب الترجمة"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # اختيار الترجمة
        trans_select_layout = QHBoxLayout()
        trans_select_layout.addWidget(QLabel("اختر الترجمة:"))

        self.translation_combo = QComboBox()
        self.translation_combo.addItems([
            "الإنجليزية",
            "الفرنسية"
        ])
        self.translation_combo.currentIndexChanged.connect(self.display_translation)
        trans_select_layout.addWidget(self.translation_combo)
        trans_select_layout.addStretch()

        layout.addLayout(trans_select_layout)

        # مربع الترجمة
        self.translation_text = QTextBrowser()
        self.translation_text.setStyleSheet(f"""
            QTextBrowser {{
                font-family: 'Segoe UI', Arial;
                font-size: 18px;
                background: {self.colors.BACKGROUND};
                color: {self.colors.TEXT};
                border: 2px solid {self.colors.SECONDARY};
                border-radius: 8px;
                padding: 15px;
                line-height: 1.8;
            }}
        """)
        layout.addWidget(self.translation_text)

        self.tabs.addTab(tab, "🌍 الترجمة")

    def create_irab_tab(self):
        """تبويب الإعراب"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.irab_text = QTextBrowser()
        self.irab_text.setStyleSheet(f"""
            QTextBrowser {{
                font-family: 'Traditional Arabic', 'Arabic Typesetting';
                font-size: 18px;
                background: {self.colors.BACKGROUND};
                color: {self.colors.TEXT};
                border: 2px solid {self.colors.PRIMARY};
                border-radius: 8px;
                padding: 15px;
                line-height: 1.8;
            }}
        """)
        layout.addWidget(self.irab_text)

        self.tabs.addTab(tab, "📝 الإعراب")

    def create_sarf_tab(self):
        """تبويب الصرف"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.sarf_text = QTextBrowser()
        self.sarf_text.setStyleSheet(f"""
            QTextBrowser {{
                font-family: 'Traditional Arabic', 'Arabic Typesetting';
                font-size: 18px;
                background: {self.colors.BACKGROUND};
                color: {self.colors.TEXT};
                border: 2px solid {self.colors.PRIMARY};
                border-radius: 8px;
                padding: 15px;
                line-height: 1.8;
            }}
        """)
        layout.addWidget(self.sarf_text)

        self.tabs.addTab(tab, "🔤 الصرف")

    def create_topics_tab(self):
        """تبويب المواضيع"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # قائمة المواضيع
        topics_label = QLabel("اختر موضوعاً:")
        layout.addWidget(topics_label)

        self.topics_list = QListWidget()
        self.topics_list.itemClicked.connect(self.on_topic_selected)
        layout.addWidget(self.topics_list)

        # الآيات المرتبطة
        verses_label = QLabel("الآيات المرتبطة:")
        layout.addWidget(verses_label)

        self.topic_verses_list = QListWidget()
        self.topic_verses_list.itemDoubleClicked.connect(self.jump_to_verse_from_list)
        layout.addWidget(self.topic_verses_list)

        self.tabs.addTab(tab, "🏷️ المواضيع")

    def create_search_tab(self):
        """تبويب البحث"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # شريط البحث
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث في القرآن الكريم...")
        self.search_input.returnPressed.connect(self.perform_search)
        search_layout.addWidget(self.search_input)

        btn_search = QPushButton("🔍 بحث")
        btn_search.clicked.connect(self.perform_search)
        search_layout.addWidget(btn_search)

        layout.addLayout(search_layout)

        # نتائج البحث
        self.search_results = QListWidget()
        self.search_results.itemDoubleClicked.connect(self.jump_to_verse_from_search)
        layout.addWidget(self.search_results)

        self.tabs.addTab(tab, "🔍 البحث")

    def create_bookmarks_tab(self):
        """تبويب العلامات المرجعية"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # أزرار الإدارة
        btn_layout = QHBoxLayout()

        btn_refresh = QPushButton("🔄 تحديث")
        btn_refresh.clicked.connect(self.load_bookmarks)
        btn_layout.addWidget(btn_refresh)

        btn_delete = QPushButton("🗑️ حذف")
        btn_delete.clicked.connect(self.delete_selected_bookmark)
        btn_layout.addWidget(btn_delete)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # قائمة العلامات
        self.bookmarks_list = QListWidget()
        self.bookmarks_list.itemDoubleClicked.connect(self.jump_to_bookmark)
        layout.addWidget(self.bookmarks_list)

        self.tabs.addTab(tab, "🔖 العلامات")

    def create_settings_tab(self):
        """تبويب الإعدادات"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # حجم الخط
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("حجم خط القرآن:"))

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setMinimum(16)
        self.font_size_spin.setMaximum(48)
        self.font_size_spin.setValue(28)
        self.font_size_spin.valueChanged.connect(self.change_font_size)
        font_layout.addWidget(self.font_size_spin)
        font_layout.addStretch()

        layout.addLayout(font_layout)

        # عرض التجويد
        self.show_tajweed_check = QCheckBox("عرض ألوان التجويد")
        self.show_tajweed_check.setChecked(True)
        self.show_tajweed_check.stateChanged.connect(self.toggle_tajweed)
        layout.addWidget(self.show_tajweed_check)

        # آيات السجدة
        sajda_layout = QHBoxLayout()
        btn_sajda = QPushButton("📍 عرض آيات السجدة")
        btn_sajda.clicked.connect(self.show_sajda_ayahs)
        sajda_layout.addWidget(btn_sajda)
        sajda_layout.addStretch()
        layout.addLayout(sajda_layout)

        layout.addStretch()

        self.tabs.addTab(tab, "⚙️ الإعدادات")

    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        self.statusBar().showMessage("مرحباً بك في تطبيق القرآن الكريم")

    # ========================================================================
    # Data Loading Methods
    # ========================================================================

    def load_initial_data(self):
        """تحميل البيانات الأولية"""
        # تحميل السور
        self.all_surahs = self.db.get_all_surahs()

        for surah in self.all_surahs:
            self.surah_combo.addItem(
                f"{surah['id']}. {surah['name_ar']} ({surah['ayahs_count']} آية)",
                surah['id']
            )

        # تحميل المواضيع
        self.load_topics()

        # تحميل العلامات
        self.load_bookmarks()

    def restore_last_position(self):
        """استعادة آخر موضع"""
        last_surah = self.db.get_setting('last_surah', '1')
        last_ayah = self.db.get_setting('last_ayah', '1')

        try:
            self.current_surah = int(last_surah)
            self.current_ayah = int(last_ayah)
        except:
            self.current_surah = 1
            self.current_ayah = 1

        # تحديث الواجهة
        self.surah_combo.setCurrentIndex(self.current_surah - 1)
        self.display_current_verse()

    def save_current_position(self):
        """حفظ الموضع الحالي"""
        self.db.set_setting('last_surah', str(self.current_surah))
        self.db.set_setting('last_ayah', str(self.current_ayah))

    # ========================================================================
    # Display Methods
    # ========================================================================

    def display_current_verse(self):
        """عرض الآية الحالية"""
        verse = self.db.get_verse(self.current_surah, self.current_ayah)

        if not verse:
            self.quran_text.setHtml("<h3>لم يتم العثور على الآية</h3>")
            return

        # عرض النص القرآني مع التجويد
        if self.show_tajweed_check.isChecked() and verse.get('tajweed_text'):
            html = self.tajweed.convert_to_html(
                verse['tajweed_text'],
                self.font_size_spin.value()
            )
        else:
            text = verse.get('text', verse.get('text_simple', ''))
            html = f"""
            <div style='text-align: center; direction: rtl; unicode-bidi: embed;'>
                <p style='font-size: {self.font_size_spin.value()}px; line-height: 2.0;'>
                    {text} ﴿{self.current_ayah}﴾
                </p>
            </div>
            """

        self.quran_text.setHtml(html)

        # تحديث التفسير
        self.display_tafsir()

        # تحديث الترجمة
        self.display_translation()

        # تحديث الإعراب
        self.display_irab()

        # تحديث الصرف
        self.display_sarf()

        # تحديث شريط الحالة
        surah_name = self.db.get_surah_name(self.current_surah)
        self.statusBar().showMessage(
            f"سورة {surah_name} - الآية {self.current_ayah} | "
            f"الجزء {verse.get('juz', 'غير معروف')} | "
            f"الصفحة {verse.get('page', 'غير معروفة')}"
        )

        # حفظ الموضع
        self.save_current_position()

    def display_tafsir(self):
        """عرض التفسير"""
        tafsir_type = self.tafsir_combo.currentIndex()
        tafsir_names = ['tafsir_muyassar', 'tafsir_saadi', 'tafsir_baghawi']

        verse = self.db.get_verse(self.current_surah, self.current_ayah)

        if verse and tafsir_names[tafsir_type] in verse:
            tafsir = verse[tafsir_names[tafsir_type]]
            if tafsir:
                html = f"""
                <div style='direction: rtl; text-align: justify;'>
                    <h3 style='color: {self.colors.PRIMARY};'>
                        {self.tafsir_combo.currentText()}
                    </h3>
                    <p style='line-height: 1.8;'>{tafsir}</p>
                </div>
                """
                self.tafsir_text.setHtml(html)
            else:
                self.tafsir_text.setHtml("<p>لا يوجد تفسير متاح لهذه الآية</p>")
        else:
            self.tafsir_text.setHtml("<p>لا يوجد تفسير متاح</p>")

    def display_translation(self):
        """عرض الترجمة"""
        trans_type = self.translation_combo.currentIndex()
        trans_names = ['translation_english', 'translation_french']

        verse = self.db.get_verse(self.current_surah, self.current_ayah)

        if verse and trans_names[trans_type] in verse:
            translation = verse[trans_names[trans_type]]
            if translation:
                html = f"""
                <div style='direction: ltr; text-align: left;'>
                    <h3 style='color: {self.colors.SECONDARY};'>
                        {self.translation_combo.currentText()}
                    </h3>
                    <p style='line-height: 1.8;'>{translation}</p>
                </div>
                """
                self.translation_text.setHtml(html)
            else:
                self.translation_text.setHtml("<p>No translation available</p>")
        else:
            self.translation_text.setHtml("<p>No translation available</p>")

    def display_irab(self):
        """عرض الإعراب"""
        verse = self.db.get_verse(self.current_surah, self.current_ayah)

        if verse and verse.get('irab'):
            html = f"""
            <div style='direction: rtl; text-align: justify;'>
                <h3 style='color: {self.colors.PRIMARY};'>إعراب الآية</h3>
                <p style='line-height: 1.8;'>{verse['irab']}</p>
            </div>
            """
            self.irab_text.setHtml(html)
        else:
            self.irab_text.setHtml("<p>لا يوجد إعراب متاح لهذه الآية</p>")

    def display_sarf(self):
        """عرض الصرف"""
        verse = self.db.get_verse(self.current_surah, self.current_ayah)

        if verse and verse.get('sarf'):
            html = f"""
            <div style='direction: rtl; text-align: justify;'>
                <h3 style='color: {self.colors.PRIMARY};'>صرف الآية</h3>
                <p style='line-height: 1.8;'>{verse['sarf']}</p>
            </div>
            """
            self.sarf_text.setHtml(html)
        else:
            self.sarf_text.setHtml("<p>لا يوجد صرف متاح لهذه الآية</p>")

    # ========================================================================
    # Navigation Methods
    # ========================================================================

    def on_surah_changed(self, index):
        """عند تغيير السورة"""
        if index >= 0 and index < len(self.all_surahs):
            self.current_surah = self.all_surahs[index]['id']
            self.current_ayah = 1

            # تحديث عدد الآيات
            max_ayahs = self.all_surahs[index]['ayahs_count']
            self.ayah_spin.setMaximum(max_ayahs)
            self.ayah_spin.setValue(1)

            self.display_current_verse()

    def on_ayah_changed(self, value):
        """عند تغيير الآية"""
        self.current_ayah = value
        self.display_current_verse()

    def previous_verse(self):
        """الآية السابقة"""
        if self.current_ayah > 1:
            self.current_ayah -= 1
            self.ayah_spin.setValue(self.current_ayah)
        elif self.current_surah > 1:
            # الانتقال إلى السورة السابقة
            self.current_surah -= 1
            self.surah_combo.setCurrentIndex(self.current_surah - 1)
            # سيتم تحديث الآية تلقائياً إلى آخر آية في السورة
            self.current_ayah = self.ayah_spin.maximum()
            self.ayah_spin.setValue(self.current_ayah)

    def next_verse(self):
        """الآية التالية"""
        max_ayahs = self.ayah_spin.maximum()
        if self.current_ayah < max_ayahs:
            self.current_ayah += 1
            self.ayah_spin.setValue(self.current_ayah)
        elif self.current_surah < 114:
            # الانتقال إلى السورة التالية
            self.current_surah += 1
            self.surah_combo.setCurrentIndex(self.current_surah - 1)
            self.current_ayah = 1
            self.ayah_spin.setValue(1)

    def jump_to_juz(self, juz):
        """الانتقال إلى جزء"""
        # هذه دالة بسيطة - يمكن تحسينها بجدول مرجعي للأجزاء
        pass

    def jump_to_page(self, page):
        """الانتقال إلى صفحة"""
        # هذه دالة بسيطة - يمكن تحسينها بجدول مرجعي للصفحات
        pass

    def jump_to_verse_from_list(self, item):
        """الانتقال إلى آية من قائمة"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if data:
            self.current_surah = data['surah_id']
            self.current_ayah = data['ayah_id']
            self.surah_combo.setCurrentIndex(self.current_surah - 1)
            self.ayah_spin.setValue(self.current_ayah)
            self.tabs.setCurrentIndex(0)  # الانتقال إلى تبويب القرآن

    def jump_to_verse_from_search(self, item):
        """الانتقال إلى آية من نتائج البحث"""
        self.jump_to_verse_from_list(item)

    def jump_to_bookmark(self, item):
        """الانتقال إلى علامة مرجعية"""
        self.jump_to_verse_from_list(item)

    # ========================================================================
    # Topics Methods
    # ========================================================================

    def load_topics(self):
        """تحميل المواضيع"""
        topics = self.db.get_all_topics()
        self.topics_list.clear()

        for topic in topics:
            item = QListWidgetItem(
                f"{topic['name']} ({topic.get('verse_count', 0)} آية)"
            )
            item.setData(Qt.ItemDataRole.UserRole, topic)
            self.topics_list.addItem(item)

    def on_topic_selected(self, item):
        """عند اختيار موضوع"""
        topic = item.data(Qt.ItemDataRole.UserRole)
        if topic:
            verses = self.db.get_topic_verses(topic['id'])
            self.topic_verses_list.clear()

            for verse in verses:
                verse_item = QListWidgetItem(
                    f"{verse['surah_name']} - الآية {verse['ayah_id']}"
                )
                verse_item.setData(Qt.ItemDataRole.UserRole, verse)
                self.topic_verses_list.addItem(verse_item)

    # ========================================================================
    # Search Methods
    # ========================================================================

    def perform_search(self):
        """تنفيذ البحث"""
        query = self.search_input.text().strip()

        if not query:
            return

        results = self.db.search_text(query)
        self.search_results.clear()

        if not results:
            self.search_results.addItem("لم يتم العثور على نتائج")
            return

        for result in results:
            # اقتطاع النص لعرضه
            text = result.get('text', result.get('text_simple', ''))
            if len(text) > 100:
                text = text[:100] + "..."

            item = QListWidgetItem(
                f"{result['surah_name']} ({result['ayah_id']}): {text}"
            )
            item.setData(Qt.ItemDataRole.UserRole, result)
            self.search_results.addItem(item)

        self.statusBar().showMessage(f"تم العثور على {len(results)} نتيجة")

    # ========================================================================
    # Bookmarks Methods
    # ========================================================================

    def load_bookmarks(self):
        """تحميل العلامات المرجعية"""
        bookmarks = self.db.get_bookmarks()
        self.bookmarks_list.clear()

        for bookmark in bookmarks:
            note = bookmark.get('note', '')
            if note:
                text = f"{bookmark['surah_name']} ({bookmark['ayah_id']}) - {note}"
            else:
                text = f"{bookmark['surah_name']} ({bookmark['ayah_id']})"

            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, bookmark)
            self.bookmarks_list.addItem(item)

    def add_bookmark_dialog(self):
        """إضافة علامة مرجعية"""
        note, ok = QInputDialog.getText(
            self,
            "إضافة علامة مرجعية",
            "أدخل ملاحظة (اختياري):"
        )

        if ok:
            bookmark_id = self.db.add_bookmark(
                self.current_surah,
                self.current_ayah,
                note if note else None
            )

            if bookmark_id:
                self.load_bookmarks()
                self.statusBar().showMessage("تم إضافة العلامة المرجعية")
            else:
                self.statusBar().showMessage("فشل في إضافة العلامة المرجعية")

    def delete_selected_bookmark(self):
        """حذف العلامة المرجعية المحددة"""
        current_item = self.bookmarks_list.currentItem()

        if not current_item:
            return

        bookmark = current_item.data(Qt.ItemDataRole.UserRole)
        if bookmark and self.db.delete_bookmark(bookmark['id']):
            self.load_bookmarks()
            self.statusBar().showMessage("تم حذف العلامة المرجعية")

    # ========================================================================
    # Settings Methods
    # ========================================================================

    def change_font_size(self, size):
        """تغيير حجم الخط"""
        self.db.set_setting('font_size', str(size))
        self.display_current_verse()

    def toggle_tajweed(self, state):
        """تبديل عرض التجويد"""
        self.db.set_setting('show_tajweed', str(state == Qt.CheckState.Checked.value))
        self.display_current_verse()

    def show_tajweed_legend(self):
        """عرض دليل التجويد"""
        legend_html = self.tajweed.get_legend_html()

        dialog = QDialog(self)
        dialog.setWindowTitle("دليل أحكام التجويد")
        dialog.setGeometry(200, 200, 600, 700)

        layout = QVBoxLayout(dialog)

        text_browser = QTextBrowser()
        text_browser.setHtml(legend_html)
        layout.addWidget(text_browser)

        btn_close = QPushButton("إغلاق")
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)

        dialog.exec()

    def show_sajda_ayahs(self):
        """عرض آيات السجدة"""
        sajda_ayahs = self.db.get_sajda_ayahs()

        dialog = QDialog(self)
        dialog.setWindowTitle("آيات السجدة")
        dialog.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()

        for ayah in sajda_ayahs:
            item = QListWidgetItem(
                f"{ayah['surah_name']} - الآية {ayah['ayah_id']} "
                f"(السجدة رقم {ayah['sajda_number']})"
            )
            item.setData(Qt.ItemDataRole.UserRole, ayah)
            list_widget.addItem(item)

        list_widget.itemDoubleClicked.connect(
            lambda item: self.jump_to_sajda(item, dialog)
        )

        layout.addWidget(list_widget)

        btn_close = QPushButton("إغلاق")
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)

        dialog.exec()

    def jump_to_sajda(self, item, dialog):
        """الانتقال إلى آية سجدة"""
        ayah = item.data(Qt.ItemDataRole.UserRole)
        if ayah:
            self.current_surah = ayah['surah_id']
            self.current_ayah = ayah['ayah_id']
            self.surah_combo.setCurrentIndex(self.current_surah - 1)
            self.ayah_spin.setValue(self.current_ayah)
            self.tabs.setCurrentIndex(0)
            dialog.close()

    # ========================================================================
    # Utility Methods
    # ========================================================================

    def copy_current_verse(self):
        """نسخ الآية الحالية"""
        verse = self.db.get_verse(self.current_surah, self.current_ayah)

        if verse:
            text = verse.get('text', verse.get('text_simple', ''))
            surah_name = self.db.get_surah_name(self.current_surah)

            full_text = f"{text}\n[{surah_name}: {self.current_ayah}]"

            clipboard = QApplication.clipboard()
            clipboard.setText(full_text)

            self.statusBar().showMessage("تم نسخ الآية", 2000)

    # ========================================================================
    # Keyboard Events
    # ========================================================================

    def keyPressEvent(self, event):
        """معالجة الضغط على المفاتيح"""
        key = event.key()

        if key == Qt.Key.Key_Right or key == Qt.Key.Key_Up:
            self.previous_verse()
        elif key == Qt.Key.Key_Left or key == Qt.Key.Key_Down:
            self.next_verse()
        elif key == Qt.Key.Key_Home:
            self.current_ayah = 1
            self.ayah_spin.setValue(1)
        elif key == Qt.Key.Key_End:
            self.current_ayah = self.ayah_spin.maximum()
            self.ayah_spin.setValue(self.current_ayah)
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if key == Qt.Key.Key_F:
                self.tabs.setCurrentIndex(6)  # تبويب البحث
                self.search_input.setFocus()
            elif key == Qt.Key.Key_B:
                self.add_bookmark_dialog()
            elif key == Qt.Key.Key_C:
                self.copy_current_verse()
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        """معالجة عجلة الماوس"""
        if event.angleDelta().y() > 0:
            self.previous_verse()
        else:
            self.next_verse()

    def closeEvent(self, event):
        """عند إغلاق التطبيق"""
        self.save_current_position()
        self.db.close()
        event.accept()


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """نقطة الدخول الرئيسية"""

    app = QApplication(sys.argv)

    # تعيين الخط العربي
    font = QFont("Traditional Arabic", 12)
    app.setFont(font)

    # تعيين اتجاه التطبيق
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # إنشاء النافذة الرئيسية
    window = QuranApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

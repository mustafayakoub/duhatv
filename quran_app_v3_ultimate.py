#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                    تطبيق القرآن الكريم النهائي - النسخة 3.0
         مُحدّث للعمل مع قاعدة بيانات quran_ultimate_final.db
================================================================================

المطور: Claude AI Assistant
النسخة: 3.0 Ultimate Edition
التاريخ: 2025-10-31

الميزات الجديدة:
✨ دعم 43 تفسير مختلف
✨ بنية قاعدة بيانات جديدة (جداول مرقمة)
✨ واجهة محسّنة للتفاسير المتعددة
✨ أداء أسرع وأكثر كفاءة
"""

import sys
import os
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any

# محاولة استيراد PyQt6، وإذا فشل نستخدم PyQt5
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTreeWidget, QTreeWidgetItem, QTabWidget, QTextEdit, QLabel,
        QPushButton, QLineEdit, QComboBox, QSplitter, QFrame, QMessageBox,
        QStatusBar
    )
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont
    PYQT_VERSION = 6
    print("✅ استخدام PyQt6")
except ImportError:
    try:
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QTreeWidget, QTreeWidgetItem, QTabWidget, QTextEdit, QLabel,
            QPushButton, QLineEdit, QComboBox, QSplitter, QFrame, QMessageBox,
            QStatusBar
        )
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QFont
        PYQT_VERSION = 5
        print("✅ استخدام PyQt5")
    except ImportError:
        print("❌ خطأ: يجب تثبيت PyQt6 أو PyQt5")
        sys.exit(1)


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

    HOVER = "#E5D4B8"
    SELECTED = "#D4C4A8"

    BORDER_LIGHT = "#E0D5C7"

    @classmethod
    def get_stylesheet(cls) -> str:
        """الحصول على ورقة الأنماط الكاملة"""
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
        }}

        QTabBar::tab:selected {{
            background-color: {cls.PRIMARY};
            color: white;
        }}

        QTextEdit {{
            background-color: {cls.BG_CONTENT};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            padding: 16px;
            font-size: 16px;
            line-height: 1.8;
        }}

        QPushButton {{
            background-color: {cls.PRIMARY};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
        }}

        QPushButton:hover {{
            background-color: {cls.ACCENT};
        }}

        QComboBox {{
            background-color: {cls.BG_CONTENT};
            border: 2px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            padding: 8px 16px;
        }}

        QLineEdit {{
            background-color: {cls.BG_CONTENT};
            border: 2px solid {cls.BORDER_LIGHT};
            border-radius: 8px;
            padding: 10px 16px;
        }}
        """


# ============================================================================
#                    مدير قاعدة البيانات الجديد - النسخة 3.0
# ============================================================================

class UltimateDatabaseManager:
    """مدير قاعدة البيانات المُحدّث لـ quran_ultimate_final.db"""

    # خريطة أسماء السور (114 سورة)
    SURAH_NAMES = {
        1: "الفاتحة", 2: "البقرة", 3: "آل عمران", 4: "النساء", 5: "المائدة",
        6: "الأنعام", 7: "الأعراف", 8: "الأنفال", 9: "التوبة", 10: "يونس",
        11: "هود", 12: "يوسف", 13: "الرعد", 14: "إبراهيم", 15: "الحجر",
        16: "النحل", 17: "الإسراء", 18: "الكهف", 19: "مريم", 20: "طه",
        21: "الأنبياء", 22: "الحج", 23: "المؤمنون", 24: "النور", 25: "الفرقان",
        26: "الشعراء", 27: "النمل", 28: "القصص", 29: "العنكبوت", 30: "الروم",
        31: "لقمان", 32: "السجدة", 33: "الأحزاب", 34: "سبأ", 35: "فاطر",
        36: "يس", 37: "الصافات", 38: "ص", 39: "الزمر", 40: "غافر",
        41: "فصلت", 42: "الشورى", 43: "الزخرف", 44: "الدخان", 45: "الجاثية",
        46: "الأحقاف", 47: "محمد", 48: "الفتح", 49: "الحجرات", 50: "ق",
        51: "الذاريات", 52: "الطور", 53: "النجم", 54: "القمر", 55: "الرحمن",
        56: "الواقعة", 57: "الحديد", 58: "المجادلة", 59: "الحشر", 60: "الممتحنة",
        61: "الصف", 62: "الجمعة", 63: "المنافقون", 64: "التغابن", 65: "الطلاق",
        66: "التحريم", 67: "الملك", 68: "القلم", 69: "الحاقة", 70: "المعارج",
        71: "نوح", 72: "الجن", 73: "المزمل", 74: "المدثر", 75: "القيامة",
        76: "الإنسان", 77: "المرسلات", 78: "النبأ", 79: "النازعات", 80: "عبس",
        81: "التكوير", 82: "الانفطار", 83: "المطففين", 84: "الانشقاق", 85: "البروج",
        86: "الطارق", 87: "الأعلى", 88: "الغاشية", 89: "الفجر", 90: "البلد",
        91: "الشمس", 92: "الليل", 93: "الضحى", 94: "الشرح", 95: "التين",
        96: "العلق", 97: "القدر", 98: "البينة", 99: "الزلزلة", 100: "العاديات",
        101: "القارعة", 102: "التكاثر", 103: "العصر", 104: "الهمزة", 105: "الفيل",
        106: "قريش", 107: "الماعون", 108: "الكوثر", 109: "الكافرون", 110: "النصر",
        111: "المسد", 112: "الإخلاص", 113: "الفلق", 114: "الناس"
    }

    # خريطة أسماء التفاسير (سيتم ملؤها من قاعدة البيانات)
    TAFSIR_NAMES = {}

    def __init__(self):
        self.conn: Optional[sqlite3.Connection] = None
        self.db_path: Optional[str] = None
        self.available_tafasir: List[int] = []

    def find_database(self) -> Optional[str]:
        """البحث عن قاعدة البيانات"""
        possible_paths = [
            r"C:\quran9\quran_ultimate_final.db",
            "quran_ultimate_final.db",
            "./quran_ultimate_final.db",
            "../quran_ultimate_final.db",
        ]

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

            # اكتشاف التفاسير المتوفرة
            self._discover_tafasir()

            print(f"✅ تم الاتصال بنجاح - {len(self.available_tafasir)} تفسير متوفر")
            return True

        except Exception as e:
            print(f"❌ خطأ في الاتصال: {e}")
            return False

    def _discover_tafasir(self):
        """اكتشاف التفاسير المتوفرة"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT NTafsir FROM '001' ORDER BY NTafsir")
            self.available_tafasir = [row[0] for row in cursor.fetchall()]
            print(f"📚 تم اكتشاف {len(self.available_tafasir)} تفسير")
        except Exception as e:
            print(f"⚠️ خطأ في اكتشاف التفاسير: {e}")
            self.available_tafasir = []

    def get_surahs(self) -> List[Dict[str, Any]]:
        """الحصول على قائمة السور"""
        surahs = []
        for surah_id, surah_name in self.SURAH_NAMES.items():
            surahs.append({
                'id': surah_id,
                'name': surah_name,
                'table': f"{surah_id:03d}"
            })
        return surahs

    def get_ayah_count(self, surah_id: int) -> int:
        """الحصول على عدد آيات السورة"""
        try:
            table_name = f"{surah_id:03d}"
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(DISTINCT NAya) FROM '{table_name}'")
            return cursor.fetchone()[0]
        except:
            return 0

    def get_ayah_text(self, surah_id: int, ayah_num: int, tafsir_id: int = 6) -> Optional[str]:
        """الحصول على نص آية محددة"""
        try:
            table_name = f"{surah_id:03d}"
            cursor = self.conn.cursor()
            cursor.execute(
                f"SELECT Texte FROM '{table_name}' WHERE NAya = ? AND NTafsir = ? LIMIT 1",
                (ayah_num, tafsir_id)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print(f"خطأ في جلب الآية: {e}")
            return None

    def get_tafsir(self, surah_id: int, ayah_num: int, tafsir_id: int) -> Optional[str]:
        """الحصول على تفسير آية محددة"""
        return self.get_ayah_text(surah_id, ayah_num, tafsir_id)

    def search_text(self, text: str, limit: int = 100) -> List[Dict[str, Any]]:
        """البحث في القرآن"""
        if not text:
            return []

        results = []
        try:
            for surah_id in range(1, 115):
                table_name = f"{surah_id:03d}"
                cursor = self.conn.cursor()

                # البحث في التفسير 6 (نص القرآن الأساسي)
                cursor.execute(
                    f"SELECT NAya, Texte FROM '{table_name}' WHERE NTafsir = 6 AND Texte LIKE ? LIMIT ?",
                    (f'%{text}%', limit)
                )

                for row in cursor.fetchall():
                    results.append({
                        'surah_id': surah_id,
                        'surah_name': self.SURAH_NAMES.get(surah_id, f'سورة {surah_id}'),
                        'ayah_num': row[0],
                        'text': row[1]
                    })

                    if len(results) >= limit:
                        return results

        except Exception as e:
            print(f"خطأ في البحث: {e}")

        return results

    def close(self):
        """إغلاق الاتصال"""
        if self.conn:
            self.conn.close()


# ============================================================================
#                              التطبيق الرئيسي
# ============================================================================

# (باقي الكود سيكون في الملف التالي...)

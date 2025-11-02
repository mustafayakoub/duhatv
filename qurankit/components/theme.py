#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 QuranThemeComponent - المظاهر والثيمات
Theme Component for managing application themes
"""

from typing import Dict, Any, Optional
from pathlib import Path
import json


class QuranThemeComponent:
    """مكون إدارة المظاهر والثيمات"""

    THEMES = {
        'light': {
            'name': 'فاتح',
            'name_en': 'Light',
            'background': '#ffffff',
            'text': '#212121',
            'text_secondary': '#757575',
            'primary': '#1e3c72',
            'secondary': '#2a5298',
            'accent': '#2c5aa0',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'border': '#e0e0e0',
            'card_bg': '#f9f9f9',
            'hover': '#f5f5f5',
            'selected': '#e3f2fd',
            'gradient_start': '#1e3c72',
            'gradient_end': '#2a5298',
            'highlight': '#ffeb3b',
        },
        'dark': {
            'name': 'داكن',
            'name_en': 'Dark',
            'background': '#1a1a1a',
            'text': '#ffffff',
            'text_secondary': '#b0b0b0',
            'primary': '#2a5298',
            'secondary': '#3d6bb3',
            'accent': '#4a7bc8',
            'success': '#2ecc71',
            'warning': '#f1c40f',
            'error': '#e67e73',
            'border': '#333333',
            'card_bg': '#252525',
            'hover': '#2d2d2d',
            'selected': '#1e4d8b',
            'gradient_start': '#2a5298',
            'gradient_end': '#3d6bb3',
            'highlight': '#ffd54f',
        },
        'sepia': {
            'name': 'بني',
            'name_en': 'Sepia',
            'background': '#f4ecd8',
            'text': '#5b4636',
            'text_secondary': '#8b7355',
            'primary': '#8b6914',
            'secondary': '#a67c1b',
            'accent': '#d4af37',
            'success': '#6b8e23',
            'warning': '#cd853f',
            'error': '#a0522d',
            'border': '#d4c5a9',
            'card_bg': '#f9f6ed',
            'hover': '#eee6d5',
            'selected': '#efe0c7',
            'gradient_start': '#8b6914',
            'gradient_end': '#a67c1b',
            'highlight': '#ffeb99',
        },
        'green': {
            'name': 'أخضر',
            'name_en': 'Green',
            'background': '#ffffff',
            'text': '#212121',
            'text_secondary': '#757575',
            'primary': '#2e7d32',
            'secondary': '#388e3c',
            'accent': '#43a047',
            'success': '#66bb6a',
            'warning': '#ffa726',
            'error': '#ef5350',
            'border': '#e0e0e0',
            'card_bg': '#f1f8f4',
            'hover': '#e8f5e9',
            'selected': '#c8e6c9',
            'gradient_start': '#2e7d32',
            'gradient_end': '#388e3c',
            'highlight': '#ffeb3b',
        }
    }

    def __init__(self, theme_name: str = 'light', config: Dict = None):
        self.config = config or {}
        self.current_theme = theme_name
        self.custom_themes = {}
        self.config_file = Path(self.config.get('config_file', Path.home() / '.qurankit' / 'theme_config.json'))

        # تحميل المظاهر المخصصة
        self.load_custom_themes()

    def get_theme(self, name: str = None) -> Dict[str, str]:
        """الحصول على ثيم"""
        name = name or self.current_theme

        # البحث في المظاهر الافتراضية أولاً
        if name in self.THEMES:
            return self.THEMES[name].copy()

        # ثم المظاهر المخصصة
        if name in self.custom_themes:
            return self.custom_themes[name].copy()

        # الافتراضي
        return self.THEMES['light'].copy()

    def set_theme(self, theme_name: str):
        """تعيين الثيم الحالي"""
        if theme_name in self.THEMES or theme_name in self.custom_themes:
            self.current_theme = theme_name
            self.save_config()

    def get_available_themes(self) -> Dict[str, str]:
        """الحصول على قائمة المظاهر المتاحة"""
        themes = {}

        # المظاهر الافتراضية
        for theme_id, theme_data in self.THEMES.items():
            themes[theme_id] = theme_data.get('name', theme_id)

        # المظاهر المخصصة
        for theme_id, theme_data in self.custom_themes.items():
            themes[theme_id] = theme_data.get('name', theme_id)

        return themes

    def create_custom_theme(self, theme_id: str, theme_name: str, colors: Dict[str, str]) -> bool:
        """إنشاء ثيم مخصص"""
        # التحقق من أن الثيم لا يستخدم اسم محجوز
        if theme_id in self.THEMES:
            return False

        theme_data = {
            'name': theme_name,
            'name_en': theme_id,
            **colors
        }

        self.custom_themes[theme_id] = theme_data
        self.save_custom_themes()
        return True

    def delete_custom_theme(self, theme_id: str) -> bool:
        """حذف ثيم مخصص"""
        if theme_id in self.custom_themes:
            del self.custom_themes[theme_id]
            self.save_custom_themes()

            # إذا كان الثيم المحذوف هو الحالي، العودة للافتراضي
            if self.current_theme == theme_id:
                self.current_theme = 'light'
                self.save_config()

            return True
        return False

    def apply_theme_to_stylesheet(self, widget, theme_name: str = None) -> str:
        """تطبيق ثيم على widget وإرجاع stylesheet"""
        theme = self.get_theme(theme_name)

        stylesheet = f"""
        QWidget {{
            background-color: {theme['background']};
            color: {theme['text']};
            font-family: 'Arial', 'Traditional Arabic', sans-serif;
        }}

        QPushButton {{
            background-color: {theme['primary']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
            font-weight: bold;
        }}

        QPushButton:hover {{
            background-color: {theme['secondary']};
        }}

        QPushButton:pressed {{
            background-color: {theme['accent']};
        }}

        QPushButton:disabled {{
            background-color: {theme['border']};
            color: {theme['text_secondary']};
        }}

        QLineEdit, QTextEdit, QTextBrowser {{
            background-color: {theme['card_bg']};
            color: {theme['text']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
            padding: 4px;
        }}

        QLineEdit:focus, QTextEdit:focus {{
            border: 2px solid {theme['primary']};
        }}

        QComboBox {{
            background-color: {theme['card_bg']};
            color: {theme['text']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
            padding: 4px;
        }}

        QComboBox:hover {{
            border: 1px solid {theme['primary']};
        }}

        QTreeWidget, QListWidget {{
            background-color: {theme['card_bg']};
            color: {theme['text']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
        }}

        QTreeWidget::item:hover, QListWidget::item:hover {{
            background-color: {theme['hover']};
        }}

        QTreeWidget::item:selected, QListWidget::item:selected {{
            background-color: {theme['selected']};
            color: {theme['text']};
        }}

        QScrollBar:vertical {{
            background-color: {theme['card_bg']};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {theme['primary']};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {theme['secondary']};
        }}

        QMenuBar {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}

        QMenuBar::item:selected {{
            background-color: {theme['hover']};
        }}

        QMenu {{
            background-color: {theme['card_bg']};
            color: {theme['text']};
            border: 1px solid {theme['border']};
        }}

        QMenu::item:selected {{
            background-color: {theme['selected']};
        }}

        QStatusBar {{
            background-color: {theme['card_bg']};
            color: {theme['text_secondary']};
        }}

        QGroupBox {{
            border: 2px solid {theme['border']};
            border-radius: 6px;
            margin-top: 10px;
            font-weight: bold;
        }}

        QGroupBox::title {{
            color: {theme['primary']};
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        """

        return stylesheet

    def get_color(self, color_name: str, theme_name: str = None) -> str:
        """الحصول على لون محدد من الثيم"""
        theme = self.get_theme(theme_name)
        return theme.get(color_name, '#000000')

    def is_dark_theme(self, theme_name: str = None) -> bool:
        """التحقق إذا كان الثيم داكناً"""
        theme_name = theme_name or self.current_theme
        return theme_name in ['dark']

    def save_custom_themes(self):
        """حفظ المظاهر المخصصة"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'current_theme': self.current_theme,
                    'custom_themes': self.custom_themes
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ المظاهر: {e}")

    def load_custom_themes(self):
        """تحميل المظاهر المخصصة"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.current_theme = data.get('current_theme', 'light')
                    self.custom_themes = data.get('custom_themes', {})
        except Exception as e:
            print(f"خطأ في تحميل المظاهر: {e}")

    def save_config(self):
        """حفظ إعدادات الثيم"""
        self.save_custom_themes()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
📦 QuranKit - مكتبة المكونات القرآنية القابلة لإعادة الاستخدام
Quran Components Library - Reusable Modular Components
═══════════════════════════════════════════════════════════════

🎯 الهدف:
توفير مكونات جاهزة وقابلة لإعادة الاستخدام لبناء تطبيقات القرآن الكريم

🌟 المكونات المتوفرة:
1. QuranSearchComponent - البحث المتقدم
2. QuranTreeComponent - شجرة التصفح (أجزاء/سور/آيات)
3. QuranMorphologyComponent - البحث الصرفي
4. QuranDisplayComponent - عرض الآيات
5. QuranAudioComponent - مشغل الصوت
6. QuranBookmarksComponent - الإشارات المرجعية
7. QuranThemeComponent - المظاهر والثيمات
8. QuranTajweedComponent - ألوان وأحكام التجويد 🎨

═══════════════════════════════════════════════════════════════
🏢 AiGrow | 👨‍💻 Mustafa Yakoub
📧 duhatv@gmail.com | 🌐 duhatv.net
═══════════════════════════════════════════════════════════════
"""

__version__ = "1.0.0"
__author__ = "Mustafa Yakoub"
__email__ = "duhatv@gmail.com"
__all__ = [
    'QuranSearchComponent',
    'QuranTreeComponent',
    'QuranMorphologyComponent',
    'QuranDisplayComponent',
    'QuranAudioComponent',
    'QuranBookmarksComponent',
    'QuranThemeComponent',
    'QuranTajweedComponent'
]

# ═══════════════════════════════════════════════════════════════
# Imports
# ═══════════════════════════════════════════════════════════════

from .components.search import QuranSearchComponent
from .components.tree import QuranTreeComponent
from .components.morphology import QuranMorphologyComponent
from .components.display import QuranDisplayComponent
from .components.audio import QuranAudioComponent
from .components.bookmarks import QuranBookmarksComponent
from .components.theme import QuranThemeComponent
from .components.tajweed import QuranTajweedComponent, TajweedRule

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

class QuranKitConfig:
    """إعدادات QuranKit العامة"""

    # الخطوط الافتراضية
    DEFAULT_ARABIC_FONT = "Arial"
    DEFAULT_FONT_SIZE = 14

    # الألوان الافتراضية
    PRIMARY_COLOR = "#1e3c72"
    SECONDARY_COLOR = "#2a5298"
    HIGHLIGHT_COLOR = "#ffeb3b"
    TEXT_COLOR = "#212121"

    # إعدادات البحث
    SEARCH_LIMIT = 50
    SEARCH_MIN_LENGTH = 2

    # إعدادات العرض
    DISPLAY_ANIMATION = True
    SMOOTH_SCROLL = True

    @classmethod
    def load_from_file(cls, config_path: str):
        """تحميل الإعدادات من ملف"""
        pass

    @classmethod
    def save_to_file(cls, config_path: str):
        """حفظ الإعدادات في ملف"""
        pass


# ═══════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════

def init_qurankit(config=None):
    """
    تهيئة QuranKit

    Args:
        config: كائن الإعدادات (اختياري)

    Example:
        >>> import qurankit
        >>> qurankit.init_qurankit()
    """
    if config:
        QuranKitConfig.__dict__.update(config.__dict__)

    print(f"✅ QuranKit v{__version__} initialized")


def get_version():
    """الحصول على رقم الإصدار"""
    return __version__


def list_components():
    """عرض جميع المكونات المتاحة"""
    return __all__


# ═══════════════════════════════════════════════════════════════
# Usage Example
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 70)
    print(f"📦 QuranKit v{__version__}")
    print("═" * 70)
    print("\n✨ مكتبة المكونات القرآنية القابلة لإعادة الاستخدام\n")

    print("🎯 المكونات المتوفرة:")
    for i, component in enumerate(__all__, 1):
        print(f"   {i}. {component}")

    print("\n📖 للاستخدام:")
    print("   from qurankit import QuranSearchComponent")
    print("   search = QuranSearchComponent(database)")
    print("   results = search.search('الله')")

    print("\n🌐 المزيد من المعلومات:")
    print("   https://github.com/duhatv/qurankit")
    print("   duhatv@gmail.com")
    print("═" * 70)

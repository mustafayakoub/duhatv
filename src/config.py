#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
📖 ملف الإعدادات - تطبيق القرآن الكريم Pro
═══════════════════════════════════════════════════════════════
"""

from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# معلومات التطبيق
# ═══════════════════════════════════════════════════════════════

APP_NAME = "القرآن الكريم Pro"
APP_VERSION = "2.1.0"
COMPANY = "AiGrow"
DEVELOPER = "Mustafa Yakoub"
EMAIL = "duhatv@gmail.com"
WEBSITE = "duhatv.net"
PHONE = "+905342390000"

# ═══════════════════════════════════════════════════════════════
# المسارات
# ═══════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
FONTS_DIR = BASE_DIR / "fonts"
DOCS_DIR = BASE_DIR / "docs"

# قاعدة البيانات
DB_PATH = DATA_DIR / "quran_ultimate_final.db"
DB_BACKUP_DIR = DATA_DIR / "backups"

# الخطوط
FONT_AMIRI = FONTS_DIR / "Amiri-Quran.ttf"
FONT_UTHMAN = FONTS_DIR / "UthmanicHafs.otf"
FONT_NOOREHUDA = FONTS_DIR / "noorehuda.ttf"
FONT_NOOREHIRA = FONTS_DIR / "noorehira.ttf"
FONT_SCHEHERAZADE = FONTS_DIR / "ScheherazadeNew-Regular.ttf"

# الأدلة
USER_GUIDE_AR = DOCS_DIR / "user_guide_ar.pdf"
USER_GUIDE_EN = DOCS_DIR / "user_guide_en.pdf"

# الأيقونة
ICON_PATH = BASE_DIR / "icon.ico"

# ═══════════════════════════════════════════════════════════════
# إعدادات النافذة
# ═══════════════════════════════════════════════════════════════

WINDOW_SIZE = {
    'width': 1400,
    'height': 900,
    'min_width': 1000,
    'min_height': 700,
    'fullscreen': False
}

# ═══════════════════════════════════════════════════════════════
# الألوان (مستوحاة من Tanzil.net)
# ═══════════════════════════════════════════════════════════════

COLORS = {
    # الألوان الأساسية
    'primary': '#2c5aa0',           # أزرق داكن
    'secondary': '#4a90e2',         # أزرق فاتح
    'success': '#27ae60',           # أخضر
    'warning': '#f39c12',           # برتقالي
    'danger': '#e74c3c',            # أحمر
    'info': '#3498db',              # أزرق سماوي

    # ألوان الخلفية
    'bg_light': '#f8f9fa',          # خلفية فاتحة
    'bg_dark': '#2c3e50',           # خلفية داكنة
    'bg_selected': '#e8f4f8',       # خلفية محددة
    'bg_hover': '#d6eaf8',          # عند التمرير

    # ألوان النصوص
    'text_primary': '#2c3e50',      # نص رئيسي
    'text_secondary': '#7f8c8d',    # نص ثانوي
    'text_light': '#95a5a6',        # نص فاتح
    'white': '#ffffff',
    'black': '#000000',

    # ألوان القرآن
    'quran_text': '#1a1a1a',        # نص القرآن
    'aya_number': '#2c5aa0',        # رقم الآية
    'basmalah': '#27ae60',          # البسملة

    # ألوان التفاسير
    'tafsir_bg': '#fff8e7',         # خلفية التفسير
    'tafsir_border': '#f39c12',     # حدود التفسير

    # ألوان الترجمة
    'translation_bg': '#e8f8f5',    # خلفية الترجمة
    'translation_border': '#27ae60',

    # التدرجات
    'gradient_start': '#2c5aa0',
    'gradient_end': '#4a90e2',
}

# ═══════════════════════════════════════════════════════════════
# الخطوط المتاحة
# ═══════════════════════════════════════════════════════════════

AVAILABLE_FONTS = {
    'amiri': {
        'name': 'Amiri Quran',
        'family': 'Amiri Quran',
        'path': FONT_AMIRI,
        'size': 28
    },
    'uthman': {
        'name': 'الخط العثماني',
        'family': 'Uthmanic Hafs',
        'path': FONT_UTHMAN,
        'size': 26
    },
    'noorehuda': {
        'name': 'نور الهدى',
        'family': 'KFGQPC Uthman Taha Naskh',
        'path': FONT_NOOREHUDA,
        'size': 28
    },
    'noorehira': {
        'name': 'نور الحرا',
        'family': 'noorehira',
        'path': FONT_NOOREHIRA,
        'size': 26
    },
    'scheherazade': {
        'name': 'Scheherazade',
        'family': 'Scheherazade New',
        'path': FONT_SCHEHERAZADE,
        'size': 26
    },
    'traditional': {
        'name': 'Traditional Arabic',
        'family': 'Traditional Arabic',
        'path': None,  # خط نظام
        'size': 24
    },
    'arial': {
        'name': 'Arial Unicode',
        'family': 'Arial Unicode MS',
        'path': None,
        'size': 22
    },
}

DEFAULT_FONT = 'amiri'

# ═══════════════════════════════════════════════════════════════
# أنواع الرسم
# ═══════════════════════════════════════════════════════════════

RASM_TYPES = {
    'uthmani': {
        'name': 'العثماني',
        'icon': '📜',
        'column': 'text_uthmani',
        'description': 'الرسم العثماني (المصحف الكلاسيكي)'
    },
    'simple': {
        'name': 'الإملائي البسيط',
        'icon': '✍',
        'column': 'text_simple',
        'description': 'الرسم الإملائي المبسط'
    },
    'simple_clean': {
        'name': 'المبسط النظيف',
        'icon': '✨',
        'column': 'text_simple_clean',
        'description': 'نص مبسط بدون تشكيل'
    },
    'imlaei': {
        'name': 'الإملائي',
        'icon': '📝',
        'column': 'text_imlaei',
        'description': 'الرسم الإملائي الحديث'
    }
}

DEFAULT_RASM = 'uthmani'

# ═══════════════════════════════════════════════════════════════
# أنواع التفاسير
# ═══════════════════════════════════════════════════════════════

TAFSIR_TYPES = {
    'muyassar': {
        'name': 'التفسير الميسر',
        'icon': '📗',
        'color': '#27ae60',
        'table': 'tafsir_muyassar'
    },
    'jalalayn': {
        'name': 'تفسير الجلالين',
        'icon': '📘',
        'color': '#3498db',
        'table': 'tafsir_jalalayn'
    },
    'tabari': {
        'name': 'تفسير الطبري',
        'icon': '📕',
        'color': '#e74c3c',
        'table': 'tafsir_tabari'
    },
    'kathir': {
        'name': 'تفسير ابن كثير',
        'icon': '📙',
        'color': '#f39c12',
        'table': 'tafsir_kathir'
    },
    'saadi': {
        'name': 'تفسير السعدي',
        'icon': '📒',
        'color': '#9b59b6',
        'table': 'tafsir_saadi'
    }
}

DEFAULT_TAFSIR = 'muyassar'

# ═══════════════════════════════════════════════════════════════
# القراء الصوتيون
# ═══════════════════════════════════════════════════════════════

RECITERS = {
    'abdulbasit': {
        'name': 'عبد الباسط عبد الصمد',
        'name_en': 'Abdul Basit Abdul Samad',
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/Abdul_Basit_Murattal_192kbps',
        'bitrate': '192kbps',
        'icon': '🎙️',
        'popular': True
    },
    'minshawy': {
        'name': 'محمد صديق المنشاوي',
        'name_en': 'Mohamed Siddiq El-Minshawi',
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/MinShawi_Murattal_128kbps',
        'bitrate': '128kbps',
        'icon': '🎙️',
        'popular': True
    },
    'maher': {
        'name': 'ماهر المعيقلي',
        'name_en': 'Maher Al Muaiqly',
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/Maher_AlMuaiqly_64kbps',
        'bitrate': '64kbps',
        'icon': '🎙️',
        'popular': True
    },
    'sudais': {
        'name': 'عبد الرحمن السديس',
        'name_en': 'Abdur-Rahman as-Sudais',
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/Abdurrahmaan_As-Sudais_64kbps',
        'bitrate': '64kbps',
        'icon': '🎙️',
        'popular': True
    },
    'shuraim': {
        'name': 'سعود الشريم',
        'name_en': 'Saud ash-Shuraim',
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/Saood_ash-Shuraym_64kbps',
        'bitrate': '64kbps',
        'icon': '🎙️',
        'popular': True
    },
    'alafasy': {
        'name': 'مشاري راشد العفاسي',
        'name_en': 'Mishari Rashid al-Afasy',
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/Alafasy_128kbps',
        'bitrate': '128kbps',
        'icon': '🎙️',
        'popular': True
    },
    'ghamadi': {
        'name': 'سعد الغامدي',
        'name_en': "Saad al-Ghamidi",
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/Ghamadi_40kbps',
        'bitrate': '40kbps',
        'icon': '🎙️',
        'popular': True
    },
    'qatami': {
        'name': 'ناصر القطامي',
        'name_en': 'Nasser al-Qatami',
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/Nasser_Alqatami_128kbps',
        'bitrate': '128kbps',
        'icon': '🎙️',
        'popular': True
    },
    'husary': {
        'name': 'محمود خليل الحصري',
        'name_en': 'Mahmoud Khalil al-Hussary',
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/Husary_128kbps',
        'bitrate': '128kbps',
        'icon': '🎙️',
        'popular': False
    },
    'ajmi': {
        'name': 'أحمد العجمي',
        'name_en': 'Ahmed al-Ajmi',
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/Ahmed_ibn_Ali_al-Ajamy_128kbps',
        'bitrate': '128kbps',
        'icon': '🎙️',
        'popular': False
    },
    'juhany': {
        'name': 'عبد الله الجهني',
        'name_en': 'Abdullah al-Juhany',
        'style': 'مرتل',
        'url_base': 'https://everyayah.com/data/Abdullah_Awad_Al-Juhany_128kbps',
        'bitrate': '128kbps',
        'icon': '🎙️',
        'popular': False
    },
}

DEFAULT_RECITER = 'abdulbasit'

# مجلد تخزين الملفات الصوتية
AUDIO_DIR = DATA_DIR / "audio"
AUDIO_CACHE_DIR = AUDIO_DIR / "cache"

# إعدادات الصوت
AUDIO_SETTINGS = {
    'auto_play_next': True,  # تشغيل الآية التالية تلقائياً
    'repeat_aya': False,      # تكرار الآية
    'download_ahead': 3,      # تحميل مسبق لعدد آيات
    'cache_size_mb': 500,     # حجم الكاش بالميجابايت
}

# ═══════════════════════════════════════════════════════════════
# إعدادات البحث
# ═══════════════════════════════════════════════════════════════

SEARCH_TYPES = {
    'text': {
        'name': 'بحث نصي',
        'icon': '📝',
        'description': 'البحث في نص القرآن'
    },
    'root': {
        'name': 'بحث بالجذر',
        'icon': '🌳',
        'description': 'البحث بالجذر اللغوي'
    },
    'pattern': {
        'name': 'بحث بالنمط',
        'icon': '⚖️',
        'description': 'البحث بالنمط الصرفي'
    },
    'topic': {
        'name': 'بحث بالموضوع',
        'icon': '📑',
        'description': 'البحث في المواضيع'
    }
}

SEARCH_PLACES = {
    'quran': {
        'name': 'القرآن الكريم',
        'icon': '📖',
        'checked': True
    },
    'tafsir': {
        'name': 'التفاسير',
        'icon': '📚',
        'checked': False
    },
    'translation': {
        'name': 'الترجمات',
        'icon': '🌍',
        'checked': False
    }
}

SEARCH_SETTINGS = {
    'min_chars': 2,
    'max_results': 500,
    'highlight_color': '#ffeb3b',
    'case_sensitive': False
}

# ═══════════════════════════════════════════════════════════════
# التابات الرئيسية
# ═══════════════════════════════════════════════════════════════

MAIN_TABS = [
    {
        'id': 'quran',
        'name': 'القرآن الكريم',
        'icon': '📖'
    },
    {
        'id': 'tafsir',
        'name': 'التفاسير',
        'icon': '📚'
    },
    {
        'id': 'translations',
        'name': 'الترجمات',
        'icon': '🌍'
    },
    {
        'id': 'sciences',
        'name': 'علوم القرآن',
        'icon': '🔬'
    },
    {
        'id': 'search',
        'name': 'البحث',
        'icon': '🔍'
    }
]

# ═══════════════════════════════════════════════════════════════
# إعدادات العرض
# ═══════════════════════════════════════════════════════════════

DISPLAY_SETTINGS = {
    'show_basmalah': True,
    'show_aya_numbers': True,
    'show_sura_info': True,
    'show_juz_info': True,
    'show_page_info': True,
    'line_spacing': 2.0,
    'paragraph_spacing': 15,
    'aya_separator': '۝',
    'center_text': True,
    'justify_text': True
}

# ═══════════════════════════════════════════════════════════════
# اختصارات لوحة المفاتيح
# ═══════════════════════════════════════════════════════════════

SHORTCUTS = {
    'quit': 'Ctrl+Q',
    'save': 'Ctrl+S',
    'print': 'Ctrl+P',
    'copy': 'Ctrl+C',
    'select_all': 'Ctrl+A',
    'find': 'Ctrl+F',
    'find_next': 'F3',
    'goto': 'Ctrl+G',
    'bookmark': 'Ctrl+D',
    'fullscreen': 'F11',
    'zoom_in': 'Ctrl++',
    'zoom_out': 'Ctrl+-',
    'zoom_reset': 'Ctrl+0'
}

# ═══════════════════════════════════════════════════════════════
# الرسائل
# ═══════════════════════════════════════════════════════════════

MESSAGES = {
    'loading': '⏳ جارٍ التحميل...',
    'searching': '🔍 جارٍ البحث...',
    'no_results': '❌ لا توجد نتائج',
    'single_result': '✅ نتيجة واحدة',
    'results_count': '✅ {count} نتيجة',
    'error': '❌ حدث خطأ',
    'success': '✅ تمت العملية بنجاح',
    'db_error': '❌ خطأ في قاعدة البيانات',
    'min_chars': '⚠️ الرجاء إدخال {min} أحرف على الأقل'
}

# ═══════════════════════════════════════════════════════════════
# أسلوب التطبيق (Stylesheet)
# ═══════════════════════════════════════════════════════════════

APP_STYLE = f"""
QMainWindow {{
    background-color: {COLORS['bg_light']};
}}

QMenuBar {{
    background-color: {COLORS['primary']};
    color: {COLORS['white']};
    padding: 5px;
}}

QMenuBar::item {{
    background-color: transparent;
    padding: 8px 12px;
}}

QMenuBar::item:selected {{
    background-color: {COLORS['secondary']};
}}

QMenu {{
    background-color: {COLORS['white']};
    border: 1px solid {COLORS['primary']};
}}

QMenu::item {{
    padding: 8px 25px;
}}

QMenu::item:selected {{
    background-color: {COLORS['bg_selected']};
}}

QToolBar {{
    background-color: {COLORS['bg_light']};
    border-bottom: 2px solid {COLORS['primary']};
    padding: 5px;
    spacing: 5px;
}}

QPushButton {{
    background-color: {COLORS['primary']};
    color: {COLORS['white']};
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {COLORS['secondary']};
}}

QPushButton:pressed {{
    background-color: #1e4378;
}}

QComboBox {{
    background-color: {COLORS['white']};
    border: 2px solid {COLORS['primary']};
    border-radius: 5px;
    padding: 5px 10px;
    min-width: 150px;
}}

QComboBox:hover {{
    border-color: {COLORS['secondary']};
}}

QComboBox::drop-down {{
    border: none;
}}

QLineEdit {{
    background-color: {COLORS['white']};
    border: 2px solid {COLORS['primary']};
    border-radius: 5px;
    padding: 8px;
}}

QLineEdit:focus {{
    border-color: {COLORS['secondary']};
}}

QTreeWidget {{
    background-color: {COLORS['white']};
    border: 1px solid {COLORS['primary']};
    border-radius: 5px;
    padding: 5px;
}}

QTreeWidget::item {{
    padding: 8px;
    border-radius: 3px;
}}

QTreeWidget::item:selected {{
    background-color: {COLORS['bg_selected']};
    color: {COLORS['text_primary']};
}}

QTreeWidget::item:hover {{
    background-color: {COLORS['bg_hover']};
}}

QTextBrowser {{
    background-color: {COLORS['white']};
    border: 2px solid {COLORS['primary']};
    border-radius: 8px;
    padding: 20px;
}}

QListWidget {{
    background-color: {COLORS['white']};
    border: 2px solid {COLORS['primary']};
    border-radius: 5px;
}}

QListWidget::item {{
    padding: 10px;
    border-bottom: 1px solid {COLORS['bg_light']};
}}

QListWidget::item:selected {{
    background-color: {COLORS['bg_selected']};
}}

QListWidget::item:hover {{
    background-color: {COLORS['bg_hover']};
}}

QTabWidget::pane {{
    border: 2px solid {COLORS['primary']};
    border-radius: 5px;
    background-color: {COLORS['white']};
}}

QTabBar::tab {{
    background-color: {COLORS['bg_light']};
    border: 1px solid {COLORS['primary']};
    padding: 10px 20px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['primary']};
    color: {COLORS['white']};
}}

QTabBar::tab:hover {{
    background-color: {COLORS['secondary']};
    color: {COLORS['white']};
}}

QStatusBar {{
    background-color: {COLORS['bg_light']};
    border-top: 2px solid {COLORS['primary']};
    padding: 5px;
}}

QGroupBox {{
    border: 2px solid {COLORS['primary']};
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    padding: 0 5px;
    color: {COLORS['primary']};
}}

QCheckBox {{
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
}}

QRadioButton {{
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
}}

QScrollBar:vertical {{
    background-color: {COLORS['bg_light']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['primary']};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['secondary']};
}}

QScrollBar:horizontal {{
    background-color: {COLORS['bg_light']};
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['primary']};
    border-radius: 6px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS['secondary']};
}}
"""

# ═══════════════════════════════════════════════════════════════
# نص "حول البرنامج"
# ═══════════════════════════════════════════════════════════════

def get_about_text() -> str:
    """نص صفحة حول البرنامج"""
    return f"""
    <html dir='rtl'>
    <head>
    <style>
    body {{
        font-family: 'Traditional Arabic', Arial;
        padding: 20px;
        text-align: center;
    }}
    h1 {{
        color: {COLORS['primary']};
        font-size: 28px;
        margin-bottom: 10px;
    }}
    .version {{
        color: {COLORS['secondary']};
        font-size: 18px;
        margin-bottom: 20px;
    }}
    .section {{
        background: {COLORS['bg_light']};
        padding: 15px;
        margin: 15px 0;
        border-radius: 10px;
        border-right: 4px solid {COLORS['primary']};
    }}
    .feature {{
        margin: 8px 0;
        padding: 8px;
        background: white;
        border-radius: 5px;
    }}
    .contact {{
        color: {COLORS['text_secondary']};
        margin-top: 20px;
    }}
    a {{
        color: {COLORS['primary']};
        text-decoration: none;
    }}
    </style>
    </head>
    <body>

    <h1>📖 {APP_NAME}</h1>
    <div class='version'>الإصدار {APP_VERSION}</div>

    <div class='section'>
        <h2>✨ الميزات الرئيسية</h2>
        <div class='feature'>📜 عرض القرآن بأنواع الرسم المختلفة (عثماني، إملائي، مبسط)</div>
        <div class='feature'>🔤 15 خط قرآني احترافي</div>
        <div class='feature'>📚 تفاسير متعددة (الميسر، الجلالين، الطبري، ابن كثير، السعدي)</div>
        <div class='feature'>🌍 ترجمات للعديد من اللغات</div>
        <div class='feature'>🔍 بحث متقدم (نصي، بالجذر، بالنمط، بالموضوع)</div>
        <div class='feature'>📘 التنقل السريع (سورة:آية، جزء، صفحة)</div>
        <div class='feature'>🔖 العلامات المرجعية</div>
        <div class='feature'>🔬 علوم القرآن (السجدات، الأحكام، المواضيع)</div>
        <div class='feature'>📊 168 MB من البيانات القرآنية</div>
    </div>

    <div class='section'>
        <h2>🏢 معلومات التطوير</h2>
        <p><b>الشركة:</b> {COMPANY}</p>
        <p><b>المطور:</b> {DEVELOPER}</p>
        <p><b>البريد الإلكتروني:</b> <a href='mailto:{EMAIL}'>{EMAIL}</a></p>
        <p><b>الموقع:</b> <a href='https://{WEBSITE}'>{WEBSITE}</a></p>
        <p><b>الهاتف:</b> {PHONE}</p>
    </div>

    <div class='contact'>
        <p>جميع الحقوق محفوظة © 2025</p>
        <p>تم التطوير بكل ❤️ لخدمة كتاب الله</p>
    </div>

    </body>
    </html>
    """

# ═══════════════════════════════════════════════════════════════
# التحقق من المسارات
# ═══════════════════════════════════════════════════════════════

def ensure_directories():
    """التأكد من وجود المجلدات المطلوبة"""
    for directory in [DATA_DIR, FONTS_DIR, DOCS_DIR, DB_BACKUP_DIR, AUDIO_DIR, AUDIO_CACHE_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

# تنفيذ عند الاستيراد
ensure_directories()

# ═══════════════════════════════════════════════════════════════
# نهاية الملف
# ═══════════════════════════════════════════════════════════════

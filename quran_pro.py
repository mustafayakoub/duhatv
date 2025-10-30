#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
📖 القرآن الكريم Pro v2.1.0
═══════════════════════════════════════════════════════════════
🎨 واجهة أنيقة مستوحاة من Tanzil.net
🚀 أداء محسّن | 📊 168 MB من البيانات القرآنية
═══════════════════════════════════════════════════════════════
🏢 AiGrow | 👨‍💻 Mustafa Yakoub
📧 duhatv@gmail.com | 🌐 duhatv.net | 📱 +905342390000
═══════════════════════════════════════════════════════════════
"""

import sys
from pathlib import Path

# إضافة مجلد src للمسار
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter

from config import *
from db_manager import QuranDatabase
from audio_player import QuranAudioPlayer
from audio_widget import AudioControlWidget
from dialogs import ReciterDialog


# ═══════════════════════════════════════════════════════════════
# الواجهة الرئيسية
# ═══════════════════════════════════════════════════════════════

class QuranProApp(QMainWindow):
    """التطبيق الرئيسي للقرآن الكريم Pro"""

    def __init__(self):
        super().__init__()

        # قاعدة البيانات
        try:
            self.db = QuranDatabase()
        except Exception as e:
            QMessageBox.critical(
                self, "خطأ",
                f"فشل الاتصال بقاعدة البيانات:\n{e}\n\n"
                f"الرجاء وضع ملف quran_ultimate_final.db في مجلد data"
            )
            sys.exit(1)

        # المتغيرات
        self.current_sura = 1
        self.current_aya = 1
        self.current_page = None
        self.current_juz = None
        self.current_rasm = DEFAULT_RASM
        self.current_font = DEFAULT_FONT
        self.current_tafsir = DEFAULT_TAFSIR
        self.current_language = 'english'

        # الخطوط المحملة
        self.loaded_fonts = {}

        # تحميل الخطوط
        self.load_fonts()

        # مشغل الصوت
        self.audio_player = QuranAudioPlayer()

        # بناء الواجهة
        self.init_ui()

        # ربط إشارات التحكم الصوتي
        self.connect_audio_signals()

        # تحميل الفاتحة
        self.load_sura_aya(1, 1)

    def load_fonts(self):
        """تحميل كل الخطوط المتاحة"""
        print("\n🔤 تحميل الخطوط...")
        for font_id, font_info in AVAILABLE_FONTS.items():
            if font_info['path'] and font_info['path'].exists():
                font_path = str(font_info['path'])
                font_db_id = QFontDatabase.addApplicationFont(font_path)
                if font_db_id != -1:
                    families = QFontDatabase.applicationFontFamilies(font_db_id)
                    print(f"✅ {font_info['name']} → {families}")
                    self.loaded_fonts[font_id] = families[0] if families else font_info['family']
                else:
                    print(f"⚠️  فشل تحميل: {font_info['name']}")
            else:
                # خطوط النظام
                self.loaded_fonts[font_id] = font_info['family']
                print(f"📝 استخدام خط النظام: {font_info['name']}")

    def init_ui(self):
        """بناء الواجهة"""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, WINDOW_SIZE['width'], WINDOW_SIZE['height'])
        self.setMinimumSize(WINDOW_SIZE['min_width'], WINDOW_SIZE['min_height'])
        self.setStyleSheet(APP_STYLE)

        # الأيقونة
        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))

        # القوائم
        self.create_menu_bar()

        # شريط الأدوات
        self.create_toolbar()

        # المحتوى الرئيسي
        self.create_main_widget()

        # شريط الحالة
        self.create_status_bar()

        # المركز
        if not WINDOW_SIZE['fullscreen']:
            self.center_window()
        else:
            self.showMaximized()

    def center_window(self):
        """توسيط النافذة"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    # ═══════════════════════════════════════════════════════════════
    # التحكم الصوتي
    # ═══════════════════════════════════════════════════════════════

    def connect_audio_signals(self):
        """ربط إشارات التحكم الصوتي"""
        # إشارات من عنصر التحكم إلى المشغل
        self.audio_widget.play_requested.connect(self.on_audio_play_requested)
        self.audio_widget.pause_requested.connect(self.audio_player.pause)
        self.audio_widget.stop_requested.connect(self.audio_player.stop)
        self.audio_widget.next_requested.connect(self.audio_player.play_next)
        self.audio_widget.previous_requested.connect(self.audio_player.play_previous)
        self.audio_widget.volume_changed.connect(self.audio_player.set_volume)
        self.audio_widget.reciter_change_requested.connect(self.on_reciter_change_requested)

        # إشارات من المشغل إلى عنصر التحكم
        self.audio_player.state_changed.connect(self.on_audio_state_changed)
        self.audio_player.position_changed.connect(self.audio_widget.set_position)
        self.audio_player.duration_changed.connect(self.audio_widget.set_duration)
        self.audio_player.aya_changed.connect(self.on_audio_aya_changed)
        self.audio_player.error_occurred.connect(self.on_audio_error)

        # تعيين القارئ الافتراضي
        reciter_name = RECITERS[DEFAULT_RECITER]['name']
        self.audio_widget.set_reciter_name(reciter_name)

    def on_audio_play_requested(self, sura: int, aya: int):
        """عند طلب التشغيل"""
        # إذا كانت القيم 0، نشغل الآية الحالية
        if sura == 0 or aya == 0:
            self.audio_player.play_aya(self.current_sura, self.current_aya)
        else:
            self.audio_player.play_aya(sura, aya)

    def on_reciter_change_requested(self):
        """عند طلب تغيير القارئ"""
        dialog = ReciterDialog(self, self.audio_player.current_reciter)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            reciter_id = dialog.get_selected_reciter()
            self.audio_player.set_reciter(reciter_id)
            reciter_name = RECITERS[reciter_id]['name']
            self.audio_widget.set_reciter_name(reciter_name)

    def on_audio_state_changed(self, state: str):
        """عند تغيير حالة التشغيل"""
        is_playing = (state == "playing")
        self.audio_widget.set_playing_state(is_playing)

        if state == "loading":
            self.audio_widget.set_status("جاري التحميل...", COLORS['warning'])
        elif state == "error":
            self.audio_widget.set_status("خطأ في التشغيل", COLORS['error'])

    def on_audio_aya_changed(self, sura: int, aya: int):
        """عند تغيير الآية المُشغلة"""
        # يمكن تحديث العرض أو التمييز
        if sura != self.current_sura:
            self.load_sura_aya(sura, aya)

    def on_audio_error(self, error_msg: str):
        """عند حدوث خطأ صوتي"""
        self.audio_widget.set_status(error_msg, COLORS['error'])

    # ═══════════════════════════════════════════════════════════════
    # القوائم
    # ═══════════════════════════════════════════════════════════════

    def create_menu_bar(self):
        """القائمة العلوية"""
        menubar = self.menuBar()

        # الملف
        file_menu = menubar.addMenu("📁 الملف")

        save_action = QAction("💾 حفظ باسم...", self)
        save_action.setShortcut(SHORTCUTS['save'])
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        print_action = QAction("🖨️ طباعة", self)
        print_action.setShortcut(SHORTCUTS['print'])
        print_action.triggered.connect(self.print_content)
        file_menu.addAction(print_action)

        file_menu.addSeparator()

        exit_action = QAction("🚪 خروج", self)
        exit_action.setShortcut(SHORTCUTS['quit'])
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # التحرير
        edit_menu = menubar.addMenu("✏️ التحرير")

        copy_action = QAction("📋 نسخ", self)
        copy_action.setShortcut(SHORTCUTS['copy'])
        copy_action.triggered.connect(self.copy_text)
        edit_menu.addAction(copy_action)

        select_all_action = QAction("📑 تحديد الكل", self)
        select_all_action.setShortcut(SHORTCUTS['select_all'])
        select_all_action.triggered.connect(self.select_all)
        edit_menu.addAction(select_all_action)

        edit_menu.addSeparator()

        bookmark_action = QAction("🔖 إضافة علامة مرجعية", self)
        bookmark_action.setShortcut(SHORTCUTS['bookmark'])
        bookmark_action.triggered.connect(self.add_bookmark)
        edit_menu.addAction(bookmark_action)

        # العرض
        view_menu = menubar.addMenu("👁️ العرض")

        # أنواع الرسم
        rasm_submenu = view_menu.addMenu("📜 نوع الرسم")
        for rasm_id, rasm_info in RASM_TYPES.items():
            action = QAction(f"{rasm_info['icon']} {rasm_info['name']}", self)
            action.triggered.connect(lambda checked, r=rasm_id: self.change_rasm(r))
            rasm_submenu.addAction(action)

        # اختيار الخط
        font_submenu = view_menu.addMenu("🔤 اختيار الخط")
        for font_id, font_info in AVAILABLE_FONTS.items():
            action = QAction(f"📝 {font_info['name']}", self)
            action.triggered.connect(lambda checked, f=font_id: self.change_font(f))
            font_submenu.addAction(action)

        view_menu.addSeparator()

        fullscreen_action = QAction("⛶ ملء الشاشة", self)
        fullscreen_action.setShortcut(SHORTCUTS['fullscreen'])
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        # الانتقال
        nav_menu = menubar.addMenu("🧭 الانتقال")

        goto_sura_action = QAction("📖 انتقال إلى سورة:آية", self)
        goto_sura_action.setShortcut("Ctrl+G")
        goto_sura_action.triggered.connect(self.show_goto_dialog)
        nav_menu.addAction(goto_sura_action)

        goto_juz_action = QAction("📘 انتقال إلى جزء", self)
        goto_juz_action.setShortcut("Ctrl+J")
        goto_juz_action.triggered.connect(self.show_goto_juz_dialog)
        nav_menu.addAction(goto_juz_action)

        goto_page_action = QAction("📃 انتقال إلى صفحة", self)
        goto_page_action.setShortcut("Ctrl+P")
        goto_page_action.triggered.connect(self.show_goto_page_dialog)
        nav_menu.addAction(goto_page_action)

        # المساعدة
        help_menu = menubar.addMenu("❓ المساعدة")

        guide_ar = QAction("📖 دليل الاستخدام (عربي)", self)
        guide_ar.triggered.connect(lambda: self.open_user_guide('ar'))
        help_menu.addAction(guide_ar)

        guide_en = QAction("📖 User Guide (English)", self)
        guide_en.triggered.connect(lambda: self.open_user_guide('en'))
        help_menu.addAction(guide_en)

        help_menu.addSeparator()

        about_action = QAction("ℹ️ حول البرنامج", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """شريط الأدوات"""
        toolbar = self.addToolBar("الأدوات")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))

        # الانتقال السريع
        toolbar.addWidget(QLabel("  🧭 الانتقال: "))

        btn_goto = QPushButton("📖 سورة:آية")
        btn_goto.clicked.connect(self.show_goto_dialog)
        toolbar.addWidget(btn_goto)

        btn_goto_juz = QPushButton("📘 جزء")
        btn_goto_juz.clicked.connect(self.show_goto_juz_dialog)
        toolbar.addWidget(btn_goto_juz)

        btn_goto_page = QPushButton("📃 صفحة")
        btn_goto_page.clicked.connect(self.show_goto_page_dialog)
        toolbar.addWidget(btn_goto_page)

        toolbar.addSeparator()

        # نوع الرسم
        toolbar.addWidget(QLabel("  📜 الرسم: "))
        self.rasm_combo = QComboBox()
        for rasm_id, rasm_info in RASM_TYPES.items():
            self.rasm_combo.addItem(f"{rasm_info['icon']} {rasm_info['name']}", rasm_id)
        self.rasm_combo.currentIndexChanged.connect(self.on_rasm_changed)
        toolbar.addWidget(self.rasm_combo)

        toolbar.addSeparator()

        # اختيار الخط
        toolbar.addWidget(QLabel("  🔤 الخط: "))
        self.font_combo = QComboBox()
        for font_id, font_info in AVAILABLE_FONTS.items():
            self.font_combo.addItem(font_info['name'], font_id)
        self.font_combo.currentIndexChanged.connect(self.on_font_changed)
        toolbar.addWidget(self.font_combo)

        toolbar.addSeparator()

        # البحث
        btn_search = QPushButton("🔍 بحث")
        btn_search.clicked.connect(self.show_search_dialog)
        toolbar.addWidget(btn_search)

        # العلامات
        btn_bookmarks = QPushButton("🔖 العلامات")
        btn_bookmarks.clicked.connect(self.show_bookmarks)
        toolbar.addWidget(btn_bookmarks)

    def create_status_bar(self):
        """شريط الحالة المحسّن"""
        self.status_bar = self.statusBar()

        # القسم الأيسر - معلومات السورة الحالية
        self.status_sura_label = QLabel("السورة: الفاتحة | الآية: 1")
        self.status_sura_label.setStyleSheet("padding: 0 10px; font-weight: bold;")
        self.status_bar.addWidget(self.status_sura_label)

        # فاصل
        separator1 = QLabel("|")
        separator1.setStyleSheet("color: #bdc3c7;")
        self.status_bar.addWidget(separator1)

        # الجزء
        self.status_juz_label = QLabel("الجزء: 1")
        self.status_juz_label.setStyleSheet("padding: 0 10px; cursor: pointer;")
        self.status_juz_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.status_juz_label.mousePressEvent = lambda e: self.show_goto_juz_dialog()
        self.status_bar.addWidget(self.status_juz_label)

        # فاصل
        separator2 = QLabel("|")
        separator2.setStyleSheet("color: #bdc3c7;")
        self.status_bar.addWidget(separator2)

        # الصفحة
        self.status_page_label = QLabel("الصفحة: 1")
        self.status_page_label.setStyleSheet("padding: 0 10px; cursor: pointer;")
        self.status_page_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.status_page_label.mousePressEvent = lambda e: self.show_goto_page_dialog()
        self.status_bar.addWidget(self.status_page_label)

        # فراغ مرن
        self.status_bar.addPermanentWidget(QWidget(), 1)

        # القسم الأيمن - إحصائيات
        stats = self.db.get_statistics()
        stats_text = f"📖 {stats.get('suras_count', 114)} سورة  |  📄 {stats.get('ayas_count', 6236)} آية  |  📘 {stats.get('juz_count', 30)} جزء"
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet("padding: 0 10px; color: #7f8c8d;")
        self.status_bar.addPermanentWidget(stats_label)

    def update_status_bar(self):
        """تحديث شريط الحالة"""
        sura_info = self.db.get_sura_info(self.current_sura)

        # معلومات السورة والآية
        self.status_sura_label.setText(f"السورة: {sura_info['name']} | الآية: {self.current_aya}")

        # الجزء والصفحة
        aya_info = self.db.get_aya(self.current_sura, self.current_aya)
        if aya_info:
            self.current_juz = aya_info.get('juz')
            self.current_page = aya_info.get('page')

            if self.current_juz:
                self.status_juz_label.setText(f"الجزء: {self.current_juz}")

            if self.current_page:
                self.status_page_label.setText(f"الصفحة: {self.current_page}")

    # ═══════════════════════════════════════════════════════════════
    # المحتوى الرئيسي
    # ═══════════════════════════════════════════════════════════════

    def create_main_widget(self):
        """المحتوى الرئيسي"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # الشريط الجانبي
        sidebar = self.create_sidebar()
        splitter.addWidget(sidebar)

        # منطقة العرض
        content = self.create_content_area()
        splitter.addWidget(content)

        # النسب
        splitter.setSizes([250, 650])

        main_layout.addWidget(splitter)

    def create_sidebar(self):
        """الشريط الجانبي"""
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # التابات
        self.tabs_widget = QTabWidget()

        for tab_info in MAIN_TABS:
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)

            if tab_info['id'] == 'search':
                search_widget = self.create_search_widget()
                tab_layout.addWidget(search_widget)
            else:
                tree = QTreeWidget()
                tree.setHeaderHidden(True)
                tree.itemClicked.connect(
                    lambda item, col, tid=tab_info['id']: self.on_tree_item_clicked(item, tid)
                )

                # ملء الشجرة
                if tab_info['id'] == 'quran':
                    self.populate_quran_tree(tree)
                elif tab_info['id'] == 'tafsir':
                    self.populate_tafsir_tree(tree)
                elif tab_info['id'] == 'translations':
                    self.populate_translations_tree(tree)
                elif tab_info['id'] == 'sciences':
                    self.populate_sciences_tree(tree)

                tab_layout.addWidget(tree)
                setattr(self, f'{tab_info["id"]}_tree', tree)

            self.tabs_widget.addTab(tab, f'{tab_info["icon"]} {tab_info["name"]}')

        sidebar_layout.addWidget(self.tabs_widget)

        return sidebar

    def populate_quran_tree(self, tree):
        """شجرة القرآن"""
        print("🌳 بناء شجرة القرآن...")

        # الأجزاء
        for juz_num in range(1, 31):
            juz_item = QTreeWidgetItem([f"📘 الجزء {juz_num}"])
            juz_item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'juz', 'juz': juz_num})

            # السور في الجزء
            suras = self.db.get_suras_in_juz(juz_num)
            for sura_info in suras:
                sura_num = sura_info['sura']
                full_info = self.db.get_sura_info(sura_num)
                sura_text = f"📄 {sura_num}. {full_info['name']} ({full_info['ayas_count']} آية)"
                sura_item = QTreeWidgetItem([sura_text])
                sura_item.setData(0, Qt.ItemDataRole.UserRole, {
                    'type': 'sura',
                    'sura': sura_num
                })
                juz_item.addChild(sura_item)

            tree.addTopLevelItem(juz_item)

        print("✅ شجرة القرآن جاهزة!")

    def populate_tafsir_tree(self, tree):
        """شجرة التفاسير"""
        # أنواع التفاسير
        for tafsir_id, tafsir_info in TAFSIR_TYPES.items():
            parent = QTreeWidgetItem([f"{tafsir_info['icon']} {tafsir_info['name']}"])
            parent.setData(0, Qt.ItemDataRole.UserRole, {
                'type': 'tafsir_type',
                'tafsir': tafsir_id
            })

            # السور
            for sura_num in range(1, 115):
                sura_info = self.db.get_sura_info(sura_num)
                sura_text = f"{sura_num}. {sura_info['name']}"
                sura_item = QTreeWidgetItem([sura_text])
                sura_item.setData(0, Qt.ItemDataRole.UserRole, {
                    'type': 'tafsir_sura',
                    'sura': sura_num,
                    'tafsir': tafsir_id
                })
                parent.addChild(sura_item)

            tree.addTopLevelItem(parent)

    def populate_translations_tree(self, tree):
        """شجرة الترجمات"""
        languages = self.db.get_available_languages()

        if not languages:
            item = QTreeWidgetItem(["لا توجد ترجمات متاحة"])
            tree.addTopLevelItem(item)
            return

        for lang_code, lang_name in languages:
            parent = QTreeWidgetItem([f"🌍 {lang_name}"])
            parent.setData(0, Qt.ItemDataRole.UserRole, {
                'type': 'language',
                'language': lang_code
            })

            # السور
            for sura_num in range(1, 115):
                sura_info = self.db.get_sura_info(sura_num)
                sura_text = f"{sura_num}. {sura_info['name']}"
                sura_item = QTreeWidgetItem([sura_text])
                sura_item.setData(0, Qt.ItemDataRole.UserRole, {
                    'type': 'translation_sura',
                    'sura': sura_num,
                    'language': lang_code
                })
                parent.addChild(sura_item)

            tree.addTopLevelItem(parent)

    def populate_sciences_tree(self, tree):
        """شجرة علوم القرآن"""
        sciences = [
            ("📜", "آيات السجدة"),
            ("🔬", "علوم السور"),
            ("📑", "المواضيع"),
            ("⏸️", "علامات الوقف"),
        ]

        for icon, name in sciences:
            item = QTreeWidgetItem([f"{icon} {name}"])
            item.setData(0, Qt.ItemDataRole.UserRole, {
                'type': 'science',
                'name': name
            })
            tree.addTopLevelItem(item)

    def create_content_area(self):
        """منطقة العرض"""
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 10, 10, 10)

        # معلومات السورة
        self.info_label = QLabel()
        self.info_label.setStyleSheet(f"""
            QLabel {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 {COLORS['gradient_start']},
                                            stop:1 {COLORS['gradient_end']});
                color: {COLORS['white']};
                padding: 12px;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }}
        """)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.info_label)

        # متصفح النصوص
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(False)
        self.text_browser.setReadOnly(True)
        self.text_browser.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.text_browser.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.text_browser.customContextMenuRequested.connect(self.show_context_menu)

        content_layout.addWidget(self.text_browser)

        # عناصر التحكم الصوتي
        self.audio_widget = AudioControlWidget()
        content_layout.addWidget(self.audio_widget)

        return content

    def create_search_widget(self):
        """واجهة البحث"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # حقل البحث
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث في القرآن الكريم...")
        self.search_input.returnPressed.connect(self.perform_quick_search)
        search_layout.addWidget(self.search_input)

        btn_search = QPushButton("🔍")
        btn_search.clicked.connect(self.perform_quick_search)
        search_layout.addWidget(btn_search)

        layout.addLayout(search_layout)

        # نوع البحث
        type_group = QGroupBox("نوع البحث")
        type_layout = QVBoxLayout()

        self.search_type_group = QButtonGroup()
        for search_id, search_info in SEARCH_TYPES.items():
            radio = QRadioButton(f"{search_info['icon']} {search_info['name']}")
            radio.setProperty('search_id', search_id)
            self.search_type_group.addButton(radio)
            type_layout.addWidget(radio)
            if search_id == 'text':
                radio.setChecked(True)

        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        # أماكن البحث
        places_group = QGroupBox("أماكن البحث")
        places_layout = QVBoxLayout()

        self.search_places = {}
        for place_id, place_info in SEARCH_PLACES.items():
            checkbox = QCheckBox(f"{place_info['icon']} {place_info['name']}")
            checkbox.setChecked(place_info['checked'])
            self.search_places[place_id] = checkbox
            places_layout.addWidget(checkbox)

        places_group.setLayout(places_layout)
        layout.addWidget(places_group)

        # النتائج
        self.quick_results_list = QListWidget()
        self.quick_results_list.itemDoubleClicked.connect(self.on_quick_result_clicked)
        layout.addWidget(self.quick_results_list)

        return widget

    # ═══════════════════════════════════════════════════════════════
    # معالجة الأحداث
    # ═══════════════════════════════════════════════════════════════

    def on_tree_item_clicked(self, item, tab_id):
        """عند النقر على عنصر في الشجرة"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return

        item_type = data.get('type')

        if item_type == 'sura':
            self.load_sura_aya(data['sura'], 1)
        elif item_type == 'juz':
            # الانتقال لأول سورة في الجزء
            suras = self.db.get_suras_in_juz(data['juz'])
            if suras:
                self.load_sura_aya(suras[0]['sura'], 1)
        elif item_type == 'tafsir_sura':
            self.load_tafsir(data['sura'], data.get('tafsir', DEFAULT_TAFSIR))
        elif item_type == 'translation_sura':
            self.load_translation(data['sura'], data.get('language', 'english'))
        elif item_type == 'science':
            self.load_science(data['name'])

    def on_rasm_changed(self, index):
        """عند تغيير نوع الرسم"""
        rasm_id = self.rasm_combo.itemData(index)
        self.current_rasm = rasm_id
        self.load_sura_aya(self.current_sura, self.current_aya)

    def on_font_changed(self, index):
        """عند تغيير الخط"""
        font_id = self.font_combo.itemData(index)
        self.current_font = font_id
        self.load_sura_aya(self.current_sura, self.current_aya)

    # ═══════════════════════════════════════════════════════════════
    # تحميل المحتوى
    # ═══════════════════════════════════════════════════════════════

    def load_sura_aya(self, sura_num: int, aya_num: int = 1):
        """تحميل سورة من آية معينة"""
        self.current_sura = sura_num
        self.current_aya = aya_num

        # معلومات السورة
        info = self.db.get_sura_info(sura_num)
        self.info_label.setText(
            f"{info['name']} | {info['type_full']} | {info['ayas_count']} آية"
        )

        # الآيات
        ayas = self.db.get_sura_ayas(sura_num, self.current_rasm)

        # التنسيق
        html = self.format_quran_html(info, ayas, highlight_aya=aya_num)
        self.text_browser.setHtml(html)

        # التمرير للآية
        if aya_num > 1:
            self.text_browser.find(f"﴿{aya_num}﴾")

        # تحديث شريط الحالة
        self.update_status_bar()

    def format_quran_html(self, sura_info: dict, ayas: list, highlight_aya: int = None) -> str:
        """تنسيق القرآن بـ HTML"""
        # الحصول على معلومات الخط الحالي
        font_info = AVAILABLE_FONTS.get(self.current_font, AVAILABLE_FONTS[DEFAULT_FONT])
        font_family = self.loaded_fonts.get(self.current_font, font_info['family'])
        font_size = font_info['size']

        html = f"""
        <html dir='rtl'>
        <head>
        <style>
        body {{
            font-family: '{font_family}', 'Traditional Arabic', Arial;
            font-size: {font_size}px;
            line-height: {DISPLAY_SETTINGS['line_spacing']};
            text-align: center;
            padding: 20px;
        }}
        .sura-header {{
            background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 18px;
            font-weight: bold;
        }}
        .basmalah {{
            font-size: {font_size + 4}px;
            color: {COLORS['primary']};
            margin: 20px 0;
            font-weight: bold;
        }}
        .aya {{
            display: inline;
            margin: 0 5px;
        }}
        .aya-number {{
            color: {COLORS['aya_number']};
            font-weight: bold;
            font-size: {font_size - 4}px;
            margin: 0 8px;
        }}
        .aya-highlight {{
            background-color: {COLORS['bg_selected']};
            padding: 5px;
            border-radius: 5px;
        }}
        </style>
        </head>
        <body>
        """

        # رأس السورة
        html += f"""
        <div class='sura-header'>
        {sura_info['name']}<br>
        <span style='font-size: 14px;'>{sura_info['type_full']} - {sura_info['ayas_count']} آية</span>
        </div>
        """

        # البسملة (إلا التوبة)
        if sura_info['sura'] != 9 and DISPLAY_SETTINGS['show_basmalah']:
            html += "<div class='basmalah'>بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>"

        # الآيات
        html += "<div style='text-align: justify; text-justify: inter-word;'>"
        for aya in ayas:
            aya_text = aya['text'].strip()
            aya_num = aya['aya']

            # تمييز الآية المطلوبة
            aya_class = 'aya-highlight' if aya_num == highlight_aya else ''

            if DISPLAY_SETTINGS['show_aya_numbers']:
                html += f"<span class='aya {aya_class}'>{aya_text}</span> <span class='aya-number'>﴿{aya_num}﴾</span> "
            else:
                html += f"<span class='aya {aya_class}'>{aya_text}</span> {DISPLAY_SETTINGS['aya_separator']} "
        html += "</div>"

        html += "</body></html>"
        return html

    def load_tafsir(self, sura_num: int, tafsir_type: str):
        """تحميل التفسير"""
        self.current_sura = sura_num
        self.current_tafsir = tafsir_type

        info = self.db.get_sura_info(sura_num)
        tafsir_info = TAFSIR_TYPES[tafsir_type]

        self.info_label.setText(
            f"{tafsir_info['icon']} {tafsir_info['name']} - {info['name']}"
        )

        # جلب التفسير
        if tafsir_type == 'muyassar':
            tafsirs = self.db.get_tafsir_muyassar(sura_num)
        elif tafsir_type == 'jalalayn':
            tafsirs = self.db.get_tafsir_jalalayn(sura_num)
        elif tafsir_type == 'tabari':
            tafsirs = self.db.get_historical_all_sura(sura_num)
        else:
            tafsirs = []

        html = self.format_tafsir_html(info, tafsirs, tafsir_type)
        self.text_browser.setHtml(html)

    def format_tafsir_html(self, sura_info: dict, tafsirs: list, tafsir_type: str) -> str:
        """تنسيق التفسير"""
        tafsir_info = TAFSIR_TYPES[tafsir_type]

        html = f"""
        <html dir='rtl'>
        <head>
        <style>
        body {{
            font-family: 'Traditional Arabic', Arial;
            font-size: 16px;
            line-height: 1.8;
            padding: 20px;
        }}
        .header {{
            background: {tafsir_info['color']};
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .tafsir-item {{
            background: {COLORS['tafsir_bg']};
            border-right: 4px solid {tafsir_info['color']};
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
        }}
        .aya-num {{
            color: {tafsir_info['color']};
            font-weight: bold;
            font-size: 18px;
        }}
        </style>
        </head>
        <body>
        """

        html += f"""
        <div class='header'>
        {tafsir_info['icon']} {tafsir_info['name']}<br>
        <span style='font-size: 14px;'>{sura_info['name']}</span>
        </div>
        """

        for item in tafsirs:
            aya_num = item.get('aya', 0)
            text = item.get('text', '').strip()

            if aya_num == 0:  # مقدمة
                html += f"""
                <div class='tafsir-item'>
                <div class='aya-num'>مقدمة السورة</div>
                <p>{text}</p>
                </div>
                """
            else:
                html += f"""
                <div class='tafsir-item'>
                <div class='aya-num'>﴿{aya_num}﴾</div>
                <p>{text}</p>
                </div>
                """

        html += "</body></html>"
        return html

    def load_translation(self, sura_num: int, language: str):
        """تحميل الترجمة"""
        self.current_sura = sura_num
        self.current_language = language

        info = self.db.get_sura_info(sura_num)
        translations = self.db.get_sura_translations(sura_num, language)

        self.info_label.setText(f"🌍 {language} - {info['name']}")

        html = self.format_translation_html(info, translations, language)
        self.text_browser.setHtml(html)

    def format_translation_html(self, sura_info: dict, translations: list, language: str) -> str:
        """تنسيق الترجمة"""
        html = f"""
        <html dir='ltr'>
        <head>
        <style>
        body {{
            font-family: Arial, 'Segoe UI';
            font-size: 16px;
            line-height: 1.8;
            padding: 20px;
        }}
        .header {{
            background: {COLORS['success']};
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .translation-item {{
            background: {COLORS['translation_bg']};
            border-left: 4px solid {COLORS['success']};
            padding: 12px;
            margin: 10px 0;
            border-radius: 8px;
        }}
        .aya-num {{
            color: {COLORS['success']};
            font-weight: bold;
        }}
        </style>
        </head>
        <body>
        """

        html += f"""
        <div class='header'>
        Translation: {language}<br>
        <span style='font-size: 14px;'>{sura_info['name']}</span>
        </div>
        """

        for item in translations:
            html += f"""
            <div class='translation-item'>
            <span class='aya-num'>[{item['aya']}]</span> {item['text']}
            </div>
            """

        html += "</body></html>"
        return html

    def load_science(self, science_name: str):
        """تحميل علوم القرآن"""
        self.info_label.setText(f"🔬 {science_name}")

        html = "<html dir='rtl'><body style='padding: 20px; font-family: Arial;'>"
        html += f"<h2>{science_name}</h2>"

        if science_name == "آيات السجدة":
            sajdas = self.db.get_sajda_ayas()
            html += "<ul>"
            for sajda in sajdas:
                html += f"<li>{sajda.get('sura_name', '')} - آية {sajda.get('aya', '')}</li>"
            html += "</ul>"
        else:
            html += "<p>قريباً...</p>"

        html += "</body></html>"
        self.text_browser.setHtml(html)

    # ═══════════════════════════════════════════════════════════════
    # نوافذ الانتقال السريع
    # ═══════════════════════════════════════════════════════════════

    def show_goto_dialog(self):
        """نافذة الانتقال إلى سورة:آية"""
        from dialogs import GotoDialog
        dialog = GotoDialog(self, self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            sura, aya = dialog.get_values()
            self.load_sura_aya(sura, aya)

    def show_goto_juz_dialog(self):
        """نافذة الانتقال إلى جزء"""
        juz, ok = QInputDialog.getInt(
            self, "الانتقال إلى جزء",
            "رقم الجزء (1-30):",
            self.current_juz or 1, 1, 30, 1
        )
        if ok:
            # الانتقال لأول سورة في الجزء
            suras = self.db.get_suras_in_juz(juz)
            if suras:
                self.load_sura_aya(suras[0]['sura'], 1)

    def show_goto_page_dialog(self):
        """نافذة الانتقال إلى صفحة"""
        page, ok = QInputDialog.getInt(
            self, "الانتقال إلى صفحة",
            "رقم الصفحة (1-604):",
            self.current_page or 1, 1, 604, 1
        )
        if ok:
            # الانتقال لأول آية في الصفحة
            ayas = self.db.get_page_ayas(page)
            if ayas:
                self.load_sura_aya(ayas[0]['sura'], ayas[0]['aya'])

    # ═══════════════════════════════════════════════════════════════
    # البحث
    # ═══════════════════════════════════════════════════════════════

    def perform_quick_search(self):
        """بحث سريع"""
        query = self.search_input.text().strip()
        if len(query) < SEARCH_SETTINGS['min_chars']:
            return

        # نوع البحث
        search_type = 'text'
        for btn in self.search_type_group.buttons():
            if btn.isChecked():
                search_type = btn.property('search_id')
                break

        # أماكن البحث
        places = [pid for pid, cb in self.search_places.items() if cb.isChecked()]

        # البحث
        if search_type == 'text':
            results = self.db.search_text(query, places)
        elif search_type == 'root':
            results = self.db.search_by_root(query, places)
        elif search_type == 'pattern':
            results = self.db.search_by_pattern(query, places)
        elif search_type == 'topic':
            results = self.db.search_by_topic(query, places)
        else:
            results = []

        # عرض النتائج
        self.quick_results_list.clear()
        for result in results:
            sura_name = result.get('sura_name', '')
            aya = result.get('aya', '')
            text = result.get('text', '')[:80]
            source = result.get('source', '')

            icons = {
                'quran': '📖',
                'tafsir': '📚',
                'historical': '📜',
                'translation': '🌍'
            }
            icon = icons.get(source, '📄')

            item_text = f"{icon} {sura_name}:{aya} - {text}..."
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, result)
            self.quick_results_list.addItem(item)

    def on_quick_result_clicked(self, item):
        """عند النقر على نتيجة بحث"""
        result = item.data(Qt.ItemDataRole.UserRole)
        if result:
            sura = result.get('sura')
            aya = result.get('aya', 1)
            if sura:
                self.load_sura_aya(sura, aya)

    def show_search_dialog(self):
        """نافذة البحث المتقدم"""
        from dialogs import SearchDialog
        dialog = SearchDialog(self, self.db)
        dialog.exec()

    # ═══════════════════════════════════════════════════════════════
    # الإجراءات
    # ═══════════════════════════════════════════════════════════════

    def change_rasm(self, rasm_id: str):
        """تغيير نوع الرسم"""
        self.current_rasm = rasm_id
        index = list(RASM_TYPES.keys()).index(rasm_id)
        self.rasm_combo.setCurrentIndex(index)
        self.load_sura_aya(self.current_sura, self.current_aya)

    def change_font(self, font_id: str):
        """تغيير الخط"""
        self.current_font = font_id
        # إيجاد الفهرس في القائمة
        for i in range(self.font_combo.count()):
            if self.font_combo.itemData(i) == font_id:
                self.font_combo.setCurrentIndex(i)
                break
        self.load_sura_aya(self.current_sura, self.current_aya)

    def copy_text(self):
        """نسخ النص"""
        cursor = self.text_browser.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            QApplication.clipboard().setText(text)
            self.status_sura_label.setText("✅ تم النسخ")
            QTimer.singleShot(2000, self.update_status_bar)

    def select_all(self):
        """تحديد الكل"""
        self.text_browser.selectAll()

    def add_bookmark(self):
        """إضافة علامة مرجعية"""
        note, ok = QInputDialog.getText(
            self, "إضافة علامة مرجعية",
            f"ملاحظة لـ {self.db.get_sura_name(self.current_sura)}:{self.current_aya}"
        )
        if ok:
            self.db.add_bookmark(self.current_sura, self.current_aya, note)
            self.status_sura_label.setText("✅ تمت الإضافة")
            QTimer.singleShot(2000, self.update_status_bar)

    def show_bookmarks(self):
        """عرض العلامات المرجعية"""
        from dialogs import BookmarksDialog
        dialog = BookmarksDialog(self, self.db)
        if dialog.result_sura and dialog.result_aya:
            self.load_sura_aya(dialog.result_sura, dialog.result_aya)

    def save_file(self):
        """حفظ باسم"""
        sura_name = self.db.get_sura_name(self.current_sura)
        filename, _ = QFileDialog.getSaveFileName(
            self, "حفظ باسم",
            f"{sura_name}.html",
            "HTML Files (*.html);;Text Files (*.txt)"
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.text_browser.toHtml())
            self.status_sura_label.setText(f"✅ تم الحفظ")
            QTimer.singleShot(2000, self.update_status_bar)

    def print_content(self):
        """طباعة"""
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.text_browser.print(printer)

    def toggle_fullscreen(self):
        """ملء الشاشة"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def show_context_menu(self, pos):
        """قائمة السياق"""
        menu = QMenu(self)

        copy_action = menu.addAction("📋 نسخ")
        copy_action.triggered.connect(self.copy_text)

        menu.addSeparator()

        bookmark_action = menu.addAction("🔖 إضافة علامة")
        bookmark_action.triggered.connect(self.add_bookmark)

        menu.exec(self.text_browser.mapToGlobal(pos))

    def open_user_guide(self, lang: str):
        """فتح دليل الاستخدام"""
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl

        guide_path = USER_GUIDE_AR if lang == 'ar' else USER_GUIDE_EN
        if guide_path.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(guide_path)))
        else:
            QMessageBox.information(self, "تنبيه", "دليل الاستخدام غير متوفر حالياً")

    def show_about(self):
        """حول البرنامج"""
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("حول البرنامج")
        about_dialog.setMinimumWidth(500)

        layout = QVBoxLayout(about_dialog)

        text_browser = QTextBrowser()
        text_browser.setHtml(get_about_text())
        text_browser.setOpenExternalLinks(True)
        layout.addWidget(text_browser)

        btn_close = QPushButton("إغلاق")
        btn_close.clicked.connect(about_dialog.close)
        layout.addWidget(btn_close)

        about_dialog.exec()


# ═══════════════════════════════════════════════════════════════
# البرنامج الرئيسي
# ═══════════════════════════════════════════════════════════════

def main():
    """نقطة البدء"""
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    app.setStyle('Fusion')

    # عرض شاشة التحميل
    print("=" * 60)
    print(f"📖 {APP_NAME} v{APP_VERSION}")
    print(f"🏢 {COMPANY} | 👨‍💻 {DEVELOPER}")
    print("=" * 60)

    window = QuranProApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

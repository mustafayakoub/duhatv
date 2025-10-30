#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
💬 النوافذ المنبثقة - تطبيق القرآن الكريم Pro
═══════════════════════════════════════════════════════════════
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from config import *


# ═══════════════════════════════════════════════════════════════
# نافذة الانتقال إلى سورة:آية
# ═══════════════════════════════════════════════════════════════

class GotoDialog(QDialog):
    """نافذة الانتقال إلى سورة:آية"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("📖 الانتقال إلى سورة:آية")
        self.setModal(True)
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        # السورة
        sura_layout = QHBoxLayout()
        sura_layout.addWidget(QLabel("السورة:"))
        self.sura_combo = QComboBox()
        for i in range(1, 115):
            sura_info = self.db.get_sura_info(i)
            self.sura_combo.addItem(f"{i}. {sura_info['name']}", i)
        self.sura_combo.currentIndexChanged.connect(self.on_sura_changed)
        sura_layout.addWidget(self.sura_combo)
        layout.addLayout(sura_layout)

        # الآية
        aya_layout = QHBoxLayout()
        aya_layout.addWidget(QLabel("الآية:"))
        self.aya_spin = QSpinBox()
        self.aya_spin.setMinimum(1)
        self.aya_spin.setMaximum(286)  # أطول سورة
        aya_layout.addWidget(self.aya_spin)
        layout.addLayout(aya_layout)

        # الأزرار
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # تحديث عدد الآيات
        self.on_sura_changed(0)

    def on_sura_changed(self, index):
        """تحديث عدد الآيات عند تغيير السورة"""
        sura_num = self.sura_combo.itemData(index)
        if sura_num:
            sura_info = self.db.get_sura_info(sura_num)
            self.aya_spin.setMaximum(sura_info['ayas_count'])

    def get_values(self):
        """الحصول على القيم"""
        sura = self.sura_combo.currentData()
        aya = self.aya_spin.value()
        return sura, aya


# ═══════════════════════════════════════════════════════════════
# نافذة البحث المتقدم
# ═══════════════════════════════════════════════════════════════

class SearchDialog(QDialog):
    """نافذة البحث المتقدم"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("🔍 البحث المتقدم")
        self.setModal(True)
        self.resize(700, 500)

        layout = QVBoxLayout(self)

        # حقل البحث
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث في القرآن الكريم...")
        self.search_input.returnPressed.connect(self.perform_search)
        search_layout.addWidget(self.search_input)

        btn_search = QPushButton("🔍 بحث")
        btn_search.clicked.connect(self.perform_search)
        search_layout.addWidget(btn_search)

        layout.addLayout(search_layout)

        # خيارات البحث
        options_layout = QHBoxLayout()

        # نوع البحث
        type_group = QGroupBox("نوع البحث")
        type_layout = QVBoxLayout()
        self.search_type_group = QButtonGroup()

        for sid, sinfo in SEARCH_TYPES.items():
            radio = QRadioButton(f"{sinfo['icon']} {sinfo['name']}")
            radio.setProperty('search_id', sid)
            self.search_type_group.addButton(radio)
            type_layout.addWidget(radio)
            if sid == 'text':
                radio.setChecked(True)

        type_group.setLayout(type_layout)
        options_layout.addWidget(type_group)

        # أماكن البحث
        places_group = QGroupBox("أماكن البحث")
        places_layout = QVBoxLayout()
        self.places_checkboxes = {}

        for pid, pinfo in SEARCH_PLACES.items():
            checkbox = QCheckBox(f"{pinfo['icon']} {pinfo['name']}")
            checkbox.setChecked(pinfo['checked'])
            self.places_checkboxes[pid] = checkbox
            places_layout.addWidget(checkbox)

        places_group.setLayout(places_layout)
        options_layout.addWidget(places_group)

        layout.addLayout(options_layout)

        # النتائج
        self.results_label = QLabel("النتائج: 0")
        self.results_label.setStyleSheet(f"color: {COLORS['primary']}; font-weight: bold;")
        layout.addWidget(self.results_label)

        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.on_result_clicked)
        layout.addWidget(self.results_list)

        # أزرار
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.close)
        layout.addWidget(buttons)

    def perform_search(self):
        """تنفيذ البحث"""
        query = self.search_input.text().strip()
        if len(query) < SEARCH_SETTINGS['min_chars']:
            self.results_label.setText(MESSAGES['min_chars'].format(min=SEARCH_SETTINGS['min_chars']))
            return

        # نوع البحث
        search_type = 'text'
        for btn in self.search_type_group.buttons():
            if btn.isChecked():
                search_type = btn.property('search_id')
                break

        # أماكن البحث
        places = [pid for pid, cb in self.places_checkboxes.items() if cb.isChecked()]

        if not places:
            self.results_label.setText("⚠️ اختر مكان البحث")
            return

        # البحث
        self.results_label.setText(MESSAGES['searching'])
        QApplication.processEvents()

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
        self.results_list.clear()
        for result in results:
            sura_name = result.get('sura_name', '')
            aya = result.get('aya', '')
            text = result.get('text', '')[:100]
            source = result.get('source', '')
            extra = result.get('extra', '')

            icons = {
                'quran': '📖',
                'tafsir': '📚',
                'historical': '📜',
                'translation': '🌍',
                'root': '🌳',
                'pattern': '⚖️',
                'topic': '📑'
            }
            icon = icons.get(source, '📄')

            extra_text = f" [{extra}]" if extra else ""
            item_text = f"{icon} {sura_name}:{aya}{extra_text} - {text}..."

            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, result)
            self.results_list.addItem(item)

        # تحديث العداد
        count = len(results)
        if count == 0:
            self.results_label.setText(MESSAGES['no_results'])
        elif count == 1:
            self.results_label.setText(MESSAGES['single_result'])
        else:
            self.results_label.setText(MESSAGES['results_count'].format(count=count))

    def on_result_clicked(self, item):
        """عند النقر على نتيجة"""
        result = item.data(Qt.ItemDataRole.UserRole)
        if result:
            QMessageBox.information(
                self, "النتيجة",
                f"{result.get('sura_name', '')}:{result.get('aya', '')}\n\n{result.get('text', '')}"
            )


# ═══════════════════════════════════════════════════════════════
# نافذة العلامات المرجعية
# ═══════════════════════════════════════════════════════════════

class BookmarksDialog(QDialog):
    """نافذة العلامات المرجعية"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.result_sura = None
        self.result_aya = None
        self.init_ui()
        self.load_bookmarks()

    def init_ui(self):
        self.setWindowTitle("🔖 العلامات المرجعية")
        self.setModal(True)
        self.resize(600, 400)

        layout = QVBoxLayout(self)

        self.bookmarks_list = QListWidget()
        self.bookmarks_list.itemDoubleClicked.connect(self.on_bookmark_clicked)
        layout.addWidget(self.bookmarks_list)

        buttons_layout = QHBoxLayout()

        btn_goto = QPushButton("📖 انتقال")
        btn_goto.clicked.connect(self.goto_bookmark)
        buttons_layout.addWidget(btn_goto)

        btn_delete = QPushButton("🗑️ حذف")
        btn_delete.clicked.connect(self.delete_bookmark)
        buttons_layout.addWidget(btn_delete)

        buttons_layout.addStretch()

        btn_close = QPushButton("إغلاق")
        btn_close.clicked.connect(self.close)
        buttons_layout.addWidget(btn_close)

        layout.addLayout(buttons_layout)

    def load_bookmarks(self):
        """تحميل العلامات"""
        self.bookmarks_list.clear()
        bookmarks = self.db.get_bookmarks()

        for bookmark in bookmarks:
            text = f"{bookmark.get('sura_name', '')}:{bookmark.get('aya', '')}"
            note = bookmark.get('note', '')
            if note:
                text += f" - {note}"

            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, bookmark)
            self.bookmarks_list.addItem(item)

    def on_bookmark_clicked(self, item):
        """عند النقر المزدوج على علامة"""
        self.goto_bookmark()

    def goto_bookmark(self):
        """الانتقال للعلامة"""
        current = self.bookmarks_list.currentItem()
        if current:
            bookmark = current.data(Qt.ItemDataRole.UserRole)
            self.result_sura = bookmark.get('sura')
            self.result_aya = bookmark.get('aya', 1)
            self.close()

    def delete_bookmark(self):
        """حذف علامة"""
        current = self.bookmarks_list.currentItem()
        if current:
            bookmark = current.data(Qt.ItemDataRole.UserRole)
            reply = QMessageBox.question(
                self, "تأكيد الحذف",
                "هل تريد حذف هذه العلامة؟",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.db.remove_bookmark(bookmark.get('id'))
                self.load_bookmarks()


# ═══════════════════════════════════════════════════════════════
# نهاية الملف
# ═══════════════════════════════════════════════════════════════

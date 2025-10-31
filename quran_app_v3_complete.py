#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
           تطبيق القرآن الكريم النسخة 3.0 - متوافق مع quran_ultimate_final.db
================================================================================
"""

import sys
import os
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any

# استيراد PyQt
try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont
    PYQT_VERSION = 6
except ImportError:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont
    PYQT_VERSION = 5


# نظام الألوان
class ClaudeColors:
    PRIMARY = "#CC9B66"
    BG_MAIN = "#F8F6F4"
    BG_SIDEBAR = "#F0EBE3"
    BG_CONTENT = "#FFFFFF"
    TEXT_PRIMARY = "#2C2416"
    TEXT_SECONDARY = "#5C5445"
    HOVER = "#E5D4B8"
    SELECTED = "#D4C4A8"
    BORDER_LIGHT = "#E0D5C7"

    @classmethod
    def get_stylesheet(cls):
        return f"""
        QMainWindow {{ background-color: {cls.BG_MAIN}; }}
        QTreeWidget {{ background-color: {cls.BG_SIDEBAR}; border: 1px solid {cls.BORDER_LIGHT};
                      border-radius: 8px; padding: 8px; }}
        QTreeWidget::item:hover {{ background-color: {cls.HOVER}; }}
        QTreeWidget::item:selected {{ background-color: {cls.SELECTED}; }}
        QTextEdit {{ background-color: {cls.BG_CONTENT}; border: 1px solid {cls.BORDER_LIGHT};
                    border-radius: 8px; padding: 16px; }}
        QPushButton {{ background-color: {cls.PRIMARY}; color: white; border-radius: 8px;
                      padding: 10px 20px; font-weight: bold; }}
        QTabBar::tab {{ padding: 12px 24px; }}
        QTabBar::tab:selected {{ background-color: {cls.PRIMARY}; color: white; }}
        """


# مدير قاعدة البيانات
class QuranDatabaseManager:
    def __init__(self):
        self.conn = None
        self.surahs = []
        self.tafasir = {}

    def find_database(self):
        paths = [r"C:\quran9\quran_ultimate_final.db", "quran_ultimate_final.db"]
        for p in paths:
            if os.path.exists(p):
                return p
        return None

    def connect(self):
        self.db_path = self.find_database()
        if not self.db_path:
            return False
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self._load_surahs()
            self._load_tafasir()
            return True
        except Exception as e:
            print(f"خطأ: {e}")
            return False

    def _load_surahs(self):
        c = self.conn.cursor()
        c.execute("SELECT NSoura, Nom, makki_madani FROM Souar ORDER BY NSoura")
        for row in c.fetchall():
            self.surahs.append({
                'id': row[0],
                'name': row[1],
                'type': 'مكية' if row[2] == 'ك' else 'مدنية'
            })

    def _load_tafasir(self):
        c = self.conn.cursor()
        c.execute("SELECT NTafsir, Nom_S, Nom FROM Tafassir ORDER BY NTafsir")
        for row in c.fetchall():
            self.tafasir[row[0]] = {'short': row[1], 'full': row[2]}

    def get_surahs(self):
        return self.surahs

    def get_ayah_count(self, surah_id):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM Ayat WHERE NSoura = ?", (surah_id,))
        return c.fetchone()[0]

    def get_ayah_text(self, surah_id, ayah_num):
        c = self.conn.cursor()
        c.execute("SELECT Aya, Aya2, NPage, NPartie FROM Ayat WHERE NSoura = ? AND NAya = ?",
                  (surah_id, ayah_num))
        row = c.fetchone()
        if row:
            return {
                'text': row[0],
                'text_simple': row[1],
                'page': row[2],
                'juz': row[3]
            }
        return None

    def get_tafsir(self, surah_id, ayah_num, tafsir_id):
        c = self.conn.cursor()
        table = f"{surah_id:03d}"
        c.execute(f"SELECT Texte FROM '{table}' WHERE NAya = ? AND NTafsir = ?",
                  (ayah_num, tafsir_id))
        row = c.fetchone()
        return row[0] if row else None

    def search_text(self, text, limit=100):
        c = self.conn.cursor()
        c.execute("SELECT NSoura, NAya, Aya FROM Ayat WHERE Aya LIKE ? OR Aya2 LIKE ? LIMIT ?",
                  (f'%{text}%', f'%{text}%', limit))
        results = []
        for row in c.fetchall():
            results.append({
                'surah_id': row[0],
                'surah_name': self.surahs[row[0]-1]['name'],
                'ayah_num': row[1],
                'text': row[2]
            })
        return results

    def close(self):
        if self.conn:
            self.conn.close()


# التطبيق الرئيسي
class QuranApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = QuranDatabaseManager()
        self.current_surah = None
        self.current_ayah = None
        self.init_ui()
        self.init_database()

    def init_ui(self):
        self.setWindowTitle("تطبيق القرآن الكريم 3.0")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(ClaudeColors.get_stylesheet())

        # الويدجت الرئيسي
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal if PYQT_VERSION == 6 else Qt.Horizontal)

        # الشجرة
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("📖 القرآن الكريم")
        self.tree.setMinimumWidth(300)
        self.tree.itemClicked.connect(self.on_tree_clicked)
        self.tree.itemExpanded.connect(self.on_tree_expanded)
        splitter.addWidget(self.tree)

        # المحتوى
        content = self.create_content_area()
        splitter.addWidget(content)

        splitter.setSizes([300, 1100])
        layout.addWidget(splitter)

        # شريط الحالة
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def create_content_area(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # التبويبات
        self.tabs = QTabWidget()

        # تاب القرآن
        self.quran_text = QTextEdit()
        self.quran_text.setReadOnly(True)
        self.quran_text.setFont(QFont("Traditional Arabic", 18))
        self.tabs.addTab(self.quran_text, "📖 القرآن")

        # تاب التفسير
        tafsir_widget = QWidget()
        tafsir_layout = QVBoxLayout(tafsir_widget)

        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("اختر التفسير:"))
        self.tafsir_combo = QComboBox()
        self.tafsir_combo.currentIndexChanged.connect(self.update_tafsir)
        selector_layout.addWidget(self.tafsir_combo)
        selector_layout.addStretch()
        tafsir_layout.addLayout(selector_layout)

        self.tafsir_text = QTextEdit()
        self.tafsir_text.setReadOnly(True)
        self.tafsir_text.setFont(QFont("Traditional Arabic", 14))
        tafsir_layout.addWidget(self.tafsir_text)

        self.tabs.addTab(tafsir_widget, "📚 التفسير")

        # تاب البحث
        search_widget = self.create_search_tab()
        self.tabs.addTab(search_widget, "🔍 البحث")

        layout.addWidget(self.tabs)
        return widget

    def create_search_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # حقل البحث
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث في القرآن...")
        self.search_input.returnPressed.connect(self.perform_search)
        search_layout.addWidget(self.search_input)

        search_btn = QPushButton("🔍 بحث")
        search_btn.clicked.connect(self.perform_search)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        # النتائج
        self.search_results = QTreeWidget()
        self.search_results.setHeaderLabels(["السورة", "الآية", "النص"])
        self.search_results.itemClicked.connect(self.on_search_result_clicked)
        layout.addWidget(self.search_results)

        return widget

    def init_database(self):
        if not self.db.connect():
            QMessageBox.critical(self, "خطأ", "لم يتم العثور على قاعدة البيانات!")
            return

        self.load_surahs()
        self.load_tafasir_list()
        self.status_bar.showMessage(f"✅ تم تحميل {len(self.db.surahs)} سورة")

    def load_surahs(self):
        for surah in self.db.get_surahs():
            item = QTreeWidgetItem(self.tree)
            item.setText(0, f"📖 {surah['name']} ({surah['type']})")
            item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole,
                        {'type': 'surah', 'id': surah['id']})
            # عنصر وهمي
            QTreeWidgetItem(item).setText(0, "...")

    def load_tafasir_list(self):
        self.tafsir_combo.clear()
        for tid, info in sorted(self.db.tafasir.items()):
            self.tafsir_combo.addItem(f"{info['short']}", tid)

    def on_tree_expanded(self, item):
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)
        if data and data['type'] == 'surah':
            item.takeChildren()
            surah_id = data['id']
            count = self.db.get_ayah_count(surah_id)
            for i in range(1, count + 1):
                ayah_item = QTreeWidgetItem(item)
                ayah_item.setText(0, f"آية {i}")
                ayah_item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole,
                                 {'type': 'ayah', 'surah_id': surah_id, 'ayah_num': i})

    def on_tree_clicked(self, item, column):
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)
        if data and data['type'] == 'ayah':
            self.display_ayah(data['surah_id'], data['ayah_num'])

    def display_ayah(self, surah_id, ayah_num):
        self.current_surah = surah_id
        self.current_ayah = ayah_num

        ayah_data = self.db.get_ayah_text(surah_id, ayah_num)
        if not ayah_data:
            return

        surah_name = self.db.surahs[surah_id-1]['name']

        # عرض القرآن
        self.quran_text.setHtml(f"""
            <div style='text-align: center; direction: rtl; padding: 20px;'>
                <h2 style='color: {ClaudeColors.PRIMARY};'>{surah_name} - الآية {ayah_num}</h2>
                <p style='font-size: 24px; line-height: 2.5;'>{ayah_data['text']}</p>
                <p style='color: {ClaudeColors.TEXT_SECONDARY}; margin-top: 20px;'>
                    الصفحة: {ayah_data['page']} | الجزء: {ayah_data['juz']}
                </p>
            </div>
        """)

        # تحديث التفسير
        self.update_tafsir()
        self.tabs.setCurrentIndex(0)
        self.status_bar.showMessage(f"{surah_name} - آية {ayah_num}")

    def update_tafsir(self):
        if not self.current_surah or not self.current_ayah:
            return

        tafsir_id = self.tafsir_combo.currentData()
        if not tafsir_id:
            return

        tafsir_text = self.db.get_tafsir(self.current_surah, self.current_ayah, tafsir_id)
        if tafsir_text:
            self.tafsir_text.setHtml(f"""
                <div style='direction: rtl; padding: 20px;'>
                    <p style='font-size: 16px; line-height: 2;'>{tafsir_text}</p>
                </div>
            """)
        else:
            self.tafsir_text.setText("لا يوجد تفسير متاح")

    def perform_search(self):
        text = self.search_input.text().strip()
        if not text:
            return

        self.search_results.clear()
        results = self.db.search_text(text, 100)

        for r in results:
            item = QTreeWidgetItem(self.search_results)
            item.setText(0, r['surah_name'])
            item.setText(1, str(r['ayah_num']))
            item.setText(2, r['text'][:80] + "...")
            item.setData(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole, r)

        self.status_bar.showMessage(f"✅ {len(results)} نتيجة")

    def on_search_result_clicked(self, item, column):
        data = item.data(0, Qt.ItemDataRole.UserRole if PYQT_VERSION == 6 else Qt.UserRole)
        if data:
            self.display_ayah(data['surah_id'], data['ayah_num'])

    def closeEvent(self, event):
        self.db.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft if PYQT_VERSION == 6 else Qt.RightToLeft)
    window = QuranApp()
    window.show()
    sys.exit(app.exec() if PYQT_VERSION == 6 else app.exec_())


if __name__ == "__main__":
    main()

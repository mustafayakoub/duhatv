#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
📖 القرآن الكريم Ultimate v3.0.0
═══════════════════════════════════════════════════════════════
🎨 واجهة عصرية محسّنة
🚀 دعم PostgreSQL + SQLite | 🔍 بحث متقدم
📊 قاعدة بيانات هرمية ذكية
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

from config import *

try:
    from postgres_manager import PostgresQuranDatabase
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("⚠️  psycopg2 غير متوفر - سيتم استخدام SQLite فقط")

from db_manager import QuranDatabase


# ═══════════════════════════════════════════════════════════════
# نافذة اختيار قاعدة البيانات
# ═══════════════════════════════════════════════════════════════

class DatabaseSelectionDialog(QDialog):
    """نافذة اختيار نوع قاعدة البيانات"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_db = None
        self.init_ui()

    def init_ui(self):
        """بناء الواجهة"""
        self.setWindowTitle("🚀 اختر قاعدة البيانات")
        self.setFixedSize(500, 350)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e3c72, stop:1 #2a5298);
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 20px;
                font-size: 14pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.5);
            }
            QLabel {
                color: white;
                font-size: 12pt;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # العنوان
        title = QLabel("📖 القرآن الكريم Ultimate")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20pt; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        subtitle = QLabel("اختر نوع قاعدة البيانات")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14pt; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        # زر PostgreSQL
        if POSTGRES_AVAILABLE:
            postgres_btn = QPushButton("🐘 PostgreSQL\nقاعدة بيانات هرمية ذكية\nبحث متقدم + إحصائيات")
            postgres_btn.clicked.connect(lambda: self.select_database('postgres'))
            layout.addWidget(postgres_btn)
        else:
            postgres_label = QLabel("⚠️  PostgreSQL غير متوفر\nقم بتثبيت psycopg2")
            postgres_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            postgres_label.setStyleSheet("color: #ffaa00; font-size: 10pt;")
            layout.addWidget(postgres_label)

        # زر SQLite
        sqlite_btn = QPushButton("💾 SQLite\nقاعدة بيانات محلية\nسريع وبسيط")
        sqlite_btn.clicked.connect(lambda: self.select_database('sqlite'))
        layout.addWidget(sqlite_btn)

        # معلومات إضافية
        info_label = QLabel("💡 يمكنك التبديل لاحقاً من الإعدادات")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 9pt; color: rgba(255, 255, 255, 0.7);")
        layout.addWidget(info_label)

        self.setLayout(layout)

    def select_database(self, db_type):
        """اختيار قاعدة البيانات"""
        self.selected_db = db_type
        self.accept()


# ═══════════════════════════════════════════════════════════════
# الواجهة الرئيسية
# ═══════════════════════════════════════════════════════════════

class QuranUltimateApp(QMainWindow):
    """التطبيق الرئيسي للقرآن الكريم Ultimate"""

    def __init__(self):
        super().__init__()

        # اختيار قاعدة البيانات
        dialog = DatabaseSelectionDialog()
        if dialog.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)

        self.db_type = dialog.selected_db

        # الاتصال بقاعدة البيانات
        self.init_database()

        # المتغيرات
        self.current_sura = 1
        self.current_aya = 1
        self.current_rasm = 'uthmani'

        # بناء الواجهة
        self.init_ui()

        # تحميل الفاتحة
        self.load_sura(1)

    def init_database(self):
        """تهيئة الاتصال بقاعدة البيانات"""
        try:
            if self.db_type == 'postgres':
                self.db = PostgresQuranDatabase(
                    host='localhost',
                    database='quran_hierarchical_db',
                    user='postgres',
                    password=''
                )
                print("✅ متصل بـ PostgreSQL")
            else:
                self.db = QuranDatabase()
                print("✅ متصل بـ SQLite")

        except Exception as e:
            QMessageBox.critical(
                self, "خطأ",
                f"فشل الاتصال بقاعدة البيانات:\n{e}"
            )
            sys.exit(1)

    def init_ui(self):
        """بناء الواجهة الرئيسية"""
        self.setWindowTitle(f"📖 القرآن الكريم Ultimate v3.0 - {self.db_type.upper()}")
        self.setGeometry(100, 100, 1200, 800)

        # أيقونة
        self.setWindowIcon(QIcon.fromTheme("quran"))

        # الستايل العام
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3c72, stop:1 #2a5298);
                border: none;
                padding: 5px;
                spacing: 10px;
            }
            QToolButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 11pt;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                font-size: 18pt;
                line-height: 2.0;
            }
            QComboBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 11pt;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #2a5298;
            }
            QLineEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 8px;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border-color: #2a5298;
            }
        """)

        # الودجت المركزي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # التخطيط الرئيسي
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # شريط الأدوات
        self.create_toolbar()

        # منطقة العرض
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.text_display)

        # شريط الحالة
        self.create_statusbar()

    def create_toolbar(self):
        """إنشاء شريط الأدوات"""
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # قائمة السور
        self.sura_combo = QComboBox()
        self.sura_combo.setMaxVisibleItems(15)
        self.load_suras_list()
        self.sura_combo.currentIndexChanged.connect(self.on_sura_changed)
        toolbar.addWidget(QLabel(" 📖 السورة: "))
        toolbar.addWidget(self.sura_combo)

        toolbar.addSeparator()

        # حقل البحث
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 ابحث في القرآن...")
        self.search_input.setMaximumWidth(300)
        self.search_input.returnPressed.connect(self.search)
        toolbar.addWidget(self.search_input)

        search_btn = QToolButton()
        search_btn.setText("بحث")
        search_btn.clicked.connect(self.search)
        toolbar.addWidget(search_btn)

        toolbar.addSeparator()

        # نوع الرسم
        rasm_combo = QComboBox()
        rasm_combo.addItems(["عثماني", "إملائي"])
        rasm_combo.currentIndexChanged.connect(self.change_rasm)
        toolbar.addWidget(QLabel(" ✍️ الرسم: "))
        toolbar.addWidget(rasm_combo)

        # مساحة فارغة
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        # معلومات القاعدة
        db_label = QToolButton()
        db_label.setText(f"💾 {self.db_type.upper()}")
        db_label.setEnabled(False)
        toolbar.addWidget(db_label)

    def create_statusbar(self):
        """إنشاء شريط الحالة"""
        self.statusBar().showMessage("✅ جاهز")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #2a5298;
                color: white;
                font-size: 10pt;
                padding: 5px;
            }
        """)

    def load_suras_list(self):
        """تحميل قائمة السور"""
        suras = self.db.get_all_suras()
        for sura in suras:
            name = sura.get('name', sura.get('name_arabic', f"السورة {sura['sura']}"))
            self.sura_combo.addItem(f"{sura['sura']:03d}. {name}", sura['sura'])

    def on_sura_changed(self, index):
        """عند تغيير السورة"""
        if index >= 0:
            sura_num = self.sura_combo.itemData(index)
            self.load_sura(sura_num)

    def load_sura(self, sura_num: int):
        """تحميل سورة كاملة"""
        self.current_sura = sura_num

        # معلومات السورة
        sura_info = self.db.get_sura_info(sura_num)

        # الآيات
        ayas = self.db.get_sura_ayas(sura_num, self.current_rasm)

        # بناء النص
        html = self.build_sura_html(sura_info, ayas)

        self.text_display.setHtml(html)

        # تحديث شريط الحالة
        self.statusBar().showMessage(
            f"📖 {sura_info['name']} | "
            f"الآيات: {sura_info['ayas_count']} | "
            f"{sura_info.get('type_full', 'مكية')}"
        )

    def build_sura_html(self, sura_info, ayas) -> str:
        """بناء HTML للسورة"""
        html = f"""
        <div style='text-align: center; direction: rtl;'>
            <h1 style='color: #1e3c72; font-size: 28pt; margin: 20px 0;'>
                سُورَةُ {sura_info['name']}
            </h1>
            <p style='color: #666; font-size: 14pt; margin-bottom: 30px;'>
                {sura_info.get('type_full', 'مكية')} -
                {sura_info['ayas_count']} آية
            </p>
        """

        # البسملة (ما عدا التوبة)
        if sura_info['sura'] != 9:
            html += """
            <p style='font-size: 24pt; color: #2a5298; margin: 20px 0;'>
                بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
            </p>
            """

        # الآيات
        for aya in ayas:
            html += f"""
            <p style='font-size: 20pt; line-height: 2.5; margin: 15px 0; text-align: justify;'>
                {aya['text']}
                <span style='color: #2a5298; font-size: 14pt;'> ﴿{aya['aya']}﴾ </span>
            </p>
            """

        html += "</div>"
        return html

    def search(self):
        """البحث في القرآن"""
        search_term = self.search_input.text().strip()

        if not search_term:
            QMessageBox.warning(self, "تنبيه", "الرجاء إدخال نص للبحث")
            return

        # البحث
        try:
            results = self.db.search_text(search_term, limit=50)

            if not results:
                QMessageBox.information(self, "نتائج البحث", "لم يتم العثور على نتائج")
                return

            # عرض النتائج
            self.show_search_results(search_term, results)

        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل البحث:\n{e}")

    def show_search_results(self, search_term, results):
        """عرض نتائج البحث"""
        html = f"""
        <div style='text-align: right; direction: rtl;'>
            <h2 style='color: #1e3c72; text-align: center;'>
                🔍 نتائج البحث عن: "{search_term}"
            </h2>
            <p style='color: #666; text-align: center; margin-bottom: 20px;'>
                تم العثور على {len(results)} نتيجة
            </p>
        """

        for i, result in enumerate(results, 1):
            # تمييز كلمة البحث
            text = result['text']
            highlighted = text.replace(search_term, f"<mark>{search_term}</mark>")

            html += f"""
            <div style='background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px;'>
                <p style='font-size: 16pt; line-height: 2;'>
                    {highlighted}
                </p>
                <p style='color: #666; font-size: 11pt; margin-top: 10px;'>
                    📖 السورة {result['sura']} - الآية {result['aya']} |
                    📄 الصفحة {result.get('page', '-')} |
                    📚 الجزء {result.get('juz', '-')}
                </p>
            </div>
            """

        html += "</div>"
        self.text_display.setHtml(html)

    def change_rasm(self, index):
        """تغيير نوع الرسم"""
        self.current_rasm = 'uthmani' if index == 0 else 'simple'
        self.load_sura(self.current_sura)


# ═══════════════════════════════════════════════════════════════
# البرنامج الرئيسي
# ═══════════════════════════════════════════════════════════════

def main():
    """البرنامج الرئيسي"""
    app = QApplication(sys.argv)

    # الخط العربي
    font = QFont("Arial", 12)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(font)

    # النافذة الرئيسية
    window = QuranUltimateApp()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

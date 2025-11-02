#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 QuranKit Tajweed Example - مثال على استخدام مكون التجويد
Demonstrates the powerful Tajweed Component from QuranKit
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextBrowser, QPushButton, QComboBox, QLabel, QGroupBox,
    QListWidget, QSplitter, QTabWidget, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# استيراد QuranKit Tajweed
from qurankit import QuranTajweedComponent, TajweedRule


class TajweedDemoApp(QMainWindow):
    """تطبيق توضيحي لمكون التجويد"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 QuranKit - مثال التجويد")
        self.setGeometry(100, 100, 1400, 900)

        # إنشاء مكون التجويد
        self.tajweed = QuranTajweedComponent()

        # نصوص تجريبية (من سورة الفاتحة)
        self.sample_texts = {
            'الفاتحة 1': '<4>بِسۡمِ</4> <10>ٱللَّهِ</10> <4>ٱلرَّحۡمَٰنِ</4> <4>ٱلرَّحِيمِ</4>',
            'الفاتحة 2': '<1>ٱلۡحَمۡدُ</1> <10>لِلَّهِ</10> <5>رَبِّ</5> <4>ٱلۡعَٰلَمِينَ</4>',
            'الفاتحة 3': '<4>ٱلرَّحۡمَٰنِ</4> <4>ٱلرَّحِيمِ</4>',
            'الفاتحة 4': '<4>مَٰلِكِ</4> <4>يَوۡمِ</4> <4>ٱلدِّينِ</4>',
            'الفاتحة 5': '<12>إِيَّاكَ</12> <7>نَعۡبُدُ</7> <12>وَإِيَّاكَ</12> <7>نَسۡتَعِينُ</7>',
            'الفاتحة 6': '<12>ٱهۡدِنَا</12> <8>ٱلصِّرَٰطَ</8> <4>ٱلۡمُسۡتَقِيمَ</4>',
            'الفاتحة 7': '<13>صِرَٰطَ</13> <4>ٱلَّذِينَ</4> <1>أَنۡعَمۡتَ</1> <3>عَلَيۡهِمۡ</3> <1>غَيۡرِ</1> <12>ٱلۡمَغۡضُوبِ</12> <3>عَلَيۡهِمۡ</3> <14>وَلَا</14> <13>ٱلضَّآلِّينَ</13>',
        }

        self.current_text = self.sample_texts['الفاتحة 1']

        # بناء الواجهة
        self.init_ui()

        # عرض أول آية
        self.display_current_text()

    def init_ui(self):
        """بناء الواجهة"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # العنوان
        title = QLabel("🎨 QuranKit - نظام ألوان التجويد الذكي")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1e3c72;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f0f0f0, stop:1 #e0e0e0);
                border-radius: 10px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # اختيار الآية
        selection_layout = QHBoxLayout()
        selection_layout.addWidget(QLabel("اختر آية:"))

        self.verse_combo = QComboBox()
        self.verse_combo.addItems(self.sample_texts.keys())
        self.verse_combo.currentTextChanged.connect(self.on_verse_changed)
        selection_layout.addWidget(self.verse_combo)

        selection_layout.addStretch()

        # اختيار الخط
        selection_layout.addWidget(QLabel("الخط:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems(self.tajweed.get_recommended_fonts())
        self.font_combo.currentTextChanged.connect(self.display_current_text)
        selection_layout.addWidget(self.font_combo)

        layout.addLayout(selection_layout)

        # Splitter رئيسي
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # اليمين: قائمة الأحكام
        rules_widget = self.create_rules_panel()
        splitter.addWidget(rules_widget)

        # اليسار: العرض
        display_widget = self.create_display_panel()
        splitter.addWidget(display_widget)

        splitter.setSizes([350, 1050])
        layout.addWidget(splitter)

        # شريط الحالة
        self.statusBar().showMessage("✅ جاهز - QuranKit Tajweed Component")

    def create_rules_panel(self) -> QWidget:
        """لوحة الأحكام التجويدية"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)

        # عنوان
        title = QLabel("📋 أحكام التجويد")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e3c72;")
        layout.addWidget(title)

        # قائمة الأحكام
        self.rules_list = QListWidget()
        self.rules_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1e3c72;
            }
        """)

        # ملء القائمة بالأحكام
        for rule_id in sorted(self.tajweed.get_all_rules().keys()):
            rule = self.tajweed.get_rule_info(rule_id)
            item_text = f"⬛ {rule.name} ({rule.name_en})"
            self.rules_list.addItem(item_text)

        self.rules_list.itemClicked.connect(self.on_rule_selected)
        layout.addWidget(self.rules_list)

        # زر إعادة الضبط
        btn_reset = QPushButton("🔄 إعادة ضبط الألوان")
        btn_reset.clicked.connect(self.reset_colors)
        btn_reset.setStyleSheet("""
            QPushButton {
                background-color: #2a5298;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1e3c72;
            }
        """)
        layout.addWidget(btn_reset)

        return widget

    def create_display_panel(self) -> QWidget:
        """لوحة العرض"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)

        # التابات
        self.tabs = QTabWidget()

        # تاب العرض الملون
        self.colored_display = QTextBrowser()
        self.colored_display.setFont(QFont("Traditional Arabic", 18))
        self.colored_display.setStyleSheet("""
            QTextBrowser {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
                background-color: white;
            }
        """)
        self.tabs.addTab(self.colored_display, "🎨 العرض الملون")

        # تاب الإحصائيات
        self.stats_display = QTextBrowser()
        self.stats_display.setFont(QFont("Traditional Arabic", 14))
        self.stats_display.setStyleSheet("""
            QTextBrowser {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
                background-color: white;
            }
        """)
        self.tabs.addTab(self.stats_display, "📊 الإحصائيات")

        # تاب الكلمات المستخرجة
        self.words_display = QTextBrowser()
        self.words_display.setFont(QFont("Traditional Arabic", 13))
        self.words_display.setStyleSheet("""
            QTextBrowser {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
                background-color: white;
            }
        """)
        self.tabs.addTab(self.words_display, "🔍 استخراج الكلمات")

        # تاب البحث
        search_tab = self.create_search_tab()
        self.tabs.addTab(search_tab, "🔎 البحث")

        layout.addWidget(self.tabs)

        return widget

    def create_search_tab(self) -> QWidget:
        """تاب البحث عن حكم تجويدي"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # شريط البحث
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("ابحث عن حكم:"))

        self.search_combo = QComboBox()
        for rule_id in sorted(self.tajweed.get_all_rules().keys()):
            rule = self.tajweed.get_rule_info(rule_id)
            self.search_combo.addItem(f"{rule.name} - {rule.name_en}", rule_id)
        search_layout.addWidget(self.search_combo)

        btn_search = QPushButton("🔍 بحث")
        btn_search.clicked.connect(self.search_rule)
        btn_search.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        search_layout.addWidget(btn_search)

        layout.addLayout(search_layout)

        # النتائج
        self.search_results = QTextBrowser()
        self.search_results.setFont(QFont("Traditional Arabic", 16))
        self.search_results.setStyleSheet("""
            QTextBrowser {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
                background-color: white;
            }
        """)
        layout.addWidget(self.search_results)

        return widget

    def on_verse_changed(self, verse_name: str):
        """عند تغيير الآية"""
        self.current_text = self.sample_texts[verse_name]
        self.display_current_text()

    def display_current_text(self):
        """عرض النص الحالي"""
        font = self.font_combo.currentText()

        # العرض الملون
        html = self.tajweed.format_ayah_with_tajweed(
            self.current_text,
            surah_name="الفاتحة",
            ayah_number=self.verse_combo.currentIndex() + 1,
            show_legend=True
        )
        self.colored_display.setHtml(html)

        # الإحصائيات
        stats = self.tajweed.get_tajweed_statistics(self.current_text)
        stats_html = self.tajweed.format_statistics_html(stats)
        self.stats_display.setHtml(stats_html)

        self.statusBar().showMessage(f"✅ تم عرض: {self.verse_combo.currentText()}")

    def on_rule_selected(self, item):
        """عند اختيار حكم من القائمة"""
        rule_index = self.rules_list.currentRow()
        rule_id = list(sorted(self.tajweed.get_all_rules().keys()))[rule_index]
        rule = self.tajweed.get_rule_info(rule_id)

        # استخراج الكلمات المحتوية على هذا الحكم
        words = self.tajweed.extract_words_by_rule(self.current_text, rule_id)

        if words:
            words_html = f"""
            <div style='direction: rtl; padding: 20px; font-family: "Traditional Arabic", Arial;'>
                <h2 style='color: #1e3c72;'>
                    📋 الكلمات المحتوية على: {rule.name}
                </h2>
                <p><strong>اللون:</strong>
                    <span style='display: inline-block; width: 40px; height: 20px;
                                 background-color: {rule.color}; border-radius: 4px;
                                 vertical-align: middle;'></span>
                </p>
                <p><strong>الوصف:</strong> {rule.description}</p>
                <hr style='border: 1px solid #e0e0e0; margin: 20px 0;'>
                <h3>الكلمات ({len(words)}):</h3>
                <ul style='font-size: 20px; line-height: 2.5;'>
            """

            for word in words:
                words_html += f"""
                    <li style='color: {rule.color}; font-weight: bold;'>{word}</li>
                """

            words_html += """
                </ul>
            </div>
            """

            self.words_display.setHtml(words_html)
            self.tabs.setCurrentIndex(2)  # الانتقال لتاب الكلمات
        else:
            self.words_display.setHtml(f"""
                <div style='direction: rtl; padding: 20px; text-align: center;'>
                    <h2>⚠️ لا توجد كلمات</h2>
                    <p>لم يتم العثور على كلمات تحتوي على حكم: {rule.name}</p>
                </div>
            """)

        self.statusBar().showMessage(f"✅ تم تحديد: {rule.name}")

    def search_rule(self):
        """البحث عن حكم تجويدي"""
        rule_id = self.search_combo.currentData()
        rule = self.tajweed.get_rule_info(rule_id)

        # تمييز الحكم في النص
        highlighted_text = self.tajweed.highlight_rule(
            self.current_text,
            rule_id,
            highlight_color="#FFEB3B"
        )

        # تحويل إلى HTML
        html = self.tajweed.format_ayah_with_tajweed(
            highlighted_text,
            surah_name="الفاتحة (مع التمييز)",
            ayah_number=self.verse_combo.currentIndex() + 1,
            show_legend=True
        )

        self.search_results.setHtml(html)
        self.statusBar().showMessage(f"✅ تم البحث عن: {rule.name}")

    def reset_colors(self):
        """إعادة ضبط الألوان"""
        self.tajweed.reset_colors()
        self.display_current_text()
        self.statusBar().showMessage("✅ تم إعادة ضبط الألوان الافتراضية")


def main():
    """نقطة البداية"""
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # تطبيق ستايل عام
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QComboBox {
            padding: 6px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            background-color: white;
            font-size: 13px;
        }
        QComboBox:hover {
            border: 2px solid #1e3c72;
        }
        QLabel {
            font-size: 13px;
        }
    """)

    window = TajweedDemoApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    print("=" * 70)
    print("🎨 QuranKit Tajweed Component - تطبيق توضيحي")
    print("=" * 70)
    print("\n✨ الميزات:")
    print("   • عرض القرآن بألوان التجويد")
    print("   • 15 حكم تجويدي مختلف")
    print("   • البحث عن أحكام معينة")
    print("   • إحصائيات كاملة")
    print("   • استخراج الكلمات")
    print("   • تخصيص الألوان")
    print("\n🚀 بدء التشغيل...\n")
    print("=" * 70)

    main()

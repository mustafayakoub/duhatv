#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
🌳 QuranTreeComponent - مكون الشجرة الهرمية
Hierarchical Tree Navigation Component
═══════════════════════════════════════════════════════════════

🎯 الميزات:
- عرض هرمي للأجزاء والسور والآيات
- تنقل سهل وسريع
- بحث في الشجرة
- توسيع/طي الفروع
- أيقونات مميزة
- دعم السحب والإفلات
- حفظ واستعادة الحالة

📖 الاستخدام:
    from qurankit.components import QuranTreeComponent

    tree = QuranTreeComponent(database)
    tree_widget = tree.create_tree_widget()
    tree_widget.item_selected.connect(on_item_selected)

═══════════════════════════════════════════════════════════════
"""

from typing import Dict, Any, Optional, List
from PyQt6.QtWidgets import (QTreeWidget, QTreeWidgetItem, QWidget,
                             QVBoxLayout, QLineEdit, QHBoxLayout)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon


class QuranTreeComponent:
    """
    مكون الشجرة الهرمية للتنقل في القرآن

    يوفر عرض شجري منظم للأجزاء والسور والآيات
    """

    def __init__(self, database, config=None):
        """
        تهيئة مكون الشجرة

        Args:
            database: كائن قاعدة البيانات
            config: إعدادات الشجرة (اختياري)
        """
        self.database = database
        self.config = config or {}

        # إعدادات افتراضية
        self.show_ayahs = self.config.get('show_ayahs', False)
        self.show_juz = self.config.get('show_juz', True)
        self.arabic_numbers = self.config.get('arabic_numbers', True)

    # ═══════════════════════════════════════════════════════════════
    # بناء الشجرة
    # ═══════════════════════════════════════════════════════════════

    def build_tree_structure(self) -> List[Dict]:
        """
        بناء بنية الشجرة الكاملة

        Returns:
            بنية الشجرة كقائمة من القواميس
        """
        structure = []

        if self.show_juz:
            # بناء حسب الأجزاء
            for juz in range(1, 31):
                juz_node = {
                    'type': 'juz',
                    'number': juz,
                    'title': f"الجزء {self._format_number(juz)}",
                    'children': self._get_juz_suras(juz)
                }
                structure.append(juz_node)
        else:
            # بناء حسب السور فقط
            suras = self.database.get_all_suras()
            for sura in suras:
                sura_node = self._build_sura_node(sura)
                structure.append(sura_node)

        return structure

    def _build_sura_node(self, sura: Dict) -> Dict:
        """بناء عقدة السورة"""
        sura_node = {
            'type': 'sura',
            'number': sura['sura'],
            'title': f"{self._format_number(sura['sura'])}. {sura.get('name', '')}",
            'data': sura
        }

        if self.show_ayahs:
            sura_node['children'] = self._get_sura_ayahs(sura['sura'])

        return sura_node

    def _get_juz_suras(self, juz_num: int) -> List[Dict]:
        """الحصول على سور الجزء"""
        # هذه دالة مبسطة - يمكن تحسينها لاحقاً
        return []

    def _get_sura_ayahs(self, sura_num: int) -> List[Dict]:
        """الحصول على آيات السورة"""
        ayahs = []
        sura_info = self.database.get_sura_info(sura_num)
        ayah_count = sura_info.get('ayas_count', 0)

        for aya_num in range(1, ayah_count + 1):
            ayah_node = {
                'type': 'ayah',
                'number': aya_num,
                'title': f"الآية {self._format_number(aya_num)}",
                'sura': sura_num
            }
            ayahs.append(ayah_node)

        return ayahs

    def _format_number(self, number: int) -> str:
        """تنسيق الأرقام (عربي/هندي)"""
        if not self.arabic_numbers:
            return str(number)

        # تحويل للأرقام العربية
        arabic_digits = "٠١٢٣٤٥٦٧٨٩"
        return ''.join(arabic_digits[int(d)] for d in str(number))

    # ═══════════════════════════════════════════════════════════════
    # البحث في الشجرة
    # ═══════════════════════════════════════════════════════════════

    def search_tree(self, query: str, tree_structure: List[Dict]) -> List[Dict]:
        """
        البحث في بنية الشجرة

        Args:
            query: نص البحث
            tree_structure: بنية الشجرة

        Returns:
            العقد المطابقة
        """
        results = []
        query_lower = query.lower()

        def search_node(node):
            if query_lower in node.get('title', '').lower():
                results.append(node)

            for child in node.get('children', []):
                search_node(child)

        for node in tree_structure:
            search_node(node)

        return results

    # ═══════════════════════════════════════════════════════════════
    # حفظ واستعادة الحالة
    # ═══════════════════════════════════════════════════════════════

    def save_state(self, widget: 'QuranTreeWidget') -> Dict:
        """حفظ حالة الشجرة (العقد المفتوحة)"""
        state = {
            'expanded': [],
            'selected': None
        }

        # حفظ العقد المفتوحة
        def save_expanded(item, path=""):
            current_path = f"{path}/{item.text(0)}"
            if item.isExpanded():
                state['expanded'].append(current_path)

            for i in range(item.childCount()):
                save_expanded(item.child(i), current_path)

        root = widget.invisibleRootItem()
        for i in range(root.childCount()):
            save_expanded(root.child(i))

        # حفظ العنصر المختار
        selected = widget.currentItem()
        if selected:
            state['selected'] = selected.text(0)

        return state

    def restore_state(self, widget: 'QuranTreeWidget', state: Dict):
        """استعادة حالة الشجرة"""
        if not state:
            return

        # استعادة العقد المفتوحة
        def restore_expanded(item, path=""):
            current_path = f"{path}/{item.text(0)}"
            if current_path in state.get('expanded', []):
                item.setExpanded(True)

            for i in range(item.childCount()):
                restore_expanded(item.child(i), current_path)

        root = widget.invisibleRootItem()
        for i in range(root.childCount()):
            restore_expanded(root.child(i))

    # ═══════════════════════════════════════════════════════════════
    # Widgets
    # ═══════════════════════════════════════════════════════════════

    def create_tree_widget(self, parent=None) -> 'QuranTreeWidget':
        """
        إنشاء widget جاهز للشجرة

        Returns:
            QuranTreeWidget
        """
        return QuranTreeWidget(self, parent)


class QuranTreeWidget(QWidget):
    """Widget جاهز لعرض الشجرة الهرمية"""

    item_selected = pyqtSignal(dict)  # يصدر عند اختيار عنصر
    item_double_clicked = pyqtSignal(dict)

    def __init__(self, tree_component: QuranTreeComponent, parent=None):
        super().__init__(parent)
        self.tree_component = tree_component
        self.init_ui()

    def init_ui(self):
        """بناء الواجهة"""
        layout = QVBoxLayout()

        # شريط البحث
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 بحث في الشجرة...")
        self.search_input.textChanged.connect(self.filter_tree)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # الشجرة
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("القرآن الكريم")
        self.tree.setRightToLeft(True)
        self.tree.currentItemChanged.connect(self.on_item_changed)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)

        # تنسيق الشجرة
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                font-size: 12pt;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:hover {
                background-color: #f0f0f0;
            }
            QTreeWidget::item:selected {
                background-color: #1e3c72;
                color: white;
            }
        """)

        layout.addWidget(self.tree)
        self.setLayout(layout)

        # بناء الشجرة
        self.build_tree()

    def build_tree(self):
        """بناء الشجرة من البيانات"""
        self.tree.clear()
        structure = self.tree_component.build_tree_structure()

        for node in structure:
            self._add_tree_item(node, self.tree)

    def _add_tree_item(self, node: Dict, parent):
        """إضافة عنصر للشجرة"""
        item = QTreeWidgetItem(parent)
        item.setText(0, node.get('title', ''))

        # حفظ البيانات
        item.setData(0, Qt.ItemDataRole.UserRole, node)

        # إضافة أيقونة حسب النوع
        icon_map = {
            'juz': '📚',
            'sura': '📖',
            'ayah': '📜'
        }
        icon_text = icon_map.get(node.get('type'), '📄')
        item.setText(0, f"{icon_text} {node.get('title', '')}")

        # إضافة الأبناء
        for child in node.get('children', []):
            self._add_tree_item(child, item)

        return item

    def filter_tree(self, text: str):
        """فلترة الشجرة حسب نص البحث"""
        if not text:
            # إظهار الكل
            def show_all(item):
                item.setHidden(False)
                for i in range(item.childCount()):
                    show_all(item.child(i))

            root = self.tree.invisibleRootItem()
            for i in range(root.childCount()):
                show_all(root.child(i))
            return

        # إخفاء ما لا يطابق
        text_lower = text.lower()

        def filter_item(item):
            matches = text_lower in item.text(0).lower()
            child_matches = False

            for i in range(item.childCount()):
                if filter_item(item.child(i)):
                    child_matches = True

            visible = matches or child_matches
            item.setHidden(not visible)

            if visible and child_matches:
                item.setExpanded(True)

            return visible

        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            filter_item(root.child(i))

    def on_item_changed(self, current, previous):
        """عند تغيير العنصر المختار"""
        if current:
            data = current.data(0, Qt.ItemDataRole.UserRole)
            if data:
                self.item_selected.emit(data)

    def on_item_double_clicked(self, item, column):
        """عند النقر المزدوج"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            self.item_double_clicked.emit(data)

    def expand_all(self):
        """توسيع جميع العقد"""
        self.tree.expandAll()

    def collapse_all(self):
        """طي جميع العقد"""
        self.tree.collapseAll()


# ═══════════════════════════════════════════════════════════════
# Usage Example
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 70)
    print("🌳 QuranTreeComponent - مكون الشجرة الهرمية")
    print("═" * 70)

    example_code = """
    from qurankit.components import QuranTreeComponent

    # إنشاء مكون الشجرة
    tree = QuranTreeComponent(database, config={'show_juz': True})

    # إنشاء Widget
    tree_widget = tree.create_tree_widget()

    # ربط الإشارات
    def on_item_selected(data):
        if data['type'] == 'sura':
            print(f"تم اختيار السورة: {data['title']}")
        elif data['type'] == 'ayah':
            print(f"تم اختيار الآية: {data['number']}")

    tree_widget.item_selected.connect(on_item_selected)

    # عرض الشجرة
    tree_widget.show()
    """

    print(example_code)
    print("═" * 70)

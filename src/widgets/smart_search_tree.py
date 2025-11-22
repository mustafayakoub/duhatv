"""
🌳 الشجرة الديناميكية الذكية - دُحى TV
==========================================
شجرة بحث وعرض ديناميكية مرتبطة عصبياً مع كل مكونات التطبيق
"""

from PyQt6.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QStyle, QStyleOptionViewItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QFont, QColor, QBrush, QIcon
from typing import List, Dict, Optional, Any, Callable
from enum import Enum


class TreeItemType(Enum):
    """أنواع عناصر الشجرة"""
    ROOT = "root"                    # الجذر
    CATEGORY = "category"            # التصنيف (عرض، بحث، موضوعات)
    SOURCE = "source"                # المصدر (قرآن، تفاسير، ترجمات...)
    SURAH = "surah"                  # سورة
    VERSE = "verse"                  # آية
    TOPIC = "topic"                  # موضوع
    TOPIC_LEVEL_1 = "topic_l1"      # موضوع مستوى 1
    TOPIC_LEVEL_2 = "topic_l2"      # موضوع مستوى 2
    TOPIC_LEVEL_3 = "topic_l3"      # موضوع مستوى 3
    BOOK = "book"                    # كتاب (تفسير/ترجمة)
    WORD = "word"                    # كلمة
    SEARCH_RESULT = "search_result"  # نتيجة بحث


class SmartTreeItem(QTreeWidgetItem):
    """عنصر شجرة ذكي مع بيانات إضافية"""

    def __init__(
        self,
        parent: Optional[QTreeWidgetItem] = None,
        item_type: TreeItemType = TreeItemType.ROOT,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        تهيئة عنصر الشجرة

        Args:
            parent: العنصر الأب
            item_type: نوع العنصر
            data: البيانات المرتبطة
        """
        super().__init__(parent)

        self.item_type = item_type
        self.item_data = data or {}

        # إعداد المظهر
        self._setup_appearance()

    def _setup_appearance(self):
        """إعداد المظهر حسب نوع العنصر"""
        # الخط
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(11)

        # حسب النوع
        if self.item_type == TreeItemType.CATEGORY:
            font.setBold(True)
            font.setPointSize(12)
            self.setForeground(0, QBrush(QColor("#2c3e50")))

        elif self.item_type == TreeItemType.SURAH:
            font.setBold(True)
            self.setForeground(0, QBrush(QColor("#34495e")))

        elif self.item_type == TreeItemType.VERSE:
            self.setForeground(0, QBrush(QColor("#555555")))

        elif self.item_type in [TreeItemType.TOPIC_LEVEL_1]:
            font.setBold(True)
            font.setPointSize(12)
            self.setForeground(0, QBrush(QColor("#8e44ad")))

        elif self.item_type in [TreeItemType.TOPIC_LEVEL_2]:
            font.setPointSize(11)
            self.setForeground(0, QBrush(QColor("#9b59b6")))

        elif self.item_type in [TreeItemType.TOPIC_LEVEL_3]:
            self.setForeground(0, QBrush(QColor("#a569bd")))

        elif self.item_type == TreeItemType.SEARCH_RESULT:
            self.setForeground(0, QBrush(QColor("#27ae60")))

        self.setFont(0, font)

    def get_data(self, key: str, default: Any = None) -> Any:
        """جلب بيانات محددة"""
        return self.item_data.get(key, default)

    def set_data(self, key: str, value: Any):
        """تعيين بيانات"""
        self.item_data[key] = value


class SmartSearchTree(QTreeWidget):
    """
    الشجرة الديناميكية الذكية

    Features:
    - تحديث ديناميكي
    - ربط عصبي
    - بحث فوري
    - التنقل بالكيبورد
    - تخزين مؤقت
    """

    # الإشارات
    item_selected = pyqtSignal(dict)         # عند اختيار عنصر
    verse_selected = pyqtSignal(int)         # عند اختيار آية
    surah_selected = pyqtSignal(int)         # عند اختيار سورة
    topic_selected = pyqtSignal(int)         # عند اختيار موضوع
    search_triggered = pyqtSignal(str)       # عند تفعيل البحث

    def __init__(self, db_manager, parent: Optional[QWidget] = None):
        """
        تهيئة الشجرة

        Args:
            db_manager: مدير قاعدة البيانات
            parent: Widget الأب
        """
        super().__init__(parent)

        self.db = db_manager
        self.current_mode = "عرض"  # عرض / بحث / موضوعات
        self.cache = {}  # التخزين المؤقت

        # إعداد الشجرة
        self._setup_tree()

        # إعداد الاتصالات
        self._setup_connections()

        # تحميل البيانات الأولية
        self._load_initial_data()

    def _setup_tree(self):
        """إعداد خصائص الشجرة"""
        # إخفاء الهيدر
        self.setHeaderHidden(True)

        # تمكين السحب والإسقاط
        self.setDragEnabled(False)
        self.setAcceptDrops(False)

        # التمديد التلقائي
        self.setAnimated(True)

        # الاختيار
        self.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)

        # الخط
        font = QFont()
        font.setFamily("Amiri")
        font.setPointSize(12)
        self.setFont(font)

        # المحاذاة RTL
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # الستايل
        self.setStyleSheet("""
            QTreeWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 5px;
                outline: none;
            }

            QTreeWidget::item {
                padding: 8px;
                border-radius: 4px;
                margin: 2px 0;
            }

            QTreeWidget::item:hover {
                background-color: #e9ecef;
            }

            QTreeWidget::item:selected {
                background-color: #667eea;
                color: white;
            }

            QTreeWidget::item:selected:active {
                background-color: #5568d3;
            }

            QTreeWidget::branch {
                background-color: transparent;
            }

            QTreeWidget::branch:has-children:closed {
                image: url(resources/icons/arrow_left.png);
            }

            QTreeWidget::branch:has-children:open {
                image: url(resources/icons/arrow_down.png);
            }
        """)

    def _setup_connections(self):
        """إعداد الاتصالات والإشارات"""
        # عند النقر على عنصر
        self.itemClicked.connect(self._on_item_clicked)

        # عند التوسيع
        self.itemExpanded.connect(self._on_item_expanded)

        # عند الانهيار
        self.itemCollapsed.connect(self._on_item_collapsed)

        # التنقل بالكيبورد
        self.itemSelectionChanged.connect(self._on_selection_changed)

    def _load_initial_data(self):
        """تحميل البيانات الأولية"""
        self.clear()

        # إنشاء الفئات الرئيسية
        self._create_main_categories()

    def _create_main_categories(self):
        """إنشاء الفئات الرئيسية"""
        # فئة العرض
        display_category = SmartTreeItem(
            parent=None,
            item_type=TreeItemType.CATEGORY,
            data={'name': 'عرض', 'mode': 'display'}
        )
        display_category.setText(0, "📖 عرض")
        self.addTopLevelItem(display_category)

        # إضافة مصادر العرض
        self._add_display_sources(display_category)

        # فئة البحث
        search_category = SmartTreeItem(
            parent=None,
            item_type=TreeItemType.CATEGORY,
            data={'name': 'بحث', 'mode': 'search'}
        )
        search_category.setText(0, "🔍 بحث")
        self.addTopLevelItem(search_category)

        # إضافة مصادر البحث
        self._add_search_sources(search_category)

        # فئة الموضوعات
        topics_category = SmartTreeItem(
            parent=None,
            item_type=TreeItemType.CATEGORY,
            data={'name': 'موضوعات', 'mode': 'topics'}
        )
        topics_category.setText(0, "📚 موضوعات")
        self.addTopLevelItem(topics_category)

        # تحميل الموضوعات (Lazy Loading)
        # سيتم تحميلها عند التوسيع

        # توسيع الفئة الأولى افتراضياً
        display_category.setExpanded(True)

    def _add_display_sources(self, parent: SmartTreeItem):
        """إضافة مصادر العرض"""
        # القرآن الكريم
        quran_item = SmartTreeItem(
            parent=parent,
            item_type=TreeItemType.SOURCE,
            data={'name': 'القرآن الكريم', 'source_type': 'quran'}
        )
        quran_item.setText(0, "القرآن الكريم")

        # تحميل السور (Lazy Loading)
        # نضيف عنصر وهمي ليظهر السهم
        dummy = SmartTreeItem(parent=quran_item)
        dummy.setText(0, "جارٍ التحميل...")

        # التفاسير
        tafseer_item = SmartTreeItem(
            parent=parent,
            item_type=TreeItemType.SOURCE,
            data={'name': 'التفاسير', 'source_type': 'tafseer'}
        )
        tafseer_item.setText(0, "التفاسير")

        # الترجمات
        trans_item = SmartTreeItem(
            parent=parent,
            item_type=TreeItemType.SOURCE,
            data={'name': 'الترجمات', 'source_type': 'translations'}
        )
        trans_item.setText(0, "الترجمات")

        # علوم القرآن
        sciences_item = SmartTreeItem(
            parent=parent,
            item_type=TreeItemType.SOURCE,
            data={'name': 'علوم القرآن', 'source_type': 'sciences'}
        )
        sciences_item.setText(0, "علوم القرآن")

        # التدبرات
        tadabbur_item = SmartTreeItem(
            parent=parent,
            item_type=TreeItemType.SOURCE,
            data={'name': 'التدبرات', 'source_type': 'tadabbur'}
        )
        tadabbur_item.setText(0, "التدبرات")

    def _add_search_sources(self, parent: SmartTreeItem):
        """إضافة مصادر البحث"""
        sources = [
            ("البحث في كل شيء", "all"),
            ("البحث في القرآن", "quran"),
            ("البحث في التفاسير", "tafseer"),
            ("البحث في الترجمات", "translations"),
            ("البحث في الموضوعات", "topics"),
            ("البحث في الكلمات", "words"),
            ("البحث في الجذور", "roots"),
        ]

        for name, source_type in sources:
            item = SmartTreeItem(
                parent=parent,
                item_type=TreeItemType.SOURCE,
                data={'name': name, 'source_type': source_type, 'search_mode': True}
            )
            item.setText(0, name)

    # =====================================================
    # 🌳 إدارة الشجرة
    # =====================================================

    def _on_item_clicked(self, item: SmartTreeItem, column: int):
        """معالج النقر على عنصر"""
        if not isinstance(item, SmartTreeItem):
            return

        # إرسال البيانات
        data = {
            'type': item.item_type.value,
            'data': item.item_data
        }
        self.item_selected.emit(data)

        # حسب النوع
        if item.item_type == TreeItemType.VERSE:
            verse_id = item.get_data('verse_id')
            if verse_id:
                self.verse_selected.emit(verse_id)

        elif item.item_type == TreeItemType.SURAH:
            surah_id = item.get_data('surah_id')
            if surah_id:
                self.surah_selected.emit(surah_id)

        elif item.item_type == TreeItemType.TOPIC:
            topic_id = item.get_data('topic_id')
            if topic_id:
                self.topic_selected.emit(topic_id)

    def _on_item_expanded(self, item: SmartTreeItem):
        """معالج توسيع عنصر"""
        if not isinstance(item, SmartTreeItem):
            return

        # Lazy Loading: تحميل البيانات عند التوسيع
        if item.childCount() == 1 and item.child(0).text(0) == "جارٍ التحميل...":
            # حذف العنصر الوهمي
            item.takeChild(0)

            # تحميل البيانات
            self._load_item_children(item)

    def _on_item_collapsed(self, item: SmartTreeItem):
        """معالج انهيار عنصر"""
        pass

    def _on_selection_changed(self):
        """معالج تغيير الاختيار"""
        current = self.currentItem()
        if current and isinstance(current, SmartTreeItem):
            self._on_item_clicked(current, 0)

    def _load_item_children(self, item: SmartTreeItem):
        """تحميل أبناء عنصر (Lazy Loading)"""
        item_type = item.item_type
        source_type = item.get_data('source_type')

        # حسب النوع
        if item_type == TreeItemType.SOURCE and source_type == 'quran':
            self._load_surahs(item)

        elif item_type == TreeItemType.SURAH:
            self._load_verses(item)

        elif item_type == TreeItemType.CATEGORY and item.get_data('mode') == 'topics':
            self._load_topics(item)

        elif item_type in [TreeItemType.TOPIC_LEVEL_1, TreeItemType.TOPIC_LEVEL_2, TreeItemType.TOPIC_LEVEL_3]:
            self._load_topic_children(item)

    # =====================================================
    # 📖 تحميل البيانات
    # =====================================================

    def _load_surahs(self, parent: SmartTreeItem):
        """تحميل السور"""
        try:
            # جلب السور من قاعدة البيانات
            surahs = self.db.connection.execute("""
                SELECT surah_id, surah_name_arabic, verses_count, revelation_type
                FROM surahs
                ORDER BY surah_id
            """).fetchall()

            for surah in surahs:
                surah_item = SmartTreeItem(
                    parent=parent,
                    item_type=TreeItemType.SURAH,
                    data={
                        'surah_id': surah['surah_id'],
                        'name': surah['surah_name_arabic'],
                        'verses_count': surah['verses_count'],
                        'type': surah['revelation_type']
                    }
                )

                # النص المعروض
                text = f"{surah['surah_name_arabic']} ({surah['verses_count']})"
                surah_item.setText(0, text)

                # إضافة عنصر وهمي للآيات
                dummy = SmartTreeItem(parent=surah_item)
                dummy.setText(0, "جارٍ التحميل...")

        except Exception as e:
            print(f"❌ خطأ في تحميل السور: {e}")

    def _load_verses(self, parent: SmartTreeItem):
        """تحميل آيات سورة"""
        surah_id = parent.get_data('surah_id')
        if not surah_id:
            return

        try:
            verses = self.db.get_surah_verses(surah_id)

            for verse in verses:
                # اختصار النص للعرض (أول 7 كلمات)
                text = verse.get('text_othmani', '')
                words = text.split()[:7]
                display_text = ' '.join(words)
                if len(text.split()) > 7:
                    display_text += '...'

                verse_item = SmartTreeItem(
                    parent=parent,
                    item_type=TreeItemType.VERSE,
                    data={
                        'verse_id': verse['verse_id'],
                        'surah_id': verse['surah_id'],
                        'verse_number': verse['verse_number'],
                        'text': verse['text_othmani']
                    }
                )

                verse_item.setText(0, f"{verse['verse_number']}. {display_text}")

        except Exception as e:
            print(f"❌ خطأ في تحميل الآيات: {e}")

    def _load_topics(self, parent: SmartTreeItem):
        """تحميل الموضوعات الرئيسية"""
        try:
            topics = self.db.get_topics_tree(parent_id=None)

            for topic in topics:
                topic_item = SmartTreeItem(
                    parent=parent,
                    item_type=TreeItemType.TOPIC_LEVEL_1,
                    data={
                        'topic_id': topic['topic_id'],
                        'name': topic['topic_name'],
                        'level': topic['level']
                    }
                )

                topic_item.setText(0, topic['topic_name'])

                # إضافة عنصر وهمي إذا كان لديه أبناء
                if topic.get('children'):
                    dummy = SmartTreeItem(parent=topic_item)
                    dummy.setText(0, "جارٍ التحميل...")

        except Exception as e:
            print(f"❌ خطأ في تحميل الموضوعات: {e}")

    def _load_topic_children(self, parent: SmartTreeItem):
        """تحميل الموضوعات الفرعية"""
        topic_id = parent.get_data('topic_id')
        level = parent.get_data('level', 1)

        if not topic_id:
            return

        try:
            children = self.db.get_topics_tree(parent_id=topic_id)

            # تحديد نوع العنصر حسب المستوى
            if level == 1:
                child_type = TreeItemType.TOPIC_LEVEL_2
            elif level == 2:
                child_type = TreeItemType.TOPIC_LEVEL_3
            else:
                child_type = TreeItemType.TOPIC

            for child in children:
                child_item = SmartTreeItem(
                    parent=parent,
                    item_type=child_type,
                    data={
                        'topic_id': child['topic_id'],
                        'name': child['topic_name'],
                        'level': child['level']
                    }
                )

                child_item.setText(0, child['topic_name'])

                # إضافة عنصر وهمي إذا كان لديه أبناء
                if child.get('children'):
                    dummy = SmartTreeItem(parent=child_item)
                    dummy.setText(0, "جارٍ التحميل...")

        except Exception as e:
            print(f"❌ خطأ في تحميل الموضوعات الفرعية: {e}")

    # =====================================================
    # 🔍 تحديث من البحث
    # =====================================================

    def update_from_search(self, results: Dict[str, Any], query: str):
        """
        تحديث الشجرة من نتائج البحث

        Args:
            results: نتائج البحث
            query: نص البحث
        """
        self.clear()

        # إنشاء عقدة النتائج
        results_root = SmartTreeItem(
            parent=None,
            item_type=TreeItemType.CATEGORY,
            data={'name': f'نتائج البحث: {query}', 'query': query}
        )
        results_root.setText(0, f"🔍 نتائج البحث: \"{query}\"")
        self.addTopLevelItem(results_root)
        results_root.setExpanded(True)

        # عرض النتائج حسب النوع
        total = results.get('total', 0)

        # نتائج القرآن
        quran_results = results.get('quran', [])
        if quran_results:
            quran_node = SmartTreeItem(
                parent=results_root,
                item_type=TreeItemType.SOURCE,
                data={'name': f'القرآن ({len(quran_results)})', 'source_type': 'quran'}
            )
            quran_node.setText(0, f"📖 القرآن الكريم ({len(quran_results)} آية)")
            quran_node.setExpanded(True)

            for verse in quran_results:
                verse_item = self._create_verse_item(verse, quran_node)

        # نتائج التفاسير
        tafseer_results = results.get('tafseer', [])
        if tafseer_results:
            tafseer_node = SmartTreeItem(
                parent=results_root,
                item_type=TreeItemType.SOURCE,
                data={'name': f'التفاسير ({len(tafseer_results)})', 'source_type': 'tafseer'}
            )
            tafseer_node.setText(0, f"📚 التفاسير ({len(tafseer_results)} نتيجة)")
            tafseer_node.setExpanded(True)

            for tafseer in tafseer_results:
                tafseer_item = self._create_tafseer_item(tafseer, tafseer_node)

        # نتائج الموضوعات
        topics_results = results.get('topics', [])
        if topics_results:
            topics_node = SmartTreeItem(
                parent=results_root,
                item_type=TreeItemType.SOURCE,
                data={'name': f'الموضوعات ({len(topics_results)})', 'source_type': 'topics'}
            )
            topics_node.setText(0, f"📑 الموضوعات ({len(topics_results)})")
            topics_node.setExpanded(True)

            for topic in topics_results:
                topic_item = self._create_topic_item(topic, topics_node)

        # إذا لم تكن هناك نتائج
        if total == 0:
            no_results = SmartTreeItem(parent=results_root)
            no_results.setText(0, "لا توجد نتائج")
            no_results.setForeground(0, QBrush(QColor("#999")))

    def _create_verse_item(self, verse: Dict, parent: SmartTreeItem) -> SmartTreeItem:
        """إنشاء عنصر آية"""
        # اختصار النص
        text = verse.get('text_othmani', '')
        words = text.split()[:7]
        display_text = ' '.join(words)
        if len(text.split()) > 7:
            display_text += '...'

        verse_item = SmartTreeItem(
            parent=parent,
            item_type=TreeItemType.VERSE,
            data=verse
        )

        surah_name = verse.get('surah_name_arabic', '')
        verse_num = verse.get('verse_number', '')

        verse_item.setText(0, f"[{surah_name}: {verse_num}] {display_text}")

        return verse_item

    def _create_tafseer_item(self, tafseer: Dict, parent: SmartTreeItem) -> SmartTreeItem:
        """إنشاء عنصر تفسير"""
        text = tafseer.get('tafseer_text', '')
        preview = text[:50] + '...' if len(text) > 50 else text

        tafseer_item = SmartTreeItem(
            parent=parent,
            item_type=TreeItemType.SEARCH_RESULT,
            data=tafseer
        )

        book_name = tafseer.get('book_name_arabic', '')
        surah_name = tafseer.get('surah_name_arabic', '')
        verse_num = tafseer.get('verse_number', '')

        tafseer_item.setText(0, f"[{book_name}] {surah_name}: {verse_num} - {preview}")

        return tafseer_item

    def _create_topic_item(self, topic: Dict, parent: SmartTreeItem) -> SmartTreeItem:
        """إنشاء عنصر موضوع"""
        topic_item = SmartTreeItem(
            parent=parent,
            item_type=TreeItemType.TOPIC,
            data=topic
        )

        topic_item.setText(0, topic.get('topic_name', ''))

        return topic_item

    # =====================================================
    # 🎨 التنقل والتحكم
    # =====================================================

    def navigate_next(self):
        """الانتقال إلى العنصر التالي"""
        current = self.currentItem()
        if not current:
            # اختيار أول عنصر
            if self.topLevelItemCount() > 0:
                self.setCurrentItem(self.topLevelItem(0))
            return

        # البحث عن العنصر التالي
        next_item = self._get_next_item(current)
        if next_item:
            self.setCurrentItem(next_item)
            self.scrollToItem(next_item)

    def navigate_previous(self):
        """الانتقال إلى العنصر السابق"""
        current = self.currentItem()
        if not current:
            return

        # البحث عن العنصر السابق
        prev_item = self._get_previous_item(current)
        if prev_item:
            self.setCurrentItem(prev_item)
            self.scrollToItem(prev_item)

    def _get_next_item(self, item: QTreeWidgetItem) -> Optional[QTreeWidgetItem]:
        """جلب العنصر التالي"""
        # إذا كان موسعاً وله أبناء
        if item.isExpanded() and item.childCount() > 0:
            return item.child(0)

        # البحث في الأخوة
        parent = item.parent()
        if parent:
            index = parent.indexOfChild(item)
            if index < parent.childCount() - 1:
                return parent.child(index + 1)
            else:
                # البحث في مستوى الأب
                return self._get_next_item(parent)
        else:
            # مستوى أعلى
            index = self.indexOfTopLevelItem(item)
            if index < self.topLevelItemCount() - 1:
                return self.topLevelItem(index + 1)

        return None

    def _get_previous_item(self, item: QTreeWidgetItem) -> Optional[QTreeWidgetItem]:
        """جلب العنصر السابق"""
        parent = item.parent()

        if parent:
            index = parent.indexOfChild(item)
            if index > 0:
                # الأخ السابق
                prev = parent.child(index - 1)
                # الذهاب إلى آخر طفل
                while prev.isExpanded() and prev.childCount() > 0:
                    prev = prev.child(prev.childCount() - 1)
                return prev
            else:
                return parent
        else:
            index = self.indexOfTopLevelItem(item)
            if index > 0:
                prev = self.topLevelItem(index - 1)
                while prev.isExpanded() and prev.childCount() > 0:
                    prev = prev.child(prev.childCount() - 1)
                return prev

        return None

    def expand_all_results(self):
        """توسيع كل النتائج"""
        self.expandAll()

    def collapse_all_results(self):
        """طي كل النتائج"""
        self.collapseAll()

    # =====================================================
    # 🛠️ وظائف مساعدة
    # =====================================================

    def clear_tree(self):
        """مسح الشجرة"""
        self.clear()
        self.cache.clear()
        self._create_main_categories()

    def refresh_tree(self):
        """تحديث الشجرة"""
        self.clear_tree()


# =====================================================
# 🧪 اختبار سريع
# =====================================================

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    # محاكاة مدير قاعدة البيانات
    class MockDB:
        def __init__(self):
            self.connection = None

        def get_surah_verses(self, surah_id):
            return []

        def get_topics_tree(self, parent_id=None):
            return []

    tree = SmartSearchTree(MockDB())
    tree.resize(400, 600)
    tree.show()

    sys.exit(app.exec())

# 📘 دليل الدمج السريع - نظام البحث الذكي

## نظرة سريعة

هذا الدليل يشرح كيفية دمج نظام البحث الذكي في تطبيق دُحى TV الحالي بثلاث خطوات بسيطة.

---

## 🎯 خطوات الدمج السريع

### الخطوة 1: التحقق من الملفات

تأكد من وجود المجلدات التالية:

```
duhatv/
├── src/
│   ├── database/
│   │   └── neural_database.py         ✅
│   ├── widgets/
│   │   └── smart_search_tree.py       ✅
│   ├── search/
│   │   └── smart_search_engine.py     ✅
│   └── windows/
│       └── smart_search_window.py     ✅
└── database/
    └── smart_search_schema.sql        ✅
```

### الخطوة 2: إضافة زر في الواجهة الرئيسية

في ملف `main_window.py` أو `duhatv.py`:

```python
# في قسم الاستيرادات
from src.windows.smart_search_window import SmartSearchWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ... الكود الموجود ...

        # إضافة زر البحث الذكي
        self.smart_search_btn = QPushButton("🔍 البحث الذكي")
        self.smart_search_btn.clicked.connect(self.open_smart_search)

        # أو إضافة في القائمة
        search_action = QAction("البحث الذكي", self)
        search_action.setShortcut("Ctrl+F")
        search_action.triggered.connect(self.open_smart_search)

        # إضافة للقائمة
        search_menu = self.menuBar().addMenu("بحث")
        search_menu.addAction(search_action)

    def open_smart_search(self):
        """فتح نافذة البحث الذكي"""
        if not hasattr(self, 'search_window') or self.search_window is None:
            self.search_window = SmartSearchWindow(parent=self)

        self.search_window.show()
        self.search_window.raise_()
        self.search_window.activateWindow()
```

### الخطوة 3: إنشاء قاعدة البيانات

```bash
# قم بتشغيل هذا الأمر مرة واحدة
python -c "from src.database.neural_database import NeuralDatabase; db = NeuralDatabase('data/duhatv.db'); print('✅ تم إنشاء قاعدة البيانات')"
```

**أو** استخدم السكريبت التالي:

```python
# create_database.py
from src.database.neural_database import NeuralDatabase

db = NeuralDatabase("data/duhatv.db")
print("✅ تم إنشاء قاعدة البيانات بنجاح")

# اختبار
stats = db.get_database_stats()
print(f"📊 الإحصائيات: {stats}")

db.close()
```

---

## 🎨 خيارات الدمج المتقدمة

### الخيار 1: كتاب منفصل في التطبيق الرئيسي

```python
# دمج كتاب في QTabWidget الموجود
from src.search.smart_search_engine import SmartSearchEngine
from src.widgets.smart_search_tree import SmartSearchTree
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter

class SmartSearchTab(QWidget):
    """تاب البحث الذكي"""

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # محرك البحث
        self.search_engine = SmartSearchEngine(db_manager)
        layout.addWidget(self.search_engine)

        # Splitter: شجرة + عرض
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # منطقة العرض
        self.display = QTextBrowser()

        # الشجرة
        self.tree = SmartSearchTree(db_manager)

        splitter.addWidget(self.display)
        splitter.addWidget(self.tree)
        splitter.setSizes([700, 300])

        layout.addWidget(splitter)

        # الاتصالات
        self.tree.verse_selected.connect(self.show_verse)
        self.search_engine.results_ready.connect(self.update_tree)

    def show_verse(self, verse_id):
        """عرض آية"""
        # ... الكود ...
        pass

    def update_tree(self, results):
        """تحديث الشجرة"""
        query = self.search_engine.get_search_text()
        self.tree.update_from_search(results, query)

# في main_window.py
search_tab = SmartSearchTab(self.db)
self.tabs.addTab(search_tab, "🔍 البحث الذكي")
```

### الخيار 2: مشاركة قاعدة البيانات

إذا كان لديك قاعدة بيانات موجودة:

```python
# في main_window.py
from src.database.neural_database import NeuralDatabase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # إنشاء أو الاتصال بقاعدة البيانات
        self.db = NeuralDatabase("data/duhatv.db")

        # مشاركتها مع المكونات الأخرى
        self.search_window = SmartSearchWindow(parent=self)
        self.search_window.db = self.db  # استخدام نفس الاتصال
```

### الخيار 3: استخدام المكونات الفردية

يمكنك استخدام أي مكون بشكل منفصل:

```python
# استخدام محرك البحث فقط
from src.search.smart_search_engine import SmartSearchEngine

search_engine = SmartSearchEngine(db_manager)
search_engine.results_ready.connect(self.handle_results)

# استخدام الشجرة فقط
from src.widgets.smart_search_tree import SmartSearchTree

tree = SmartSearchTree(db_manager)
tree.verse_selected.connect(self.show_verse)

# استخدام قاعدة البيانات فقط
from src.database.neural_database import NeuralDatabase

db = NeuralDatabase()
results = db.search_quran("الحمد", limit=50)
```

---

## 🔧 التخصيص

### تخصيص الألوان لتتناسب مع التطبيق

```python
# في smart_search_window.py
# غيّر الألوان في الـ StyleSheet

MAIN_COLOR = "#YOUR_PRIMARY_COLOR"
SECONDARY_COLOR = "#YOUR_SECONDARY_COLOR"

stylesheet = f"""
    QTreeWidget::item:selected {{
        background-color: {MAIN_COLOR};
        color: white;
    }}

    QPushButton {{
        background-color: {SECONDARY_COLOR};
    }}
"""
```

### استخدام نفس الخطوط

```python
# في smart_search_window.py
from PyQt6.QtGui import QFont

# استخدم نفس خطوط التطبيق الرئيسي
MAIN_FONT = QFont("Amiri", 14)  # خط التطبيق الرئيسي

self.quran_display.setFont(MAIN_FONT)
```

---

## 📊 استيراد البيانات

### استيراد السور

```python
from src.database.neural_database import NeuralDatabase

db = NeuralDatabase()

# بيانات السور (مثال)
surahs_data = [
    (1, "الفاتحة", "Al-Fatihah", "مكية", 7),
    (2, "البقرة", "Al-Baqarah", "مدنية", 286),
    # ... باقي السور
]

with db.transaction() as conn:
    conn.executemany("""
        INSERT OR REPLACE INTO surahs
        (surah_id, surah_name_arabic, surah_name_english, revelation_type, verses_count)
        VALUES (?, ?, ?, ?, ?)
    """, surahs_data)

print("✅ تم استيراد السور")
```

### استيراد الآيات

```python
# من ملف CSV أو JSON
import json

with open("data/quran_verses.json", "r", encoding="utf-8") as f:
    verses = json.load(f)

with db.transaction() as conn:
    for verse in verses:
        conn.execute("""
            INSERT INTO verses
            (surah_id, verse_number, text_othmani, text_simplified)
            VALUES (?, ?, ?, ?)
        """, (
            verse['surah_id'],
            verse['verse_number'],
            verse['text'],
            remove_tashkeel(verse['text'])
        ))

print(f"✅ تم استيراد {len(verses)} آية")
```

### استيراد التفاسير

```python
# استيراد من قاعدة البيانات الحالية
import sqlite3

# الاتصال بقاعدة البيانات القديمة
old_db = sqlite3.connect("data/old_tafseer.db")
old_cursor = old_db.cursor()

# جلب التفاسير
tafseer_data = old_cursor.execute("""
    SELECT book_id, verse_id, tafseer_text
    FROM tafseer
""").fetchall()

# إدخالها في القاعدة الجديدة
with db.transaction() as conn:
    conn.executemany("""
        INSERT INTO tafseer_texts (book_id, verse_id, tafseer_text)
        VALUES (?, ?, ?)
    """, tafseer_data)

print(f"✅ تم استيراد {len(tafseer_data)} تفسير")
```

---

## ✅ قائمة التحقق

### قبل الدمج
- [ ] نسخ المجلدات المطلوبة
- [ ] تثبيت المتطلبات: `pip install -r requirements_smart_search.txt`
- [ ] إنشاء قاعدة البيانات
- [ ] اختبار التشغيل المستقل: `python src/main_smart_search.py`

### أثناء الدمج
- [ ] إضافة زر/قائمة في الواجهة الرئيسية
- [ ] اختبار فتح النافذة
- [ ] اختبار البحث الأساسي
- [ ] اختبار الفلاتر
- [ ] اختبار الشجرة

### بعد الدمج
- [ ] استيراد كل البيانات (سور، آيات، تفاسير)
- [ ] اختبار الأداء (< 100ms)
- [ ] اختبار مع بيانات حقيقية
- [ ] تخصيص الألوان والخطوط
- [ ] اختبار نهائي شامل

---

## 🐛 استكشاف أخطاء الدمج

### المشكلة: "ModuleNotFoundError"

**السبب:** المسارات غير صحيحة

**الحل:**
```python
import sys
from pathlib import Path

# إضافة المسار
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))
```

### المشكلة: قاعدة البيانات فارغة

**السبب:** لم يتم استيراد البيانات

**الحل:**
```python
# تحقق من وجود البيانات
stats = db.get_database_stats()
print(stats)

# إذا كانت فارغة، استورد البيانات
# راجع قسم "استيراد البيانات" أعلاه
```

### المشكلة: البحث لا يعمل

**السبب:** جداول FTS5 فارغة

**الحل:**
```python
# ملء جداول FTS5
with db.transaction() as conn:
    # نسخ من الجدول الأساسي إلى FTS
    conn.execute("""
        INSERT INTO quran_fts (verse_id, surah_id, verse_number, text_othmani, text_no_tashkeel, text_simplified)
        SELECT verse_id, surah_id, verse_number, text_othmani, text_othmani_no_tashkeel, text_simplified
        FROM verses
    """)
```

### المشكلة: النافذة لا تفتح

**السبب:** خطأ في الاستيراد أو التهيئة

**الحل:**
```python
# تحقق من الأخطاء
try:
    search_window = SmartSearchWindow(parent=self)
    search_window.show()
except Exception as e:
    print(f"خطأ: {e}")
    import traceback
    traceback.print_exc()
```

---

## 📞 الدعم الفني

إذا واجهت أي مشكلة:

1. **تحقق من السجلات (Logs)**
2. **استخدم `print()` للتتبع**
3. **راجع الأمثلة في هذا الدليل**
4. **راجع [README](SMART_SEARCH_README.md) للتفاصيل**

---

## 🎉 بعد الدمج الناجح

بمجرد الدمج، ستحصل على:

✅ **بحث فوري وذكي**
- بحث في القرآن بمجرد كتابة حرف
- فلاتر ديناميكية متعددة
- نتائج في أقل من 100ms

✅ **شجرة ديناميكية**
- عرض منظم لكل المحتوى
- تنقل سريع بالكيبورد
- Lazy Loading للأداء

✅ **ربط عصبي**
- كل آية مرتبطة بتفاسيرها وترجماتها
- آيات مرتبطة بموضوعاتها
- علاقات ذكية بين العناصر

✅ **أداء عالي**
- FTS5 للبحث السريع
- فهارس متعددة
- تخزين مؤقت ذكي

---

**🌟 مبروك! نظام البحث الذكي جاهز للاستخدام في تطبيق دُحى TV**

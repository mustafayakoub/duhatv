# 🔍 نظام البحث الذكي - دُحى TV

## نظرة عامة

نظام بحث ذكي ومتقدم يجمع بين:
- ⚡ **السرعة**: بحث فوري في أقل من 100ms
- 🧠 **الذكاء**: ربط عصبي بين جميع العناصر
- 🎨 **البساطة**: واجهة شجرية بديهية
- 🌊 **العمق**: بيانات ضخمة ومترابطة

---

## 📁 هيكل المشروع

```
duhatv/
├── database/
│   └── smart_search_schema.sql          # مخطط قاعدة البيانات
├── src/
│   ├── database/
│   │   └── neural_database.py           # محرك قاعدة البيانات العصبية
│   ├── widgets/
│   │   └── smart_search_tree.py         # الشجرة الديناميكية
│   ├── search/
│   │   └── smart_search_engine.py       # محرك البحث الذكي
│   ├── windows/
│   │   └── smart_search_window.py       # النافذة الرئيسية
│   └── main_smart_search.py             # نقطة التشغيل
├── SMART_SEARCH_ARCHITECTURE.md         # المخطط المعماري
└── SMART_SEARCH_README.md               # هذا الملف
```

---

## 🚀 التشغيل السريع

### 1. المتطلبات

```bash
# Python 3.8+
pip install PyQt6
```

### 2. التشغيل المستقل

```bash
python src/main_smart_search.py
```

### 3. الدمج في التطبيق الرئيسي

```python
from src.windows.smart_search_window import SmartSearchWindow

# في التطبيق الرئيسي
search_window = SmartSearchWindow(parent=self)
search_window.show()
```

---

## 🏗️ المكونات الأساسية

### 1. قاعدة البيانات العصبية

```python
from src.database.neural_database import NeuralDatabase

# إنشاء اتصال
db = NeuralDatabase("data/duhatv.db")

# البحث في القرآن
results = db.search_quran("الحمد", limit=50)

# البحث الشامل
all_results = db.search_all("الإيمان", filters={'quran': True, 'tafseer': True})

# جلب البيانات المرتبطة بآية
linked_data = db.get_linked_data(verse_id=1)
```

**المميزات:**
- ✅ FTS5 للبحث النصي السريع
- ✅ فهارس متعددة للأداء العالي
- ✅ Lazy Loading للبيانات الكبيرة
- ✅ LRU Cache للنتائج الشائعة
- ✅ Thread-safe connections

---

### 2. الشجرة الديناميكية

```python
from src.widgets.smart_search_tree import SmartSearchTree

tree = SmartSearchTree(db_manager)

# الإشارات
tree.verse_selected.connect(on_verse_selected)
tree.surah_selected.connect(on_surah_selected)
tree.topic_selected.connect(on_topic_selected)

# تحديث من نتائج البحث
tree.update_from_search(search_results, query)

# التنقل
tree.navigate_next()
tree.navigate_previous()
```

**المميزات:**
- ✅ تحديث ديناميكي
- ✅ Lazy Loading للأداء
- ✅ التنقل بالكيبورد
- ✅ ألوان وأيقونات مميزة
- ✅ RTL Support

---

### 3. محرك البحث الذكي

```python
from src.search.smart_search_engine import SmartSearchEngine

engine = SmartSearchEngine(db_manager)

# الإشارات
engine.results_ready.connect(on_results_ready)
engine.filter_added.connect(on_filter_added)

# إضافة فلتر
engine.add_filter(
    filter_type=FilterType.SOURCE,
    filter_value="quran",
    display_name="القرآن الكريم"
)

# البحث
engine.set_search_text("الحمد")
```

**المميزات:**
- ✅ بحث فوري (< 100ms)
- ✅ Autocomplete ذكي
- ✅ فلاتر ديناميكية (Chips)
- ✅ Worker Thread منفصل
- ✅ إحصائيات الأداء

---

### 4. النافذة الرئيسية

```python
from src.windows.smart_search_window import SmartSearchWindow

window = SmartSearchWindow()
window.show()
```

**المكونات:**
- 🔍 محرك البحث (أعلى)
- 🌳 الشجرة الديناميكية (يمين)
- 📄 منطقة العرض (وسط)
- 📊 شريط الإحصائيات (أسفل)

---

## 📊 نماذج الاستخدام

### مثال 1: البحث البسيط

```python
# البحث عن كلمة "الحمد"
db = NeuralDatabase()
results = db.search_quran("الحمد", limit=50)

for verse in results:
    print(f"{verse['surah_name_arabic']}: {verse['verse_number']}")
    print(verse['text_othmani'])
    print("-" * 50)
```

### مثال 2: البحث مع الفلاتر

```python
# البحث في التفاسير المحددة
results = db.search_tafseer(
    "الإيمان",
    book_ids=[1, 2, 3],  # الطبري، ابن كثير، القرطبي
    limit=50
)
```

### مثال 3: الربط العصبي

```python
# جلب كل البيانات المرتبطة بآية
linked_data = db.get_linked_data(verse_id=1)

print("الآية:", linked_data['verse']['text_othmani'])
print("عدد التفاسير:", len(linked_data['tafseer']))
print("عدد الترجمات:", len(linked_data['translations']))
print("الموضوعات:", [t['topic_name'] for t in linked_data['topics']])
```

### مثال 4: شجرة الموضوعات

```python
# جلب شجرة الموضوعات
topics_tree = db.get_topics_tree(parent_id=None)

def print_tree(topics, level=0):
    for topic in topics:
        print("  " * level + topic['topic_name'])
        if topic.get('children'):
            print_tree(topic['children'], level + 1)

print_tree(topics_tree)
```

---

## 🎯 الدمج في التطبيق الرئيسي

### الطريقة 1: كنافذة منفصلة

```python
# في main_window.py
from src.windows.smart_search_window import SmartSearchWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.search_window = None

    def open_smart_search(self):
        if not self.search_window:
            self.search_window = SmartSearchWindow(parent=self)
        self.search_window.show()
        self.search_window.raise_()
        self.search_window.activateWindow()
```

### الطريقة 2: كـ Widget مدمج

```python
# دمج في تاب
from src.search.smart_search_engine import SmartSearchEngine
from src.widgets.smart_search_tree import SmartSearchTree

search_tab = QWidget()
layout = QVBoxLayout(search_tab)

engine = SmartSearchEngine(self.db)
tree = SmartSearchTree(self.db)

layout.addWidget(engine)
layout.addWidget(tree)

self.tabs.addTab(search_tab, "🔍 البحث الذكي")
```

### الطريقة 3: مشاركة قاعدة البيانات

```python
# استخدام قاعدة البيانات الموجودة
from src.database.neural_database import NeuralDatabase

# في التطبيق الرئيسي
self.db = NeuralDatabase("data/duhatv.db")

# مشاركتها مع نافذة البحث
search_window = SmartSearchWindow(parent=self)
search_window.db = self.db  # استخدام نفس قاعدة البيانات
```

---

## ⚡ تحسين الأداء

### 1. الفهرسة

```sql
-- تأكد من وجود الفهارس المهمة
CREATE INDEX IF NOT EXISTS idx_verses_surah ON verses(surah_id);
CREATE INDEX IF NOT EXISTS idx_words_root ON words(root);
CREATE INDEX IF NOT EXISTS idx_neural_source ON neural_links(source_type, source_id);
```

### 2. التخزين المؤقت

```python
# استخدام LRU Cache
from functools import lru_cache

@lru_cache(maxsize=500)
def get_verse(self, verse_id):
    return self.db.get_verse(verse_id)
```

### 3. Lazy Loading

```python
# تحميل البيانات عند الحاجة فقط
if item.childCount() == 1 and item.child(0).text(0) == "جارٍ التحميل...":
    self._load_item_children(item)
```

### 4. Worker Thread

```python
# البحث في thread منفصل
self.search_worker.moveToThread(self.search_thread)
self.search_worker.search(query, filters)
```

---

## 🔧 التخصيص

### 1. تخصيص الألوان

```python
# في smart_search_tree.py
self.setStyleSheet("""
    QTreeWidget::item:selected {
        background-color: #YOUR_COLOR;
        color: white;
    }
""")
```

### 2. تخصيص الخطوط

```python
# في display_area.py
self.quran_display.setFont(QFont("Amiri", 18))  # خط مخصص
```

### 3. إضافة فلاتر جديدة

```python
# في smart_search_engine.py
class FilterType(Enum):
    # أضف أنواع جديدة
    CUSTOM_FILTER = "custom"

# إضافة زر فلتر
self._add_quick_filter(layout, "فلتر مخصص", FilterType.CUSTOM_FILTER, "value")
```

### 4. إضافة مصادر بيانات جديدة

```python
# في neural_database.py
def search_custom_source(self, query, limit=100):
    """بحث في مصدر مخصص"""
    # تنفيذ البحث
    pass
```

---

## 📈 الإحصائيات والمراقبة

### 1. إحصائيات البحث

```python
stats = engine.get_stats()
print(f"عدد عمليات البحث: {stats['total_searches']}")
print(f"متوسط الوقت: {stats['avg_time']*1000:.1f}ms")
```

### 2. إحصائيات قاعدة البيانات

```python
db_stats = db.get_database_stats()
print(f"عدد الآيات: {db_stats['total_verses']}")
print(f"عدد الكلمات: {db_stats['total_words']}")
print(f"عدد الروابط العصبية: {db_stats['total_links']}")
```

### 3. مراقبة الأداء

```python
import time

start = time.time()
results = db.search_quran("الحمد", limit=100)
elapsed = time.time() - start

print(f"⏱️ وقت البحث: {elapsed*1000:.1f}ms")
print(f"📊 عدد النتائج: {len(results)}")
```

---

## 🐛 استكشاف الأخطاء

### مشكلة: البحث بطيء

**الحل:**
1. تأكد من وجود الفهارس:
```sql
-- فحص الفهارس
SELECT name FROM sqlite_master WHERE type='index';
```

2. تفعيل WAL mode:
```python
conn.execute("PRAGMA journal_mode = WAL")
```

3. زيادة حجم الـ cache:
```python
conn.execute("PRAGMA cache_size = -128000")  # 128MB
```

### مشكلة: الشجرة لا تتحدث

**الحل:**
```python
# تأكد من ربط الإشارات
tree.verse_selected.connect(self.on_verse_selected)

# تأكد من تنفيذ المعالج
@pyqtSlot(int)
def on_verse_selected(self, verse_id):
    print(f"تم اختيار الآية: {verse_id}")
```

### مشكلة: الفلاتر لا تعمل

**الحل:**
```python
# تأكد من تطبيق الفلاتر في البحث
filters_dict = self._filters_to_dict(self.active_filters)
results = self.db.search_all(query, filters_dict)
```

---

## 📚 مصادر إضافية

- [المخطط المعماري الكامل](SMART_SEARCH_ARCHITECTURE.md)
- [مخطط قاعدة البيانات](database/smart_search_schema.sql)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [SQLite FTS5 Documentation](https://www.sqlite.org/fts5.html)

---

## 🎓 أمثلة متقدمة

### مثال 1: بناء سلسلة فلاتر معقدة

```python
engine = SmartSearchEngine(db)

# فلتر المصدر
engine.add_filter(FilterType.SOURCE, "quran", "القرآن الكريم")

# فلتر السورة
engine.add_filter(FilterType.SURAH, 2, "سورة البقرة")

# فلتر النحو
engine.add_filter(FilterType.GRAMMAR, "noun", "اسم")

# البحث مع كل الفلاتر
engine.set_search_text("الإيمان")
```

### مثال 2: إنشاء روابط عصبية

```python
# ربط آية بآية أخرى
db.add_neural_link(
    source_type="verse",
    source_id=1,
    target_type="verse",
    target_id=285,
    relation_type="similar",
    weight=0.9,
    metadata={"reason": "موضوع مشترك"}
)

# جلب الآيات المرتبطة
related = db.get_neural_links("verse", 1, target_type="verse")
```

### مثال 3: استخراج إحصائيات متقدمة

```python
# الكلمات الأكثر تكراراً
cursor = db.connection.execute("""
    SELECT word_no_tashkeel, COUNT(*) as count
    FROM words
    GROUP BY word_no_tashkeel
    ORDER BY count DESC
    LIMIT 10
""")

for word, count in cursor.fetchall():
    print(f"{word}: {count} مرة")
```

---

## ✅ قائمة التحقق للدمج

- [ ] تثبيت المتطلبات: `pip install PyQt6`
- [ ] نسخ المجلدات: `src/database`, `src/widgets`, `src/search`, `src/windows`
- [ ] إنشاء قاعدة البيانات من `smart_search_schema.sql`
- [ ] استيراد البيانات الأساسية (السور، الموضوعات، إلخ)
- [ ] اختبار البحث الأساسي
- [ ] اختبار الشجرة الديناميكية
- [ ] اختبار الفلاتر
- [ ] اختبار الربط العصبي
- [ ] اختبار الأداء (< 100ms)
- [ ] دمج في التطبيق الرئيسي
- [ ] اختبار النهائي الشامل

---

## 🎉 النتيجة النهائية

بعد الدمج الكامل، ستحصل على:

✨ **نظام بحث ذكي يجمع بين:**
- ⚡ سرعة Everything
- 🧠 ذكاء الباحث القرآني
- 🎨 سهولة Windows Explorer
- 🌊 عمق قاعدة بيانات عصبية

**بسيط في الظاهر، عميق في الباطن**

---

## 📞 الدعم والمساعدة

للمساعدة والدعم:
- راجع [المخطط المعماري](SMART_SEARCH_ARCHITECTURE.md)
- افحص أمثلة الكود أعلاه
- استخدم `print()` للتتبع
- تأكد من الإشارات والمعالجات

---

## 🚀 الخطوات التالية

1. **ملء قاعدة البيانات**: استيراد كل بيانات القرآن والتفاسير
2. **بناء الروابط العصبية**: إنشاء علاقات بين الآيات والموضوعات
3. **التحسين**: قياس الأداء وتحسين الفهارس
4. **الاختبار**: اختبار شامل مع مستخدمين حقيقيين
5. **التوثيق**: توثيق API للمطورين

---

**🌟 صُمّم بعناية لدُحى TV - نظام بحث ذكي بعمق البحر وسرعة البرق**

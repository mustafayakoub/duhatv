# 🏗️ المعمارية الشاملة لنظام البحث الذكي - دُحى TV

## 📊 نظرة عامة

نظام بحث ذكي وفوري ومتقدم يجمع بين:
- **سرعة Everything**: بحث فوري بمجرد كتابة حرف
- **ذكاء الباحث القرآني**: فلاتر متعددة وديناميكية
- **سهولة Windows Explorer**: واجهة شجرية بديهية
- **عمق البيانات**: ربط عصبي بين جميع العناصر

---

## 🎯 المتطلبات الأساسية

### 1. السرعة والأداء
- ⚡ بحث فوري: نتائج في أقل من 100ms
- 🚀 فهرسة ذكية: FTS5 + Trigram Indexing
- 💾 تخزين مؤقت: LRU Cache للنتائج الشائعة
- 🔄 تحديث ديناميكي: بدون إعادة تحميل

### 2. الربط العصبي
```
رقم_الآية ─┐
             ├─→ [محرك الربط العصبي] ─→ كل النوافذ
رقم_السورة ─┤
رقم_الكلمة ─┤
رقم_الصفحة ─┘
```

### 3. مصادر البيانات
- القرآن الكريم (9 رسوم مختلفة)
- التفاسير (50+ كتاب)
- الترجمات (30+ لغة)
- علوم القرآن
- التدبرات
- الموضوعات القرآنية
- السور والآيات
- الكلمات والجذور
- الحروف والإعراب

---

## 🗄️ معمارية قاعدة البيانات

### البنية الأساسية

```
┌─────────────────────────────────────────────┐
│         قاعدة البيانات الرئيسية            │
│              (duhatv.db)                    │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │  quran_text  │  │ quran_index  │        │
│  │  (9 رسوم)    │  │   (FTS5)     │        │
│  └──────────────┘  └──────────────┘        │
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │   tafseer    │  │tafseer_index │        │
│  │  (50 كتاب)   │  │   (FTS5)     │        │
│  └──────────────┘  └──────────────┘        │
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ translations │  │  topics      │        │
│  └──────────────┘  └──────────────┘        │
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │    words     │  │   grammar    │        │
│  │  (الجذور)    │  │  (الإعراب)   │        │
│  └──────────────┘  └──────────────┘        │
│                                             │
└─────────────────────────────────────────────┘
```

### جداول FTS5 للبحث السريع

```sql
-- 1. فهرس القرآن الكريم
CREATE VIRTUAL TABLE quran_fts USING fts5(
    verse_text,          -- نص الآية
    verse_no_tashkeel,   -- بدون تشكيل
    verse_simplified,    -- مبسط للبحث
    surah_id,           -- رقم السورة
    verse_id,           -- رقم الآية
    tokenize = 'unicode61 remove_diacritics 2'
);

-- 2. فهرس الكلمات والجذور
CREATE VIRTUAL TABLE words_fts USING fts5(
    word_text,          -- الكلمة
    root,               -- الجذر
    stem,               -- الجذع
    word_no_tashkeel,   -- بدون تشكيل
    tokenize = 'trigram'
);

-- 3. فهرس التفاسير
CREATE VIRTUAL TABLE tafseer_fts USING fts5(
    tafseer_text,       -- نص التفسير
    book_id,            -- رقم الكتاب
    verse_id,           -- رقم الآية
    tokenize = 'unicode61'
);
```

### جدول الربط العصبي

```sql
-- جدول الروابط المتقاطعة
CREATE TABLE neural_links (
    id INTEGER PRIMARY KEY,
    source_type TEXT,        -- نوع المصدر (verse, word, topic)
    source_id INTEGER,       -- رقم المصدر
    target_type TEXT,        -- نوع الهدف
    target_id INTEGER,       -- رقم الهدف
    relation_type TEXT,      -- نوع العلاقة
    weight REAL DEFAULT 1.0  -- وزن العلاقة
);

-- فهارس للأداء
CREATE INDEX idx_neural_source ON neural_links(source_type, source_id);
CREATE INDEX idx_neural_target ON neural_links(target_type, target_id);
CREATE INDEX idx_neural_relation ON neural_links(relation_type);
```

---

## 🌳 بنية الشجرة الديناميكية

### التصميم الهيكلي

```
SmartSearchTree (QTreeWidget)
│
├─ 📖 عرض
│  ├─ القرآن الكريم
│  │  ├─ الفاتحة
│  │  │  ├─ بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِیمِ
│  │  │  ├─ ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَـٰلَمِینَ
│  │  │  └─ ...
│  │  ├─ البقرة
│  │  └─ ...
│  │
│  ├─ التفاسير
│  │  ├─ ☑ الطبري
│  │  ├─ ☑ ابن كثير
│  │  └─ ☐ القرطبي
│  │
│  ├─ الترجمات
│  ├─ علوم القرآن
│  └─ التدبرات
│
├─ 🔍 بحث
│  ├─ البحث في كل شيء
│  ├─ البحث في القرآن
│  │  ├─ الرسم العثماني
│  │  ├─ الرسم الإملائي
│  │  └─ ...
│  ├─ البحث في التفاسير
│  └─ البحث في الموضوعات
│
└─ 📚 موضوعات
   ├─ العقيدة
   │  ├─ التوحيد
   │  │  ├─ توحيد الربوبية
   │  │  └─ توحيد الألوهية
   │  └─ ...
   ├─ الأحكام
   └─ القصص
```

### آلية التحديث الديناميكي

```python
class SmartSearchTree(QTreeWidget):
    # إشارات مخصصة
    item_selected = pyqtSignal(dict)  # عند اختيار عنصر
    filter_changed = pyqtSignal(list) # عند تغيير الفلتر

    def __init__(self):
        super().__init__()
        self.neural_engine = NeuralLinkEngine()
        self.cache = LRUCache(maxsize=1000)

    def update_from_search(self, results):
        """تحديث الشجرة من نتائج البحث"""
        self.clear()
        for result in results:
            self.add_result_item(result)

    def on_item_clicked(self, item):
        """عند النقر على عنصر"""
        # جلب البيانات المرتبطة
        data = self.neural_engine.get_linked_data(item.data)

        # إرسال إشارة لتحديث كل النوافذ
        self.item_selected.emit(data)
```

---

## 🔍 نظام البحث الذكي

### مراحل البحث

```
المستخدم يكتب "حمد"
         ↓
    ┌────────────────┐
    │  Auto-complete │  ← قائمة الاقتراحات
    └────────────────┘
         ↓
    ┌────────────────┐
    │ Search Engine  │  ← محرك البحث FTS5
    └────────────────┘
         ↓
    ┌────────────────┐
    │ Filter System  │  ← تطبيق الفلاتر
    └────────────────┘
         ↓
    ┌────────────────┐
    │ Neural Expand  │  ← توسيع النتائج
    └────────────────┘
         ↓
    ┌────────────────┐
    │ Display Results│  ← عرض في الشجرة
    └────────────────┘
```

### خوارزمية البحث

```python
class SmartSearchEngine:
    def search(self, query, filters=None):
        """
        البحث الذكي متعدد المراحل
        """
        # المرحلة 1: البحث الأساسي
        basic_results = self.fts_search(query)

        # المرحلة 2: تطبيق الفلاتر
        if filters:
            filtered_results = self.apply_filters(basic_results, filters)
        else:
            filtered_results = basic_results

        # المرحلة 3: التوسيع العصبي
        expanded_results = self.neural_expand(filtered_results)

        # المرحلة 4: الترتيب والتصنيف
        ranked_results = self.rank_results(expanded_results)

        # المرحلة 5: التخزين المؤقت
        self.cache.put(query, ranked_results)

        return ranked_results

    def fts_search(self, query):
        """بحث FTS5 السريع"""
        # إزالة التشكيل للبحث
        query_clean = remove_tashkeel(query)

        # بحث في كل المصادر بالتوازي
        results = []

        # البحث في القرآن
        quran_results = self.db.execute("""
            SELECT * FROM quran_fts
            WHERE verse_simplified MATCH ?
            ORDER BY rank
            LIMIT 100
        """, (query_clean,))

        # البحث في التفاسير
        tafseer_results = self.db.execute("""
            SELECT * FROM tafseer_fts
            WHERE tafseer_text MATCH ?
            LIMIT 100
        """, (query_clean,))

        return {
            'quran': quran_results,
            'tafseer': tafseer_results,
            'total_count': len(quran_results) + len(tafseer_results)
        }
```

---

## 🎨 واجهة المستخدم

### التصميم الرئيسي

```
┌────────────────────────────────────────────────────────────┐
│  [عرض] [بحث] [موضوعات]                          [⚙️]     │ ← التابات
├────────────────────────────────────────────────────────────┤
│                                                            │
│  🔍 [أدخل كلمات البحث أو أضف قيداً...]        [🔽]      │ ← البحث
│                                                            │
│  [× القرآن] [× اسم] [× الطبري]                           │ ← الفلاتر
│                                                            │
├──────────────────────────┬─────────────────────────────────┤
│                          │                                 │
│  🌳 الشجرة               │  📄 منطقة العرض                │
│                          │                                 │
│  📖 الفاتحة              │  ┌─────────────────────────┐   │
│    ├─ بسم الله...        │  │ بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ │   │
│    ├─ الحمد لله...       │  │ ٱلرَّحِیمِ                │   │
│    └─ الرحمن...          │  └─────────────────────────┘   │
│                          │                                 │
│  📖 البقرة               │  ┌─────────────────────────┐   │
│    ├─ الم ذلك...         │  │ التفسير الميسر:         │   │
│    └─ ...                │  │ استفتاح السورة...       │   │
│                          │  └─────────────────────────┘   │
│  [الفلاتر]               │                                 │
│  ☑ التفاسير              │                                 │
│    ☑ الطبري              │                                 │
│    ☑ ابن كثير            │                                 │
│    ☐ القرطبي            │                                 │
│                          │                                 │
├──────────────────────────┴─────────────────────────────────┤
│  سورة الفاتحة: 1 | مكية 7 آيات | الجزء: 1 | ص: 1        │ ← المعلومات
└────────────────────────────────────────────────────────────┘
```

---

## ⚡ نظام الفلاتر الديناميكية

### أنواع الفلاتر

```python
FILTER_TYPES = {
    'source': {          # المصدر
        'quran': 'القرآن الكريم',
        'tafseer': 'التفاسير',
        'translation': 'الترجمات',
        'topics': 'الموضوعات'
    },
    'rasm': {            # الرسم
        'othmani': 'العثماني',
        'emlai': 'الإملائي',
        'kufi': 'الكوفي'
    },
    'tashkeel': {        # التشكيل
        'none': 'بدون تشكيل',
        'light': 'تشكيل خفيف',
        'full': 'تشكيل كامل'
    },
    'grammar': {         # النحو
        'noun': 'اسم',
        'verb': 'فعل',
        'particle': 'حرف'
    },
    'books': {           # الكتب
        'tabari': 'الطبري',
        'kathir': 'ابن كثير',
        'qurtubi': 'القرطبي'
    }
}
```

### آلية الفلترة

```python
class FilterChip(QWidget):
    """فلتر قابل للإزالة"""
    removed = pyqtSignal(str)

    def __init__(self, filter_id, filter_name):
        super().__init__()
        self.filter_id = filter_id

        # التصميم
        layout = QHBoxLayout()
        label = QLabel(filter_name)
        remove_btn = QPushButton("×")
        remove_btn.clicked.connect(self.on_remove)

        layout.addWidget(label)
        layout.addWidget(remove_btn)
        self.setLayout(layout)

    def on_remove(self):
        self.removed.emit(self.filter_id)
        self.deleteLater()

class FilterManager(QObject):
    """مدير الفلاتر"""
    filters_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.active_filters = []

    def add_filter(self, filter_type, filter_value):
        """إضافة فلتر"""
        filter_obj = {
            'id': f"{filter_type}_{filter_value}",
            'type': filter_type,
            'value': filter_value
        }

        if filter_obj not in self.active_filters:
            self.active_filters.append(filter_obj)
            self.filters_changed.emit(self.active_filters)

    def remove_filter(self, filter_id):
        """إزالة فلتر"""
        self.active_filters = [
            f for f in self.active_filters
            if f['id'] != filter_id
        ]
        self.filters_changed.emit(self.active_filters)
```

---

## 🔗 محرك الربط العصبي

### آلية الربط

```python
class NeuralLinkEngine:
    """
    محرك الربط العصبي - يربط كل العناصر ببعضها
    """

    def __init__(self, db_path):
        self.db = Database(db_path)
        self.cache = {}

    def get_linked_data(self, verse_id):
        """
        جلب كل البيانات المرتبطة بآية
        """
        # التحقق من الكاش أولاً
        if verse_id in self.cache:
            return self.cache[verse_id]

        linked_data = {
            'verse': self.get_verse(verse_id),
            'tafseer': self.get_tafseer(verse_id),
            'translations': self.get_translations(verse_id),
            'topics': self.get_topics(verse_id),
            'words': self.get_words(verse_id),
            'grammar': self.get_grammar(verse_id),
            'related_verses': self.get_related_verses(verse_id)
        }

        # حفظ في الكاش
        self.cache[verse_id] = linked_data

        return linked_data

    def get_related_verses(self, verse_id):
        """جلب الآيات المرتبطة"""
        return self.db.execute("""
            SELECT target_id, relation_type, weight
            FROM neural_links
            WHERE source_type = 'verse'
            AND source_id = ?
            ORDER BY weight DESC
            LIMIT 10
        """, (verse_id,))
```

---

## 📊 استراتيجية الأداء

### 1. الفهرسة المتقدمة

```sql
-- فهارس أساسية
CREATE INDEX idx_verses_surah ON verses(surah_id);
CREATE INDEX idx_verses_page ON verses(page_number);
CREATE INDEX idx_verses_juz ON verses(juz_number);

-- فهارس مركبة
CREATE INDEX idx_verses_location ON verses(surah_id, verse_number);
CREATE INDEX idx_words_verse ON words(verse_id, word_position);

-- فهارس للبحث
CREATE INDEX idx_words_root ON words(root);
CREATE INDEX idx_words_stem ON words(stem);
```

### 2. التخزين المؤقت

```python
from functools import lru_cache

class CacheManager:
    def __init__(self):
        self.lru_cache = LRUCache(maxsize=1000)
        self.frequent_cache = {}  # للبيانات الأكثر استخداماً

    @lru_cache(maxsize=500)
    def get_verse(self, verse_id):
        """جلب آية مع كاش"""
        return db.get_verse(verse_id)

    def warm_cache(self):
        """تسخين الكاش بالبيانات الشائعة"""
        # تحميل السور الأولى
        for surah_id in range(1, 10):
            self.get_surah_verses(surah_id)
```

### 3. البحث المتوازي

```python
from concurrent.futures import ThreadPoolExecutor

class ParallelSearchEngine:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)

    def search_all(self, query):
        """بحث متوازي في كل المصادر"""
        futures = []

        # البحث في القرآن
        futures.append(
            self.executor.submit(self.search_quran, query)
        )

        # البحث في التفاسير
        futures.append(
            self.executor.submit(self.search_tafseer, query)
        )

        # البحث في الموضوعات
        futures.append(
            self.executor.submit(self.search_topics, query)
        )

        # جمع النتائج
        results = [f.result() for f in futures]
        return self.merge_results(results)
```

---

## 🎯 الخلاصة

هذا النظام يجمع:
- ⚡ **السرعة**: FTS5 + فهرسة متقدمة + كاش ذكي
- 🧠 **الذكاء**: ربط عصبي + فلاتر ديناميكية
- 🎨 **البساطة**: واجهة شجرية سهلة
- 🌊 **العمق**: بيانات ضخمة ومترابطة

الخطوات التالية:
1. ✅ تصميم قاعدة البيانات
2. ✅ بناء محرك البحث
3. ✅ تطوير الشجرة الديناميكية
4. ✅ دمج النظام الكامل

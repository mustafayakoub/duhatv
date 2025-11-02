# 📦 QuranKit - دليل التثبيت والاستخدام السريع

## 📥 التحميل

تم ضغط المكتبة في الملف: **QuranKit_Library.zip** (31 KB)

## 📁 محتويات الملف المضغوط

```
QuranKit_Library.zip
├── qurankit/                    # 📚 المكتبة الرئيسية
│   ├── __init__.py             # نقطة الدخول
│   ├── README.md               # الدليل الشامل
│   └── components/             # المكونات
│       ├── search.py          # 🔍 البحث
│       ├── tree.py            # 🌳 الشجرة
│       ├── audio.py           # 🔊 الصوت
│       ├── display.py         # 📺 العرض
│       ├── bookmarks.py       # 🔖 الإشارات
│       ├── theme.py           # 🎨 المظاهر
│       └── morphology.py      # 🔬 التحليل الصرفي
└── qurankit_example.py         # 📖 تطبيق مثال كامل
```

## 🚀 خطوات التثبيت

### 1️⃣ فك الضغط

```bash
unzip QuranKit_Library.zip
```

أو افتح الملف بأي برنامج فك ضغط واستخرج المحتويات.

### 2️⃣ نسخ المكتبة لمشروعك

انسخ مجلد `qurankit` إلى مشروعك:

```
مشروعك/
├── qurankit/           ← انسخ هذا المجلد
├── main.py
└── ...
```

### 3️⃣ تثبيت المتطلبات

```bash
pip install PyQt6
```

## ⚡ الاستخدام السريع

### تشغيل التطبيق المثال

```bash
python qurankit_example.py
```

**ملاحظة:** يحتاج التطبيق المثال لقاعدة بيانات القرآن (`quran_ultimate_final.db`)

### استخدام المكتبة في مشروعك

```python
# استيراد المكونات
from qurankit import (
    QuranSearchComponent,
    QuranTreeComponent,
    QuranDisplayComponent,
    QuranBookmarksComponent,
    QuranThemeComponent,
    QuranAudioComponent,
    QuranMorphologyComponent
)

# مثال: البحث
search = QuranSearchComponent(database=your_db)
results = search.search('الرحمن', search_type='text')
print(f"وجدت {len(results)} نتيجة")

# مثال: العرض
display = QuranDisplayComponent()
html = display.format_ayah_html({'sura': 1, 'aya': 1, 'text': 'بسم الله'})

# مثال: المظاهر
theme = QuranThemeComponent('dark')
colors = theme.get_theme()
print(f"اللون الأساسي: {colors['primary']}")
```

## 📖 أمثلة الاستخدام

### 1. البحث في القرآن

```python
from qurankit import QuranSearchComponent

search = QuranSearchComponent(database=db, config={
    'max_results': 100
})

# بحث بسيط
results = search.search('الله')

# بحث متقدم مع فلاتر
results = search.advanced_search('الرحمن', filters={
    'sura': 1,    # البحث في سورة الفاتحة فقط
    'juz': None,
    'page': None
})

# تنسيق النتائج HTML
html = search.format_results_html(results, query='الله')
```

### 2. التصفح بالشجرة

```python
from qurankit import QuranTreeComponent, QuranTreeWidget
from PyQt6.QtWidgets import QApplication

app = QApplication([])

# إنشاء الشجرة
tree = QuranTreeComponent(database=db, config={'mode': 'juz'})
widget = QuranTreeWidget(tree)

# الاستماع للاختيارات
def on_select(data):
    if data['type'] == 'sura':
        print(f"تم اختيار السورة: {data['sura']}")

widget.item_selected.connect(on_select)
widget.show()
app.exec()
```

### 3. تشغيل الصوت

```python
from qurankit import QuranAudioComponent

audio = QuranAudioComponent(database=db, config={
    'cache_dir': Path.home() / '.quran_audio',
    'default_reciter': 'abdulbasit',
    'reciters': {
        'abdulbasit': {
            'name': 'عبد الباسط عبد الصمد',
            'url_base': 'https://server8.mp3quran.net/abd_basit/Alafasy_128kbps'
        }
    }
})

# تشغيل الفاتحة
audio.play_ayah(sura=1, ayah=1)

# استماع للأحداث
audio.state_changed.connect(lambda s: print(f"الحالة: {s}"))

# التحكم
audio.set_volume(0.8)
audio.play_next()
```

### 4. الإشارات المرجعية

```python
from qurankit import QuranBookmarksComponent

bookmarks = QuranBookmarksComponent(database=db)

# إضافة إشارة
bookmarks.add_bookmark(sura=1, ayah=1, note='أول آية في القرآن')

# عرض كل الإشارات
all_bookmarks = bookmarks.get_all_bookmarks()
for b in all_bookmarks:
    print(f"{b['sura_name']}:{b['ayah']} - {b['note']}")

# البحث في الإشارات
results = bookmarks.search_bookmarks('فاتحة')

# إحصائيات
stats = bookmarks.get_statistics()
print(f"إجمالي الإشارات: {stats['total_bookmarks']}")
```

### 5. المظاهر

```python
from qurankit import QuranThemeComponent

theme = QuranThemeComponent('light')

# المظاهر المتاحة: light, dark, sepia, green
themes_available = theme.get_available_themes()

# تطبيق مظهر
theme.set_theme('dark')
stylesheet = theme.apply_theme_to_stylesheet(your_widget)
your_widget.setStyleSheet(stylesheet)

# الحصول على لون محدد
primary_color = theme.get_color('primary')
```

## 🔌 متطلبات قاعدة البيانات

المكتبة تعمل مع أي قاعدة بيانات توفر الواجهات التالية:

```python
class YourDatabase:
    def get_sura_info(self, sura: int) -> dict:
        """معلومات السورة: name, ayas_count, type_full, etc."""
        pass

    def get_sura(self, sura: int) -> list:
        """قائمة آيات السورة"""
        pass

    def search_text(self, query: str, limit: int = 100) -> list:
        """بحث نصي"""
        pass
```

## 📚 التوثيق الكامل

اقرأ الملف `qurankit/README.md` للتوثيق الشامل والأمثلة المتقدمة.

## 🎯 المكونات السبعة

| المكون | الوظيفة | السطور |
|--------|---------|--------|
| 🔍 Search | بحث متقدم (نصي، جذر، وزن) | 300+ |
| 🌳 Tree | تصفح هرمي (جزء/سورة/آية) | 300+ |
| 🔊 Audio | مشغل صوتي كامل | 440+ |
| 📺 Display | تنسيق HTML جميل | 230+ |
| 🔖 Bookmarks | إدارة الإشارات | 200+ |
| 🎨 Theme | 4 مظاهر + مخصص | 340+ |
| 🔬 Morphology | تحليل صرفي | 170+ |

## ✨ المميزات

- ✅ **جاهز للاستخدام** - فقط استورد واستخدم
- ✅ **مجرب ومختبر** - مستخرج من تطبيقات ناجحة
- ✅ **موثق بالكامل** - أمثلة وشروحات بالعربية
- ✅ **قابل للتوسع** - سهل التخصيص والإضافة
- ✅ **واجهة موحدة** - نمط برمجي متسق
- ✅ **دعم PyQt6** - واجهات رسومية جاهزة

## 🆘 الدعم

للأسئلة والمشاكل:
- 📧 Email: duhatv@gmail.com
- 🌐 Website: duhatv.net

## 📄 الترخيص

MIT License - استخدم بحرية في مشاريعك!

---

**صنع بـ ❤️ لخدمة القرآن الكريم**

**Mustafa Yakoub | AiGrow**

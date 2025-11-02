# 📚 QuranKit - مكتبة المكونات القرآنية

**QuranKit** هي مكتبة Python قابلة لإعادة الاستخدام توفر مكونات جاهزة لبناء تطبيقات القرآن الكريم. تم استخراج هذه المكونات من تطبيقات قرآنية ناجحة لتوفير الوقت والجهد في إعادة تنفيذ الميزات الشائعة.

## ✨ المميزات

- 🔍 **بحث متقدم**: بحث نصي، بالجذر، بالوزن الصرفي
- 🌳 **تصفح هرمي**: شجرة تصفح بالأجزاء والسور والآيات
- 🔊 **تشغيل صوتي**: مشغل قرآن كامل مع تحميل تلقائي
- 📺 **عرض منسق**: تنسيق HTML وتصدير للطباعة
- 🔖 **إشارات مرجعية**: حفظ وإدارة الآيات المفضلة
- 🎨 **مظاهر متعددة**: ثيمات فاتحة، داكنة، بنية، خضراء
- 🔬 **تحليل صرفي**: استخراج الجذور والأوزان
- 📦 **قابل للتوسع**: سهل الإضافة والتخصيص

## 📋 المتطلبات

```bash
Python 3.8+
PyQt6
```

## 🚀 التثبيت

### من المصدر:

```bash
# نسخ المشروع
git clone https://github.com/your-username/qurankit.git
cd qurankit

# تثبيت التبعيات
pip install PyQt6
```

### كمكتبة:

```python
# انسخ مجلد qurankit إلى مشروعك
# أو أضفه لمسار Python
import sys
sys.path.insert(0, '/path/to/qurankit')

from qurankit import *
```

## 📖 الاستخدام السريع

### 1. مكون البحث

```python
from qurankit import QuranSearchComponent

# تهيئة البحث
search = QuranSearchComponent(database=your_db, config={
    'max_results': 100,
    'search_types': ['text', 'root', 'pattern']
})

# بحث نصي بسيط
results = search.search('الرحمن', search_type='text')

# بحث متقدم مع فلاتر
results = search.advanced_search('الرحمن', filters={
    'sura': 1,  # البحث في سورة محددة
    'juz': 1,   # البحث في جزء محدد
})

# تنسيق النتائج HTML
html = search.format_results_html(results, query='الرحمن')
```

### 2. مكون الشجرة

```python
from qurankit import QuranTreeComponent, QuranTreeWidget
from PyQt6.QtWidgets import QApplication

app = QApplication([])

# إنشاء الشجرة
tree_component = QuranTreeComponent(database=your_db)
tree_widget = QuranTreeWidget(tree_component)

# الاستماع للنقرات
def on_item_selected(item_data):
    print(f"تم اختيار: {item_data}")

tree_widget.item_selected.connect(on_item_selected)

tree_widget.show()
app.exec()
```

### 3. مكون الصوت

```python
from qurankit import QuranAudioComponent

# إعداد المشغل
audio = QuranAudioComponent(
    database=your_db,
    config={
        'cache_dir': Path.home() / '.quran_audio',
        'default_reciter': 'abdulbasit',
        'auto_play_next': True,
        'reciters': {
            'abdulbasit': {
                'name': 'عبد الباسط عبد الصمد',
                'url_base': 'https://server.com/abdulbasit'
            }
        }
    }
)

# تشغيل آية
audio.play_ayah(sura=1, ayah=1)

# الاستماع للأحداث
def on_state_changed(state):
    print(f"الحالة: {state}")

audio.state_changed.connect(on_state_changed)

# التحكم
audio.pause()
audio.play_next()
audio.set_volume(0.8)
```

### 4. مكون العرض

```python
from qurankit import QuranDisplayComponent

display = QuranDisplayComponent(config={
    'arabic_font': 'Traditional Arabic',
    'font_size': 20,
    'primary_color': '#1e3c72'
})

# تنسيق آية
ayah_data = {'sura': 1, 'aya': 1, 'text': 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ'}
html = display.format_ayah_html(ayah_data)

# تنسيق سورة كاملة
sura_data = {'sura': 1, 'name': 'الفاتحة', 'ayas_count': 7}
ayas = [...]  # قائمة الآيات
html = display.format_sura_html(sura_data, ayas)

# تنسيق نتائج البحث
html = display.format_search_results_html(results, query='الرحمن')
```

### 5. مكون الإشارات المرجعية

```python
from qurankit import QuranBookmarksComponent

bookmarks = QuranBookmarksComponent(
    database=your_db,
    config={'bookmarks_file': Path.home() / '.quran_bookmarks.json'}
)

# إضافة إشارة
bookmarks.add_bookmark(sura=1, ayah=1, note='الفاتحة الأولى')

# الحصول على كل الإشارات
all_bookmarks = bookmarks.get_all_bookmarks()

# البحث في الإشارات
results = bookmarks.search_bookmarks('فاتحة')

# إحصائيات
stats = bookmarks.get_statistics()
print(f"عدد الإشارات: {stats['total_bookmarks']}")
```

### 6. مكون المظاهر

```python
from qurankit import QuranThemeComponent

theme = QuranThemeComponent(theme_name='light')

# الحصول على ألوان الثيم
colors = theme.get_theme('dark')

# تطبيق على widget
stylesheet = theme.apply_theme_to_stylesheet(your_widget, 'sepia')
your_widget.setStyleSheet(stylesheet)

# المظاهر المتاحة
themes = theme.get_available_themes()
# {'light': 'فاتح', 'dark': 'داكن', 'sepia': 'بني', 'green': 'أخضر'}

# إنشاء ثيم مخصص
theme.create_custom_theme('my_theme', 'ثيمي', {
    'background': '#ffffff',
    'text': '#000000',
    'primary': '#ff0000'
})
```

### 7. مكون التحليل الصرفي

```python
from qurankit import QuranMorphologyComponent

morphology = QuranMorphologyComponent(database=your_db)

# البحث بالجذر
results = morphology.search_by_root('علم')

# تحليل كلمة
analysis = morphology.analyze_word('المؤمنون')
print(f"الجذر: {analysis['root']}")
print(f"النوع: {analysis['type']}")

# عد التكرارات
count = morphology.count_root_occurrences('علم')
print(f"تكرار الجذر 'علم': {count} مرة")
```

## 🏗️ بناء تطبيق كامل

مثال على تطبيق قرآن بسيط باستخدام QuranKit:

```python
from PyQt6.QtWidgets import *
from qurankit import *

class SimpleQuranApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تطبيق القرآن - QuranKit")

        # إعداد قاعدة البيانات
        self.db = YourQuranDatabase()

        # إعداد المكونات
        self.setup_components()
        self.setup_ui()

    def setup_components(self):
        # البحث
        self.search = QuranSearchComponent(self.db)

        # الشجرة
        self.tree = QuranTreeComponent(self.db)

        # الصوت
        self.audio = QuranAudioComponent(self.db, config={
            'reciters': {...}
        })

        # العرض
        self.display = QuranDisplayComponent()

        # الإشارات
        self.bookmarks = QuranBookmarksComponent(self.db)

        # الثيم
        self.theme = QuranThemeComponent('light')

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        # الشجرة على اليسار
        tree_widget = QuranTreeWidget(self.tree)
        tree_widget.item_selected.connect(self.on_item_selected)
        layout.addWidget(tree_widget, 1)

        # منطقة العرض على اليمين
        self.text_browser = QTextBrowser()
        layout.addWidget(self.text_browser, 3)

        # تطبيق الثيم
        self.setStyleSheet(self.theme.apply_theme_to_stylesheet(self))

    def on_item_selected(self, data):
        if data['type'] == 'sura':
            # عرض السورة
            sura = data['sura']
            sura_info = self.db.get_sura_info(sura)
            ayas = self.db.get_sura(sura)
            html = self.display.format_sura_html(sura_info, ayas)
            self.text_browser.setHtml(html)

if __name__ == '__main__':
    app = QApplication([])
    window = SimpleQuranApp()
    window.resize(1200, 800)
    window.show()
    app.exec()
```

## 📁 بنية المشروع

```
qurankit/
├── __init__.py              # النقطة الرئيسية للاستيراد
├── README.md                # هذا الملف
└── components/              # المكونات
    ├── __init__.py
    ├── search.py           # 🔍 مكون البحث
    ├── tree.py             # 🌳 مكون الشجرة
    ├── audio.py            # 🔊 مكون الصوت
    ├── display.py          # 📺 مكون العرض
    ├── bookmarks.py        # 🔖 مكون الإشارات
    ├── theme.py            # 🎨 مكون المظاهر
    └── morphology.py       # 🔬 مكون التحليل الصرفي
```

## 🔌 التوافقية

QuranKit مصمم للعمل مع أي قاعدة بيانات قرآنية طالما توفر الواجهات التالية:

```python
class YourQuranDatabase:
    def get_sura_info(self, sura: int) -> Dict:
        """معلومات السورة"""
        pass

    def get_sura(self, sura: int) -> List[Dict]:
        """آيات السورة"""
        pass

    def search_text(self, query: str, limit: int = 100) -> List[Dict]:
        """بحث نصي"""
        pass

    # ... واجهات أخرى اختيارية
```

## 🎯 حالات الاستخدام

- ✅ تطبيقات القرآن المكتبية (PyQt6)
- ✅ أدوات البحث القرآني
- ✅ برامج الدراسة والتفسير
- ✅ تطبيقات التحفيظ
- ✅ أنظمة المكتبات الإسلامية
- ✅ أدوات البحث اللغوي والصرفي

## 🤝 المساهمة

نرحب بالمساهمات! يمكنك:

1. Fork المشروع
2. إنشاء فرع للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى الفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📝 الترخيص

هذا المشروع مرخص بموجب رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## 👨‍💻 المطور

**Mustafa Yakoub**
- 📧 Email: duhatv@gmail.com
- 🌐 Website: duhatv.net
- 📱 Phone: +905342390000
- 🏢 Company: AiGrow

## 🙏 شكر وتقدير

تم استخراج هذه المكونات من عدة تطبيقات قرآنية ناجحة تم تطويرها على مدار سنوات. نشكر كل من ساهم في تطوير هذه التطبيقات الأصلية.

## 📚 موارد إضافية

- [دليل التطوير](DEVELOPMENT.md)
- [أمثلة الاستخدام](examples/)
- [API Reference](API.md)
- [سجل التغييرات](CHANGELOG.md)

---

**صنع بـ ❤️ لخدمة القرآن الكريم**

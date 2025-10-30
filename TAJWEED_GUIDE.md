# 🎨 QuranTajweedComponent - دليل الاستخدام الشامل

## 📖 المقدمة

**QuranTajweedComponent** هو مكون قوي ومرن لعرض القرآن الكريم بألوان التجويد، تم استخلاصه من تطبيق ناجح وإضافته لمكتبة QuranKit.

## ✨ الميزات الرئيسية

### 1. عرض ملون للتجويد
- **15 حكم تجويدي** مختلف بألوان مميزة
- تحويل تلقائي من رموز XML إلى HTML ملون
- دعم tooltips تفاعلية

### 2. البحث والاستخراج
- البحث عن حكم تجويدي معين
- استخراج كل الكلمات المحتوية على حكم
- تمييز أحكام محددة بالتظليل

### 3. إحصائيات شاملة
- حساب تكرار كل حكم في النص
- عرض النسب المئوية
- جداول تفصيلية ملونة

### 4. تخصيص كامل
- تغيير ألوان الأحكام
- دعم خطوط متعددة
- تصدير/استيراد الإعدادات

## 🎯 أحكام التجويد المدعومة

| ID | الحكم | الاسم بالإنجليزية | اللون الافتراضي | الفئة |
|----|-------|-------------------|-----------------|-------|
| 1 | إظهار | Izhar | #696969 | نون ساكنة وتنوين |
| 2 | إدغام | Idgham | #228B22 | نون ساكنة وتنوين |
| 3 | إدغام بغنة | Idgham Ghunnah | #2E8B57 | نون ساكنة وتنوين |
| 4 | مد | Madd | #DC143C | المدود |
| 5 | قلقلة | Qalqalah | #4169E1 | الحروف المقلقلة |
| 6 | سكون | Sukoon | #2F4F4F | السكون |
| 7 | غنة | Ghunnah | #FF8C00 | الغنة |
| 8 | شدة | Shaddah | #8B0000 | الشدة |
| 9 | إقلاب | Iqlab | #9370DB | نون ساكنة وتنوين |
| 10 | تفخيم | Tafkheem | #8B4513 | حروف الاستعلاء |
| 11 | ترقيق | Tarqeeq | #4682B4 | الحروف المرققة |
| 12 | إخفاء | Ikhfa | #D4AF37 | نون ساكنة وتنوين |
| 13 | صفير | Safeer | #20B2AA | حروف الصفير |
| 14 | لين | Leen | #DDA0DD | حروف اللين |
| 15 | مد لازم | Madd Lazim | #B22222 | المدود |

## 🚀 الاستخدام السريع

### التثبيت

```bash
# تأكد من تثبيت QuranKit
pip install PyQt6

# استيراد المكون
from qurankit import QuranTajweedComponent
```

### مثال بسيط

```python
from qurankit import QuranTajweedComponent

# إنشاء المكون
tajweed = QuranTajweedComponent()

# نص قرآني مع رموز التجويد
text = '<4>بِسۡمِ</4> <10>ٱللَّهِ</10> <4>ٱلرَّحۡمَٰنِ</4> <4>ٱلرَّحِيمِ</4>'

# تحويل إلى HTML ملون
html = tajweed.convert_to_html(text)

# عرض في QTextBrowser
browser.setHtml(html)
```

## 📚 أمثلة الاستخدام المتقدم

### 1. عرض آية كاملة مع معلومات

```python
tajweed = QuranTajweedComponent()

ayah_text = '<4>بِسۡمِ</4> <10>ٱللَّهِ</10> <4>ٱلرَّحۡمَٰنِ</4> <4>ٱلرَّحِيمِ</4>'

# تنسيق كامل مع عنوان ومفتاح ألوان
html = tajweed.format_ayah_with_tajweed(
    ayah_text,
    surah_name="الفاتحة",
    ayah_number=1,
    show_legend=True  # عرض مفتاح الألوان
)

text_browser.setHtml(html)
```

### 2. البحث عن حكم تجويدي

```python
# البحث عن كل حالات "الإخفاء" (رقم 12)
results = tajweed.search_by_rule(text, rule_id=12)

# results = [(start_pos, end_pos, 'النص المطابق'), ...]

for start, end, matched_text in results:
    print(f"وجدت إخفاء: {matched_text} في الموضع {start}")
```

### 3. استخراج كلمات بحكم معين

```python
# استخراج كل الكلمات المحتوية على "مد" (رقم 4)
words = tajweed.extract_words_by_rule(text, rule_id=4)

# ['بِسۡمِ', 'ٱلرَّحۡمَٰنِ', 'ٱلرَّحِيمِ']

for word in words:
    print(f"كلمة بها مد: {word}")
```

### 4. إحصائيات التجويد

```python
# حساب الإحصائيات
stats = tajweed.get_tajweed_statistics(text)

# stats = {1: 0, 2: 0, 3: 0, 4: 3, 5: 0, ...}

# عرض بتنسيق HTML جميل
stats_html = tajweed.format_statistics_html(stats)
text_browser.setHtml(stats_html)
```

### 5. تمييز حكم معين

```python
# تمييز كل حالات "القلقلة" بلون أصفر
highlighted = tajweed.highlight_rule(
    text,
    rule_id=5,  # قلقلة
    highlight_color="#FFEB3B"
)

html = tajweed.convert_to_html(highlighted)
text_browser.setHtml(html)
```

### 6. تخصيص الألوان

```python
# تغيير لون حكم معين
tajweed.set_custom_color(rule_id=4, color="#FF0000")  # مد = أحمر فاقع

# إعادة الألوان الافتراضية
tajweed.reset_colors()

# تصدير الإعدادات
config = tajweed.export_config()
# {'custom_colors': {4: '#FF0000'}, 'rules': {...}}

# استيراد إعدادات
tajweed.import_config(config)
```

### 7. إزالة رموز التجويد

```python
# الحصول على نص نظيف بدون رموز
text = '<4>بِسۡمِ</4> <10>ٱللَّهِ</10> <4>ٱلرَّحۡمَٰنِ</4> <4>ٱلرَّحِيمِ</4>'
clean = tajweed.convert_to_plain_text(text)

# 'بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ'
```

### 8. معلومات حكم تجويدي

```python
# الحصول على معلومات حكم
rule = tajweed.get_rule_info(rule_id=12)

print(f"الاسم: {rule.name}")          # إخفاء
print(f"English: {rule.name_en}")     # Ikhfa
print(f"اللون: {rule.color}")         # #D4AF37
print(f"الوصف: {rule.description}")   # إخفاء
print(f"الفئة: {rule.category}")      # نون ساكنة وتنوين
```

## 🎨 تخصيص العرض

### اختيار الخط المناسب

```python
# الخطوط الموصى بها
fonts = tajweed.get_recommended_fonts()

# ['Traditional Arabic', 'Arial', 'Tahoma', ...]

# استخدام خط معين
html = tajweed.convert_to_html(
    text,
    font_family="Traditional Arabic",
    font_size=20
)
```

**ملاحظة مهمة**: لعرض التجويد بشكل صحيح:
- اختر خط **ليس عريضاً** جداً
- تأكد من أن الأحرف متصلة بشكل سلس
- الخطوط الموصى بها: Traditional Arabic, Arial, Tahoma

### التحكم بـ Tooltips

```python
# إخفاء تلميحات الأحكام
html = tajweed.convert_to_html(
    text,
    show_tooltips=False  # لا تظهر tooltips عند التمرير
)
```

### تمييز حكم محدد

```python
# تمييز "الغنة" فقط
html = tajweed.convert_to_html(
    text,
    highlight_rule=7  # غنة
)
```

## 🔧 الإعدادات المتقدمة

### إنشاء بإعدادات مخصصة

```python
config = {
    'custom_colors': {
        4: '#FF0000',   # مد = أحمر
        12: '#00FF00',  # إخفاء = أخضر
    }
}

tajweed = QuranTajweedComponent(config=config)
```

### الحصول على كل الأحكام

```python
all_rules = tajweed.get_all_rules()

# {1: TajweedRule(...), 2: TajweedRule(...), ...}

for rule_id, rule in all_rules.items():
    print(f"{rule_id}: {rule.name} - {rule.color}")
```

## 📊 حالات الاستخدام

### 1. تطبيق تعليم التجويد
```python
# عرض آية مع التركيز على حكم واحد
def show_rule_lesson(text, rule_id):
    tajweed = QuranTajweedComponent()

    # تمييز الحكم
    highlighted = tajweed.highlight_rule(text, rule_id)

    # الحصول على معلومات
    rule = tajweed.get_rule_info(rule_id)

    # استخراج الأمثلة
    examples = tajweed.extract_words_by_rule(text, rule_id)

    return highlighted, rule, examples
```

### 2. محرك بحث تجويدي
```python
def search_tajweed_rule(quran_text_list, rule_id):
    """البحث في كل القرآن عن حكم معين"""
    tajweed = QuranTajweedComponent()
    results = []

    for surah, ayah, text in quran_text_list:
        words = tajweed.extract_words_by_rule(text, rule_id)
        if words:
            results.append({
                'surah': surah,
                'ayah': ayah,
                'words': words
            })

    return results
```

### 3. إحصائيات القرآن الكاملة
```python
def analyze_full_quran(quran_database):
    """تحليل أحكام التجويد في القرآن كاملاً"""
    tajweed = QuranTajweedComponent()
    total_stats = {i: 0 for i in range(1, 16)}

    for verse in quran_database.get_all_verses():
        stats = tajweed.get_tajweed_statistics(verse['text'])
        for rule_id, count in stats.items():
            total_stats[rule_id] += count

    return total_stats
```

### 4. مقارنة القراءات
```python
def compare_qiraat(text_hafs, text_warsh):
    """مقارنة التجويد بين قراءتين"""
    tajweed = QuranTajweedComponent()

    stats_hafs = tajweed.get_tajweed_statistics(text_hafs)
    stats_warsh = tajweed.get_tajweed_statistics(text_warsh)

    differences = {}
    for rule_id in stats_hafs:
        if stats_hafs[rule_id] != stats_warsh[rule_id]:
            differences[rule_id] = {
                'hafs': stats_hafs[rule_id],
                'warsh': stats_warsh[rule_id]
            }

    return differences
```

## 🔍 نظام الترميز

النظام يستخدم XML tags بسيطة:

```
<رقم_الحكم>النص</رقم_الحكم>
```

**أمثلة**:
- `<4>بِسۡمِ</4>` - مد
- `<12>إِيَّاكَ</12>` - إخفاء
- `<5>رَبِّ</5>` - قلقلة
- `<10>ٱللَّهِ</10>` - تفخيم

## 📁 بنية البيانات المطلوبة

للاستفادة الكاملة من المكون، يجب أن تكون قاعدة بيانات القرآن تحتوي على:

```sql
-- جدول النصوص مع التجويد
CREATE TABLE quran_text_with_tajweed (
    surah_id INTEGER,
    ayah_id INTEGER,
    text_with_tajweed TEXT,  -- النص مع رموز <number>...</number>
    PRIMARY KEY (surah_id, ayah_id)
);
```

**مثال على البيانات**:
```
surah_id: 1
ayah_id: 1
text_with_tajweed: '<4>بِسۡمِ</4> <10>ٱللَّهِ</10> <4>ٱلرَّحۡمَٰنِ</4> <4>ٱلرَّحِيمِ</4>'
```

## 🎓 نصائح مهمة

1. **اختيار الخط**: استخدم خطوط غير عريضة لضمان التصاق الألوان
2. **الأداء**: للنصوص الطويلة، استخدم `convert_to_html()` مرة واحدة واحفظ النتيجة
3. **الإحصائيات**: للقرآن الكامل، احسب الإحصائيات في الخلفية (threading)
4. **التخصيص**: احفظ إعدادات المستخدم باستخدام `export_config()`

## 🐛 حل المشاكل الشائعة

### المشكلة: الألوان لا تظهر

**الحل**:
```python
# تأكد من استخدام QTextBrowser أو QTextEdit مع HTML
text_browser.setHtml(html)  # ✅ صحيح
text_browser.setText(html)  # ❌ خطأ - لن تظهر الألوان
```

### المشكلة: الحروف منفصلة

**الحل**: استخدم خط مناسب
```python
html = tajweed.convert_to_html(text, font_family="Traditional Arabic")
```

### المشكلة: الإحصائيات فارغة

**الحل**: تأكد من وجود رموز التجويد في النص
```python
# تحقق من النص
if '<' in text and '>' in text:
    stats = tajweed.get_tajweed_statistics(text)
else:
    print("النص لا يحتوي على رموز تجويد")
```

## 🔗 التكامل مع QuranKit

```python
from qurankit import (
    QuranTajweedComponent,
    QuranDisplayComponent,
    QuranSearchComponent
)

# استخدام مع مكونات أخرى
tajweed = QuranTajweedComponent()
display = QuranDisplayComponent()

# عرض آية بالتجويد
html = tajweed.format_ayah_with_tajweed(ayah_text)

# ثم عرضها باستخدام Display Component
# أو دمجها مع البحث...
```

## 📞 الدعم والمساهمة

للأسئلة والمشاكل:
- 📧 Email: duhatv@gmail.com
- 🌐 Website: duhatv.net
- 📦 GitHub: [QuranKit Repository]

---

**صنع بـ ❤️ لخدمة القرآن الكريم**

**Mustafa Yakoub | AiGrow**

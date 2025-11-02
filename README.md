# 📖 القرآن الكريم Pro v2.1

<div dir="rtl">

## نظرة عامة

تطبيق شامل وحديث للقرآن الكريم مع واجهة رسومية أنيقة مستوحاة من Tanzil.net، يوفر تجربة غنية لقراءة وتصفح وتفسير وترجمة القرآن الكريم.

## ✨ الميزات الرئيسية

### 📖 عرض القرآن الكريم
- ✅ أنواع رسم متعددة (عثماني، إملائي، مبسط، نظيف)
- ✅ 15 خط قرآني احترافي قابل للتغيير
- ✅ عرض مريح مع تمييز الآيات
- ✅ البسملة التلقائية
- ✅ عرض رقم الجزء والصفحة

### 📚 التفاسير
- التفسير الميسر
- تفسير الجلالين
- تفسير الطبري
- تفسير ابن كثير
- تفسير السعدي

### 🌍 الترجمات
- دعم ترجمات متعددة اللغات
- عرض منسق للترجمات
- مقارنة بين اللغات

### 🔍 البحث المتقدم
- بحث نصي في القرآن والتفاسير
- بحث بالجذر اللغوي
- بحث بالنمط الصرفي
- بحث بالموضوع

### 🧭 التنقل السريع
- الانتقال إلى سورة:آية
- الانتقال إلى جزء معين
- الانتقال إلى صفحة محددة
- شجرة تصفح بالأجزاء والسور

### 🔖 ميزات إضافية
- العلامات المرجعية مع ملاحظات
- نسخ النصوص
- طباعة
- حفظ بصيغ متعددة (HTML, TXT)
- وضع ملء الشاشة

### 🔬 علوم القرآن
- آيات السجدة
- علوم السور
- المواضيع القرآنية
- علامات الوقف

## 📊 الإحصائيات

- 📖 114 سورة
- 📄 6236 آية
- 📘 30 جزء
- 📃 604 صفحة
- 💾 168 MB من البيانات القرآنية

## 🚀 التثبيت والتشغيل

### المتطلبات

- Python 3.8 أو أحدث
- PyQt6
- 200 MB مساحة خالية

### خطوات التثبيت

#### 1️⃣ تثبيت المكتبات

```bash
pip install -r requirements.txt
```

#### 2️⃣ إضافة قاعدة البيانات

ضع ملف `quran_ultimate_final.db` في مجلد `data/`:

```
duhatv/
├── data/
│   └── quran_ultimate_final.db  ← ضع الملف هنا
├── src/
├── fonts/
└── ...
```

#### 3️⃣ (اختياري) إضافة الخطوط

ضع ملفات الخطوط القرآنية (.ttf, .otf) في مجلد `fonts/`:

```
duhatv/
├── fonts/
│   ├── Amiri-Quran.ttf
│   ├── UthmanicHafs.otf
│   ├── noorehuda.ttf
│   └── ...
```

### التشغيل

#### Windows

```bash
run.bat
```

أو:

```bash
python quran_pro.py
```

#### Linux/Mac

```bash
./run.sh
```

أو:

```bash
python3 quran_pro.py
```

## 📁 بنية المشروع

```
duhatv/
├── quran_pro.py           # الملف الرئيسي للتطبيق
├── src/                   # الكود المصدري
│   ├── config.py         # الإعدادات والثوابت
│   ├── db_manager.py     # مدير قاعدة البيانات
│   └── dialogs.py        # النوافذ المنبثقة
├── data/                  # البيانات
│   └── quran_ultimate_final.db  # قاعدة البيانات
├── fonts/                 # الخطوط القرآنية
├── docs/                  # الوثائق
├── requirements.txt       # المتطلبات
├── run.sh                # تشغيل Linux/Mac
├── run.bat               # تشغيل Windows
└── README.md             # هذا الملف
```

## ⌨️ اختصارات لوحة المفاتيح

| الاختصار | الوظيفة |
|----------|---------|
| `Ctrl+G` | الانتقال إلى سورة:آية |
| `Ctrl+J` | الانتقال إلى جزء |
| `Ctrl+P` | الانتقال إلى صفحة |
| `Ctrl+F` | البحث |
| `Ctrl+D` | إضافة علامة مرجعية |
| `Ctrl+C` | نسخ |
| `Ctrl+A` | تحديد الكل |
| `Ctrl+S` | حفظ باسم |
| `Ctrl+P` | طباعة |
| `F11` | ملء الشاشة |
| `Ctrl+Q` | خروج |

## 🎨 لقطات الشاشة

(يمكن إضافة لقطات شاشة هنا)

## 🔧 الإعدادات

يمكنك تخصيص الإعدادات من خلال ملف `src/config.py`:

- الألوان والثيم
- الخطوط الافتراضية
- نوع الرسم الافتراضي
- إعدادات العرض
- إعدادات البحث

## 📝 ملاحظات مهمة

### قاعدة البيانات

- يجب أن يكون ملف `quran_ultimate_final.db` موجوداً في مجلد `data/`
- حجم قاعدة البيانات: ~168 MB
- تحتوي على كل النصوص والتفاسير والترجمات

### الخطوط

- الخطوط القرآنية اختيارية
- إذا لم تكن متوفرة، سيستخدم التطبيق خطوط النظام
- للحصول على أفضل تجربة، ننصح بتثبيت الخطوط

## 🐛 الإبلاغ عن المشاكل

إذا واجهت أي مشكلة:

1. تأكد من وجود قاعدة البيانات في المكان الصحيح
2. تأكد من تثبيت PyQt6 بشكل صحيح
3. تحقق من إصدار Python (3.8+)
4. راجع رسائل الخطأ في Terminal/CMD

## 🔄 التحديثات المستقبلية

- [ ] دعم أصوات القراء
- [ ] تحفيظ القرآن
- [ ] إعراب القرآن الكريم
- [ ] تحليل بلاغي ونحوي
- [ ] مزيد من التفاسير
- [ ] ثيمات متعددة (فاتح/داكن)
- [ ] تصدير بصيغ متعددة (PDF, DOCX)

## 👨‍💻 معلومات المطور

- **الشركة:** AiGrow
- **المطور:** Mustafa Yakoub
- **البريد الإلكتروني:** duhatv@gmail.com
- **الموقع:** duhatv.net
- **الهاتف:** +905342390000

## 📜 الترخيص

هذا المشروع مفتوح المصدر ومخصص لخدمة كتاب الله الكريم.

## 🤲 الدعاء

نسأل الله أن يجعل هذا العمل في ميزان حسناتنا وأن ينفع به المسلمين في كل مكان.

---

**تم التطوير بكل ❤️ لخدمة كتاب الله**

</div>

---

<div dir="ltr">

# 📖 Quran Pro v2.1

## Overview

A comprehensive and modern application for the Holy Quran with an elegant graphical interface inspired by Tanzil.net, providing a rich experience for reading, browsing, interpreting, and translating the Holy Quran.

## ✨ Key Features

- Multiple Quran text styles (Uthmani, Imlaei, Simple)
- 15+ professional Quranic fonts
- Multiple Tafsir (Muyassar, Jalalayn, Tabari, Ibn Kathir, Saadi)
- Multi-language translations
- Advanced search (text, root, pattern, topic)
- Quick navigation (Sura:Aya, Juz, Page)
- Bookmarks with notes
- Print and export capabilities
- Quranic sciences (Sajdah verses, topics, etc.)
- 168 MB of Quranic data

## 🚀 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Place database file
# Put quran_ultimate_final.db in data/ folder

# Run application
python quran_pro.py
```

## 📊 Statistics

- 📖 114 Suras
- 📄 6,236 Verses
- 📘 30 Juz
- 📃 604 Pages

## 👨‍💻 Developer

**Mustafa Yakoub** | AiGrow
- Email: duhatv@gmail.com
- Website: duhatv.net

</div>

# 🚀 دليل التثبيت - تطبيق القرآن الكريم Pro

<div dir="rtl">

## المتطلبات الأساسية

### 1. Python 3.8 أو أحدث

#### Windows
- قم بتحميل Python من [python.org](https://www.python.org/downloads/)
- تأكد من تحديد "Add Python to PATH" أثناء التثبيت

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### macOS
```bash
# باستخدام Homebrew
brew install python3
```

### 2. قاعدة البيانات

يجب توفر ملف `quran_ultimate_final.db` (حجمه ~168 MB)

## خطوات التثبيت التفصيلية

### الخطوة 1: تحميل المشروع

```bash
git clone <repository-url>
cd duhatv
```

### الخطوة 2: تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

أو يدوياً:

```bash
pip install PyQt6
```

### الخطوة 3: إضافة قاعدة البيانات

```bash
# أنشئ مجلد data إذا لم يكن موجوداً
mkdir -p data

# انسخ قاعدة البيانات
cp /path/to/quran_ultimate_final.db data/
```

البنية المطلوبة:
```
duhatv/
├── data/
│   └── quran_ultimate_final.db  ✅ ضع الملف هنا
```

### الخطوة 4: (اختياري) إضافة الخطوط

للحصول على أفضل تجربة، أضف الخطوط القرآنية:

```bash
# أنشئ مجلد fonts إذا لم يكن موجوداً
mkdir -p fonts

# انسخ الخطوط
cp /path/to/fonts/*.ttf fonts/
cp /path/to/fonts/*.otf fonts/
```

الخطوط الموصى بها:
- Amiri-Quran.ttf
- UthmanicHafs.otf
- noorehuda.ttf
- noorehira.ttf
- ScheherazadeNew-Regular.ttf

### الخطوة 5: اختبار التثبيت

```bash
python quran_pro.py
```

إذا ظهرت الواجهة، فالتثبيت ناجح! 🎉

## حل المشاكل الشائعة

### مشكلة: "❌ قاعدة البيانات غير موجودة"

**الحل:**
```bash
# تحقق من وجود الملف
ls -la data/quran_ultimate_final.db

# إذا لم يكن موجوداً، انسخه
cp /path/to/quran_ultimate_final.db data/
```

### مشكلة: "ModuleNotFoundError: No module named 'PyQt6'"

**الحل:**
```bash
pip install PyQt6

# أو باستخدام pip3
pip3 install PyQt6
```

### مشكلة: "python: command not found"

**الحل:**
```bash
# استخدم python3 بدلاً من python
python3 quran_pro.py

# أو قم بإنشاء alias
alias python=python3
```

### مشكلة: صلاحيات تشغيل run.sh

**الحل:**
```bash
chmod +x run.sh
./run.sh
```

### مشكلة: الخطوط لا تظهر بشكل صحيح

**الحل:**
1. تأكد من وجود ملفات الخطوط في مجلد `fonts/`
2. جرّب خط آخر من قائمة الخطوط
3. سيستخدم التطبيق خطوط النظام تلقائياً كبديل

## التثبيت في بيئة افتراضية (موصى به)

### Windows
```bash
# إنشاء بيئة افتراضية
python -m venv venv

# تفعيلها
venv\Scripts\activate

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل التطبيق
python quran_pro.py
```

### Linux/Mac
```bash
# إنشاء بيئة افتراضية
python3 -m venv venv

# تفعيلها
source venv/bin/activate

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل التطبيق
python quran_pro.py
```

## التحقق من التثبيت

قم بتشغيل هذه الأوامر للتحقق:

```bash
# التحقق من Python
python --version
# يجب أن يكون 3.8 أو أحدث

# التحقق من PyQt6
python -c "import PyQt6; print('PyQt6 OK')"

# التحقق من قاعدة البيانات
ls -lh data/quran_ultimate_final.db
# يجب أن يظهر الملف بحجم ~168MB
```

## الإعداد للتطوير

إذا كنت تريد تطوير التطبيق:

```bash
# تثبيت أدوات التطوير
pip install -r requirements-dev.txt  # (قم بإنشائه إذا لزم)

# تشغيل في وضع التطوير
python quran_pro.py --debug
```

## دعم

إذا واجهت أي مشكلة:

1. راجع قسم "حل المشاكل الشائعة" أعلاه
2. تأكد من توفر كل المتطلبات
3. تحقق من رسائل الخطأ في Terminal/CMD
4. اتصل بـ: duhatv@gmail.com

---

**بالتوفيق! 🎉**

</div>

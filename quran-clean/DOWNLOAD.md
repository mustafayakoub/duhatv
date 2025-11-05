# 📥 تحميل الأكواد

## ✅ الملف المضغوط

تم ضغط جميع أكواد المشروع في ملف واحد:

**الملف:** `quran-clean-source.tar.gz` (23 KB)

**المحتويات:**
- ✅ جميع ملفات Python (app.py, import_data.py)
- ✅ Schema قاعدة البيانات (schema.sql)
- ✅ الواجهة HTML/CSS/JS
- ✅ جميع ملفات التوثيق
- ✅ بنية المجلدات الفارغة

---

## 📦 فك الضغط

### في Windows (PowerShell):
```powershell
# باستخدام WSL
wsl tar -xzf quran-clean-source.tar.gz

# أو باستخدام 7-Zip/WinRAR
```

### في Linux:
```bash
tar -xzf quran-clean-source.tar.gz
cd quran-clean
```

---

## 🔗 روابط التحميل

### 1️⃣ **من GitHub:**
```
https://github.com/mustafayakoub/duhatv/tree/claude/start-project-011CUpGw1vgyzJcVKt4CMne6/quran-clean
```

### 2️⃣ **تنزيل الملف المضغوط:**
```
https://github.com/mustafayakoub/duhatv/raw/claude/start-project-011CUpGw1vgyzJcVKt4CMne6/quran-clean/quran-clean-source.tar.gz
```

### 3️⃣ **استنساخ المشروع كاملاً:**
```bash
git clone -b claude/start-project-011CUpGw1vgyzJcVKt4CMne6 https://github.com/mustafayakoub/duhatv.git
cd duhatv/quran-clean
```

---

## 🚀 البدء السريع بعد التحميل

### 1. فك الضغط:
```bash
tar -xzf quran-clean-source.tar.gz
cd quran-clean
```

### 2. نسخ ملفاتك:
```bash
# الآيات
cp /path/to/your/ayat/* data/ayat/

# السور
cp /path/to/suar_quran_Mustafa_Yakoub.xlsx data/surahs/

# الكلمات
cp /path/to/your/words/* data/words/

# الخطوط
cp /path/to/your/fonts/* data/fonts/
cp /path/to/your/fonts/* static/fonts/
```

### 3. تثبيت وتشغيل:
```bash
pip install -r requirements.txt
python import_data.py
python app.py
```

### 4. فتح المتصفح:
```
http://localhost:5000
```

---

## 📂 محتويات الملف المضغوط

```
quran-clean/
├── app.py                     ✅ 300 سطر
├── import_data.py             ✅ 500 سطر
├── schema.sql                 ✅ بنية قاعدة البيانات
├── requirements.txt           ✅ المتطلبات
├── templates/
│   └── index.html             ✅ 400 سطر
├── static/
│   ├── css/
│   │   └── style.css          ✅ 600 سطر
│   └── js/
│       └── app.js             ✅ 500 سطر
├── data/                      (مجلدات فارغة)
│   ├── ayat/
│   ├── surahs/
│   ├── words/
│   └── fonts/
├── README.md                  ✅ دليل شامل
├── INSTRUCTIONS.md            ✅ تعليمات مفصلة
├── SUMMARY.md                 ✅ ملخص المشروع
├── START.md                   ✅ بداية سريعة
└── DOWNLOAD.md                ✅ هذا الملف
```

**الحجم الإجمالي:** 23 KB فقط!

---

## ⚠️ ملاحظة مهمة

الملف المضغوط **لا يحتوي** على:
- ❌ ملفات الآيات (18 ملف)
- ❌ ملف السور (Excel)
- ❌ ملفات الكلمات (6 ملفات)
- ❌ الخطوط (16 خط)
- ❌ قاعدة البيانات (quran.db)

**يجب عليك إضافتها يدوياً كما هو موضح أعلاه.**

---

## 📞 الدعم

إذا واجهت مشاكل:
1. اقرأ `README.md`
2. اقرأ `INSTRUCTIONS.md`
3. اقرأ `START.md`

---

**بالتوفيق! 🚀**

"إِنَّ هَٰذَا الْقُرْآنَ يَهْدِي لِلَّتِي هِيَ أَقْوَمُ" (الإسراء: 9)

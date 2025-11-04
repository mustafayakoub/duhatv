# 📦 التحديثات - الروابط المباشرة

## 🔗 آخر إصدار: v2 (دعم الخطوط)

### **رابط التحميل المباشر:**

```
https://github.com/mustafayakoub/duhatv/raw/claude/fresh-start-no-errors-011CUmiYSzwrefKsJhPgd5ay/duhatv-app-v2-fonts.zip
```

**الحجم**: 51 KB
**التاريخ**: 4 نوفمبر 2025

---

## ✨ ما الجديد في v2:

### **15 خط قرآني احترافي:**

#### 🕌 خطوط عثمانية (4):
- ✅ Uthmanic Hafs V22 (الافتراضي) ⭐
- ✅ Uthmanic Hafs V18
- ✅ Uthman TN
- ✅ Uthman TN1

#### 📐 خطوط كوفية (3):
- ✅ KFGQPC Kufi Extended
- ✅ KFGQPC Kufi Style
- ✅ DQ7 KFI

#### ✍️ خطوط أخرى (4):
- ✅ AlJalil
- ✅ AlJalil Dot (بالنقاط)
- ✅ KFGQPC An
- ✅ KFGQPC An Light

#### 🌐 خطوط ويب (3):
- ✅ Amiri
- ✅ Cairo
- ✅ Scheherazade

### **التحديثات:**
- ✅ قائمة منسدلة منظمة بمجموعات
- ✅ Uthmanic Hafs V22 كخط افتراضي
- ✅ دعم كامل لجميع الخطوط
- ✅ تحميل تلقائي للخطوط

---

## 📋 الإصدارات السابقة:

### **v1 - الإصدار الأولي**

```
https://github.com/mustafayakoub/duhatv/raw/claude/fresh-start-no-errors-011CUmiYSzwrefKsJhPgd5ay/duhatv-app.zip
```

**الحجم**: 46 KB
**المميزات**: التطبيق الأساسي + 40 آية

---

## 🚀 التثبيت السريع:

### **Windows:**

```powershell
# تحميل آخر إصدار
Invoke-WebRequest -Uri "https://github.com/mustafayakoub/duhatv/raw/claude/fresh-start-no-errors-011CUmiYSzwrefKsJhPgd5ay/duhatv-app-v2-fonts.zip" -OutFile "duhatv-v2.zip"

# فك الضغط
Expand-Archive -Path duhatv-v2.zip -DestinationPath duhatv-v2 -Force

# الدخول
cd duhatv-v2

# نسخ الخطوط (من مجلدك)
mkdir static\fonts
Copy-Item ..\data\Fonts\*.ttf static\fonts\
Copy-Item ..\data\Fonts\*.otf static\fonts\

# استيراد القرآن الكامل
python scripts\import_quran_smart.py --file ..\data\sources\quran_Ayat\hafs_smart_v8.json

# تشغيل
python app.py
```

### **Linux/Mac:**

```bash
# تحميل
wget https://github.com/mustafayakoub/duhatv/raw/claude/fresh-start-no-errors-011CUmiYSzwrefKsJhPgd5ay/duhatv-app-v2-fonts.zip

# فك الضغط
unzip duhatv-app-v2-fonts.zip -d duhatv-v2
cd duhatv-v2

# نسخ الخطوط
mkdir -p static/fonts
cp ../data/Fonts/*.ttf static/fonts/
cp ../data/Fonts/*.otf static/fonts/

# استيراد
python3 scripts/import_quran_smart.py --file ../data/sources/quran_Ayat/hafs_smart_v8.json

# تشغيل
python3 app.py
```

---

## 📊 المحتويات:

```
duhatv-app-v2-fonts.zip (51 KB)
├── app.py                          # Flask Backend
├── templates/
│   └── index.html                  # الواجهة (محدثة بـ 15 خط)
├── static/
│   ├── css/
│   │   └── style.css               # التصميم (@font-face مضاف)
│   ├── js/
│   │   └── app.js                  # JavaScript (دعم الخطوط)
│   └── fonts/                      # (فارغ - ستنسخ خطوطك)
├── databases/
│   └── AYAHS_DATABASE_ENHANCED.db  # 40 آية
├── scripts/
│   ├── import_quran_smart.py       # استيراد ذكي
│   ├── create_enhanced_ayahs_db.py # إنشاء القاعدة
│   └── verify_enhanced_db.py       # التحقق
├── README_APP.md                   # الدليل
└── DOWNLOAD.md                     # روابط التحميل
```

---

## ⚡ ملاحظات مهمة:

1. **الخطوط غير مضمّنة** في الملف المضغوط (لتقليل الحجم)
2. **انسخ خطوطك** من `data\Fonts` إلى `static\fonts`
3. **استورد القرآن الكامل** باستخدام السكريبت
4. **اختر الخط** من القائمة المنسدلة في التطبيق

---

## 🎯 الخطوات القادمة:

### **v3 - قريباً:**
- [ ] استيراد تلقائي للقرآن الكامل
- [ ] نسخ الآية بضغطة زر
- [ ] حفظ الإعدادات
- [ ] Favicon
- [ ] صفحة إحصائيات

---

## 🔄 تحديث من v1 إلى v2:

```powershell
# فقط استبدل الملفات:
Copy-Item duhatv-v2\templates\index.html templates\ -Force
Copy-Item duhatv-v2\static\css\style.css static\css\ -Force
Copy-Item duhatv-v2\static\js\app.js static\js\ -Force

# نسخ الخطوط
mkdir static\fonts
Copy-Item data\Fonts\*.ttf static\fonts\
Copy-Item data\Fonts\*.otf static\fonts\
```

---

## 📞 الدعم:

- **التوثيق الكامل**: README_APP.md
- **دليل التحميل**: DOWNLOAD.md
- **التحديثات**: هذا الملف (UPDATES.md)

---

## 🌟 الخلاصة:

**آخر إصدار**: v2 (51 KB)
**المميزات**: 15 خط قرآني + دعم كامل
**الرابط المباشر**: ⬇️

```
https://github.com/mustafayakoub/duhatv/raw/claude/fresh-start-no-errors-011CUmiYSzwrefKsJhPgd5ay/duhatv-app-v2-fonts.zip
```

**الحمد لله** 🤲

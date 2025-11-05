# 📋 تعليمات رفع الملفات وتشغيل التطبيق

## ✅ ما أحتاجه منك الآن:

### 1️⃣ **ملفات الآيات** (18 ملف)

ضع هذه الملفات في مجلد: `/home/user/duhatv/quran-clean/data/ayat/`

```
1. Ajami-.txt
2. AlAWWal.txt
3. Amiry-Mushakkal.txt
4. DouriData_v2-0.json
5. Emalei_-Mini_Mushakkal_fasel.txt
6. Emalei_-Mushakkal_fasel.txt
7. Emalei_-No-Mushakkal_fasel.txt
8. hafsData_v2-0.json
9. QalounData_v2-1.json
10. quran_text_with_tajweed.json
11. quran-simple-plain_-Mushakkal_Fasel.txt
12. quran-simple-plain_-Mushakkal_Tam.txt
13. quran-uthmani-min_-Mushakkal.txt
14. quran-uthmani-min_No_Mushakkel.txt
15. shubaData_v2-0.json
16. SousiData_v2-0.json
17. Transliteration_Latin.txt
18. warshData_v2-1.json
```

**كيفية النسخ:**

من Windows:
```cmd
# انسخ من C:\Qgo3\quran_Ayat\
# إلى /home/user/duhatv/quran-clean/data/ayat/
```

---

### 2️⃣ **ملف السور** (ملف Excel واحد)

ضع هذا الملف في مجلد: `/home/user/duhatv/quran-clean/data/surahs/`

```
suar_quran_Mustafa_Yakoub.xlsx
```

**المسار الكامل:**
```
/home/user/duhatv/quran-clean/data/surahs/suar_quran_Mustafa_Yakoub.xlsx
```

---

### 3️⃣ **ملفات الكلمات** (6 ملفات)

ضع هذه الملفات في مجلد: `/home/user/duhatv/quran-clean/data/words/`

```
1. quran_word Mustafa_Y2.txt
2. word_content_irab.json
3. word_content_meaning.json
4. word_content_rasm.json
5. word_content_sarf.json
6. word_statistics.json
```

**كيفية النسخ:**

```bash
# انسخ من C:\Qgo3\quran_word\
# إلى /home/user/duhatv/quran-clean/data/words/
```

---

### 4️⃣ **ملفات الخطوط** (16 خط)

ضع هذه الملفات في مجلدين:
1. `/home/user/duhatv/quran-clean/data/fonts/`
2. `/home/user/duhatv/quran-clean/static/fonts/`

```
1. Al Mushaf_pakistan.ttf
2. AlJalil_v01.ttf
3. AlJalilDot_v01.ttf
4. DQ7_KFI_M1.ttf
5. KFGQPCAnBold.ttf
6. KFGQPCAnExtra.ttf
7. KFGQPCAnLight.ttf
8. KFGQPCAnRegular.ttf
9. KFGQPC-KufiExtV14.ttf
10. KFGQPC-KufiStyV14.ttf
11. Magreb_rabat.ttf
12. uthmanic_hafs_v22.ttf
13. UthmanicHafs_V22.ttf
14. UthmanicHafs1 Ver18.ttf
15. UthmanTN_v2-0.ttf
16. UthmanTN1 Ver10.otf
17. UthmanTNB_v2-0.ttf
```

**كيفية النسخ:**

```bash
# انسخ من C:\Qgo3\Fonts\
# إلى /home/user/duhatv/quran-clean/data/fonts/
# و /home/user/duhatv/quran-clean/static/fonts/
```

---

## 🚀 خطوات التشغيل

### الخطوة 1: التأكد من وجود كل الملفات

```bash
cd /home/user/duhatv/quran-clean

# التحقق من ملفات الآيات
ls -l data/ayat/

# التحقق من ملف السور
ls -l data/surahs/

# التحقق من ملفات الكلمات
ls -l data/words/

# التحقق من الخطوط
ls -l data/fonts/
```

يجب أن ترى:
- ✅ 18 ملف في `data/ayat/`
- ✅ 1 ملف Excel في `data/surahs/`
- ✅ 6 ملفات في `data/words/`
- ✅ 16-17 خط في `data/fonts/`

---

### الخطوة 2: تثبيت المتطلبات

```bash
pip install flask openpyxl
```

**الحزم المطلوبة:**
- `flask` - لتشغيل الخادم
- `openpyxl` - لقراءة ملف Excel

---

### الخطوة 3: استيراد البيانات

```bash
cd /home/user/duhatv/quran-clean
python import_data.py
```

**سيستغرق:** 5-10 دقائق

**ما سيحدث:**
1. ✅ إنشاء قاعدة البيانات `quran.db`
2. ✅ استيراد 114 سورة
3. ✅ استيراد ~6,236 آية × 18 نمط
4. ✅ استيراد 77,432 كلمة
5. ✅ استيراد التفاصيل (إعراب، صرف، معاني)

---

### الخطوة 4: تشغيل التطبيق

```bash
python app.py
```

سترى:
```
╔══════════════════════════════════════════════════════════╗
║         📖 Quran Clean - التطبيق القرآني النظيف       ║
╚══════════════════════════════════════════════════════════╝

🚀 التطبيق يعمل على: http://127.0.0.1:5000
📖 افتح المتصفح واذهب إلى العنوان أعلاه

💡 للإيقاف: اضغط Ctrl+C
```

---

### الخطوة 5: فتح التطبيق

افتح المتصفح واذهب إلى:
```
http://127.0.0.1:5000
```

أو:
```
http://localhost:5000
```

---

## 🎨 استخدام التطبيق

### 1. اختيار السورة
- اختر سورة من القائمة المنسدلة
- سيتم عرض الآيات تلقائياً

### 2. اختيار النمط/القراءة
يمكنك الاختيار من:
- الرسم الأول
- الرسم العثماني الكامل ⭐
- قراءة حفص
- قراءة ورش
- قراءة قالون
- ... (18 خيار في المجموع)

### 3. تخصيص الخط
- اختر خطاً من القائمة
- غيّر الحجم باستخدام المؤشر

### 4. البحث
اضغط على 🔍 للبحث:
- بحث نصي
- بحث بالجذر
- بحث بالإعراب
- بحث بالمعنى

### 5. تفاصيل الكلمات
- انقر على أي كلمة
- سيظهر:
  - الإعراب
  - الصرف
  - المعنى
  - الرسم القرآني

---

## 🔧 حل المشاكل

### المشكلة: "ملف السور غير موجود"

```bash
# تحقق من المسار
ls /home/user/duhatv/quran-clean/data/surahs/suar_quran_Mustafa_Yakoub.xlsx
```

إذا لم يكن موجوداً، انسخه من:
```
C:\Qgo3\quran_suar\suar_quran_Mustafa_Yakoub.xlsx
```

---

### المشكلة: "openpyxl غير مثبت"

```bash
pip install openpyxl
```

---

### المشكلة: "فشل تحميل السور"

تأكد أن:
1. ✅ تم تشغيل `import_data.py` بنجاح
2. ✅ ملف `quran.db` موجود
3. ✅ لا توجد أخطاء في السكريبت

---

### المشكلة: "النص لا يظهر"

1. تحقق من وجود ملفات txt/json في `data/ayat/`
2. تأكد أن الملفات بصيغة UTF-8
3. جرب نمطاً مختلفاً من القائمة

---

### المشكلة: "الخط لا يظهر بشكل صحيح"

1. تحقق من نسخ الخطوط إلى:
   - `data/fonts/`
   - `static/fonts/`
2. جرب خطاً آخر من القائمة

---

## 📊 البنية النهائية للملفات

```
quran-clean/
├── data/
│   ├── ayat/                  (18 ملف) ✅
│   ├── surahs/                (1 ملف Excel) ✅
│   ├── words/                 (6 ملفات) ✅
│   └── fonts/                 (16 خط) ✅
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── fonts/                 (16 خط) ✅
│
├── templates/
│   └── index.html
│
├── app.py
├── import_data.py
├── schema.sql
├── quran.db                   (يتم إنشاؤه) ⭐
├── README.md
└── INSTRUCTIONS.md            (هذا الملف)
```

---

## ✅ Checklist

- [ ] نسخ 18 ملف إلى `data/ayat/`
- [ ] نسخ ملف Excel إلى `data/surahs/`
- [ ] نسخ 6 ملفات إلى `data/words/`
- [ ] نسخ الخطوط إلى `data/fonts/` و `static/fonts/`
- [ ] تثبيت flask و openpyxl
- [ ] تشغيل `import_data.py`
- [ ] التحقق من وجود `quran.db`
- [ ] تشغيل `app.py`
- [ ] فتح المتصفح على http://localhost:5000

---

## 📞 للمساعدة

إذا واجهت أي مشاكل:

1. تحقق من وجود جميع الملفات
2. تأكد من تثبيت المتطلبات
3. راجع رسائل الأخطاء في Terminal
4. اقرأ هذا الملف من جديد

---

**بالتوفيق! 🚀**

"إِنَّ هَٰذَا الْقُرْآنَ يَهْدِي لِلَّتِي هِيَ أَقْوَمُ" (الإسراء: 9)

# 📖 Quran Clean - تطبيق القرآن الكريم النظيف

تطبيق قرآني بسيط وأنيق وعصري مع كل القراءات والأنماط والعلوم القرآنية.

## 🚀 التشغيل السريع

### 1️⃣ رفع الملفات

ضع الملفات التالية في المجلدات المناسبة:

```bash
# ملفات الآيات (18 ملف)
data/ayat/
  ├── Ajami-.txt
  ├── AlAWWal.txt
  ├── Amiry-Mushakkal.txt
  ├── DouriData_v2-0.json
  ├── Emalei_-Mini_Mushakkal_fasel.txt
  ├── Emalei_-Mushakkal_fasel.txt
  ├── Emalei_-No-Mushakkal_fasel.txt
  ├── hafsData_v2-0.json
  ├── QalounData_v2-1.json
  ├── quran_text_with_tajweed.json
  ├── quran-simple-plain_-Mushakkal_Fasel.txt
  ├── quran-simple-plain_-Mushakkal_Tam.txt
  ├── quran-uthmani-min_-Mushakkal.txt
  ├── quran-uthmani-min_No_Mushakkel.txt
  ├── shubaData_v2-0.json
  ├── SousiData_v2-0.json
  ├── Transliteration_Latin.txt
  └── warshData_v2-1.json

# ملف السور
data/surahs/
  └── suar_quran_Mustafa_Yakoub.xlsx

# ملفات الكلمات
data/words/
  ├── quran_word Mustafa_Y2.txt
  ├── word_content_irab.json
  ├── word_content_meaning.json
  ├── word_content_rasm.json
  ├── word_content_sarf.json
  └── word_statistics.json

# الخطوط
data/fonts/
  ├── Al Mushaf_pakistan.ttf
  ├── AlJalil_v01.ttf
  ├── AlJalilDot_v01.ttf
  └── ... (باقي الخطوط)
```

### 2️⃣ تثبيت المتطلبات

```bash
pip install flask openpyxl
```

### 3️⃣ استيراد البيانات إلى قاعدة البيانات

```bash
python import_data.py
```

⏱️ سيستغرق 5-10 دقائق

### 4️⃣ تشغيل التطبيق

```bash
python app.py
```

ثم افتح: http://localhost:5000

---

## 📁 هيكل المشروع

```
quran-clean/
├── app.py                 # Flask backend
├── import_data.py         # سكريبت استيراد البيانات
├── schema.sql             # بنية قاعدة البيانات
├── quran.db               # قاعدة البيانات (يتم إنشاؤها)
├── data/                  # الملفات المصدرية
│   ├── ayat/             # ملفات الآيات (18 ملف)
│   ├── surahs/           # ملف السور (Excel)
│   ├── words/            # ملفات الكلمات (6 ملفات)
│   └── fonts/            # الخطوط (16 خط)
├── static/
│   ├── css/
│   │   └── style.css     # التصميم الأنيق
│   ├── js/
│   │   └── app.js        # JavaScript
│   └── fonts/            # نسخة الخطوط للويب
└── templates/
    └── index.html        # الواجهة

```

---

## ✨ الميزات

- ✅ **18 قراءة ونمط** في قائمة واحدة سهلة
- ✅ **قاعدة بيانات بسيطة** جداً ومترابطة
- ✅ **واجهة أنيقة عصرية** بأزرار صغيرة لطيفة
- ✅ **16 خط قرآني** قابل للتخصيص
- ✅ **بحث متقدم** (نص، جذور، إعراب، معاني)
- ✅ **إعراب وصرف** لكل كلمة
- ✅ **معاني الكلمات** والرسم القرآني
- ✅ **إحصائيات** شاملة

---

## 🎨 التصميم

- ألوان هادئة وواضحة
- أزرار دائرية صغيرة
- ظلال ناعمة
- خط واضح كبير للقراءة
- responsive design

---

## 📊 قاعدة البيانات

### جداول:
1. **surahs** - السور (114 سورة)
2. **ayahs** - الآيات (6236 آية × 18 نمط)
3. **words** - الكلمات (77432 كلمة)
4. **word_details** - تفاصيل الكلمات (إعراب، صرف، معاني)

### بسيطة ومترابطة:
```sql
ayahs.surah_id → surahs.id
words.surah_id + words.ayah_id → ayahs.surah_id + ayahs.ayah_id
word_details.word_id → words.id
```

---

## 🔍 البحث

1. **بحث نصي** - ابحث في أي قراءة أو نمط
2. **بحث بالجذور** - ابحث عن كلمات من نفس الجذر
3. **بحث بالإعراب** - ابحث حسب الموقع الإعرابي
4. **بحث بالمعاني** - ابحث في معاني الكلمات

---

## 🛠️ التطوير

### تعديل التصميم:
```bash
# عدّل: static/css/style.css
```

### إضافة ميزة جديدة:
```bash
# Backend: app.py
# Frontend: static/js/app.js
```

### تحديث البيانات:
```bash
# ضع الملفات الجديدة في data/
# شغّل: python import_data.py
```

---

## 📞 الدعم

أي مشاكل؟ تحقق من:
1. وجود كل الملفات في `data/`
2. تثبيت المتطلبات
3. تشغيل `import_data.py` بنجاح

---

**بُني بـ ❤️ باستخدام Python + Flask**

"إِنَّ هَٰذَا الْقُرْآنَ يَهْدِي لِلَّتِي هِيَ أَقْوَمُ" (الإسراء: 9)

# 📦 دليل الحصول على قاعدة بيانات القرآن الكريم

## ⚠️ **المشكلة:**

التطبيق يعمل ولكنه يحتاج إلى ملف `quran.db` لعرض البيانات.

---

## ✅ **الحلول المتاحة:**

### **الحل 1: إنشاء قاعدة بيانات تجريبية (للاختبار)**

إذا كنت تريد فقط اختبار التطبيق:

```bash
python create_demo_db.py
```

**ما سيحدث:**
- ✅ ينشئ ملف `quran.db` تجريبي
- ✅ يحتوي على سورة الفاتحة كاملة
- ✅ يحتوي على 3 آيات من سورة البقرة
- ✅ يحتوي على تفسير الفاتحة

**ملاحظة:** هذه قاعدة بيانات محدودة للاختبار فقط!

---

### **الحل 2: البحث عن قاعدة بيانات موجودة**

إذا كان لديك قاعدة بيانات من قبل:

**في PowerShell:**

```powershell
# البحث في كل المحرك C:
Get-ChildItem -Path C:\ -Recurse -Filter "*.db" -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "*quran*" }
```

**أو البحث في مجلد محدد:**

```powershell
Get-ChildItem -Path C:\QYRAN5 -Recurse -Filter "*.db" -ErrorAction SilentlyContinue
```

**إذا وجدت الملف:**
- انسخه إلى مجلد التطبيق: `C:\QYRAN5\‏‏‏‏QYRAN62\`
- تأكد أن اسمه `quran.db`

---

### **الحل 3: تحميل قاعدة بيانات كاملة**

#### **🌟 المصادر الموصى بها:**

#### **1. Tanzil.net (موصى به جداً)**

**الموقع:** https://tanzil.net/download/

**الخطوات:**
1. اذهب للموقع
2. اختر **"Database"** من القائمة
3. حمّل **"Quran Text (with Tajweed)"** بصيغة SQLite
4. أعد تسمية الملف إلى `quran.db`
5. ضعه في مجلد التطبيق

---

#### **2. Quran.com API**

**GitHub:** https://github.com/quran/quran.com-api

**الخطوات:**
1. ابحث عن **"database exports"** أو **"SQLite dumps"**
2. حمّل الملف
3. أعد تسميته إلى `quran.db`

---

#### **3. Islamic Network**

**موقع:** https://alquran.cloud/

**GitHub:** https://github.com/islamic-network

يوفرون API وقواعد بيانات جاهزة.

---

#### **4. Zekr Project**

**موقع:** https://zekr.org/

يحتوي على قواعد بيانات قرآنية كاملة.

---

### **الحل 4: قواعد بيانات محلية عربية**

ابحث في المواقع العربية:
- مشروع المصحف الإلكتروني
- مشروع نور القرآن
- موقع تفسير

---

## 📋 **البنية المطلوبة لقاعدة البيانات:**

التطبيق يبحث عن الجداول والأعمدة التالية:

### **الجدول الرئيسي (مطلوب):**

```sql
CREATE TABLE quran_text_with_tajweed (
    surahNo INTEGER,      -- رقم السورة (1-114)
    ayahNo INTEGER,       -- رقم الآية
    tajweedText TEXT,     -- نص الآية مع رموز التجويد
    PRIMARY KEY (surahNo, ayahNo)
);
```

### **جداول اختيارية (لعرض التفاسير):**

```sql
-- التفسير الميسر
CREATE TABLE tafsir_moyassar (
    surahNo INTEGER,
    ayahNo INTEGER,
    text TEXT,
    PRIMARY KEY (surahNo, ayahNo)
);

-- تفسير السعدي
CREATE TABLE tafsir_saadi (
    surahNo INTEGER,
    ayahNo INTEGER,
    text TEXT,
    PRIMARY KEY (surahNo, ayahNo)
);

-- تفسير البغوي
CREATE TABLE tafsir_baghawi (
    surahNo INTEGER,
    ayahNo INTEGER,
    text TEXT,
    PRIMARY KEY (surahNo, ayahNo)
);
```

### **جداول اختيارية أخرى:**

- `translation_en` - الترجمة الإنجليزية
- `translation_fr` - الترجمة الفرنسية
- `ayah_content_irab` - الإعراب
- جداول الصرف
- جداول الموضوعات

---

## 🔍 **التحقق من قاعدة البيانات:**

بعد الحصول على الملف، تحقق من بنيته:

```python
import sqlite3

conn = sqlite3.connect('quran.db')
cursor = conn.cursor()

# عرض جميع الجداول
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("الجداول الموجودة:")
for table in tables:
    print(f"  - {table[0]}")

# عرض أعمدة الجدول الرئيسي
cursor.execute("PRAGMA table_info(quran_text_with_tajweed)")
columns = cursor.fetchall()

print("\nأعمدة quran_text_with_tajweed:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

conn.close()
```

---

## 🎯 **الخطوات النهائية:**

بعد الحصول على قاعدة البيانات:

1. ✅ تأكد أن اسم الملف `quran.db` بالضبط
2. ✅ ضعه في نفس مجلد التطبيق
3. ✅ شغّل التطبيق:

```bash
python quran_app_v3_ultimate.py
```

أو:

```bash
RUN_APP_V3.bat
```

---

## 💡 **نصائح:**

1. **التطبيق ذكي:** يكتشف بنية قاعدة البيانات تلقائياً
2. **أسماء الأعمدة مرنة:** يدعم أسماء مختلفة (surahNo, surah_id, sora, ...)
3. **الجداول الاختيارية:** إذا لم توجد، سيعرض "غير متاح"
4. **قاعدة البيانات التجريبية:** جيدة للاختبار السريع

---

## 🆘 **حل المشاكل:**

### **التطبيق لا يجد قاعدة البيانات؟**
- تأكد أن الاسم `quran.db` بالضبط (حساس لحالة الأحرف)
- تأكد أنه في نفس مجلد `quran_app_v3_ultimate.py`

### **يعرض "لا يوجد تفسير"؟**
- قاعدة البيانات قد لا تحتوي على جداول التفسير
- حاول قاعدة بيانات أخرى تحتوي على تفاسير

### **الآيات فارغة؟**
- تحقق من بنية الجدول الرئيسي
- استخدم السكريبت أعلاه للتحقق من الأعمدة

---

## 📞 **المساعدة:**

إذا واجهت مشاكل:
1. جرّب قاعدة البيانات التجريبية أولاً
2. راجع ملف `WHATS_NEW_V3.txt`
3. راجع ملف `README_V3.md`

---

**بالتوفيق! 🚀**

التطبيق جاهز، فقط يحتاج قاعدة البيانات!

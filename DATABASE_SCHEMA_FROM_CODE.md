# 📊 تقرير دقيق: أسماء الجداول والأعمدة المستخدمة في الكود

## 🎯 تم استخراج هذه الأسماء من: `quran_app_ultimate_final_v4.py`

---

## 📋 الجداول المطلوبة (بالترتيب حسب الأهمية)

### ✅ الجدول 1: `surahs_info`
**الوصف:** معلومات السور (114 سورة)

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY | ✅ | رقم السورة (1-114) |
| `name_ar` | TEXT | ✅ | اسم السورة بالعربية |
| `ayahs_count` | INTEGER | ✅ | عدد الآيات |
| `type` | TEXT | ✅ | نوع السورة ('makkiyah' أو 'madaniyah') |
| `name_en` | TEXT | ⬜ | اسم السورة بالإنجليزية |
| `revelation_order` | INTEGER | ⬜ | ترتيب النزول |

**الاستعلام المستخدم في الكود:**
```sql
SELECT id, name_ar, ayahs_count, type
FROM surahs_info
ORDER BY id
```

---

### ✅ الجدول 2: `quran_text`
**الوصف:** النص القرآني الأساسي (6236 آية)

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف فريد |
| `surah_id` | INTEGER | ✅ | رقم السورة (1-114) |
| `ayah_id` | INTEGER | ✅ | رقم الآية في السورة |
| `text` | TEXT | ✅ | النص القرآني الكامل (مع التشكيل) |
| `text_simple` | TEXT | ⚠️ | النص بدون تشكيل (للبحث) |
| `juz` | INTEGER | ⚠️ | رقم الجزء (1-30) |
| `page` | INTEGER | ⚠️ | رقم الصفحة (1-604 في مصحف المدينة) |

**قيود:**
- `UNIQUE(surah_id, ayah_id)`
- `FOREIGN KEY (surah_id) REFERENCES surahs_info(id)`

**الاستعلامات المستخدمة:**
```sql
-- جلب آيات سورة
SELECT surah_id, ayah_id, text, text_simple, juz, page
FROM quran_text
WHERE surah_id = ?
ORDER BY ayah_id

-- جلب آية محددة
SELECT text, text_simple, juz, page
FROM quran_text
WHERE surah_id = ? AND ayah_id = ?

-- البحث
SELECT surah_id, ayah_id, text, text_simple
FROM quran_text
WHERE text_simple LIKE ?
ORDER BY surah_id, ayah_id
LIMIT ?
```

---

### ✅ الجدول 3: `quran_tajweed`
**الوصف:** النص القرآني مع رموز التجويد الملونة

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف فريد |
| `surah_id` | INTEGER | ✅ | رقم السورة |
| `ayah_id` | INTEGER | ✅ | رقم الآية |
| `tajweed_text` | TEXT | ✅ | النص مع رموز XML للتجويد |

**قيود:**
- `UNIQUE(surah_id, ayah_id)`
- `FOREIGN KEY (surah_id) REFERENCES surahs_info(id)`

**صيغة رموز التجويد:**
```xml
<1>إِظْهَارٌ</1>    <!-- إظهار -->
<2>إِدْغَامٌ</2>    <!-- إدغام -->
<4>مَدٌّ</4>         <!-- مد -->
<5>قَلْقَلَةٌ</5>    <!-- قلقلة -->
<7>غُنَّةٌ</7>       <!-- غنة -->
<12>إِخْفَاءٌ</12>  <!-- إخفاء -->
```

**الاستعلام المستخدم:**
```sql
SELECT surah_id, ayah_id, tajweed_text as text
FROM quran_tajweed
WHERE surah_id = ?
ORDER BY ayah_id
```

---

### ✅ الجدول 4: `tafsir_muyassar`
**الوصف:** التفسير الميسر

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف فريد |
| `surah_id` | INTEGER | ✅ | رقم السورة |
| `ayah_id` | INTEGER | ✅ | رقم الآية |
| `text` | TEXT | ✅ | نص التفسير |

**قيود:**
- `UNIQUE(surah_id, ayah_id)`
- `FOREIGN KEY (surah_id) REFERENCES surahs_info(id)`

**الاستعلام المستخدم:**
```sql
SELECT text
FROM tafsir_muyassar
WHERE surah_id = ? AND ayah_id = ?
```

---

### ✅ الجدول 5: `tafsir_saadi`
**الوصف:** تفسير السعدي

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف فريد |
| `surah_id` | INTEGER | ✅ | رقم السورة |
| `ayah_id` | INTEGER | ✅ | رقم الآية |
| `text` | TEXT | ✅ | نص التفسير |

**قيود:** نفس tafsir_muyassar

**الاستعلام:** نفس tafsir_muyassar

---

### ✅ الجدول 6: `tafsir_baghawi`
**الوصف:** تفسير البغوي

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف فريد |
| `surah_id` | INTEGER | ✅ | رقم السورة |
| `ayah_id` | INTEGER | ✅ | رقم الآية |
| `text` | TEXT | ✅ | نص التفسير |

**قيود:** نفس tafsir_muyassar

**الاستعلام:** نفس tafsir_muyassar

---

### ⚠️ الجدول 7: `tafsir_jalalayn`
**الوصف:** تفسير الجلالين (اختياري لكن مهم)

**نفس هيكل التفاسير السابقة**

---

### ⚠️ الجدول 8: `tafsir_tabari`
**الوصف:** تفسير الطبري (اختياري)

**نفس هيكل التفاسير السابقة**

**ملاحظة:** قد يحتوي ayah_id = 0 لمقدمات السور

---

### ✅ الجدول 9: `translation_english`
**الوصف:** الترجمة الإنجليزية

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف فريد |
| `surah_id` | INTEGER | ✅ | رقم السورة |
| `ayah_id` | INTEGER | ✅ | رقم الآية |
| `text` | TEXT | ✅ | النص المترجم |
| `translator` | TEXT | ⬜ | اسم المترجم (مثل: Sahih International) |

**قيود:** نفس quran_text

**الاستعلام:**
```sql
SELECT text
FROM translation_english
WHERE surah_id = ? AND ayah_id = ?
```

---

### ✅ الجدول 10: `translation_french`
**الوصف:** الترجمة الفرنسية

**نفس هيكل translation_english**

---

### ⚠️ الجدول 11: `irab`
**الوصف:** الإعراب النحوي

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف فريد |
| `surah_id` | INTEGER | ✅ | رقم السورة |
| `ayah_id` | INTEGER | ✅ | رقم الآية |
| `text` | TEXT | ✅ | نص الإعراب |

**الاستعلام:**
```sql
SELECT text
FROM irab
WHERE surah_id = ? AND ayah_id = ?
```

---

### ⚠️ الجدول 12: `sarf`
**الوصف:** التحليل الصرفي

**نفس هيكل irab**

---

### ⚠️ الجدول 13: `topics`
**الوصف:** الموضوعات القرآنية

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف الموضوع |
| `topic_name` | TEXT | ✅ | اسم الموضوع |
| `topic_category` | TEXT | ⬜ | التصنيف الرئيسي |
| `description` | TEXT | ⬜ | وصف الموضوع |

**الاستعلام:**
```sql
SELECT id, topic_name, topic_category, description
FROM topics
ORDER BY id
```

---

### ⚠️ الجدول 14: `topics_verses`
**الوصف:** ربط الموضوعات بالآيات

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف |
| `topic_id` | INTEGER | ✅ | معرف الموضوع |
| `surah_id` | INTEGER | ✅ | رقم السورة |
| `ayah_id` | INTEGER | ✅ | رقم الآية |
| `relevance` | INTEGER | ⬜ | درجة الصلة (1-10) |

**قيود:**
- `UNIQUE(topic_id, surah_id, ayah_id)`
- `FOREIGN KEY (topic_id) REFERENCES topics(id)`
- `FOREIGN KEY (surah_id) REFERENCES surahs_info(id)`

**الاستعلام:**
```sql
SELECT tv.surah_id, tv.ayah_id, qt.text
FROM topics_verses tv
JOIN quran_text qt ON tv.surah_id = qt.surah_id AND tv.ayah_id = qt.ayah_id
WHERE tv.topic_id = ?
ORDER BY tv.relevance DESC, tv.surah_id, tv.ayah_id
```

---

### ✅ الجدول 15: `bookmarks`
**الوصف:** العلامات المرجعية للمستخدم

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف |
| `surah_id` | INTEGER | ✅ | رقم السورة |
| `ayah_id` | INTEGER | ✅ | رقم الآية |
| `note` | TEXT | ⬜ | ملاحظة المستخدم |
| `created_at` | DATETIME | ⬜ | تاريخ الإنشاء |
| `color` | TEXT | ⬜ | لون العلامة |
| `category` | TEXT | ⬜ | التصنيف |

**الاستعلامات:**
```sql
-- جلب العلامات
SELECT id, surah_id, ayah_id, note, created_at, color, category
FROM bookmarks
ORDER BY created_at DESC

-- إضافة علامة
INSERT INTO bookmarks (surah_id, ayah_id, note, created_at)
VALUES (?, ?, ?, ?)

-- حذف علامة
DELETE FROM bookmarks WHERE id = ?
```

---

### ✅ الجدول 16: `user_settings`
**الوصف:** إعدادات المستخدم

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف |
| `setting_key` | TEXT | ✅ | مفتاح الإعداد (UNIQUE) |
| `setting_value` | TEXT | ✅ | قيمة الإعداد |
| `updated_at` | DATETIME | ⬜ | تاريخ التحديث |

**الإعدادات المستخدمة:**
- `last_surah` - آخر سورة (قيمة: "1" إلى "114")
- `last_ayah` - آخر آية
- `font_size` - حجم الخط
- `show_tajweed` - عرض التجويد ("true" أو "false")
- `theme` - السمة

**الاستعلامات:**
```sql
-- جلب إعداد
SELECT setting_value
FROM user_settings
WHERE setting_key = ?

-- حفظ إعداد
INSERT OR REPLACE INTO user_settings (setting_key, setting_value, updated_at)
VALUES (?, ?, ?)
```

---

### ⬜ الجدول 17: `sajda_ayahs`
**الوصف:** آيات السجدة (15 آية)

| اسم العمود | النوع | NOT NULL | الوصف |
|------------|-------|----------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ✅ | معرف |
| `surah_id` | INTEGER | ✅ | رقم السورة |
| `ayah_id` | INTEGER | ✅ | رقم الآية |
| `sajda_type` | TEXT | ✅ | نوع السجدة ('واجبة' أو 'مستحبة') |
| `sajda_number` | INTEGER | ✅ | رقم السجدة (1-15) |

**الاستعلام:**
```sql
SELECT surah_id, ayah_id, sajda_type, sajda_number
FROM sajda_ayahs
ORDER BY sajda_number
```

---

## 📊 ملخص الجداول

| # | اسم الجدول | الأولوية | عدد الأعمدة | الوصف |
|---|------------|---------|-------------|-------|
| 1 | `surahs_info` | ✅ ضروري | 6 | معلومات السور |
| 2 | `quran_text` | ✅ ضروري | 7 | النص القرآني |
| 3 | `quran_tajweed` | ⚠️ مهم | 4 | النص بالتجويد |
| 4 | `tafsir_muyassar` | ✅ ضروري | 4 | التفسير الميسر |
| 5 | `tafsir_saadi` | ⚠️ مهم | 4 | تفسير السعدي |
| 6 | `tafsir_baghawi` | ⚠️ مهم | 4 | تفسير البغوي |
| 7 | `tafsir_jalalayn` | ⬜ اختياري | 4 | تفسير الجلالين |
| 8 | `tafsir_tabari` | ⬜ اختياري | 4 | تفسير الطبري |
| 9 | `translation_english` | ⚠️ مهم | 5 | الترجمة الإنجليزية |
| 10 | `translation_french` | ⬜ اختياري | 5 | الترجمة الفرنسية |
| 11 | `irab` | ⬜ اختياري | 4 | الإعراب |
| 12 | `sarf` | ⬜ اختياري | 4 | الصرف |
| 13 | `topics` | ⚠️ مهم | 4 | الموضوعات |
| 14 | `topics_verses` | ⚠️ مهم | 5 | ربط موضوعات-آيات |
| 15 | `bookmarks` | ✅ ضروري | 7 | العلامات المرجعية |
| 16 | `user_settings` | ✅ ضروري | 4 | الإعدادات |
| 17 | `sajda_ayahs` | ⬜ اختياري | 5 | آيات السجدة |

**المجموع: 17 جدول**

---

## 🎯 خطوات العمل التالية

### 1. جهّز البيانات بهذه الأسماء بالضبط
قم بإنشاء ملفات نصية (CSV أو TEXT) بنفس الأسماء:

```
surahs_info.csv
quran_text.csv
quran_tajweed.csv
tafsir_muyassar.csv
... إلخ
```

### 2. استخدم سكريبت SQL لإنشاء القاعدة
سأقدم لك سكريبتاً دقيقاً بناءً على هذه الأسماء

### 3. استورد البيانات
سأساعدك في كتابة سكريبت استيراد Python

---

## 📧 معلومات الاتصال
- **البريد:** duhatv@gmail.com
- **الموقع:** duhatv.net
- **الهاتف:** +905342390000

---

✅ **هذا التقرير دقيق 100% ومستخرج من الكود الفعلي**

# 📥 دليل استيراد البيانات
## Data Import Guide

---

## 🎯 نظرة عامة

هذا الدليل يشرح كيفية استيراد بياناتك من قواعد بيانات SQLite الموجودة إلى قاعدة البيانات PostgreSQL الهرمية الجديدة.

---

## 🔧 الأدوات المتاحة

### 1️⃣ **explore_sqlite.py** - أداة الاستكشاف
استكشاف قاعدة بيانات SQLite وعرض بنيتها بالتفصيل.

```bash
# استكشاف قاعدة بيانات
python3 explore_sqlite.py /path/to/database.db

# عرض عينة من البيانات
python3 explore_sqlite.py /path/to/database.db --sample

# استكشاف جدول معين
python3 explore_sqlite.py /path/to/database.db --table quran

# تصدير البنية إلى JSON
python3 explore_sqlite.py /path/to/database.db --export schema.json
```

**الفوائد:**
- 🔍 كشف تلقائي لجداول القرآن
- 📊 عرض إحصائيات تفصيلية
- 📋 عرض الأعمدة والفهارس
- 💾 تصدير البنية إلى JSON

---

### 2️⃣ **import_from_sqlite.py** - الاستيراد البسيط
استيراد سريع وبسيط للسور والآيات.

```python
# تعديل المسار في الملف
SQLITE_DB_PATH = r"/path/to/your/quran.db"

# تشغيل
python3 import_from_sqlite.py
```

**المميزات:**
- ✅ كشف تلقائي لأسماء الجداول
- ✅ تعيين ذكي للأعمدة
- ✅ معالجة دفعية للأداء
- ✅ تقارير تقدم مباشرة

---

### 3️⃣ **import_advanced.py** - الاستيراد المتقدم
استيراد شامل مع تكوين كامل ومرن.

#### الخطوة 1: إنشاء ملف التكوين

```bash
# نسخ القالب
cp import_config.template.json import_config.json

# تعديل التكوين
nano import_config.json
```

#### الخطوة 2: تعديل التكوين

```json
{
  "sqlite": {
    "database_path": "/home/user/quran.db"
  },

  "postgresql": {
    "host": "localhost",
    "database": "quran_hierarchical_db",
    "user": "postgres",
    "password": "your_password"
  },

  "table_mappings": {
    "surahs": {
      "enabled": true,
      "source_table": "suras",
      "column_mapping": {
        "id": "sur_id",
        "name_ar": "sur_name_ar",
        "name_en": "sur_name_en"
      }
    }
  }
}
```

#### الخطوة 3: التشغيل

```bash
python3 import_advanced.py --config import_config.json
```

**المميزات:**
- 🎛️ تكوين مرن عبر JSON
- 🔄 تعيين مخصص للأعمدة
- ✅ قواعد التحقق من الصحة
- 🔀 تحويل البيانات التلقائي
- 📊 إحصائيات تفصيلية

---

## 📖 سيناريوهات الاستخدام

### السيناريو 1: لديك قاعدة بيانات بسيطة

```bash
# 1. استكشف قاعدتك أولاً
python3 explore_sqlite.py /path/to/quran.db

# 2. استخدم الاستيراد البسيط
# عدّل المسار في import_from_sqlite.py ثم:
python3 import_from_sqlite.py
```

---

### السيناريو 2: لديك قاعدة معقدة بجداول متعددة

```bash
# 1. استكشف البنية
python3 explore_sqlite.py /path/to/quran.db --export schema.json

# 2. افحص الجداول المتاحة
cat schema.json

# 3. أنشئ ملف تكوين مخصص
cp import_config.template.json import_config.json

# 4. عدّل التكوين حسب بنية قاعدتك

# 5. نفّذ الاستيراد المتقدم
python3 import_advanced.py
```

---

### السيناريو 3: لديك عدة قواعد بيانات

```bash
# استيراد السور والآيات من قاعدة
python3 import_advanced.py --config config_quran.json

# استيراد الترجمات من قاعدة أخرى
python3 import_advanced.py --config config_translations.json

# استيراد التفاسير من قاعدة ثالثة
python3 import_advanced.py --config config_tafsir.json
```

---

## 🗺️ تعيين الأعمدة (Column Mapping)

### قواعد التعيين

تستطيع تعيين أعمدة قاعدتك إلى أعمدة قاعدة PostgreSQL:

```json
"column_mapping": {
  "اسم_العمود_في_SQLite": "اسم_العمود_في_PostgreSQL"
}
```

### أمثلة شائعة

#### السور (Surahs)

| SQLite | PostgreSQL |
|--------|------------|
| `sura` / `id` / `number` | `sur_id` |
| `name` / `name_arabic` | `sur_name_ar` |
| `english_name` / `name_en` | `sur_name_en` |
| `ayah_count` / `ayas` | `sur_ayah_count` |
| `type` / `revelation` | `sur_revelation_type` |

#### الآيات (Ayahs)

| SQLite | PostgreSQL |
|--------|------------|
| `sura` / `surah` | `aya_sur_id` |
| `aya` / `ayah` / `verse` | `aya_number` |
| `text` / `text_uthmani` | `aya_text_uthmani` |
| `text_simple` / `text_plain` | `aya_text_simple` |
| `juz` / `juz_number` | `aya_juz` |
| `page` / `page_number` | `aya_page` |

#### الكلمات (Words)

| SQLite | PostgreSQL |
|--------|------------|
| `sura` | `wrd_sur_id` |
| `aya` | `wrd_aya_number` |
| `position` | `wrd_position` |
| `text` | `wrd_text_uthmani` |
| `root` | `wrd_root` |

---

## ✅ التحقق من الصحة

### قواعد مدمجة

```json
"validation_rules": {
  "surahs": {
    "sur_id": {
      "min": 1,
      "max": 114,
      "required": true
    }
  },
  "ayahs": {
    "aya_text_uthmani": {
      "min_length": 1,
      "required": true
    }
  }
}
```

### قواعد مخصصة

يمكنك إضافة قواعد التحقق الخاصة بك:

```json
"validation_rules": {
  "translations": {
    "tra_language_code": {
      "required": true,
      "allowed_values": ["ara", "eng", "urd", "fra"]
    },
    "tra_text": {
      "min_length": 10,
      "max_length": 5000,
      "required": true
    }
  }
}
```

---

## 🔄 تحويل البيانات

### التحويلات التلقائية

```json
"data_transformations": {
  "revelation_type": {
    "مكية": "meccan",
    "مدنية": "medinan",
    "Meccan": "meccan",
    "Medinan": "medinan"
  },

  "language_codes": {
    "ar": "ara",
    "en": "eng",
    "arabic": "ara",
    "english": "eng"
  }
}
```

### إضافة تحويلات مخصصة

```json
"data_transformations": {
  "qiraat_type": {
    "hafs": "hafs_an_asim",
    "warsh": "warsh_an_nafi",
    "qalun": "qalun_an_nafi"
  }
}
```

---

## 📊 الأداء والتحسين

### نصائح للأداء

1. **حجم الدفعة (Batch Size)**
```json
"import_options": {
  "batch_size": 500  // زِد للبيانات الكبيرة
}
```

2. **تعطيل الفهارس مؤقتاً**
```sql
-- قبل الاستيراد
DROP INDEX IF EXISTS quran.idx_ayah_search;

-- بعد الاستيراد
CREATE INDEX idx_ayah_search ON quran.ayahs
USING GIN (aya_text_search);
```

3. **رفع حدود PostgreSQL**
```sql
-- رفع work_mem للاستيراد
SET work_mem = '256MB';
SET maintenance_work_mem = '1GB';
```

---

## ❓ استكشاف الأخطاء

### خطأ: "table does not exist"

**السبب:** اسم الجدول في التكوين غير صحيح

**الحل:**
```bash
# استكشف القاعدة أولاً
python3 explore_sqlite.py /path/to/db.db

# تحقق من الأسماء الصحيحة
```

---

### خطأ: "column not found"

**السبب:** تعيين عمود غير موجود

**الحل:**
```bash
# اعرض أعمدة جدول معين
python3 explore_sqlite.py /path/to/db.db --table quran

# حدّث column_mapping في التكوين
```

---

### خطأ: "permission denied"

**السبب:** صلاحيات PostgreSQL

**الحل:**
```sql
-- منح الصلاحيات
GRANT INSERT ON ALL TABLES IN SCHEMA quran TO your_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA quran TO your_user;
```

---

### خطأ: "duplicate key value"

**السبب:** محاولة إدراج قيمة مكررة

**الحل:**
```json
// فعّل تخطي السجلات المكررة
"import_options": {
  "skip_existing": true
}
```

---

## 🔍 التحقق بعد الاستيراد

```sql
-- الاتصال بالقاعدة
psql -U postgres -d quran_hierarchical_db

-- عد السور
SELECT COUNT(*) FROM quran.surahs;
-- يجب أن يكون 114

-- عد الآيات
SELECT COUNT(*) FROM quran.ayahs;
-- يجب أن يكون 6236 تقريباً

-- عرض أول 5 آيات من الفاتحة
SELECT aya_number, aya_text_uthmani
FROM quran.ayahs
WHERE aya_sur_id = 1
ORDER BY aya_number
LIMIT 5;

-- التحقق من الفهارس
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'quran';
```

---

## 📚 أمثلة كاملة

### مثال 1: قاعدة Tanzil.net

```json
{
  "sqlite": {
    "database_path": "/data/tanzil.db"
  },

  "table_mappings": {
    "surahs": {
      "enabled": true,
      "source_table": "sura",
      "column_mapping": {
        "index": "sur_id",
        "name": "sur_name_ar",
        "tname": "sur_name_en",
        "aya": "sur_ayah_count",
        "type": "sur_revelation_type"
      }
    },

    "ayahs": {
      "enabled": true,
      "source_table": "quran",
      "column_mapping": {
        "sura": "aya_sur_id",
        "aya": "aya_number",
        "text": "aya_text_uthmani"
      }
    }
  }
}
```

---

### مثال 2: قاعدة مخصصة

```json
{
  "sqlite": {
    "database_path": "/data/my_quran.db"
  },

  "table_mappings": {
    "surahs": {
      "enabled": true,
      "source_table": "chapters",
      "column_mapping": {
        "chapter_number": "sur_id",
        "arabic_name": "sur_name_ar",
        "english_name": "sur_name_en",
        "verses_count": "sur_ayah_count"
      },
      "defaults": {
        "sur_revelation_type": "meccan"
      }
    }
  }
}
```

---

## 📞 الدعم

إذا واجهت أي مشاكل:

1. ✅ تحقق من `explore_sqlite.py` للتأكد من بنية قاعدتك
2. ✅ راجع ملف التكوين والتأكد من صحة التعيينات
3. ✅ راجع رسائل الأخطاء بعناية
4. ✅ تواصل معنا: duhatv@gmail.com

---

**آخر تحديث: 2025-10-30**

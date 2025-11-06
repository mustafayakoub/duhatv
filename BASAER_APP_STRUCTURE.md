# 🏗️ بنية تطبيق بصائر القرآن الكريم - المرحلة الأولى

## 🎯 الهدف
تطبيق عالمي يخدم 4 مليار مستخدم - موسوعة قرآنية شاملة

---

## 📁 هيكل الملفات المقترح

```
frontend-desktop/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx           # شجرة القرآن + قائمة السور
│   │   │   ├── TopBar.tsx            # شريط علوي رفيع للأدوات
│   │   │   ├── StatusBar.tsx         # شريط الحالة السفلي
│   │   │   └── MainLayout.tsx        # التخطيط الرئيسي
│   │   │
│   │   ├── quran/
│   │   │   ├── QuranViewer.tsx       # عارض المصحف الرئيسي
│   │   │   ├── AyahCard.tsx          # بطاقة الآية
│   │   │   ├── SurahHeader.tsx       # رأس السورة
│   │   │   ├── TajweedText.tsx       # نص مع تجويد ملون
│   │   │   └── LineHighlight.tsx     # خط تحديد السطر
│   │   │
│   │   ├── panels/
│   │   │   ├── TranslationPanel.tsx  # لوحة الترجمات
│   │   │   ├── TafseerPanel.tsx      # لوحة التفاسير
│   │   │   ├── IrabPanel.tsx         # لوحة الإعراب
│   │   │   ├── SarfPanel.tsx         # لوحة الصرف
│   │   │   ├── MeaningsPanel.tsx     # لوحة المعاني
│   │   │   └── StatsPanel.tsx        # لوحة الإحصاءات
│   │   │
│   │   ├── search/
│   │   │   ├── SearchBar.tsx         # شريط البحث الذكي
│   │   │   ├── SearchFilters.tsx     # فلاتر البحث
│   │   │   ├── SearchResults.tsx     # نتائج البحث (شجرة)
│   │   │   └── SearchTypes.tsx       # أنواع البحث
│   │   │
│   │   ├── settings/
│   │   │   ├── SettingsPanel.tsx     # لوحة الإعدادات الرئيسية
│   │   │   ├── FontSettings.tsx      # إعدادات الخطوط
│   │   │   ├── ColorSettings.tsx     # إعدادات الألوان
│   │   │   ├── DisplaySettings.tsx   # إعدادات العرض
│   │   │   └── MushafSelector.tsx    # اختيار المصحف
│   │   │
│   │   ├── topics/
│   │   │   ├── TopicsTree.tsx        # شجرة الموضوعات
│   │   │   └── TopicViewer.tsx       # عارض الموضوع
│   │   │
│   │   └── shared/
│   │       ├── Button.tsx            # زر عصري
│   │       ├── Checkbox.tsx          # خانة اختيار
│   │       ├── Select.tsx            # قائمة منسدلة
│   │       ├── Slider.tsx            # مزلاج
│   │       └── Tree.tsx              # شجرة ذكية
│   │
│   ├── hooks/
│   │   ├── useQuran.ts              # بيانات القرآن
│   │   ├── useSettings.ts           # إعدادات التطبيق
│   │   ├── useSearch.ts             # البحث
│   │   └── useTajweed.ts            # التجويد
│   │
│   ├── store/
│   │   ├── quranStore.ts            # حالة القرآن (Zustand)
│   │   ├── settingsStore.ts         # حالة الإعدادات
│   │   └── searchStore.ts           # حالة البحث
│   │
│   ├── services/
│   │   ├── db.ts                    # قاعدة البيانات المحلية
│   │   ├── api.ts                   # Tauri API
│   │   └── tajweed.ts               # معالجة التجويد
│   │
│   ├── utils/
│   │   ├── tajweedRules.ts          # قواعد التجويد 18 لون
│   │   ├── arabicNormalizer.ts      # تطبيع النصوص العربية
│   │   └── searchEngine.ts          # محرك البحث
│   │
│   └── data/
│       ├── mushaf-hafs.json         # بيانات حفص (أساسي)
│       └── tajweed-colors.json      # ألوان التجويد
│
├── src-tauri/
│   └── src/
│       ├── main.rs
│       ├── db/
│       │   ├── mod.rs
│       │   ├── quran.rs            # استعلامات القرآن
│       │   ├── search.rs           # استعلامات البحث
│       │   └── connection.rs       # اتصال SQLite
│       │
│       └── commands/
│           ├── quran.rs            # أوامر القرآن
│           ├── search.rs           # أوامر البحث
│           └── settings.rs         # أوامر الإعدادات
```

---

## 🎨 المميزات حسب الأولوية

### ⭐ Phase 1 (الأساسيات - نبدأ الآن!)
- [x] الواجهة الذهبية الأساسية
- [ ] عرض المصحف (حفص فقط أولاً)
- [ ] شجرة السور والآيات
- [ ] إعدادات الخطوط
- [ ] checkbox فصل/وصل حروف العطف
- [ ] checkbox ألوان التجويد

### ⭐⭐ Phase 2 (الأسبوع القادم)
- [ ] باقي المصاحف السبعة
- [ ] الترجمات (نافذة منفصلة)
- [ ] التفاسير
- [ ] البحث البسيط

### ⭐⭐⭐ Phase 3 (الأسبوعين القادمين)
- [ ] الإعراب والصرف
- [ ] معاني المفردات
- [ ] البحث الذكي (فلاتر)
- [ ] الموضوعات

### ⭐⭐⭐⭐ Phase 4 (الشهر القادم)
- [ ] الإحصاءات
- [ ] التصدير والطباعة
- [ ] الإشارات المرجعية
- [ ] المفضلة

---

## 🎨 Design System (النظام التصميمي)

### الألوان
```
Primary Gold:   #eab308
Secondary:      #b8956a
Background:     #fefce8
Text Dark:      #854d0e
Borders:        #fde047
```

### الخطوط
```
Arabic:         Amiri, Scheherazade New
Uthmanic:       KFGQPC Hafs, Amiri Quran
Interface:      Inter, Segoe UI
```

### المسافات
```
Sidebar Width:  280px (قابلة للتغيير)
Top Bar:        48px (رفيعة)
Status Bar:     24px (رفيعة جداً)
Padding:        16px, 24px, 32px
```

### الأزرار
```
Primary:        rounded-lg, shadow-md, hover:shadow-lg
Secondary:      rounded-md, border-2
Icon Only:      p-2, rounded-full
```

---

## 🗄️ قاعدة البيانات

### الجداول الرئيسية

```sql
-- المصاحف السبعة
CREATE TABLE mushafs (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,        -- حفص، ورش، قالون...
  file_path TEXT,
  font_family TEXT,
  is_active BOOLEAN DEFAULT 1
);

-- السور
CREATE TABLE surahs (
  id INTEGER PRIMARY KEY,
  number INTEGER UNIQUE,
  name_arabic TEXT,
  name_english TEXT,
  ayah_count INTEGER,
  revelation_type TEXT       -- مكية / مدنية
);

-- الآيات (لكل مصحف)
CREATE TABLE ayahs (
  id INTEGER PRIMARY KEY,
  mushaf_id INTEGER,
  surah_number INTEGER,
  ayah_number INTEGER,
  text_uthmani TEXT,
  text_simple TEXT,
  text_imlaei TEXT,
  juz_number INTEGER,
  page_number INTEGER,
  line_number INTEGER,
  tajweed_data JSON,         -- بيانات التجويد
  FOREIGN KEY (mushaf_id) REFERENCES mushafs(id)
);

-- التجويد (18 لون)
CREATE TABLE tajweed_rules (
  id INTEGER PRIMARY KEY,
  rule_name TEXT,            -- إدغام، إخفاء، مد...
  color_hex TEXT,
  description_ar TEXT
);

-- الترجمات
CREATE TABLE translations (
  id INTEGER PRIMARY KEY,
  language TEXT,
  translator_name TEXT,
  is_active BOOLEAN DEFAULT 0
);

CREATE TABLE translation_texts (
  id INTEGER PRIMARY KEY,
  translation_id INTEGER,
  surah_number INTEGER,
  ayah_number INTEGER,
  text TEXT,
  FOREIGN KEY (translation_id) REFERENCES translations(id)
);

-- التفاسير
CREATE TABLE tafaseer (
  id INTEGER PRIMARY KEY,
  name TEXT,
  author TEXT,
  is_active BOOLEAN DEFAULT 0
);

CREATE TABLE tafseer_texts (
  id INTEGER PRIMARY KEY,
  tafseer_id INTEGER,
  surah_number INTEGER,
  ayah_number INTEGER,
  text TEXT,
  FOREIGN KEY (tafseer_id) REFERENCES tafaseer(id)
);

-- الإعراب
CREATE TABLE irab (
  id INTEGER PRIMARY KEY,
  surah_number INTEGER,
  ayah_number INTEGER,
  word_position INTEGER,
  irab_text TEXT
);

-- الصرف
CREATE TABLE sarf (
  id INTEGER PRIMARY KEY,
  surah_number INTEGER,
  ayah_number INTEGER,
  word_position INTEGER,
  sarf_text TEXT
);

-- معاني المفردات
CREATE TABLE word_meanings (
  id INTEGER PRIMARY KEY,
  word TEXT,
  meaning TEXT,
  root TEXT
);

-- الموضوعات
CREATE TABLE topics (
  id INTEGER PRIMARY KEY,
  name_arabic TEXT,
  parent_id INTEGER,
  description TEXT
);

CREATE TABLE ayah_topics (
  ayah_id INTEGER,
  topic_id INTEGER,
  PRIMARY KEY (ayah_id, topic_id)
);

-- الإعدادات
CREATE TABLE user_settings (
  key TEXT PRIMARY KEY,
  value TEXT
);
```

---

## 🚀 نبدأ من أين؟

### الخطوة 1: نبني Sidebar + QuranViewer (اليوم!)
### الخطوة 2: نضيف الإعدادات الأساسية (غداً)
### الخطوة 3: نربط قاعدة البيانات (بعد غد)

---

**هل نبدأ بإنشاء المكونات الأساسية الآن؟** 🎯

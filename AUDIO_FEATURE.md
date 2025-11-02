# 🎵 ميزة التشغيل الصوتي - تطبيق القرآن الكريم Pro

## نظرة عامة

تمت إضافة ميزة تشغيل صوتي كاملة تتيح للمستخدم الاستماع إلى القرآن الكريم بأصوات 11 قارئاً مشهوراً!

## ✨ الميزات المضافة

### 1️⃣ القراء المتاحون

#### القراء المشهورون (⭐):
1. **عبد الباسط عبد الصمد** - 192kbps (جودة عالية)
2. **محمد صديق المنشاوي** - 128kbps
3. **ماهر المعيقلي** - 64kbps
4. **عبد الرحمن السديس** - 64kbps
5. **سعود الشريم** - 64kbps
6. **مشاري راشد العفاسي** - 128kbps
7. **سعد الغامدي** - 40kbps
8. **ناصر القطامي** - 128kbps

#### قراء إضافيون:
9. **محمود خليل الحصري** - 128kbps
10. **أحمد العجمي** - 128kbps
11. **عبد الله الجهني** - 128kbps

### 2️⃣ الملفات المضافة

```
src/
├── audio_player.py       # مدير التشغيل الصوتي
│   ├── AudioDownloader   # تحميل الملفات الصوتية
│   └── QuranAudioPlayer  # مشغل الصوتيات
│
└── config.py             # تم تحديثه بإعدادات القراء

dialogs.py                # تم إضافة نافذة اختيار القارئ
requirements.txt          # تم إضافة PyQt6-Multimedia
```

### 3️⃣ الإعدادات المتاحة

```python
AUDIO_SETTINGS = {
    'auto_play_next': True,    # تشغيل الآية التالية تلقائياً
    'repeat_aya': False,        # تكرار الآية
    'download_ahead': 3,        # تحميل مسبق لـ 3 آيات
    'cache_size_mb': 500,       # حجم الكاش 500 MB
}
```

### 4️⃣ المجلدات الجديدة

```
data/
└── audio/                  # الملفات الصوتية
    └── cache/              # الكاش المؤقت
        ├── abdulbasit/     # مجلد لكل قارئ
        ├── minshawy/
        ├── maher/
        └── ...
```

## 🚀 كيفية الاستخدام

### التثبيت

```bash
# تحديث المتطلبات
pip install -r requirements.txt

# أو تثبيت يدوي
pip install PyQt6-Multimedia
```

### التشغيل البرمجي

```python
from audio_player import QuranAudioPlayer

# إنشاء المشغل
player = QuranAudioPlayer()

# اختيار القارئ
player.set_reciter('abdulbasit')

# تشغيل آية
player.play_aya(sura=1, aya=1)  # الفاتحة:1

# التحكم
player.pause()              # إيقاف مؤقت
player.play()               # استئناف
player.stop()               # إيقاف
player.play_next()          # الآية التالية
player.play_previous()      # الآية السابقة

# مستوى الصوت (0.0 - 1.0)
player.set_volume(0.8)

# الإعدادات
player.set_auto_play_next(True)   # تشغيل تلقائي
player.set_repeat_aya(False)       # عدم التكرار
```

### نافذة اختيار القارئ

```python
from dialogs import ReciterDialog

# فتح نافذة الاختيار
dialog = ReciterDialog(parent_window, current_reciter='abdulbasit')

if dialog.exec() == QDialog.DialogCode.Accepted:
    selected = dialog.get_selected_reciter()
    player.set_reciter(selected)
```

## 📊 مصادر الملفات الصوتية

### المصدر: EveryAyah.com

```
https://everyayah.com/data/[RECITER_FOLDER]/[SURA_AYA].mp3

مثال:
https://everyayah.com/data/Abdul_Basit_Murattal_192kbps/001001.mp3
```

#### تنسيق الملفات:
- `001001.mp3` = السورة 1، الآية 1
- `002005.mp3` = السورة 2، الآية 5
- `114006.mp3` = السورة 114، الآية 6

### التحميل التلقائي

- يتم التحميل تلقائياً عند التشغيل
- التخزين المؤقت لتجنب إعادة التحميل
- تحميل مسبق للآيات التالية (3 آيات افتراضياً)
- عرض نسبة التحميل

## 🎯 الميزات المتقدمة

### 1. التحميل الذكي

```python
# التحقق من الكاش
if downloader.is_cached('abdulbasit', 1, 1):
    # الملف موجود، تشغيل فوري
    pass
else:
    # تحميل من الإنترنت
    downloader.download_audio('abdulbasit', 1, 1)

# تحميل مسبق
downloader.preload_next_ayas('abdulbasit', 1, 1, count=3)
```

### 2. الإشارات (Signals)

```python
# الاستماع للأحداث
player.state_changed.connect(on_state_changed)        # تغيير الحالة
player.position_changed.connect(on_position_changed)  # موضع التشغيل
player.duration_changed.connect(on_duration_changed)  # مدة الملف
player.aya_changed.connect(on_aya_changed)            # تغيير الآية
player.error_occurred.connect(on_error_occurred)      # خطأ
```

### 3. إدارة الكاش

```python
# حجم الكاش
AUDIO_SETTINGS['cache_size_mb'] = 500  # 500 MB

# مسار الكاش
cache_path = config.AUDIO_CACHE_DIR  # data/audio/cache/

# تنظيف الكاش
import shutil
shutil.rmtree(cache_path)
cache_path.mkdir(parents=True, exist_ok=True)
```

## 🔧 الإعدادات المتقدمة

### إضافة قارئ جديد

```python
# في config.py
RECITERS['new_reciter'] = {
    'name': 'القارئ الجديد',
    'name_en': 'New Reciter',
    'style': 'مرتل',
    'url_base': 'https://everyayah.com/data/Reciter_Folder',
    'bitrate': '128kbps',
    'icon': '🎙️',
    'popular': True
}
```

### تخصيص إعدادات التشغيل

```python
# في config.py
AUDIO_SETTINGS = {
    'auto_play_next': True,     # تشغيل تلقائي للآية التالية
    'repeat_aya': False,         # تكرار الآية
    'download_ahead': 5,         # تحميل 5 آيات مسبقاً
    'cache_size_mb': 1000,       # كاش أكبر 1GB
}
```

## 🐛 حل المشاكل

### مشكلة: "لا يوجد صوت"

```bash
# تحقق من PyQt6-Multimedia
pip install --upgrade PyQt6-Multimedia

# تحقق من برامج الترميز (Linux)
sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good
```

### مشكلة: "خطأ في التحميل"

- تحقق من الاتصال بالإنترنت
- تحقق من الرابط في RECITERS config
- تحقق من صلاحيات المجلد `data/audio/`

### مشكلة: "ملف غير موجود"

```python
# التحقق من المسار
print(f"Audio dir: {config.AUDIO_DIR}")
print(f"Cache dir: {config.AUDIO_CACHE_DIR}")

# إعادة إنشاء المجلدات
from config import ensure_directories
ensure_directories()
```

## 📈 الأداء

### استهلاك المساحة

- **آية واحدة**: ~50-200 KB (حسب الجودة)
- **سورة كاملة**: ~1-10 MB
- **القرآن الكامل**: ~500 MB - 2 GB (حسب القارئ)

### التوصيات

1. **للتشغيل اليومي**: قارئ 64kbps (ماهر، السديس، الشريم)
2. **لأفضل جودة**: عبد الباسط 192kbps
3. **للسرعة**: سعد الغامدي 40kbps
4. **للتوازن**: المنشاوي أو العفاسي 128kbps

## 🎨 واجهة المستخدم (قيد التطوير)

سيتم إضافة عناصر التحكم في الواجهة الرئيسية:

```
┌─────────────────────────────────────┐
│  🎙️ عبد الباسط عبد الصمد     ▼   │
├─────────────────────────────────────┤
│  الفاتحة: بِسْمِ اللَّهِ الرَّحْمَٰنِ  │
│                                     │
│  ◀◀  ⏸  ▶▶  🔁  🔀               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  0:05 / 0:12                        │
│                                     │
│  🔊 ▬▬▬▬▬▬▬▬▬▬ 80%               │
└─────────────────────────────────────┘
```

## 📞 الدعم

لأي استفسارات:
- 📧 duhatv@gmail.com
- 🌐 duhatv.net
- 📱 +905342390000

---

**تم التطوير بكل ❤️ لخدمة كتاب الله** 📖🎵

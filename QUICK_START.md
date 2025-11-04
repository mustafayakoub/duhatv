# ⚡ البداية السريعة

## 📥 استيراد القرآن الكامل (6,236 آية):

### **الطريقة 1: استيراد الكل تلقائياً**

```powershell
# من داخل C:\QURAN2
cd C:\QURAN2

# استيراد 6 قراءات
.\import_all.ps1

# استيراد التجويد الملون
.\import_tajweed.ps1

# التحقق
python scripts\verify_enhanced_db.py
```

**المدة:** ~10 دقائق للكل

---

### **الطريقة 2: استيراد قراءة واحدة**

```powershell
# مثال: حفص فقط
python scripts\import_quran_smart.py --file "C:\QURAN2\data\sources\quran_Ayat\hafsData_v2-0.json" --version hafs
```

**المدة:** ~2 دقيقة

---

## 🎨 نسخ الخطوط:

```powershell
# إنشاء مجلد الخطوط
mkdir static\fonts

# نسخ 15 خط قرآني
Copy-Item data\Fonts\*.ttf static\fonts\
Copy-Item data\Fonts\*.otf static\fonts\
```

---

## 🚀 تشغيل التطبيق:

```powershell
python app.py
```

ثم افتح: **http://localhost:5000**

---

## 📊 الملفات المدعومة:

### **القراءات الستة:**
| الملف | القراءة | المسار |
|------|---------|--------|
| `hafsData_v2-0.json` | حفص | C:\QURAN2\data\sources\quran_Ayat\ |
| `warshData_v2-1.json` | ورش | ↑ |
| `QalounData_v2-1.json` | قالون | ↑ |
| `DouriData_v2-0.json` | الدوري | ↑ |
| `SousiData_v2-0.json` | السوسي | ↑ |
| `shubaData_v2-0.json` | شعبة | ↑ |

### **التجويد:**
| الملف | النوع | المسار |
|------|------|--------|
| `quran_text_with_tajweed.json` | تجويد ملون | C:\DataB\quran_Ayat\quran_Ayat\ |

---

## 🔍 فحص ملف قبل الاستيراد:

```powershell
python check_json.py "C:\QURAN2\data\sources\quran_Ayat\hafsData_v2-0.json"
```

**يعرض:**
- ✅ عدد الآيات الصحيحة (يجب: 6,236)
- 🕌 عدد البسملات
- 📖 عدد السور (يجب: 114)
- 📄 عينة من البيانات

---

## 📚 الأدلة الكاملة:

- **README_IMPORT.md** - دليل الاستيراد الشامل
- **TAJWEED_CODES.md** - مرجع أحكام التجويد
- **README_APP.md** - دليل التطبيق
- **DOWNLOAD.md** - روابط التحميل

---

## ⚡ نصائح:

### **لتجنب الأخطاء:**
1. ✅ تأكد أنك في C:\QURAN2 قبل تشغيل أي أمر
2. ✅ استخدم المسارات الكاملة للملفات
3. ✅ افحص الملف قبل الاستيراد بـ `check_json.py`

### **إذا حدث خطأ:**
- **"No such file"** → تحقق من المسار
- **"JSON error"** → افحص الملف بـ `check_json.py`
- **"Version not found"** → أضف `--version` يدوياً

---

## 📞 المساعدة:

**إذا واجهت مشكلة:**
1. راجع **README_IMPORT.md** (قسم "حل المشكلات")
2. افحص الملف بـ `check_json.py`
3. تحقق من المسارات الصحيحة

---

**الحمد لله** 🤲

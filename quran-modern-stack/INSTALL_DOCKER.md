# 🐳 دليل تثبيت Docker Desktop لـ Windows

<div dir="rtl">

## خطوات بسيطة لتثبيت Docker Desktop

</div>

---

## الخطوة 1️⃣: التحميل

**اذهب إلى:**
https://www.docker.com/products/docker-desktop/

**اضغط على:** "Download for Windows"

**حجم الملف:** حوالي 500 MB

---

## الخطوة 2️⃣: التثبيت

1. **شغّل الملف** المحمّل: `Docker Desktop Installer.exe`

2. **اتبع المعالج:**
   - ✅ اقبل الشروط
   - ✅ اختر "Use WSL 2 instead of Hyper-V" (إذا ظهر)
   - ✅ اضغط "Install"

3. **انتظر...** (قد يستغرق 5-10 دقائق)

4. **أعد تشغيل الكمبيوتر** (مهم!)

---

## الخطوة 3️⃣: أول تشغيل

1. **افتح Docker Desktop** من قائمة Start

2. **انتظر...** حتى ترى:
   ```
   Docker Desktop is running
   ```

3. **اقبل الشروط** (إذا ظهرت)

4. **تخطى Tutorial** (اختياري)

---

## الخطوة 4️⃣: التحقق

**افتح PowerShell** واكتب:

```powershell
docker --version
docker-compose --version
```

**يجب أن ترى:**
```
Docker version 24.0.x, build xxxxx
Docker Compose version v2.x.x
```

✅ **تم! Docker جاهز!**

---

## ❌ حل المشاكل

### مشكلة: "WSL 2 installation is incomplete"

**الحل:**

1. افتح PowerShell **كمسؤول** (Run as Administrator)

2. اكتب:
```powershell
wsl --install
```

3. أعد تشغيل الكمبيوتر

4. افتح Docker Desktop مرة أخرى

---

### مشكلة: "Hardware assisted virtualization is disabled"

**الحل:**

1. أعد تشغيل الكمبيوتر
2. ادخل BIOS/UEFI (غالباً F2 أو Del عند التشغيل)
3. فعّل **Virtualization** أو **VT-x** أو **AMD-V**
4. احفظ واخرج
5. شغّل Docker Desktop

---

### مشكلة: Docker بطيء جداً

**الحل:**

1. افتح Docker Desktop
2. Settings ⚙️
3. Resources → Advanced
4. زد **Memory** إلى 4GB على الأقل
5. زد **CPUs** إلى 2 على الأقل
6. Apply & Restart

---

## 🚀 بعد التثبيت

**ارجع إلى** `C:\quran11\`

**شغّل:**
```powershell
START.bat
```

أو

```powershell
docker-compose up -d
```

---

## 📖 معلومات إضافية

### متطلبات النظام

- ✅ Windows 10/11 (64-bit)
- ✅ 4GB RAM (على الأقل)
- ✅ Virtualization enabled in BIOS

### حجم Docker Desktop

- 💾 التثبيت: ~500 MB
- 💾 بعد الصور: ~2-3 GB

### البدائل

إذا كان Docker ثقيلاً جداً على جهازك:
- استخدم Docker في Linux VM
- استخدم WSL2 مباشرة
- شغّل الخدمات محلياً (بدون Docker)

---

<div dir="rtl" align="center">

## 🎉 بعد التثبيت، ارجع إلى START_WINDOWS.md

**وستشغّل المشروع بسهولة!**

</div>

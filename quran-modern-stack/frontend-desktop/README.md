# 🎨 Basaer Quran - Desktop App (Frontend)

تطبيق سطح مكتب ذهبي لمشروع بصائر القرآن الكريم

## 🛠️ التقنيات المستخدمة

- **Tauri** - إطار عمل لبناء تطبيقات سطح مكتب (Rust + Web)
- **React 18** - مكتبة واجهات المستخدم
- **TypeScript** - لغة برمجة مع دعم الأنواع
- **Vite** - أداة بناء سريعة
- **TailwindCSS** - إطار عمل CSS مع دعم RTL
- **React Query** - إدارة حالة البيانات
- **Zustand** - إدارة الحالة العامة

## 🚀 البدء السريع

### المتطلبات

- **Node.js** 20+
- **Rust** 1.75+ (لبناء Tauri)
- **npm** أو **yarn** أو **pnpm**

### تثبيت Rust (إذا لم يكن مثبتاً)

**على Windows:**
```powershell
# الخيار 1: استخدام rustup (موصى به)
# قم بتحميل وتثبيت من: https://rustup.rs/
# ثم قم بتثبيت Visual Studio Build Tools أو استخدم WSL2

# الخيار 2: استخدام Docker (الأسهل)
docker-compose up frontend-desktop
```

**على Linux/macOS:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### التثبيت

```bash
# 1. تثبيت مكتبات Node.js
npm install

# 2. تشغيل وضع التطوير (سيقوم ببناء Rust تلقائياً)
npm run tauri:dev

# 3. بناء التطبيق للإنتاج
npm run tauri:build
```

### إذا واجهت مشكلة في بناء Rust على Windows

**الحل 1: Docker (الأسرع والأسهل)**
```bash
cd /home/user/duhatv/quran-modern-stack
docker-compose up --build frontend-desktop
```

**الحل 2: استخدام WSL2**
```powershell
wsl --install
# ثم افتح WSL وقم بتشغيل الأوامر داخل Linux
```

## 📁 هيكل المشروع

```
frontend-desktop/
├── src/
│   ├── App.tsx           # المكون الرئيسي
│   ├── main.tsx          # نقطة الدخول
│   ├── index.css         # الأنماط الأساسية
│   ├── components/       # مكونات واجهة المستخدم
│   ├── pages/            # صفحات التطبيق
│   ├── hooks/            # React Hooks مخصصة
│   ├── api/              # استدعاءات API
│   ├── store/            # إدارة الحالة
│   └── utils/            # أدوات مساعدة
├── src-tauri/            # كود Tauri (Rust)
├── public/               # ملفات ثابتة
├── index.html            # HTML الرئيسي
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## 🎨 الألوان الذهبية

التطبيق يستخدم لوحة ألوان ذهبية دافئة:

- **Golden:** `#eab308` (الذهبي الرئيسي)
- **Bronze:** `#b8956a` (البرونزي)
- **Backgrounds:** تدرجات من الذهبي والبرونزي

## 🔥 الميزات

### ✅ المكتملة

- [x] التصميم الأساسي الذهبي
- [x] دعم RTL (من اليمين لليسار)
- [x] الخطوط العربية
- [x] TailwindCSS مع الألوان المخصصة
- [x] تكامل Tauri مع Rust Backend
- [x] نظام التحية التفاعلي (مثال على Tauri Commands)
- [x] إعدادات النافذة المخصصة (1200×800)

### 🔄 قيد التطوير

- [ ] واجهة عرض المصحف
- [ ] البحث المتقدم
- [ ] عرض التفاسير
- [ ] الترجمات المتعددة
- [ ] القراءات المختلفة
- [ ] مصحف التجويد المرمز

### 📅 مخطط لها

- [ ] وضع أوفلاين كامل
- [ ] المزامنة مع السحابة
- [ ] الإشارات المرجعية
- [ ] التدبرات الشخصية
- [ ] التصدير والطباعة

## 🧩 المكونات الرئيسية

### `App.tsx`

المكون الرئيسي الذي يحتوي على:
- Header مع العنوان الذهبي
- نظام التحية التفاعلي (يستخدم Tauri Commands للتواصل مع Rust)
  - حقل إدخال الاسم
  - زر التحية
  - عرض الرسالة من Rust Backend
- عداد React التجريبي
- عرض الإحصائيات (114 سورة، 6236 آية، 77432 كلمة)
- بطاقات الميزات الأربعة
- Footer مع آية قرآنية

### `src-tauri/src/main.rs`

كود Rust الخلفي الذي يحتوي على:
- دالة `greet` - ترجع رسالة ترحيب بالعربية
- إعداد Tauri Builder مع command handlers

### الخطط المستقبلية

سيتم إضافة المكونات التالية:
- `QuranReader` - قارئ المصحف
- `SearchBar` - شريط البحث
- `TafseerPanel` - لوحة التفاسير
- `TranslationPanel` - لوحة الترجمات
- `SettingsPanel` - لوحة الإعدادات

## 📖 دليل التطوير

### إضافة صفحة جديدة

```tsx
// src/pages/NewPage.tsx
export default function NewPage() {
  return (
    <div className="container">
      <h1 className="font-arabic">صفحة جديدة</h1>
    </div>
  )
}
```

### إضافة مكون جديد

```tsx
// src/components/NewComponent.tsx
interface Props {
  title: string
}

export default function NewComponent({ title }: Props) {
  return (
    <div className="bg-golden-100 p-4 rounded-lg">
      <h2 className="font-arabic">{title}</h2>
    </div>
  )
}
```

## 🐛 حل المشاكل

### مشكلة: `link.exe not found`

**الحل:** تثبيت Visual Studio Build Tools
```bash
# تحميل من
https://visualstudio.microsoft.com/downloads/
# اختر "Build Tools for Visual Studio 2022"
# وتأكد من تحديد "Desktop development with C++"
```

### مشكلة: `npm install` فشل

**الحل:** تأكد من إصدار Node.js
```bash
node --version  # يجب أن يكون 20+
npm --version   # يجب أن يكون 10+
```

## 📝 الترخيص

MIT License - مفتوح المصدر

---

**بُني بـ ❤️ لخدمة كتاب الله العزيز**

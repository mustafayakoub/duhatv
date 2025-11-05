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

### التثبيت

```bash
# تثبيت المكتبات
npm install

# تشغيل وضع التطوير
npm run tauri:dev

# بناء التطبيق
npm run tauri:build
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
- Header مع العنوان
- عرض الإحصائيات (114 سورة، 6236 آية، 77432 كلمة)
- بطاقات الميزات
- Footer مع آية قرآنية

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

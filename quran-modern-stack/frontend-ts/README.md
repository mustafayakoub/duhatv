# 📖 القرآن الكريم - واجهة TypeScript/React

واجهة أمامية حديثة وجميلة للقرآن الكريم مبنية بـ TypeScript و React 18 و Material-UI مع دعم كامل للغة العربية واتجاه RTL.

## ✨ المميزات

### 🎨 التصميم والواجهة
- تصميم عصري وجميل مع Material-UI
- دعم كامل للغة العربية واتجاه RTL
- وضع داكن وفاتح قابل للتبديل
- تصميم متجاوب (Mobile-First)
- خطوط عربية احترافية (Amiri, Cairo, Scheherazade)
- رسوم متحركة سلسة وتأثيرات بصرية

### 🚀 الوظائف
- عرض قائمة السور الـ 114 بتصميم بطاقات جذاب
- عرض تفاصيل كل سورة مع جميع آياتها
- بحث قوي وسريع في القرآن الكريم (عبر خدمة Go)
- إعدادات قابلة للتخصيص:
  - حجم الخط (صغير، متوسط، كبير)
  - إظهار/إخفاء الترجمة
  - إظهار/إخفاء النقحرة
  - الوضع الداكن/الفاتح

### ⚡ الأداء والتقنية
- بناء سريع جداً مع Vite
- TypeScript للأمان والموثوقية
- React Query للتخزين المؤقت الذكي
- Zustand لإدارة الحالة
- تحميل بيانات ذكي مع Caching

## 🛠️ التقنيات المستخدمة

```json
{
  "frontend": "React 18",
  "language": "TypeScript",
  "build": "Vite",
  "ui": "Material-UI (MUI)",
  "routing": "React Router v6",
  "state": "Zustand + React Query",
  "styling": "Emotion + RTL Plugin",
  "http": "Axios"
}
```

## 📦 البنية

```
frontend-ts/
├── src/
│   ├── api/              # API clients and hooks
│   │   ├── client.ts     # Axios clients for Rust & Go
│   │   └── hooks.ts      # React Query hooks
│   ├── components/       # Reusable components
│   │   ├── Navbar.tsx
│   │   ├── SurahCard.tsx
│   │   ├── AyahCard.tsx
│   │   ├── Loading.tsx
│   │   └── ErrorMessage.tsx
│   ├── pages/           # Page components
│   │   ├── Home.tsx
│   │   ├── SurahDetail.tsx
│   │   ├── Search.tsx
│   │   └── Settings.tsx
│   ├── store/           # State management
│   │   └── settings.ts  # Zustand store
│   ├── theme/           # MUI theme config
│   │   └── index.ts
│   ├── types/           # TypeScript types
│   │   └── index.ts
│   ├── App.tsx          # Main app component
│   └── main.tsx         # Entry point
├── public/              # Static assets
├── Dockerfile           # Multi-stage Docker build
├── nginx.conf           # Nginx configuration
├── vite.config.ts       # Vite configuration
├── tsconfig.json        # TypeScript config
└── package.json         # Dependencies
```

## 🚀 التشغيل

### المتطلبات الأساسية
- Node.js 18+ و npm
- خدمة Rust Backend تعمل على المنفذ 8000
- خدمة Go Search تعمل على المنفذ 8001

### 1. التثبيت

```bash
cd frontend-ts
npm install
```

### 2. إعداد متغيرات البيئة

```bash
cp .env.example .env
```

قم بتعديل `.env` حسب الحاجة:
```env
VITE_RUST_API_URL=http://localhost:8000
VITE_GO_SEARCH_URL=http://localhost:8001
```

### 3. التشغيل في وضع التطوير

```bash
npm run dev
```

التطبيق سيعمل على: `http://localhost:3000`

### 4. البناء للإنتاج

```bash
npm run build
```

الملفات المبنية ستكون في مجلد `dist/`

### 5. معاينة البناء

```bash
npm run preview
```

## 🐳 Docker

### بناء الصورة

```bash
docker build -t quran-frontend:latest .
```

### التشغيل

```bash
docker run -p 80:80 quran-frontend:latest
```

أو باستخدام متغيرات البيئة:

```bash
docker run -p 80:80 \
  -e VITE_RUST_API_URL=http://backend:8000 \
  -e VITE_GO_SEARCH_URL=http://search:8001 \
  quran-frontend:latest
```

## 📡 الاتصال بالخدمات الخلفية

### Rust Backend API
```typescript
// src/api/client.ts
const RUST_API_BASE = 'http://localhost:8000';

// Endpoints:
GET /api/surahs           // Get all surahs
GET /api/surahs/:id       // Get surah with ayahs
GET /api/surahs/:id/ayahs/:number  // Get specific ayah
GET /health               // Health check
```

### Go Search Service
```typescript
// src/api/client.ts
const GO_SEARCH_BASE = 'http://localhost:8001';

// Endpoints:
GET /search?q=<query>&limit=<number>  // Search in Quran
GET /health                           // Health check
```

## 🎨 التخصيص

### تغيير الألوان والثيم

قم بتعديل ملف `src/theme/index.ts`:

```typescript
const lightTheme = createTheme({
  palette: {
    primary: {
      main: '#667eea',  // غير اللون الأساسي
    },
    // ...
  },
});
```

### تغيير الخطوط

قم بتعديل ملف `index.html` لإضافة خطوط جديدة:

```html
<link href="https://fonts.googleapis.com/css2?family=YOUR_FONT" rel="stylesheet">
```

ثم حدث `src/theme/index.ts`:

```typescript
typography: {
  fontFamily: '"YOUR_FONT", "Cairo", "Amiri", serif',
}
```

## 🧪 الاختبار

```bash
# فحص الأنواع TypeScript
npm run type-check

# Linting
npm run lint
```

## 📱 الصفحات

### 1. الصفحة الرئيسية (`/`)
- عرض جميع السور في شبكة بطاقات
- بحث سريع عن السور
- تصفية حسب الاسم أو الرقم

### 2. تفاصيل السورة (`/surah/:id`)
- عرض جميع آيات السورة
- البسملة (ما عدا سورة التوبة والفاتحة)
- التنقل بين السور
- زر العودة للأعلى
- عرض رقم الجزء والصفحة

### 3. البحث (`/search`)
- بحث فوري في القرآن الكريم
- عرض النتائج مع تمييز
- الانتقال المباشر للسورة

### 4. الإعدادات (`/settings`)
- تبديل الثيم (فاتح/داكن)
- حجم الخط
- إظهار/إخفاء الترجمة
- إظهار/إخفاء النقحرة
- إعادة تعيين الإعدادات

## 🔧 الأوامر المتاحة

```bash
npm run dev          # تشغيل في وضع التطوير
npm run build        # بناء للإنتاج
npm run preview      # معاينة البناء
npm run lint         # فحص الكود
npm run type-check   # فحص أنواع TypeScript
```

## 🌐 المتصفحات المدعومة

- Chrome (آخر إصدارين)
- Firefox (آخر إصدارين)
- Safari (آخر إصدارين)
- Edge (آخر إصدارين)

## 📄 الترخيص

هذا المشروع مفتوح المصدر ومتاح للجميع.

## 🤝 المساهمة

المساهمات مرحب بها! لا تتردد في فتح Issue أو Pull Request.

## 📞 الدعم

إذا واجهت أي مشكلة، يرجى فتح Issue في المستودع.

---

صُنع بـ ❤️ للمسلمين في كل مكان

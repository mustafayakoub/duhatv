# ═══════════════════════════════════════════════════════════════════════════════
# سكريبت تحديث تطبيق بصائر القرآن الكريم على Windows
# UPDATE Script for Basaer Quran Application on Windows
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "🚀 بدء تحديث ملفات التطبيق..." -ForegroundColor Green
Write-Host "Starting application files update..." -ForegroundColor Green
Write-Host ""

# التأكد من المسار الصحيح
$ProjectPath = "C:\basaer\quran-modern-stack\frontend-desktop"

if (!(Test-Path $ProjectPath)) {
    Write-Host "❌ خطأ: المسار غير موجود: $ProjectPath" -ForegroundColor Red
    Write-Host "❌ Error: Path not found: $ProjectPath" -ForegroundColor Red
    exit 1
}

Set-Location $ProjectPath
Write-Host "✅ المسار الحالي: $ProjectPath" -ForegroundColor Cyan
Write-Host ""

# ═══════════════════════════════════════════════════════════════════════════════
# 1️⃣ تحديث package.json
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "1️⃣  تحديث package.json..." -ForegroundColor Yellow

@"
{
  "name": "basaer-quran-desktop",
  "version": "0.1.0",
  "description": "بصائر القرآن الكريم - تطبيق سطح مكتب",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "tauri": "tauri",
    "tauri:dev": "tauri dev",
    "tauri:build": "tauri build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "@tauri-apps/api": "^1.5.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.1",
    "zustand": "^4.4.7",
    "@tanstack/react-query": "^5.17.9",
    "axios": "^1.6.5"
  },
  "devDependencies": {
    "@tauri-apps/cli": "^1.5.9",
    "@types/react": "^18.2.47",
    "@types/react-dom": "^18.2.18",
    "@typescript-eslint/eslint-plugin": "^6.18.1",
    "@typescript-eslint/parser": "^6.18.1",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.11"
  }
}
"@ | Out-File -FilePath "package.json" -Encoding UTF8 -NoNewline

Write-Host "   ✅ تم تحديث package.json" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════════════════
# 2️⃣ تحديث src/main.tsx
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "2️⃣  تحديث src/main.tsx..." -ForegroundColor Yellow

@"
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"@ | Out-File -FilePath "src\main.tsx" -Encoding UTF8 -NoNewline

Write-Host "   ✅ تم تحديث src/main.tsx" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════════════════
# 3️⃣ تحديث src/index.css
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "3️⃣  تحديث src/index.css..." -ForegroundColor Yellow

@"
@tailwind base;
@tailwind components;
@tailwind utilities;

/* خطوط عربية من Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Scheherazade+New:wght@400;700&display=swap');

:root {
  font-family: 'Amiri', 'Traditional Arabic', Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.8;
  font-weight: 400;

  color-scheme: light;
  color: rgba(0, 0, 0, 0.87);
  background-color: #fef9c3;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  display: flex;
  min-width: 320px;
  min-height: 100vh;
  direction: rtl;
}

#root {
  width: 100%;
}

.font-arabic {
  font-family: 'Amiri', 'Noto Naskh Arabic', 'Traditional Arabic', serif;
}

.font-uthmanic {
  font-family: 'KFGQPC Uthmanic Script HAFS', 'Scheherazade New', serif;
  font-size: 1.2em;
  line-height: 2;
}

button {
  font-family: inherit;
}

::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #f5f0e8;
}

::-webkit-scrollbar-thumb {
  background: #ca8a04;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a16207;
}
"@ | Out-File -FilePath "src\index.css" -Encoding UTF8 -NoNewline

Write-Host "   ✅ تم تحديث src/index.css" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════════════════
# 4️⃣ تحديث src/App.tsx (التطبيق الذهبي الكامل)
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "4️⃣  تحديث src/App.tsx بالتطبيق الذهبي..." -ForegroundColor Yellow

# بسبب طول الملف، سأقسمه
$AppTsx = @"
import { useState } from 'react'
import { invoke } from '@tauri-apps/api/tauri'

function App() {
  const [count, setCount] = useState(0)
  const [name, setName] = useState('')
  const [greetMsg, setGreetMsg] = useState('')

  async function greet() {
    if (name.trim()) {
      setGreetMsg(await invoke('greet', { name }))
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-golden-50 via-bronze-50 to-golden-100">
      <div className="container mx-auto px-4 py-12">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-golden-800 mb-4 font-arabic">
            بصائر القرآن الكريم
          </h1>
          <p className="text-xl text-bronze-700 font-arabic">
            موسوعة قرآنية شاملة
          </p>
        </header>

        <main className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-2xl p-8 border-4 border-golden-300">
            <div className="text-center mb-8">
              <div className="inline-block p-4 bg-golden-100 rounded-full mb-4">
                <svg className="w-16 h-16 text-golden-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>

              <h2 className="text-3xl font-bold text-golden-800 mb-4 font-arabic">
                مرحباً بك في بصائر القرآن
              </h2>

              <p className="text-lg text-gray-700 mb-6 leading-relaxed font-arabic">
                تطبيق شامل لتصفح القرآن الكريم، التفاسير، الترجمات، والتحليل اللغوي
              </p>
            </div>

            <div className="bg-gradient-to-r from-golden-100 to-bronze-100 p-6 rounded-xl">
              <p className="text-gray-700 mb-4 font-arabic text-center">اختبار Tauri - أدخل اسمك:</p>
              <div className="flex gap-3 mb-4">
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && greet()}
                  placeholder="اكتب اسمك هنا..."
                  className="flex-1 px-4 py-3 rounded-lg border-2 border-golden-300 focus:border-golden-500 focus:outline-none font-arabic text-right"
                />
                <button
                  onClick={greet}
                  className="bg-golden-500 hover:bg-golden-600 text-white font-bold py-3 px-8 rounded-lg transition-colors duration-200 shadow-lg font-arabic"
                >
                  تحية
                </button>
              </div>
              {greetMsg && (
                <div className="bg-white p-4 rounded-lg border-2 border-golden-400 text-center">
                  <p className="text-golden-800 font-bold text-lg font-arabic">{greetMsg}</p>
                </div>
              )}

              <div className="mt-6 text-center">
                <p className="text-gray-600 mb-2 font-arabic text-sm">عداد React:</p>
                <button
                  onClick={() => setCount((count) => count + 1)}
                  className="bg-bronze-500 hover:bg-bronze-600 text-white font-bold py-2 px-6 rounded-lg transition-colors duration-200 shadow font-arabic"
                >
                  العداد: {count}
                </button>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 mt-8">
              <div className="text-center p-4 bg-golden-50 rounded-lg">
                <div className="text-3xl font-bold text-golden-700">114</div>
                <div className="text-sm text-gray-600 font-arabic">سورة</div>
              </div>
              <div className="text-center p-4 bg-golden-50 rounded-lg">
                <div className="text-3xl font-bold text-golden-700">6,236</div>
                <div className="text-sm text-gray-600 font-arabic">آية</div>
              </div>
              <div className="text-center p-4 bg-golden-50 rounded-lg">
                <div className="text-3xl font-bold text-golden-700">77,432</div>
                <div className="text-sm text-gray-600 font-arabic">كلمة</div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6 mt-8">
            <div className="bg-white p-6 rounded-xl shadow-lg border-2 border-golden-200">
              <h3 className="text-xl font-bold text-golden-800 mb-2 font-arabic">
                📖 قراءة المصحف
              </h3>
              <p className="text-gray-600 font-arabic">
                بجميع الروايات والقراءات المتواترة
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-lg border-2 border-golden-200">
              <h3 className="text-xl font-bold text-golden-800 mb-2 font-arabic">
                🔍 البحث المتقدم
              </h3>
              <p className="text-gray-600 font-arabic">
                بحث ذكي في النص والتفاسير
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-lg border-2 border-golden-200">
              <h3 className="text-xl font-bold text-golden-800 mb-2 font-arabic">
                📚 التفاسير
              </h3>
              <p className="text-gray-600 font-arabic">
                102+ تفسير عبر التاريخ
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-lg border-2 border-golden-200">
              <h3 className="text-xl font-bold text-golden-800 mb-2 font-arabic">
                🌍 الترجمات
              </h3>
              <p className="text-gray-600 font-arabic">
                بأكثر من 72 لغة عالمية
              </p>
            </div>
          </div>
        </main>

        <footer className="text-center mt-12 text-bronze-600 font-arabic">
          <p className="text-lg mb-2">
            "إِنَّ هَٰذَا الْقُرْآنَ يَهْدِي لِلَّتِي هِيَ أَقْوَمُ"
          </p>
          <p className="text-sm">الإسراء: 9</p>
        </footer>
      </div>
    </div>
  )
}

export default App
"@

$AppTsx | Out-File -FilePath "src\App.tsx" -Encoding UTF8 -NoNewline

Write-Host "   ✅ تم تحديث src/App.tsx" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════════════════
# 5️⃣ تحديث tailwind.config.js
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "5️⃣  تحديث tailwind.config.js..." -ForegroundColor Yellow

@"
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        golden: {
          50: '#fefce8',
          100: '#fef9c3',
          200: '#fef08a',
          300: '#fde047',
          400: '#facc15',
          500: '#eab308',
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#713f12',
        },
        bronze: {
          50: '#faf8f5',
          100: '#f5f0e8',
          200: '#ebe2d1',
          300: '#dcc9aa',
          400: '#ccac7d',
          500: '#b8956a',
          600: '#9b7d57',
          700: '#7d6549',
          800: '#69543e',
          900: '#594836',
        },
      },
      fontFamily: {
        arabic: ['Amiri', 'Noto Naskh Arabic', 'Traditional Arabic', 'serif'],
        uthmanic: ['KFGQPC Uthmanic Script HAFS', 'Scheherazade New', 'serif'],
      },
    },
  },
  plugins: [],
}
"@ | Out-File -FilePath "tailwind.config.js" -Encoding UTF8 -NoNewline

Write-Host "   ✅ تم تحديث tailwind.config.js" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════════════════
# 6️⃣ تحديث postcss.config.js
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "6️⃣  تحديث postcss.config.js..." -ForegroundColor Yellow

@"
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"@ | Out-File -FilePath "postcss.config.js" -Encoding UTF8 -NoNewline

Write-Host "   ✅ تم تحديث postcss.config.js" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════════════════
# ✅ اكتمل التحديث
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "✅ تم تحديث جميع الملفات بنجاح!" -ForegroundColor Green
Write-Host "✅ All files updated successfully!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "الخطوات التالية:" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  تثبيت المكتبات الجديدة:" -ForegroundColor Yellow
Write-Host "   npm install" -ForegroundColor White
Write-Host ""
Write-Host "2️⃣  تشغيل التطبيق:" -ForegroundColor Yellow
Write-Host "   npm run tauri:dev" -ForegroundColor White
Write-Host ""
Write-Host "3️⃣  إذا لم يعمل Tauri (مشكلة Rust):" -ForegroundColor Yellow
Write-Host "   npm run dev" -ForegroundColor White
Write-Host "   ثم افتح: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green

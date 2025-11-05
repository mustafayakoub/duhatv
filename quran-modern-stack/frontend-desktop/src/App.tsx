import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-golden-50 via-bronze-50 to-golden-100">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-golden-800 mb-4 font-arabic">
            بصائر القرآن الكريم
          </h1>
          <p className="text-xl text-bronze-700 font-arabic">
            موسوعة قرآنية شاملة
          </p>
        </header>

        {/* Main Content */}
        <main className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-2xl p-8 border-4 border-golden-300">
            <div className="text-center mb-8">
              <div className="inline-block p-4 bg-golden-100 rounded-full mb-4">
                <svg
                  className="w-16 h-16 text-golden-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                  />
                </svg>
              </div>

              <h2 className="text-3xl font-bold text-golden-800 mb-4 font-arabic">
                مرحباً بك في بصائر القرآن
              </h2>

              <p className="text-lg text-gray-700 mb-6 leading-relaxed font-arabic">
                تطبيق شامل لتصفح القرآن الكريم، التفاسير، الترجمات، والتحليل اللغوي
              </p>
            </div>

            {/* Demo Counter */}
            <div className="bg-gradient-to-r from-golden-100 to-bronze-100 p-6 rounded-xl text-center">
              <p className="text-gray-700 mb-4 font-arabic">اختبار التطبيق:</p>
              <button
                onClick={() => setCount((count) => count + 1)}
                className="bg-golden-500 hover:bg-golden-600 text-white font-bold py-3 px-8 rounded-lg transition-colors duration-200 shadow-lg"
              >
                العداد: {count}
              </button>
            </div>

            {/* Stats */}
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

          {/* Features */}
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

        {/* Footer */}
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

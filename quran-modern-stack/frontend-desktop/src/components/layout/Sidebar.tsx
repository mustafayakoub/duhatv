import React, { useState } from 'react'
import { useQuranStore } from '../../store/quranStore'

// بيانات السور الـ114 (مؤقتاً - سنستبدلها بقاعدة البيانات لاحقاً)
const SURAHS = [
  { number: 1, nameArabic: 'الفاتحة', ayahCount: 7, type: 'makkah' },
  { number: 2, nameArabic: 'البقرة', ayahCount: 286, type: 'madinah' },
  { number: 3, nameArabic: 'آل عمران', ayahCount: 200, type: 'madinah' },
  { number: 4, nameArabic: 'النساء', ayahCount: 176, type: 'madinah' },
  { number: 5, nameArabic: 'المائدة', ayahCount: 120, type: 'madinah' },
  { number: 6, nameArabic: 'الأنعام', ayahCount: 165, type: 'makkah' },
  { number: 7, nameArabic: 'الأعراف', ayahCount: 206, type: 'makkah' },
  { number: 8, nameArabic: 'الأنفال', ayahCount: 75, type: 'madinah' },
  { number: 9, nameArabic: 'التوبة', ayahCount: 129, type: 'madinah' },
  { number: 10, nameArabic: 'يونس', ayahCount: 109, type: 'makkah' },
  // ... سنضيف الباقي لاحقاً
]

interface SidebarProps {
  width: number
}

export const Sidebar: React.FC<SidebarProps> = ({ width }) => {
  const { currentSurah, goToAyah } = useQuranStore()
  const [searchTerm, setSearchTerm] = useState('')

  const filteredSurahs = SURAHS.filter((surah) =>
    surah.nameArabic.includes(searchTerm) || surah.number.toString().includes(searchTerm)
  )

  return (
    <div
      className="h-full bg-gradient-to-b from-golden-50 to-bronze-50 border-l-2 border-golden-200 flex flex-col"
      style={{ width: `${width}px` }}
    >
      {/* رأس الشريط */}
      <div className="p-4 border-b-2 border-golden-200">
        <h2 className="text-lg font-bold text-golden-800 font-arabic mb-3">سور القرآن</h2>

        {/* حقل البحث */}
        <input
          type="text"
          placeholder="بحث في السور..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-3 py-2 bg-white border-2 border-golden-300 rounded-lg focus:border-golden-500 focus:outline-none font-arabic text-right text-sm"
        />
      </div>

      {/* قائمة السور */}
      <div className="flex-1 overflow-y-auto">
        {filteredSurahs.map((surah) => (
          <button
            key={surah.number}
            onClick={() => goToAyah(surah.number, 1)}
            className={`w-full px-4 py-3 flex items-center gap-3 border-b border-golden-100 transition-all duration-200 hover:bg-golden-100 ${
              currentSurah === surah.number ? 'bg-golden-200 border-l-4 border-l-golden-600' : ''
            }`}
          >
            {/* رقم السورة */}
            <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
              currentSurah === surah.number
                ? 'bg-golden-600 text-white'
                : 'bg-golden-300 text-golden-800'
            }`}>
              {surah.number}
            </div>

            {/* معلومات السورة */}
            <div className="flex-1 text-right">
              <div className="text-base font-bold text-gray-800 font-arabic">{surah.nameArabic}</div>
              <div className="text-xs text-gray-600 font-arabic">
                {surah.ayahCount} آية • {surah.type === 'makkah' ? 'مكية' : 'مدنية'}
              </div>
            </div>

            {/* أيقونة السورة الحالية */}
            {currentSurah === surah.number && (
              <svg className="w-5 h-5 text-golden-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
            )}
          </button>
        ))}
      </div>

      {/* تذييل */}
      <div className="p-3 border-t-2 border-golden-200 text-center">
        <div className="text-sm text-gray-600 font-arabic">
          {filteredSurahs.length} من 114 سورة
        </div>
      </div>
    </div>
  )
}

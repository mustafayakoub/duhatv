import React from 'react'
import { useQuranStore } from '../../store/quranStore'
import { useSettingsStore } from '../../store/settingsStore'

// بيانات تجريبية للآيات (سنستبدلها بقاعدة البيانات)
const SAMPLE_AYAHS = {
  1: [
    { number: 1, text: 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ' },
    { number: 2, text: 'الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ' },
    { number: 3, text: 'الرَّحْمَٰنِ الرَّحِيمِ' },
    { number: 4, text: 'مَالِكِ يَوْمِ الدِّينِ' },
    { number: 5, text: 'إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ' },
    { number: 6, text: 'اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ' },
    { number: 7, text: 'صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ' },
  ],
}

export const QuranViewer: React.FC = () => {
  const { currentSurah } = useQuranStore()
  const { settings } = useSettingsStore()

  const ayahs = SAMPLE_AYAHS[currentSurah as keyof typeof SAMPLE_AYAHS] || []
  const surahName = currentSurah === 1 ? 'الفاتحة' : 'السورة'

  return (
    <div className="h-full flex flex-col bg-gradient-to-br from-golden-50/30 via-white to-bronze-50/30">
      {/* رأس السورة */}
      <div className="bg-gradient-to-r from-golden-100 to-bronze-100 border-b-4 border-golden-300 px-8 py-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center">
            <div className="inline-block px-6 py-3 bg-white rounded-xl shadow-lg border-2 border-golden-400">
              <h2 className="text-3xl font-bold text-golden-800 font-arabic">سورة {surahName}</h2>
              <div className="text-sm text-gray-600 font-arabic mt-1">
                {ayahs.length} آية • مكية
              </div>
            </div>
          </div>

          {/* البسملة */}
          {currentSurah !== 1 && currentSurah !== 9 && (
            <div className="text-center mt-6">
              <p className="text-2xl font-arabic text-golden-800" style={{ fontSize: `${settings.fontSize}px` }}>
                بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
              </p>
            </div>
          )}
        </div>
      </div>

      {/* عرض الآيات */}
      <div className="flex-1 overflow-y-auto p-8">
        <div className="max-w-4xl mx-auto space-y-6">
          {ayahs.map((ayah) => (
            <div
              key={ayah.number}
              className={`group ${
                settings.showLineHighlight ? 'hover:bg-golden-50/50 rounded-lg transition-colors' : ''
              }`}
            >
              <div className="p-4">
                <p
                  className="font-arabic text-gray-900 leading-loose"
                  style={{
                    fontSize: `${settings.fontSize}px`,
                    lineHeight: settings.lineHeight,
                    fontFamily: settings.fontFamily,
                  }}
                >
                  {ayah.text}
                  {settings.showAyahNumbers && (
                    <span className="inline-flex items-center justify-center w-8 h-8 mr-2 bg-golden-200 text-golden-800 rounded-full text-sm font-bold">
                      {ayah.number}
                    </span>
                  )}
                </p>

                {/* أدوات الآية (تظهر عند hover) */}
                <div className="opacity-0 group-hover:opacity-100 transition-opacity mt-2 flex gap-2">
                  <button className="px-3 py-1 bg-golden-100 hover:bg-golden-200 rounded text-xs font-arabic text-golden-800">
                    نسخ
                  </button>
                  <button className="px-3 py-1 bg-golden-100 hover:bg-golden-200 rounded text-xs font-arabic text-golden-800">
                    تفسير
                  </button>
                  <button className="px-3 py-1 bg-golden-100 hover:bg-golden-200 rounded text-xs font-arabic text-golden-800">
                    إعراب
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* شريط سفلي */}
      <div className="bg-white border-t-2 border-golden-200 px-6 py-3 flex items-center justify-between">
        <div className="text-sm text-gray-600 font-arabic">
          المصحف: {settings.selectedMushaf === 'hafs' ? 'رواية حفص' : settings.selectedMushaf}
        </div>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-golden-100 hover:bg-golden-200 rounded-lg text-sm font-arabic text-golden-800">
            ← السابقة
          </button>
          <button className="px-4 py-2 bg-golden-500 hover:bg-golden-600 text-white rounded-lg text-sm font-arabic">
            التالية →
          </button>
        </div>
      </div>
    </div>
  )
}

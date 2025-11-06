import React, { useState } from 'react'
import { TopBar } from './TopBar'
import { Sidebar } from './Sidebar'
import { QuranViewer } from '../quran/QuranViewer'
import { SettingsPanel } from '../settings/SettingsPanel'
import { useSettingsStore } from '../../store/settingsStore'

export const MainLayout: React.FC = () => {
  const { settings } = useSettingsStore()
  const [showSettings, setShowSettings] = useState(false)
  const [showSearch, setShowSearch] = useState(false)

  return (
    <div className="h-screen flex flex-col bg-white">
      {/* الشريط العلوي */}
      <TopBar
        onSettingsClick={() => setShowSettings(true)}
        onSearchClick={() => setShowSearch(true)}
      />

      {/* المحتوى الرئيسي */}
      <div className="flex-1 flex overflow-hidden">
        {/* عارض المصحف (المركز) */}
        <div className="flex-1">
          <QuranViewer />
        </div>

        {/* Sidebar (اليمين) */}
        <Sidebar width={settings.sidebarWidth} />

        {/* النوافذ الجانبية الإضافية (اليسار) */}
        {(settings.showTranslation ||
          settings.showTafseer ||
          settings.showIrab ||
          settings.showSarf ||
          settings.showMeanings) && (
          <div
            className="border-r-2 border-golden-200 bg-white overflow-y-auto"
            style={{ width: `${settings.panelWidth}px` }}
          >
            <div className="p-4">
              <h3 className="text-lg font-bold text-golden-800 font-arabic mb-4">النوافذ المساعدة</h3>

              {settings.showTranslation && (
                <div className="mb-6 bg-golden-50 p-4 rounded-lg">
                  <h4 className="font-bold text-gray-800 font-arabic mb-2">📘 الترجمة</h4>
                  <p className="text-sm text-gray-600 font-arabic">سيتم عرض الترجمات هنا...</p>
                </div>
              )}

              {settings.showTafseer && (
                <div className="mb-6 bg-golden-50 p-4 rounded-lg">
                  <h4 className="font-bold text-gray-800 font-arabic mb-2">📚 التفسير</h4>
                  <p className="text-sm text-gray-600 font-arabic">سيتم عرض التفاسير هنا...</p>
                </div>
              )}

              {settings.showIrab && (
                <div className="mb-6 bg-golden-50 p-4 rounded-lg">
                  <h4 className="font-bold text-gray-800 font-arabic mb-2">📝 الإعراب</h4>
                  <p className="text-sm text-gray-600 font-arabic">سيتم عرض الإعراب هنا...</p>
                </div>
              )}

              {settings.showSarf && (
                <div className="mb-6 bg-golden-50 p-4 rounded-lg">
                  <h4 className="font-bold text-gray-800 font-arabic mb-2">🔤 الصرف</h4>
                  <p className="text-sm text-gray-600 font-arabic">سيتم عرض الصرف هنا...</p>
                </div>
              )}

              {settings.showMeanings && (
                <div className="mb-6 bg-golden-50 p-4 rounded-lg">
                  <h4 className="font-bold text-gray-800 font-arabic mb-2">📖 المعاني</h4>
                  <p className="text-sm text-gray-600 font-arabic">سيتم عرض معاني المفردات هنا...</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* لوحة الإعدادات (Modal) */}
      <SettingsPanel isOpen={showSettings} onClose={() => setShowSettings(false)} />

      {/* لوحة البحث (سنضيفها لاحقاً) */}
      {showSearch && (
        <div className="fixed inset-0 bg-black/50 z-40" onClick={() => setShowSearch(false)}>
          <div className="max-w-2xl mx-auto mt-20 bg-white rounded-xl shadow-2xl p-6">
            <h3 className="text-xl font-bold text-golden-800 font-arabic mb-4">🔍 البحث الذكي</h3>
            <input
              type="text"
              placeholder="ابحث في القرآن الكريم..."
              className="w-full px-4 py-3 border-2 border-golden-300 rounded-lg focus:border-golden-500 focus:outline-none font-arabic text-right"
            />
            <p className="text-sm text-gray-600 font-arabic mt-4">
              سيتم إضافة البحث الذكي قريباً...
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

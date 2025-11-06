import React from 'react'
import { useSettingsStore } from '../../store/settingsStore'
import { Checkbox } from '../shared/Checkbox'
import { Select } from '../shared/Select'
import { Button } from '../shared/Button'

interface SettingsPanelProps {
  isOpen: boolean
  onClose: () => void
}

export const SettingsPanel: React.FC<SettingsPanelProps> = ({ isOpen, onClose }) => {
  const { settings, updateSettings, resetSettings } = useSettingsStore()

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* رأس اللوحة */}
        <div className="bg-gradient-to-r from-golden-500 to-bronze-500 px-6 py-4 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white font-arabic">⚙️ إعدادات التطبيق</h2>
          <button
            onClick={onClose}
            className="text-white hover:bg-white/20 rounded-lg p-2 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* المحتوى */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* قسم المصحف */}
          <section>
            <h3 className="text-lg font-bold text-golden-800 font-arabic mb-4 flex items-center gap-2">
              <span className="text-2xl">📖</span> المصحف
            </h3>
            <div className="space-y-4 bg-golden-50 p-4 rounded-lg">
              <Select
                label="اختر المصحف"
                value={settings.selectedMushaf}
                onChange={(value) => updateSettings({ selectedMushaf: value as any })}
                options={[
                  { value: 'hafs', label: 'رواية حفص عن عاصم (الأشهر)' },
                  { value: 'warsh', label: 'رواية ورش عن نافع' },
                  { value: 'qalun', label: 'رواية قالون عن نافع' },
                  { value: 'shuba', label: 'رواية شعبة عن عاصم' },
                  { value: 'sousi', label: 'رواية السوسي عن أبي عمرو' },
                  { value: 'douri-abu-amr', label: 'رواية الدوري عن أبي عمرو' },
                  { value: 'douri-alkisai', label: 'رواية الدوري عن الكسائي' },
                ]}
              />

              <Select
                label="نوع الخط"
                value={settings.fontFamily}
                onChange={(value) => updateSettings({ fontFamily: value as string })}
                options={[
                  { value: 'Amiri', label: 'خط أميري (موصى به)' },
                  { value: 'Scheherazade New', label: 'خط شهرزاد' },
                  { value: 'KFGQPC Hafs', label: 'خط المصحف العثماني' },
                  { value: 'Traditional Arabic', label: 'خط تقليدي عربي' },
                ]}
              />

              <div>
                <label className="block text-sm font-medium text-gray-700 font-arabic mb-2">
                  حجم الخط: {settings.fontSize}px
                </label>
                <input
                  type="range"
                  min="16"
                  max="48"
                  value={settings.fontSize}
                  onChange={(e) => updateSettings({ fontSize: parseInt(e.target.value) })}
                  className="w-full h-2 bg-golden-200 rounded-lg appearance-none cursor-pointer accent-golden-500"
                />
              </div>
            </div>
          </section>

          {/* قسم التجويد والعرض */}
          <section>
            <h3 className="text-lg font-bold text-golden-800 font-arabic mb-4 flex items-center gap-2">
              <span className="text-2xl">🎨</span> التجويد والعرض
            </h3>
            <div className="space-y-3 bg-golden-50 p-4 rounded-lg">
              <Checkbox
                label="عرض ألوان التجويد (18 لون)"
                description="تلوين الحروف حسب أحكام التجويد (إدغام، إخفاء، مد...)"
                checked={settings.showTajweedColors}
                onChange={(checked) => updateSettings({ showTajweedColors: checked })}
              />

              <Checkbox
                label="فصل حروف العطف والزوائد"
                description="عرض حروف العطف (و، ف، ثم...) والزوائد منفصلة عن الكلمات"
                checked={settings.separateConjunctions}
                onChange={(checked) => updateSettings({ separateConjunctions: checked })}
              />

              <Checkbox
                label="تحديد السطر عند التمرير"
                description="إظهار خلفية ملونة للسطر عند مرور الفأرة"
                checked={settings.showLineHighlight}
                onChange={(checked) => updateSettings({ showLineHighlight: checked })}
              />

              <Checkbox
                label="عرض أرقام الآيات"
                description="إظهار رقم الآية بجانب النص"
                checked={settings.showAyahNumbers}
                onChange={(checked) => updateSettings({ showAyahNumbers: checked })}
              />
            </div>
          </section>

          {/* قسم النوافذ الجانبية */}
          <section>
            <h3 className="text-lg font-bold text-golden-800 font-arabic mb-4 flex items-center gap-2">
              <span className="text-2xl">🪟</span> النوافذ المساعدة
            </h3>
            <div className="space-y-3 bg-golden-50 p-4 rounded-lg">
              <Checkbox
                label="نافذة الترجمات"
                description="عرض ترجمات الآيات في نافذة منفصلة"
                checked={settings.showTranslation}
                onChange={(checked) => updateSettings({ showTranslation: checked })}
              />

              <Checkbox
                label="نافذة التفاسير"
                description="عرض تفاسير الآيات (102+ تفسير)"
                checked={settings.showTafseer}
                onChange={(checked) => updateSettings({ showTafseer: checked })}
              />

              <Checkbox
                label="نافذة الإعراب"
                description="عرض إعراب الكلمات والجمل"
                checked={settings.showIrab}
                onChange={(checked) => updateSettings({ showIrab: checked })}
              />

              <Checkbox
                label="نافذة الصرف"
                description="عرض التحليل الصرفي للكلمات"
                checked={settings.showSarf}
                onChange={(checked) => updateSettings({ showSarf: checked })}
              />

              <Checkbox
                label="نافذة معاني المفردات"
                description="عرض معاني الكلمات والجذور اللغوية"
                checked={settings.showMeanings}
                onChange={(checked) => updateSettings({ showMeanings: checked })}
              />
            </div>
          </section>

          {/* قسم البحث */}
          <section>
            <h3 className="text-lg font-bold text-golden-800 font-arabic mb-4 flex items-center gap-2">
              <span className="text-2xl">🔍</span> البحث الذكي
            </h3>
            <div className="space-y-4 bg-golden-50 p-4 rounded-lg">
              <Select
                label="نوع البحث الافتراضي"
                value={settings.searchType}
                onChange={(value) => updateSettings({ searchType: value as any })}
                options={[
                  { value: 'exact', label: 'مطابق تام - البحث عن النص بالضبط' },
                  { value: 'partial', label: 'مطابق جزئي - البحث عن جزء من النص' },
                  { value: 'morphological', label: 'بحث صرفي - البحث في الجذور والمشتقات' },
                  { value: 'grammatical', label: 'بحث نحوي - البحث في التراكيب النحوية' },
                  { value: 'thematic', label: 'بحث موضوعي - البحث حسب المواضيع' },
                ]}
              />
            </div>
          </section>
        </div>

        {/* أزرار السفلية */}
        <div className="border-t-2 border-golden-200 px-6 py-4 flex items-center justify-between bg-gray-50">
          <Button variant="secondary" onClick={resetSettings}>
            إعادة تعيين الإعدادات
          </Button>
          <Button variant="primary" onClick={onClose}>
            حفظ وإغلاق
          </Button>
        </div>
      </div>
    </div>
  )
}

import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface QuranSettings {
  // إعدادات المصحف
  selectedMushaf: 'hafs' | 'warsh' | 'qalun' | 'shuba' | 'sousi' | 'douri-abu-amr' | 'douri-alkisai'
  fontSize: number
  fontFamily: string
  lineHeight: number

  // إعدادات العرض
  showTajweedColors: boolean
  separateConjunctions: boolean // فصل حروف العطف
  showLineHighlight: boolean
  showAyahNumbers: boolean

  // إعدادات النوافذ
  showTranslation: boolean
  showTafseer: boolean
  showIrab: boolean
  showSarf: boolean
  showMeanings: boolean

  // الترجمات والتفاسير المختارة
  selectedTranslations: number[]
  selectedTafseer: number | null

  // إعدادات البحث
  searchType: 'exact' | 'partial' | 'morphological' | 'grammatical' | 'thematic'

  // Layout
  sidebarWidth: number
  panelWidth: number
}

interface SettingsStore {
  settings: QuranSettings
  updateSettings: (partial: Partial<QuranSettings>) => void
  resetSettings: () => void
}

const defaultSettings: QuranSettings = {
  selectedMushaf: 'hafs',
  fontSize: 24,
  fontFamily: 'Amiri',
  lineHeight: 2,

  showTajweedColors: false,
  separateConjunctions: false,
  showLineHighlight: true,
  showAyahNumbers: true,

  showTranslation: false,
  showTafseer: false,
  showIrab: false,
  showSarf: false,
  showMeanings: false,

  selectedTranslations: [],
  selectedTafseer: null,

  searchType: 'partial',

  sidebarWidth: 280,
  panelWidth: 350,
}

export const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      settings: defaultSettings,

      updateSettings: (partial) =>
        set((state) => ({
          settings: { ...state.settings, ...partial },
        })),

      resetSettings: () => set({ settings: defaultSettings }),
    }),
    {
      name: 'basaer-settings',
    }
  )
)

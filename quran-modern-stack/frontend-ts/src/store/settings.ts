import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Settings, ThemeMode } from '@/types';

interface SettingsStore extends Settings {
  setTheme: (theme: ThemeMode) => void;
  toggleTheme: () => void;
  setFontSize: (size: Settings['fontSize']) => void;
  toggleTransliteration: () => void;
  toggleTranslation: () => void;
  reset: () => void;
}

const defaultSettings: Settings = {
  theme: 'light',
  language: 'ar',
  fontSize: 'medium',
  showTransliteration: false,
  showTranslation: true,
};

export const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      ...defaultSettings,

      setTheme: (theme) => set({ theme }),

      toggleTheme: () =>
        set((state) => ({
          theme: state.theme === 'light' ? 'dark' : 'light',
        })),

      setFontSize: (fontSize) => set({ fontSize }),

      toggleTransliteration: () =>
        set((state) => ({
          showTransliteration: !state.showTransliteration,
        })),

      toggleTranslation: () =>
        set((state) => ({
          showTranslation: !state.showTranslation,
        })),

      reset: () => set(defaultSettings),
    }),
    {
      name: 'quran-settings',
    }
  )
);

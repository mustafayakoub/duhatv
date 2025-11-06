import { create } from 'zustand'

export interface Surah {
  number: number
  nameArabic: string
  nameEnglish: string
  ayahCount: number
  revelationType: 'makkah' | 'madinah'
}

export interface Ayah {
  surahNumber: number
  ayahNumber: number
  text: string
  juz: number
  page: number
  line?: number
}

interface QuranStore {
  // البيانات الحالية
  currentSurah: number
  currentAyah: number
  currentPage: number

  // البيانات
  surahs: Surah[]
  ayahs: Ayah[]

  // Actions
  setCurrentSurah: (surahNumber: number) => void
  setCurrentAyah: (ayahNumber: number) => void
  setCurrentPage: (pageNumber: number) => void
  setSurahs: (surahs: Surah[]) => void
  setAyahs: (ayahs: Ayah[]) => void
  goToAyah: (surahNumber: number, ayahNumber: number) => void
}

export const useQuranStore = create<QuranStore>((set) => ({
  currentSurah: 1,
  currentAyah: 1,
  currentPage: 1,

  surahs: [],
  ayahs: [],

  setCurrentSurah: (surahNumber) => set({ currentSurah: surahNumber }),
  setCurrentAyah: (ayahNumber) => set({ currentAyah: ayahNumber }),
  setCurrentPage: (pageNumber) => set({ currentPage: pageNumber }),

  setSurahs: (surahs) => set({ surahs }),
  setAyahs: (ayahs) => set({ ayahs }),

  goToAyah: (surahNumber, ayahNumber) =>
    set({ currentSurah: surahNumber, currentAyah: ayahNumber }),
}))

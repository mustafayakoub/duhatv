// API Response Types

export interface Surah {
  id: number;
  name: string;
  name_arabic: string;
  name_translation: string;
  revelation_type: 'Meccan' | 'Medinan';
  number_of_ayahs: number;
}

export interface Ayah {
  id: number;
  surah_id: number;
  ayah_number: number;
  text_arabic: string;
  text_translation?: string;
  text_transliteration?: string;
  juz: number;
  page: number;
}

export interface SurahDetail extends Surah {
  ayahs: Ayah[];
}

export interface SearchResult {
  surah_id: number;
  surah_name: string;
  surah_name_arabic: string;
  ayah_number: number;
  text_arabic: string;
  text_translation?: string;
  relevance_score?: number;
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
  query: string;
  took_ms?: number;
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

export interface ApiError {
  error: string;
  details?: string;
  status: number;
}

// UI State Types

export type ThemeMode = 'light' | 'dark';

export type Language = 'ar' | 'en';

export interface Settings {
  theme: ThemeMode;
  language: Language;
  fontSize: 'small' | 'medium' | 'large';
  showTransliteration: boolean;
  showTranslation: boolean;
}

// Navigation Types

export interface RouteParams {
  surahId?: string;
}

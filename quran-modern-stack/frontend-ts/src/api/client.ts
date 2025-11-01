import axios, { AxiosInstance, AxiosError } from 'axios';
import { Surah, SurahDetail, SearchResponse, ApiError } from '@/types';

// API Base URLs
const RUST_API_BASE = import.meta.env.VITE_RUST_API_URL || 'http://localhost:8000';
const GO_SEARCH_BASE = import.meta.env.VITE_GO_SEARCH_URL || 'http://localhost:8001';

// Axios instances
const rustClient: AxiosInstance = axios.create({
  baseURL: RUST_API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

const goClient: AxiosInstance = axios.create({
  baseURL: GO_SEARCH_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Error handler
const handleApiError = (error: AxiosError): ApiError => {
  if (error.response) {
    return {
      error: error.response.data?.error || error.message,
      details: error.response.data?.details,
      status: error.response.status,
    };
  } else if (error.request) {
    return {
      error: 'لا يوجد استجابة من الخادم',
      details: 'تأكد من تشغيل الخدمة الخلفية',
      status: 0,
    };
  } else {
    return {
      error: error.message,
      status: 0,
    };
  }
};

// API Methods
export const quranApi = {
  // Get all Surahs
  getSurahs: async (): Promise<Surah[]> => {
    try {
      const response = await rustClient.get<Surah[]>('/api/surahs');
      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  // Get Surah by ID with all Ayahs
  getSurahById: async (id: number): Promise<SurahDetail> => {
    try {
      const response = await rustClient.get<SurahDetail>(`/api/surahs/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  // Get specific Ayah
  getAyah: async (surahId: number, ayahNumber: number) => {
    try {
      const response = await rustClient.get(`/api/surahs/${surahId}/ayahs/${ayahNumber}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  // Health check
  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await rustClient.get('/health');
      return response.status === 200;
    } catch (error) {
      return false;
    }
  },
};

export const searchApi = {
  // Search in Quran (using Go service)
  search: async (query: string, limit: number = 20): Promise<SearchResponse> => {
    try {
      const response = await goClient.get<SearchResponse>('/search', {
        params: { q: query, limit },
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  // Health check
  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await goClient.get('/health');
      return response.status === 200;
    } catch (error) {
      return false;
    }
  },
};

// Export clients for advanced usage
export { rustClient, goClient };

import { useQuery, UseQueryResult } from 'react-query';
import { quranApi, searchApi } from './client';
import { Surah, SurahDetail, SearchResponse } from '@/types';

// Query keys
export const queryKeys = {
  surahs: ['surahs'] as const,
  surah: (id: number) => ['surah', id] as const,
  search: (query: string) => ['search', query] as const,
  health: ['health'] as const,
};

// Hooks for data fetching

export const useSurahs = (): UseQueryResult<Surah[], Error> => {
  return useQuery(queryKeys.surahs, quranApi.getSurahs, {
    staleTime: 1000 * 60 * 60, // 1 hour - surahs don't change
    cacheTime: 1000 * 60 * 60 * 24, // 24 hours
  });
};

export const useSurah = (id: number): UseQueryResult<SurahDetail, Error> => {
  return useQuery(queryKeys.surah(id), () => quranApi.getSurahById(id), {
    enabled: id > 0 && id <= 114,
    staleTime: 1000 * 60 * 30, // 30 minutes
    cacheTime: 1000 * 60 * 60, // 1 hour
  });
};

export const useSearch = (
  query: string,
  enabled: boolean = true
): UseQueryResult<SearchResponse, Error> => {
  return useQuery(
    queryKeys.search(query),
    () => searchApi.search(query),
    {
      enabled: enabled && query.length >= 2,
      staleTime: 1000 * 60 * 5, // 5 minutes
      cacheTime: 1000 * 60 * 10, // 10 minutes
    }
  );
};

export const useHealthCheck = (): UseQueryResult<boolean, Error> => {
  return useQuery(queryKeys.health, quranApi.healthCheck, {
    refetchInterval: 30000, // Check every 30 seconds
    retry: 3,
  });
};

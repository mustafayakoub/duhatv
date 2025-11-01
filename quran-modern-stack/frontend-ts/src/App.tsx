import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';
import { useSettingsStore } from '@/store/settings';
import { getTheme } from '@/theme';
import { Navbar } from '@/components/Navbar';
import { Home } from '@/pages/Home';
import { SurahDetail } from '@/pages/SurahDetail';
import { Search } from '@/pages/Search';
import { Settings } from '@/pages/Settings';
import { prefixer } from 'stylis';
import rtlPlugin from 'stylis-plugin-rtl';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';

// Create RTL cache
const cacheRtl = createCache({
  key: 'muirtl',
  stylisPlugins: [prefixer, rtlPlugin],
});

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

function App() {
  const theme = useSettingsStore((state) => state.theme);
  const muiTheme = getTheme(theme);

  return (
    <CacheProvider value={cacheRtl}>
      <ThemeProvider theme={muiTheme}>
        <QueryClientProvider client={queryClient}>
          <CssBaseline />
          <Router>
            <Box
              sx={{
                minHeight: '100vh',
                backgroundColor: 'background.default',
                transition: 'background-color 0.3s ease',
              }}
            >
              <Navbar />
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/surah/:surahId" element={<SurahDetail />} />
                <Route path="/search" element={<Search />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </Box>
          </Router>
        </QueryClientProvider>
      </ThemeProvider>
    </CacheProvider>
  );
}

export default App;

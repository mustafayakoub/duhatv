import { Container, Typography, Grid, Box, TextField, InputAdornment } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { useSurahs } from '@/api/hooks';
import { SurahCard } from '@/components/SurahCard';
import { Loading } from '@/components/Loading';
import { ErrorMessage } from '@/components/ErrorMessage';
import { useState, useMemo } from 'react';

export const Home: React.FC = () => {
  const { data: surahs, isLoading, error, refetch } = useSurahs();
  const [searchQuery, setSearchQuery] = useState('');

  const filteredSurahs = useMemo(() => {
    if (!surahs || !searchQuery) return surahs;

    const query = searchQuery.toLowerCase();
    return surahs.filter(
      (surah) =>
        surah.name_arabic.includes(searchQuery) ||
        surah.name.toLowerCase().includes(query) ||
        surah.name_translation.toLowerCase().includes(query) ||
        surah.id.toString().includes(query)
    );
  }, [surahs, searchQuery]);

  if (isLoading) {
    return <Loading message="جاري تحميل السور..." />;
  }

  if (error) {
    return (
      <ErrorMessage
        message={(error as Error).message || 'فشل تحميل قائمة السور'}
        onRetry={() => refetch()}
      />
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{
            fontFamily: '"Amiri", serif',
            fontWeight: 700,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          القرآن الكريم
        </Typography>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          114 سورة
        </Typography>
      </Box>

      {/* Search */}
      <Box sx={{ mb: 4 }}>
        <TextField
          fullWidth
          placeholder="ابحث عن سورة بالاسم أو الرقم..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
          sx={{
            '& .MuiOutlinedInput-root': {
              borderRadius: 3,
            },
          }}
        />
      </Box>

      {/* Surahs Grid */}
      <Grid container spacing={3}>
        {filteredSurahs?.map((surah) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={surah.id}>
            <SurahCard surah={surah} />
          </Grid>
        ))}
      </Grid>

      {/* No Results */}
      {filteredSurahs?.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary">
            لا توجد نتائج للبحث &quot;{searchQuery}&quot;
          </Typography>
        </Box>
      )}
    </Container>
  );
};

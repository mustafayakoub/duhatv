import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  IconButton,
  Chip,
  Divider,
  Fab,
  Tooltip,
} from '@mui/material';
import { ArrowBack, ArrowForward, KeyboardArrowUp } from '@mui/icons-material';
import { useSurah } from '@/api/hooks';
import { AyahCard } from '@/components/AyahCard';
import { Loading } from '@/components/Loading';
import { ErrorMessage } from '@/components/ErrorMessage';
import { useEffect, useState } from 'react';

export const SurahDetail: React.FC = () => {
  const { surahId } = useParams<{ surahId: string }>();
  const navigate = useNavigate();
  const [showScrollTop, setShowScrollTop] = useState(false);

  const id = parseInt(surahId || '1', 10);
  const { data: surah, isLoading, error, refetch } = useSurah(id);

  // Scroll to top on mount
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [id]);

  // Show/hide scroll to top button
  useEffect(() => {
    const handleScroll = () => {
      setShowScrollTop(window.scrollY > 400);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const goToPrevious = () => {
    if (id > 1) navigate(`/surah/${id - 1}`);
  };

  const goToNext = () => {
    if (id < 114) navigate(`/surah/${id + 1}`);
  };

  if (isLoading) {
    return <Loading message="جاري تحميل السورة..." />;
  }

  if (error || !surah) {
    return (
      <ErrorMessage
        message={(error as Error)?.message || 'فشل تحميل السورة'}
        onRetry={() => refetch()}
      />
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      {/* Header */}
      <Box
        sx={{
          mb: 4,
          p: 4,
          borderRadius: 3,
          background: (theme) =>
            theme.palette.mode === 'dark'
              ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
              : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          textAlign: 'center',
        }}
      >
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Chip
            label={surah.revelation_type === 'Meccan' ? 'مكية' : 'مدنية'}
            sx={{
              backgroundColor: 'rgba(255,255,255,0.2)',
              color: 'white',
              fontWeight: 'bold',
            }}
          />
          <Typography variant="h6">سورة {surah.id}</Typography>
        </Box>

        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{
            fontFamily: '"Amiri", serif',
            fontWeight: 700,
          }}
        >
          {surah.name_arabic}
        </Typography>

        <Typography variant="h6" gutterBottom>
          {surah.name}
        </Typography>

        <Typography variant="body1" sx={{ opacity: 0.9 }}>
          {surah.name_translation}
        </Typography>

        <Divider sx={{ my: 2, backgroundColor: 'rgba(255,255,255,0.3)' }} />

        <Typography variant="body2">
          {surah.number_of_ayahs} آية
        </Typography>
      </Box>

      {/* Bismillah (except for Surah 9 and Surah 1) */}
      {id !== 1 && id !== 9 && (
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Typography
            sx={{
              fontFamily: '"Amiri", serif',
              fontSize: '2.5rem',
              fontWeight: 700,
            }}
          >
            بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
          </Typography>
        </Box>
      )}

      {/* Ayahs */}
      <Box sx={{ mb: 4 }}>
        {surah.ayahs?.map((ayah) => (
          <AyahCard key={ayah.id} ayah={ayah} />
        ))}
      </Box>

      {/* Navigation */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mt: 4,
          p: 2,
          borderRadius: 2,
          backgroundColor: (theme) =>
            theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)',
        }}
      >
        <Tooltip title="السورة التالية">
          <span>
            <IconButton
              onClick={goToNext}
              disabled={id >= 114}
              size="large"
              color="primary"
            >
              <ArrowForward />
            </IconButton>
          </span>
        </Tooltip>

        <Typography variant="body2" color="text.secondary">
          سورة {id} من 114
        </Typography>

        <Tooltip title="السورة السابقة">
          <span>
            <IconButton
              onClick={goToPrevious}
              disabled={id <= 1}
              size="large"
              color="primary"
            >
              <ArrowBack />
            </IconButton>
          </span>
        </Tooltip>
      </Box>

      {/* Scroll to Top FAB */}
      {showScrollTop && (
        <Fab
          color="primary"
          size="medium"
          onClick={scrollToTop}
          sx={{
            position: 'fixed',
            bottom: 16,
            left: 16,
          }}
        >
          <KeyboardArrowUp />
        </Fab>
      )}
    </Container>
  );
};

import { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  TextField,
  InputAdornment,
  Card,
  CardContent,
  Chip,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';
import { useSearch } from '@/api/hooks';
import { Loading } from '@/components/Loading';
import { ErrorMessage } from '@/components/ErrorMessage';

export const Search: React.FC = () => {
  const [query, setQuery] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');
  const navigate = useNavigate();

  const { data: results, isLoading, error } = useSearch(debouncedQuery, debouncedQuery.length >= 2);

  // Debounce search
  const handleSearch = (value: string) => {
    setQuery(value);
    const timer = setTimeout(() => {
      setDebouncedQuery(value);
    }, 500);
    return () => clearTimeout(timer);
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{
            fontFamily: '"Amiri", serif',
            fontWeight: 700,
          }}
        >
          البحث في القرآن الكريم
        </Typography>
        <Typography variant="body1" color="text.secondary">
          ابحث عن أي كلمة أو عبارة في القرآن الكريم
        </Typography>
      </Box>

      {/* Search Box */}
      <Box sx={{ mb: 4 }}>
        <TextField
          fullWidth
          autoFocus
          placeholder="اكتب كلمة أو عبارة للبحث..."
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
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
              fontSize: '1.2rem',
            },
          }}
        />
      </Box>

      {/* Results */}
      {isLoading && query.length >= 2 && (
        <Loading message="جاري البحث..." fullScreen={false} />
      )}

      {error && (
        <ErrorMessage
          title="فشل البحث"
          message={(error as Error).message || 'حدث خطأ أثناء البحث'}
        />
      )}

      {results && results.results.length > 0 && (
        <>
          {/* Results Header */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              النتائج ({results.total})
            </Typography>
            {results.took_ms && (
              <Typography variant="caption" color="text.secondary">
                البحث استغرق {results.took_ms} مللي ثانية
              </Typography>
            )}
          </Box>

          {/* Results List */}
          {results.results.map((result, index) => (
            <Card
              key={index}
              sx={{
                mb: 2,
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateX(-4px)',
                  boxShadow: 4,
                },
              }}
              onClick={() => navigate(`/surah/${result.surah_id}`)}
            >
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Chip
                    label={result.surah_name_arabic}
                    color="primary"
                    size="small"
                  />
                  <Typography variant="caption" color="text.secondary">
                    آية {result.ayah_number}
                  </Typography>
                </Box>

                <Typography
                  sx={{
                    fontFamily: '"Amiri", serif',
                    fontSize: '1.5rem',
                    lineHeight: 2,
                    mb: 2,
                    direction: 'rtl',
                  }}
                >
                  {result.text_arabic}
                </Typography>

                {result.text_translation && (
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ lineHeight: 1.8 }}
                  >
                    {result.text_translation}
                  </Typography>
                )}

                {result.relevance_score && (
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      الصلة: {(result.relevance_score * 100).toFixed(1)}%
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          ))}
        </>
      )}

      {/* No Results */}
      {results && results.results.length === 0 && debouncedQuery.length >= 2 && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary">
            لا توجد نتائج للبحث &quot;{debouncedQuery}&quot;
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            جرب كلمات بحث أخرى
          </Typography>
        </Box>
      )}

      {/* Initial State */}
      {!query && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <SearchIcon sx={{ fontSize: 80, color: 'text.disabled', mb: 2 }} />
          <Typography variant="h6" color="text.secondary">
            ابدأ بكتابة كلمة للبحث
          </Typography>
        </Box>
      )}
    </Container>
  );
};

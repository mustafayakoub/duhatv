import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Surah } from '@/types';

interface SurahCardProps {
  surah: Surah;
}

export const SurahCard: React.FC<SurahCardProps> = ({ surah }) => {
  const navigate = useNavigate();

  return (
    <Card
      sx={{
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 6,
        },
      }}
      onClick={() => navigate(`/surah/${surah.id}`)}
    >
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontWeight: 'bold',
            }}
          >
            {surah.id}
          </Box>
          <Chip
            label={surah.revelation_type === 'Meccan' ? 'مكية' : 'مدنية'}
            size="small"
            color={surah.revelation_type === 'Meccan' ? 'primary' : 'secondary'}
          />
        </Box>

        <Typography
          variant="h5"
          component="h2"
          gutterBottom
          sx={{
            fontFamily: '"Amiri", serif',
            fontSize: '1.8rem',
            fontWeight: 700,
            textAlign: 'center',
            mb: 1,
          }}
        >
          {surah.name_arabic}
        </Typography>

        <Typography
          variant="subtitle1"
          color="text.secondary"
          sx={{ textAlign: 'center', mb: 1 }}
        >
          {surah.name}
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
          sx={{ textAlign: 'center', fontStyle: 'italic' }}
        >
          {surah.name_translation}
        </Typography>

        <Box display="flex" justifyContent="center" mt={2}>
          <Typography variant="body2" color="text.secondary">
            {surah.number_of_ayahs} آية
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

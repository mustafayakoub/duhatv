import { Card, CardContent, Typography, Box, Divider } from '@mui/material';
import { Ayah } from '@/types';
import { useSettingsStore } from '@/store/settings';

interface AyahCardProps {
  ayah: Ayah;
  surahName?: string;
}

export const AyahCard: React.FC<AyahCardProps> = ({ ayah, surahName }) => {
  const { fontSize, showTranslation, showTransliteration } = useSettingsStore();

  const getFontSize = () => {
    switch (fontSize) {
      case 'small':
        return '1.5rem';
      case 'large':
        return '2.2rem';
      default:
        return '1.8rem';
    }
  };

  return (
    <Card
      sx={{
        mb: 2,
        background: (theme) =>
          theme.palette.mode === 'dark'
            ? 'linear-gradient(135deg, #2d3748 0%, #1a202c 100%)'
            : 'linear-gradient(135deg, #ffffff 0%, #f7fafc 100%)',
      }}
    >
      <CardContent>
        {/* Ayah Number Badge */}
        <Box display="flex" justifyContent="center" mb={3}>
          <Box
            sx={{
              px: 3,
              py: 1,
              borderRadius: 20,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              fontWeight: 'bold',
            }}
          >
            {surahName && (
              <Typography variant="caption" component="span" sx={{ mr: 1 }}>
                {surahName}
              </Typography>
            )}
            <Typography variant="body2" component="span">
              آية {ayah.ayah_number}
            </Typography>
          </Box>
        </Box>

        {/* Arabic Text */}
        <Typography
          sx={{
            fontFamily: '"Amiri", "Scheherazade New", serif',
            fontSize: getFontSize(),
            lineHeight: 2,
            textAlign: 'center',
            mb: 2,
            direction: 'rtl',
          }}
        >
          {ayah.text_arabic}
          <Typography
            component="span"
            sx={{
              fontFamily: '"Amiri", serif',
              fontSize: '1.2em',
              mx: 0.5,
            }}
          >
            ﴿{ayah.ayah_number}﴾
          </Typography>
        </Typography>

        {/* Translation */}
        {showTranslation && ayah.text_translation && (
          <>
            <Divider sx={{ my: 2 }} />
            <Typography
              variant="body1"
              sx={{
                fontFamily: '"Cairo", sans-serif',
                lineHeight: 1.8,
                textAlign: 'justify',
                color: 'text.secondary',
              }}
            >
              {ayah.text_translation}
            </Typography>
          </>
        )}

        {/* Transliteration */}
        {showTransliteration && ayah.text_transliteration && (
          <>
            <Divider sx={{ my: 2 }} />
            <Typography
              variant="body2"
              sx={{
                fontFamily: '"Cairo", sans-serif',
                fontStyle: 'italic',
                lineHeight: 1.6,
                textAlign: 'justify',
                color: 'text.secondary',
              }}
            >
              {ayah.text_transliteration}
            </Typography>
          </>
        )}

        {/* Metadata */}
        <Box display="flex" justifyContent="space-between" mt={2} pt={2}>
          <Typography variant="caption" color="text.secondary">
            جزء {ayah.juz}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            صفحة {ayah.page}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

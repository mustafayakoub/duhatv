import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Switch,
  Divider,
  Button,
} from '@mui/material';
import {
  Brightness4,
  Brightness7,
  TextFields,
  Translate,
  RestartAlt,
} from '@mui/icons-material';
import { useSettingsStore } from '@/store/settings';

export const Settings: React.FC = () => {
  const {
    theme,
    fontSize,
    showTranslation,
    showTransliteration,
    setTheme,
    setFontSize,
    toggleTranslation,
    toggleTransliteration,
    reset,
  } = useSettingsStore();

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
          الإعدادات
        </Typography>
        <Typography variant="body1" color="text.secondary">
          خصص تجربة القراءة حسب تفضيلاتك
        </Typography>
      </Box>

      {/* Theme Settings */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            {theme === 'dark' ? <Brightness4 sx={{ mr: 1 }} /> : <Brightness7 sx={{ mr: 1 }} />}
            <Typography variant="h6">المظهر</Typography>
          </Box>
          <Divider sx={{ mb: 2 }} />
          <FormControl component="fieldset">
            <RadioGroup
              value={theme}
              onChange={(e) => setTheme(e.target.value as 'light' | 'dark')}
            >
              <FormControlLabel value="light" control={<Radio />} label="الوضع الفاتح" />
              <FormControlLabel value="dark" control={<Radio />} label="الوضع الداكن" />
            </RadioGroup>
          </FormControl>
        </CardContent>
      </Card>

      {/* Font Size Settings */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <TextFields sx={{ mr: 1 }} />
            <Typography variant="h6">حجم الخط</Typography>
          </Box>
          <Divider sx={{ mb: 2 }} />
          <FormControl component="fieldset">
            <RadioGroup
              value={fontSize}
              onChange={(e) => setFontSize(e.target.value as 'small' | 'medium' | 'large')}
            >
              <FormControlLabel value="small" control={<Radio />} label="صغير" />
              <FormControlLabel value="medium" control={<Radio />} label="متوسط" />
              <FormControlLabel value="large" control={<Radio />} label="كبير" />
            </RadioGroup>
          </FormControl>

          {/* Font Preview */}
          <Box
            sx={{
              mt: 3,
              p: 2,
              borderRadius: 2,
              backgroundColor: (theme) =>
                theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)',
            }}
          >
            <Typography
              sx={{
                fontFamily: '"Amiri", serif',
                fontSize: fontSize === 'small' ? '1.5rem' : fontSize === 'large' ? '2.2rem' : '1.8rem',
                textAlign: 'center',
              }}
            >
              بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
            </Typography>
          </Box>
        </CardContent>
      </Card>

      {/* Display Settings */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Translate sx={{ mr: 1 }} />
            <Typography variant="h6">خيارات العرض</Typography>
          </Box>
          <Divider sx={{ mb: 2 }} />

          <Box>
            <Box
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              mb={2}
            >
              <Box>
                <Typography variant="body1">عرض الترجمة</Typography>
                <Typography variant="caption" color="text.secondary">
                  إظهار ترجمة معاني الآيات
                </Typography>
              </Box>
              <Switch checked={showTranslation} onChange={toggleTranslation} />
            </Box>

            <Divider sx={{ my: 2 }} />

            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Box>
                <Typography variant="body1">عرض النقحرة</Typography>
                <Typography variant="caption" color="text.secondary">
                  إظهار النطق بالأحرف اللاتينية
                </Typography>
              </Box>
              <Switch checked={showTransliteration} onChange={toggleTransliteration} />
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Reset Settings */}
      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <RestartAlt sx={{ mr: 1 }} />
            <Typography variant="h6">إعادة تعيين</Typography>
          </Box>
          <Divider sx={{ mb: 2 }} />
          <Typography variant="body2" color="text.secondary" mb={2}>
            إعادة جميع الإعدادات إلى القيم الافتراضية
          </Typography>
          <Button variant="outlined" color="error" onClick={reset} startIcon={<RestartAlt />}>
            إعادة تعيين الإعدادات
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
};

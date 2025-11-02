import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Container,
  Tooltip,
} from '@mui/material';
import {
  Brightness4,
  Brightness7,
  Settings,
  Search,
  Home,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useSettingsStore } from '@/store/settings';

export const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { theme, toggleTheme } = useSettingsStore();

  const isActive = (path: string) => location.pathname === path;

  return (
    <AppBar
      position="sticky"
      sx={{
        background: (theme) =>
          theme.palette.mode === 'dark'
            ? 'linear-gradient(135deg, #2d3748 0%, #1a202c 100%)'
            : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        boxShadow: 3,
      }}
    >
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          {/* Logo */}
          <Typography
            variant="h5"
            component="div"
            sx={{
              flexGrow: 1,
              fontFamily: '"Amiri", serif',
              fontWeight: 700,
              cursor: 'pointer',
            }}
            onClick={() => navigate('/')}
          >
            القرآن الكريم
          </Typography>

          {/* Navigation Icons */}
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Tooltip title="الصفحة الرئيسية">
              <IconButton
                color="inherit"
                onClick={() => navigate('/')}
                sx={{
                  backgroundColor: isActive('/') ? 'rgba(255,255,255,0.2)' : 'transparent',
                }}
              >
                <Home />
              </IconButton>
            </Tooltip>

            <Tooltip title="البحث">
              <IconButton
                color="inherit"
                onClick={() => navigate('/search')}
                sx={{
                  backgroundColor: isActive('/search') ? 'rgba(255,255,255,0.2)' : 'transparent',
                }}
              >
                <Search />
              </IconButton>
            </Tooltip>

            <Tooltip title="الإعدادات">
              <IconButton
                color="inherit"
                onClick={() => navigate('/settings')}
                sx={{
                  backgroundColor: isActive('/settings')
                    ? 'rgba(255,255,255,0.2)'
                    : 'transparent',
                }}
              >
                <Settings />
              </IconButton>
            </Tooltip>

            <Tooltip title={theme === 'dark' ? 'الوضع الفاتح' : 'الوضع الداكن'}>
              <IconButton color="inherit" onClick={toggleTheme}>
                {theme === 'dark' ? <Brightness7 /> : <Brightness4 />}
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

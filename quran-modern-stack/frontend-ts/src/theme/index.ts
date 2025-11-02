import { createTheme, ThemeOptions } from '@mui/material/styles';
import { ThemeMode } from '@/types';

// RTL support
const direction = 'rtl';

// Common theme options
const commonOptions: ThemeOptions = {
  direction,
  typography: {
    fontFamily: '"Cairo", "Amiri", "Scheherazade New", "Traditional Arabic", serif',
    h1: {
      fontFamily: '"Amiri", "Scheherazade New", serif',
      fontWeight: 700,
    },
    h2: {
      fontFamily: '"Amiri", "Scheherazade New", serif',
      fontWeight: 700,
    },
    h3: {
      fontFamily: '"Amiri", "Scheherazade New", serif',
      fontWeight: 600,
    },
    body1: {
      fontFamily: '"Cairo", sans-serif',
    },
    body2: {
      fontFamily: '"Cairo", sans-serif',
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        },
      },
    },
  },
};

// Light theme
const lightTheme = createTheme({
  ...commonOptions,
  palette: {
    mode: 'light',
    primary: {
      main: '#667eea',
      light: '#9f7aea',
      dark: '#5a67d8',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#48bb78',
      light: '#68d391',
      dark: '#38a169',
      contrastText: '#ffffff',
    },
    background: {
      default: '#f7fafc',
      paper: '#ffffff',
    },
    text: {
      primary: '#2d3748',
      secondary: '#4a5568',
    },
  },
});

// Dark theme
const darkTheme = createTheme({
  ...commonOptions,
  palette: {
    mode: 'dark',
    primary: {
      main: '#9f7aea',
      light: '#b794f4',
      dark: '#805ad5',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#68d391',
      light: '#9ae6b4',
      dark: '#48bb78',
      contrastText: '#1a202c',
    },
    background: {
      default: '#1a202c',
      paper: '#2d3748',
    },
    text: {
      primary: '#f7fafc',
      secondary: '#e2e8f0',
    },
  },
});

export const getTheme = (mode: ThemeMode) => {
  return mode === 'light' ? lightTheme : darkTheme;
};

export { lightTheme, darkTheme };

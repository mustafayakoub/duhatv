import { Box, Typography, Button, Alert } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

interface ErrorMessageProps {
  title?: string;
  message: string;
  onRetry?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  title = 'حدث خطأ',
  message,
  onRetry,
}) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '400px',
        p: 3,
      }}
    >
      <Alert
        severity="error"
        icon={<ErrorOutlineIcon fontSize="large" />}
        sx={{ maxWidth: 600, mb: 2 }}
      >
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <Typography variant="body2">{message}</Typography>
      </Alert>

      {onRetry && (
        <Button variant="contained" onClick={onRetry} sx={{ mt: 2 }}>
          إعادة المحاولة
        </Button>
      )}
    </Box>
  );
};

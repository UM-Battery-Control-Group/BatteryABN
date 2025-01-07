import { Typography, Box, Button } from '@mui/material';
import HeadBar from './HeadBar';
import FootBar from './FootBar';

const Layout = ({ children, title, subTitle, onActionClick = null, actionButtonLabel = '', description = '' }) => {
  return (
    <>
      <Box sx={{ backgroundColor: '#FFCB05', height: '20px', width: '100%' }}></Box>
      <HeadBar />

      {/* Main Content */}
      <Box sx={{ display: 'flex', minHeight: '60vh', backgroundColor: '#f5f5f5', padding: '1rem' }}>
        {/* Left Sidebar Section */}
        <Box
          sx={{
            width: '20%',
            padding: '1rem',
            backgroundColor: '#ffffff',
            boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
            display: 'flex',
            flexDirection: 'column',
            gap: '2rem', // Increased gap for better spacing
            alignItems: 'flex-start',
          }}
        >
          {/* Title Section */}
          {title && (
            <Box
              sx={{
                padding: '0.5rem 1rem',
                backgroundColor: '#FFCB05',
                borderRadius: '5px',
                width: '90%',
              }}
            >
              <Typography
                variant="h5"
                component="h1"
                sx={{
                  fontFamily: "'Open Sans', sans-serif",
                  fontWeight: 'bold',
                  fontSize: '1.25rem',
                  textAlign: 'center',
                }}
              >
                {title}
              </Typography>
            </Box>
          )}

          {/* Action Button Section */}
          {onActionClick && (
            <Box sx={{ width: '100%' }}>
              <Button
                onClick={onActionClick}
                variant="contained"
                sx={{
                  backgroundColor: '#00274C',
                  color: '#FFFFFF',
                  textTransform: 'none',
                  ':hover': {
                    backgroundColor: '#001F3F',
                  },
                }}
              >
                {actionButtonLabel}
              </Button>
            </Box>
          )}

          {/* Description Section */}
          {description && (
            <Box
              sx={{
                padding: '0.5rem 1rem',
                backgroundColor: '#f9f9f9',
                borderLeft: '4px solid #FFCB05',
                borderRadius: '5px',
              }}
            >
              <Typography
                variant="body2"
                sx={{
                  fontFamily: "'Roboto', sans-serif",
                  fontSize: '0.875rem',
                  color: '#333333',
                }}
              >
                {description}
              </Typography>
            </Box>
          )}
        </Box>

        {/* Right Content Section */}
        <Box sx={{ flex: 1, padding: '2rem', backgroundColor: '#ffffff', borderRadius: '5px', boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)' }}>
          {subTitle && (
            <Typography
              variant="h6"
              component="h2"
              sx={{
                fontFamily: "'Roboto', sans-serif",
                fontWeight: 'bold',
                fontSize: '1.25rem',
                marginBottom: '0.5rem',
                color: '#00274C',
              }}
            >
              {subTitle}
            </Typography>
          )}
          <Box sx={{ backgroundColor: '#00274C', height: '3px', width: '100%', marginBottom: '10px' }}></Box>
          {/* Content */}
          {children}
        </Box>
      </Box>

      <Box sx={{ backgroundColor: '#FFCB05', height: '3px', width: '100%' }}></Box>

      <FootBar />
    </>
  );
};

export default Layout;

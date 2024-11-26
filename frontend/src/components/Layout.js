import { Typography, Box } from '@mui/material';
import HeadBar from './HeadBar';
import FootBar from './FootBar';

const Layout = ({ children, title }) => {

  return (
    <>
      <Box sx={{ backgroundColor: '#FFCB05', height: '20px', width: '100%' }}></Box>
      <HeadBar/>

      {/* Main Content */}
      <Box sx={{ padding: '2rem', minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
        {/* Title */}
        {title && (
          <Typography
            variant="h4"
            component="h1"
            gutterBottom
            sx={{
              fontFamily: "'Roboto Slab', serif",
              fontWeight: '400',
              marginBottom: '1rem',
              textAlign: 'center',  // Center align the title
            }}
          >
            {title}
          </Typography>
        )}

        {/* Content */}
        {children}
      </Box>

      <Box sx={{ backgroundColor: '#FFCB05', height: '3px', width: '100%' }}></Box>

      <FootBar />
    </>
  );
};

export default Layout;

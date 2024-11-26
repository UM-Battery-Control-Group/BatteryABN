import React from 'react';
import { Box, Container, Link, Typography } from '@mui/material';
import umFootLogo from '../logo-horizontal-hex.png';
import bclFootLogo from '../bcl-logo.png';

const FootBar = () => {
  return (
    <Box component="footer" sx={{ backgroundColor: '#f5f5f5', color: 'black', py: 6 }}>
      <Container>
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            gap: 4,
            marginBottom: '20px',
          }}
        >
          {/* Logo and Text Section */}
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              flex: '1 1 400px',
              minWidth: '400px',
              marginTop: '10px',
            }}
          >
            {/* First logo */}
            <img
              src={umFootLogo}
              alt="UM Foot Logo"
              style={{
                transform: 'scale(2.5)',
                marginBottom: '10px',
                width: '150px',
                height: 'auto',
              }}
            />

            {/* Second logo and text */}
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'row',
                alignItems: 'center',
                marginTop: '10px',
              }}
            >
              {/* Second logo */}
              <img
                src={bclFootLogo}
                alt="BCL Foot Logo"
                style={{
                  transform: 'scale(0.6)',
                  width: '100px',
                  height: 'auto',
                  marginRight: '30px',
                }}
              />

              {/* Text next to second logo */}
              <Box sx={{marginRight: '50px',}}>
                <Typography variant="h6" sx={{ fontSize: '0.9rem' }}>
                  MECHANICAL ENGINEERING
                </Typography>
                <Typography variant="h6" sx={{ fontSize: '0.9rem' }}>
                  Battery Control Group
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ fontSize: '0.7rem' }}>
                  Walter E. Lay Automotive Engineering Laboratory
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ fontSize: '0.7rem' }}>
                  1231 Beal Avenue
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ fontSize: '0.7rem' }}>
                  Ann Arbor MI 48109
                </Typography>
              </Box>
            </Box>
          </Box>

          {/* Menu Section */}
          <Box sx={{ flex: '1 1 200px', minWidth: '200px', paddingLeft: '50px' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#00274C', fontSize: '1rem' }}>
              MENU
            </Typography>
            <Box sx={{ marginY: 1 }}>
              <Link href="/" color="inherit" underline="hover" sx={{ fontSize: '0.875rem' }}>
                Project Search
              </Link>
            </Box>
            <Box sx={{ marginY: 1 }}>
              <Link href="/cells" color="inherit" underline="hover" sx={{ fontSize: '0.875rem' }}>
                Cell Search
              </Link>
            </Box>
            <Box sx={{ marginY: 1 }}>
              <Link href="/trs" color="inherit" underline="hover" sx={{ fontSize: '0.875rem' }}>
                Test Record Search
              </Link>
            </Box>
            <Box sx={{ marginY: 1 }}>
              <Link href="/tasks" color="inherit" underline="hover" sx={{ fontSize: '0.875rem' }}>
                Task Manager
              </Link>
            </Box>
          </Box>

          {/* More Links Section */}
          <Box sx={{ flex: '1 1 200px', minWidth: '200px' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#00274C', fontSize: '1rem' }}>
              MORE LINKS
            </Typography>
            <Box sx={{ marginY: 1 }}>
              <Link href="https://www.umich.edu" color="inherit" underline="hover" sx={{ fontSize: '0.875rem' }}>
                U-M Home
              </Link>
            </Box>
            <Box sx={{ marginY: 1 }}>
              <Link href="https://batterycontrolgroup.engin.umich.edu/home" color="inherit" underline="hover" sx={{ fontSize: '0.875rem' }}>
                Battery Control Group Home
              </Link>
            </Box>
          </Box>

          {/* Social Section */}
          <Box sx={{ flex: '1 1 200px', minWidth: '200px' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#00274C', fontSize: '1rem' }}>
              SOCIAL
            </Typography>
            <Box sx={{ marginY: 1 }}>
              <Link href="https://www.linkedin.com" color="inherit" underline="hover" sx={{ fontSize: '0.875rem' }}>
                LinkedIn
              </Link>
            </Box>
          </Box>
        </Box>
      </Container>

      {/* Footer copyright section */}
      <Box
        sx={{
          textAlign: 'center',
          py: 2,
          backgroundColor: '#f5f5f5',
        }}
      >
        <Typography variant="body2" color="textSecondary" sx={{ fontSize: '0.75rem' }}>
          © 2024 U-M Battery Control Group - All rights reserved.
        </Typography>
      </Box>
    </Box>
  );
};

export default FootBar;

import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import { ReactComponent as HeadLogo } from '../logo.svg';

const HeadBar = () => {
  const location = useLocation();

  return (
    <AppBar position="static" sx={{ backgroundColor: '#00274C', height: '65px' }}>
      <Toolbar sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {/* Logo and Text Section */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginLeft: '100px',
            marginRight: '400px',
          }}
        >
          <Link to="/" style={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}>
            <HeadLogo
              style={{
                height: '50px',
                width: '50px',
                marginRight: '15px',
                cursor: 'pointer',
              }}
            />
            <Typography
              variant="h6"
              sx={{
                color: 'white',
                fontFamily: "'Playfair Display', serif",
                textDecoration: 'none',
                fontWeight: '700',
                fontSize: '1.5rem',
              }}
            >
              UMBCL Data Dashboard
            </Typography>
          </Link>
        </Box>

        <Button
          color="inherit"
          component={Link}
          to="/"
          sx={{
            color: location.pathname === '/trs' ? '#f0f0f0' : 'white',
            textTransform: 'none',
          }}
        >
          Projects
        </Button>
        <Button
          color="inherit"
          component={Link}
          to="/cells"
          sx={{
            color: location.pathname === '/trs' ? '#f0f0f0' : 'white',
            textTransform: 'none',
          }}
        >
          Cells
        </Button>
        <Button
          color="inherit"
          component={Link}
          to="/trs"
          sx={{
            color: location.pathname === '/trs' ? '#f0f0f0' : 'white',
            textTransform: 'none',
          }}
        >
          TestRecords
        </Button>
        <Button
          color="inherit"
          component={Link}
          to="/tasks"
          sx={{
            color: location.pathname === '/trs' ? '#f0f0f0' : 'white',
            textTransform: 'none',
            marginRight: '100px',
          }}
        >
          Tasks
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default HeadBar;

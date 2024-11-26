import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import { ReactComponent as HeadLogo } from '../logo.svg';

const HeadBar = () => {
  const location = useLocation();

  const getButtonStyle = (path) => ({
    color: location.pathname === path ? 'black' : 'white',
    backgroundColor: location.pathname === path ? '#FFCB05' : 'transparent',
    fontWeight: location.pathname === path ? 'bold' : 'normal',
    borderRadius: '5px',
    padding: '5px 15px',
    textTransform: 'none',
  });
  

  return (
    <AppBar position="static" sx={{ backgroundColor: '#00274C', height: '65px' }}>
      <Toolbar sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {/* Logo and Text Section */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginLeft: '80px',
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
              BCL DATA DASHBOARD
            </Typography>
          </Link>
        </Box>

        {/* Buttons */}
        <Button
          component={Link}
          to="/"
          sx={getButtonStyle('/')}
        >
          PROJECTS
        </Button>
        <Button
          component={Link}
          to="/cells"
          sx={getButtonStyle('/cells')}
        >
          CELLS
        </Button>
        <Button
          component={Link}
          to="/trs"
          sx={getButtonStyle('/trs')}
        >
          TEST-RECORDS
        </Button>
        <Button
          component={Link}
          to="/tasks"
          sx={{ 
            ...getButtonStyle('/tasks'), 
            marginRight: '100px'
          }}
        >
          TASKS
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default HeadBar;

import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, Container, Paper, Drawer, List, ListItem, ListItemText, IconButton } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Link, useLocation } from 'react-router-dom';

const Layout = ({ children, title }) => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const location = useLocation();

  const toggleDrawer = (open) => () => {
    setDrawerOpen(open);
  };

  const menuItems = [
    { text: 'Projects', path: '/' },
    { text: 'Cells', path: '/cells' },
    { text: 'Test Records', path: '/trs' },
  ];

  const drawer = (
    <div role="presentation" onClick={toggleDrawer(false)} sx={{ width: 250 }}>
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            component={Link}
            to={item.path}
            sx={location.pathname === item.path ? { backgroundColor: '#f0f0f0' } : {}}
          >
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <>
      <AppBar position="static" sx={{ backgroundColor: '#1976d2' }}>
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={toggleDrawer(true)}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            component={Link}
            to="/"
            sx={{ color: 'white', textDecoration: 'none', flexGrow: 1 }}
          >
            UMBCL
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer anchor="left" open={drawerOpen} onClose={toggleDrawer(false)}>
        {drawer}
      </Drawer>
      <Container maxWidth="lg">
        <Paper elevation={3} sx={{ marginTop: '2rem', padding: '2rem' }}>
          <Typography variant="h4" component="h1" gutterBottom>
            {title}
          </Typography>
          {children}
        </Paper>
      </Container>
    </>
  );
};

export default Layout;

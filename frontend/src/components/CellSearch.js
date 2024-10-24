import React, { useState } from 'react';
import { TextField, Button, List, ListItem, ListItemText, CircularProgress, Typography } from '@mui/material';
import Layout from './Layout';
import { getCellsByKeyword } from '../services/api';
import { useNavigate } from 'react-router-dom';

const CellSearch = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [cells, setCells] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await getCellsByKeyword(searchTerm);
      setCells(response.data);
    } catch (err) {
      setError('Error fetching cells');
    } finally {
      setLoading(false);
    }
  };

  const handleCellClick = (cellName) => {
    navigate(`/cell/${cellName}`);
  };

  return (
    <Layout title="Search Cells">
      <TextField
        label="Search by Cell Name"
        variant="outlined"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        fullWidth
        sx={{ marginBottom: '1rem' }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleSearch}
        sx={{ marginBottom: '1rem' }}
      >
        Search
      </Button>

      {loading && <CircularProgress />}
      {error && <Typography color="error">{error}</Typography>}

      <List>
        {cells.map((cell) => (
          <ListItem button key={cell.cell_name} onClick={() => handleCellClick(cell.cell_name)}>
            <ListItemText primary={cell.cell_name} />
          </ListItem>
        ))}
      </List>

    </Layout>
  );
};

export default CellSearch;

import React, { useState } from 'react';
import { TextField, Button, List, ListItem, ListItemText, CircularProgress, Typography } from '@mui/material';
import Layout from '../components/Layout';
import { getTestRecordsByKeyword } from '../services/api';
import { useNavigate } from 'react-router-dom';

const TestRecordSearch = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [testRecords, setTestRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await getTestRecordsByKeyword(searchTerm);
      setTestRecords(response.data);
    } catch (err) {
      setError('Error fetching test records');
    } finally {
      setLoading(false);
    }
  };

  const handleTestRecordClick = (testRecordName) => {
    navigate(`/trs/${testRecordName}`);
  };

  return (
    <Layout title="Search Test Records">
      <TextField
        label="Search by Test Record Name"
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
        {testRecords.map((tr) => (
          <ListItem button key={tr.test_name} onClick={() => handleTestRecordClick(tr.name)}>
            <ListItemText primary={tr.test_name} />
          </ListItem>
        ))}
      </List>

    </Layout>
  );
};

export default TestRecordSearch;

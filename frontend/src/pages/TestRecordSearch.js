import React, { useState } from 'react';
import { TextField, Button, CircularProgress, Typography, Box } from '@mui/material';
import Layout from '../components/Layout';
import { getTestRecordsByKeyword } from '../services/api';
import { Link } from 'react-router-dom';

const TestRecordSearch = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [testRecords, setTestRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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


  return (
    <Layout title="TESTRECORDS" subTitle={'TestRecord Search'}>
      <Box sx={{ padding: '2rem', minHeight: '60vh', backgroundColor: '#f5f5f5' }}>
        {/* Search Box */}
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', marginBottom: '2rem' }}>
          <TextField
            label="Search by Test Record Name"
            variant="outlined"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            sx={{
              marginBottom: '1rem',
              width: '350px',
              margin: '0.5rem',
              backgroundColor: 'white',
            }}
          />
          <Button
            variant="contained"
            onClick={handleSearch}
            sx={{
              backgroundColor: '#FFCB05',
              color: '#00274C',
              textTransform: 'none',
              padding: '0.3rem 0.8rem',
              borderRadius: '5px',
              ':hover': {
                backgroundColor: '#F9B500',
              },
              margin: '0.5rem',
            }}
          >
            Search
          </Button>
        </Box>
  
        {/* Loading or Error State */}
        {loading && <CircularProgress sx={{ display: 'block', margin: '1rem auto' }} />}
        {error && <Typography color="error" sx={{ textAlign: 'center', marginTop: '1rem' }}>{error}</Typography>}
  
        {/* Test Record Buttons Layout */}
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap', 
            gap: '1rem', 
            justifyContent: 'flex-start',
            marginTop: '2rem',
          }}
        >
          {testRecords.map((tr) => (
            <Button
              key={tr.test_name}
              component={Link}
              to={`/tr/${tr.test_name}`}
              sx={{
                backgroundColor: '#FFCB05',
                color: '#00274C',
                textTransform: 'none',
                padding: '0.5rem 1rem',
                borderRadius: '5px',
                ':hover': {
                  backgroundColor: '#F9B500',
                },
                whiteSpace: 'nowrap',
              }}
            >
              {tr.test_name}
            </Button>
          ))}
        </Box>
      </Box>
    </Layout>
  );
  
};

export default TestRecordSearch;

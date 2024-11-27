import React, { useEffect, useState } from 'react';
import { Box, Button, CircularProgress } from '@mui/material';
import { Link, useParams } from 'react-router-dom';
import { getTestRecordsByCell } from '../services/api';
import Layout from '../components/Layout';

const TestRecordList = () => {
  const { cellName } = useParams();  
  const [testRecords, setTestRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTestRecordsByCell(cellName)
      .then(response => {
        setTestRecords(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching test records:", error);
        setLoading(false);
      });
  }, [cellName]);

  useEffect(() => {
    console.log("Test Records:", testRecords);
  } , [testRecords]);


  return (
    <Layout title="TESTRECORDS" subTitle={'TestRecord List'}>
      {loading ? (
        <CircularProgress />
      ) : (
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '1rem',
            justifyContent: 'center',
            margin: '1rem 0',
          }}
        >
          {testRecords.map((record) => (
            <Button
              key={record.test_name}
              component={Link}
              to={`/tr/${record.test_name}`}
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
              {record.test_name}
            </Button>
          ))}
        </Box>
      )}
    </Layout>
  );
};

export default TestRecordList;

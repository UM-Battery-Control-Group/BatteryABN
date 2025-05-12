import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Typography, CircularProgress } from '@mui/material';
import { getTestRecord } from '../services/api';
import Layout from '../components/Layout';

const TestRecordDetails = () => {
  const { trName, trType } = useParams();
  const [testRecord, setTestRecord] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTestRecord(trName, trType)
      .then(response => {
        setTestRecord(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching test record:", error);
        setLoading(false);
      });
  }, [trName, trType]);

  return (
    <Layout title="TESTRECORDS" subTitle={'TestRecord Detail'}>
      {loading ? (
        <CircularProgress />
      ) : testRecord ? (
        <>
          <Typography variant="h5">{testRecord.name}</Typography>
          {/* <Typography variant="body1">Result: {testRecord.result}</Typography> */}
        </>
      ) : (
        <Typography variant="body1">Test record not found</Typography>
      )}
    </Layout>
  );
};

export default TestRecordDetails;

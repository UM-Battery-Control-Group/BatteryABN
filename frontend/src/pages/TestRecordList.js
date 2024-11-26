import React, { useEffect, useState } from 'react';
import { List, ListItem, ListItemText, CircularProgress } from '@mui/material';
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
    <Layout title={`Test Records for Cell: ${cellName}`}>
      {loading ? (
        <CircularProgress />
      ) : (
        <List>
          {testRecords.map(record => (
            <ListItem 
              button={true}
              component={Link}
              to={`/tr/${record.test_name}`}
              key={record.test_name}
            >
              <ListItemText primary={record.test_name} />
            </ListItem>
          ))}
        </List>
      )}
    </Layout>
  );
};

export default TestRecordList;

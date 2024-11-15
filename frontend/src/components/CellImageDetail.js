import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { CircularProgress, Box, Typography } from '@mui/material';
import { getCellImageHtmls } from '../services/api';
import Layout from './Layout';

const CellImageDetail = () => {
  const { cellName, index } = useParams();  
  const [htmlUrl, setHtmlUrl] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHtml = async () => {
      try {
        console.log(`Fetching HTML for cell: ${cellName}, index: ${index}`);
        const fetchedHtmlUrl = await getCellImageHtmls(cellName, index);
        setHtmlUrl(fetchedHtmlUrl);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching HTML:', error);
        setLoading(false);
      }
    };

    fetchHtml();
  }, [cellName, index]);

  return (
    <Layout title={`Interactive Plot for Cell: ${cellName}, Detail ${parseInt(index) + 1}`}>
      {loading ? (
        <CircularProgress />
      ) : (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
          <Typography variant="h6" gutterBottom>
          </Typography>
          {htmlUrl && (
            <iframe
              src={htmlUrl}
              title={`Interactive Plot for Cell: ${cellName}`}
              style={{ width: '100%', height: '1000px', border: 'none' }}
            />
          )}
        </Box>
      )}
    </Layout>
  );
};

export default CellImageDetail;

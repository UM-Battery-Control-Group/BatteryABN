import React, { useEffect, useState } from 'react';
import { Typography, CircularProgress, Card, CardMedia, Box, Button } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { getCellImages } from '../services/api';
import Layout from './Layout';

const CellDetails = () => {
  const { cellName } = useParams();  
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate(); 

  useEffect(() => {
    const fetchImages = async () => {
      try {
        console.log('Fetching images for cell:', cellName);
        const imagePromises = [0, 1, 2].map(index => getCellImages(cellName, index));
        const fetchedImages = await Promise.all(imagePromises);
        setImages(fetchedImages);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching cell images:', error);
        setLoading(false);
      }
    };

    fetchImages();
  }, [cellName]);

  const handleViewDetail = (index) => {
    navigate(`/cell/${cellName}/images/${index}`);
  };

  return (
    <Layout title={`Details for Cell: ${cellName}`}>
      {loading ? (
        <CircularProgress />
      ) : (
        <>
          <Typography variant="h5" gutterBottom>
            Images for Cell: {cellName}
          </Typography>

          <Box sx={{ display: 'flex', flexDirection: 'column', gap: '48px' }}>
            {images.map((image, index) => (
              <Card key={index} sx={{ maxWidth: '100%' }}>
                <CardMedia
                  component="img"
                  image={image}
                  alt={`Cell ${cellName} Image ${index + 1}`}
                  sx={{ width: '100%', height: 'auto' }}
                />
                <Box sx={{ textAlign: 'center', marginTop: '1rem' }}>
                  <Button
                    variant="outlined"
                    color="primary"
                    onClick={() => handleViewDetail(index)}
                  >
                    View Detail
                  </Button>
                </Box>
              </Card>
            ))}
          </Box>
        </>
      )}
    </Layout>
  );
};

export default CellDetails;

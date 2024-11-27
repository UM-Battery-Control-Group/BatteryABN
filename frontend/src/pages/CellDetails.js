import React, { useEffect, useState } from 'react';
import { CircularProgress, Card, CardMedia, Box, Button } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { getCellImages } from '../services/api';
import Layout from '../components/Layout';

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
    <Layout title={`CELLS`} subTitle={`Cell Detail: ${cellName}`}>
      {loading ? (
        <CircularProgress />
      ) : (
        <>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: '48px', marginTop: '30px' }}>
            {images.map((image, index) => (
              <Card key={index} sx={{ maxWidth: '100%' }}>
                <CardMedia
                  component="img"
                  image={image}
                  alt={`Cell ${cellName} Image ${index + 1}`}
                  sx={{ display: 'block', margin: '0 auto', width: '90%', height: 'auto', objectFit: 'contain', overflow: 'hidden',  }}
                />
                <Box sx={{ textAlign: 'center', marginTop: '2rem', marginBottom: '2rem' }}>
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

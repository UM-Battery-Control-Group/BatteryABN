import React, { useEffect, useState } from 'react';
import { CircularProgress, Card, CardMedia, Box, Button} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { getCellImages, getCellLatestCellInfo } from '../services/api';
import Layout from '../components/Layout';

const CellDetails = () => {
  const { cellName } = useParams();  
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [latestInfo, setLatestInfo] = useState(null); // 新的状态变量
  const navigate = useNavigate();

  useEffect(() => {
    const fetchImages = async () => {
      try {
        console.log('Fetching images for cell:', cellName);
        const imagePromises = [0, 1, 2].map(index => getCellImages(cellName, index));
        const fetchedImages = await Promise.all(imagePromises);
        setImages(fetchedImages);
      } catch (error) {
        console.error('Error fetching cell images:', error);
      } finally {
        setLoading(false);
      }
    };

    const fetchLatestInfo = async () => {
      try {
        console.log('Fetching latest info for cell:', cellName);
        const response = await getCellLatestCellInfo(cellName);
        setLatestInfo(response.data);
      } catch (error) {
        console.error('Error fetching latest info:', error);
      }
    };

    fetchImages();
    fetchLatestInfo();
  }, [cellName]);

  const handleViewDetail = (index) => {
    navigate(`/cell/${cellName}/images/${index}`);
  };


  const description = latestInfo
    ? `Latest Test: ${latestInfo.latest_test_name}
      Capacity: ${latestInfo.capacity.toFixed(2)} mAh
      Timestamp: ${new Date(latestInfo.timestamp).toLocaleString()}
      Protocol: ${latestInfo.protocol}
      Cycle Type: ${latestInfo.cycle_type}`
    : 'Loading latest information...';

  return (
    <Layout title={`CELLS`} subTitle={`Cell Detail: ${cellName}`} description={description}>
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
                  sx={{ display: 'block', margin: '0 auto', width: '90%', height: 'auto', objectFit: 'contain', overflow: 'hidden' }}
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

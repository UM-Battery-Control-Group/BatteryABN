import React, { useEffect, useState } from 'react';
import { Box, Button, CircularProgress } from '@mui/material';
import { Link, useParams } from 'react-router-dom';
import { getCellsByProject, enqueueUpdateProjectTask } from '../services/api';
import Layout from '../components/Layout';

const CellList = () => {
  const { projectName } = useParams();  
  const [cells, setCells] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    getCellsByProject(projectName)
      .then(response => {
        setCells(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching cells:", error);
        setLoading(false);
      });
  }, [projectName]);

  const handleUpdateProject = () => {
    setIsUpdating(true);
    enqueueUpdateProjectTask(projectName)
      .then(() => {
        alert('Project update task enqueued successfully!');
      })
      .catch(error => {
        console.error("Error enqueuing update project task:", error);
        alert('Failed to enqueue project update task.');
      })
      .finally(() => {
        setIsUpdating(false);
      });
  };

  return (
    <Layout
      title={`CELLS`}
      subTitle={'Cell List'}
      onActionClick={handleUpdateProject}
      actionButtonLabel={isUpdating ? 'Updating...' : 'Update Project'}
      description={`Manage cells for the project: ${projectName}`}
    >
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
          {cells.map(cell => (
            <Button
              key={cell.cell_name}
              component={Link}
              to={`/cell/${cell.cell_name}`}
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
              {cell.cell_name}
            </Button>
          ))}
        </Box>
      )}
    </Layout>
  );
};

export default CellList;

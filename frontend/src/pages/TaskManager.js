import React, { useState } from 'react';
import { TextField, Button, Typography, Box} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { enqueueUpdateTask, enqueueResetTask, enqueueCreateTask, enqueueProcessTask } from '../services/api';

const TaskManager = () => {
  const [cellName, setCellName] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleTask = async (taskType) => {
    setError('');
    setSuccessMessage('');
    try {
      if (taskType === 'update') {
        await enqueueUpdateTask(cellName);
        setSuccessMessage('Update task enqueued successfully.');
      } else if (taskType === 'reset') {
        await enqueueResetTask(cellName);
        setSuccessMessage('Reset task enqueued successfully.');
      } else if (taskType === 'create') {
        await enqueueCreateTask(cellName);
        setSuccessMessage('Create task enqueued successfully.');
      } else if (taskType === 'process') {
        await enqueueProcessTask(cellName);
        setSuccessMessage('Process task enqueued successfully.');
      }
    } catch (err) {
      setError(`Error enqueuing ${taskType} task`);
    }
  };

  const handleViewStatus = () => {
    navigate('/tasks/status');
  };

  return (
    <Layout title="TASKS" subTitle={'Task Manager'}>
      <Box sx={{ padding: '2rem', minHeight: '60vh', backgroundColor: '#f5f5f5' }}>
        {/* Search Box */}
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', marginBottom: '2rem' }}>
          <TextField
            label="Cell Name"
            variant="outlined"
            value={cellName}
            onChange={(e) => setCellName(e.target.value)}
            sx={{
              marginBottom: '1rem',
              width: '250px',
              margin: '0.5rem',
              backgroundColor: 'white',
            }}
          />
          {error && <Typography color="error" sx={{ textAlign: 'center', marginTop: '1rem' }}>{error}</Typography>}
          {successMessage && <Typography color="success.main" sx={{ textAlign: 'center', marginTop: '1rem' }}>{successMessage}</Typography>}
        </Box>
  
        {/* Task Buttons Layout */}
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '1rem', 
            marginBottom: '0.5rem',
            justifyContent: 'center'
          }}
        >
          <Button
            variant="contained"
            color="primary"
            onClick={() => handleTask('update')}
            sx={{
              padding: '0.5rem 1rem',
              borderRadius: '5px',
              backgroundColor: '#FFCB05',
              color: '#00274C',
              textTransform: 'none',
              ':hover': {
                backgroundColor: '#F9B500',
              },
              marginBottom: '0.3rem',
            }}
          >
            Update
          </Button>
  
          <Button
            variant="contained"
            color="secondary"
            onClick={() => handleTask('reset')}
            sx={{
              padding: '0.5rem 1rem',
              borderRadius: '5px',
              backgroundColor: '#FFCB05',
              color: '#00274C',
              textTransform: 'none',
              ':hover': {
                backgroundColor: '#F9B500',
              },
              marginBottom: '0.3rem',
            }}
          >
            Reset
          </Button>
  
          <Button
            variant="contained"
            color="success"
            onClick={() => handleTask('create')}
            sx={{
              padding: '0.5rem 1rem',
              borderRadius: '5px',
              backgroundColor: '#FFCB05',
              color: '#00274C',
              textTransform: 'none',
              ':hover': {
                backgroundColor: '#F9B500',
              },
              marginBottom: '0.3rem',
            }}
          >
            Create
          </Button>
  
          <Button
            variant="contained"
            color="info"
            onClick={() => handleTask('process')}
            sx={{
              padding: '0.5rem 1rem',
              borderRadius: '5px',
              backgroundColor: '#FFCB05',
              color: '#00274C',
              textTransform: 'none',
              ':hover': {
                backgroundColor: '#F9B500',
              },
              marginBottom: '0.3rem',
            }}
          >
            Process
          </Button>
        </Box>
  
        {/* View Task Status Button at the bottom */}
        <Box sx={{ display: 'flex', justifyContent: 'center' }}>
          <Button
            variant="outlined"
            color="info"
            onClick={handleViewStatus}
            sx={{
              padding: '0.5rem 1rem',
              borderRadius: '5px',
              backgroundColor: 'white',
              color: '#00274C',
              textTransform: 'none',
              ':hover': {
                backgroundColor: '#F9B500',
              },
              marginTop: '2rem',
              width: 'auto',
            }}
          >
            View Task Status
          </Button>
        </Box>
      </Box>
    </Layout>
  );
  
};

export default TaskManager;

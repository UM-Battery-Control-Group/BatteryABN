import React, { useState } from 'react';
import { TextField, Button, Typography, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Layout from './Layout';
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
    <Layout title="Task Management">
      <Container sx={{ textAlign: 'center', marginTop: '2rem' }}>
        <TextField
          label="Cell Name"
          variant="outlined"
          value={cellName}
          onChange={(e) => setCellName(e.target.value)}
          fullWidth
          sx={{ marginBottom: '1rem' }}
        />
        {error && <Typography color="error">{error}</Typography>}
        {successMessage && <Typography color="success.main">{successMessage}</Typography>}
        
        <Button
          variant="contained"
          color="primary"
          onClick={() => handleTask('update')}
          sx={{ marginRight: '1rem', marginBottom: '1rem' }}
        >
          Enqueue Update Task
        </Button>

        <Button
          variant="contained"
          color="secondary"
          onClick={() => handleTask('reset')}
          sx={{ marginRight: '1rem', marginBottom: '1rem' }}
        >
          Enqueue Reset Task
        </Button>

        <Button
          variant="contained"
          color="success"
          onClick={() => handleTask('create')}
          sx={{ marginBottom: '1rem' }}
        >
          Enqueue Create Task
        </Button>

        <Button
          variant="contained"
          color="info"
          onClick={() => handleTask('process')}
          sx={{ marginBottom: '1rem' }}
        >
          Enqueue Process Task
        </Button>

        <Button
          variant="outlined"
          color="info"
          onClick={handleViewStatus}
          sx={{ display: 'block', marginTop: '2rem' }}
        >
          View Task Status
        </Button>
      </Container>
    </Layout>
  );
};

export default TaskManager;

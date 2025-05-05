import React, { useState, useEffect } from 'react';
import { CircularProgress, List, ListItem, ListItemText, Typography, Box, Button } from '@mui/material';
import Layout from '../components/Layout';
import { getTasksStatus, clearAllTasks, clearFinishedTasks, clearFailedTasks } from '../services/api';

const TaskStatus = () => {
  const [taskStatus, setTaskStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const fetchTaskStatus = async () => {
    setLoading(true);
    setError('');
    setSuccessMessage('');
    try {
      const response = await getTasksStatus();
      setTaskStatus(response.data);
    } catch (err) {
      setError('Error fetching task status');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTaskStatus();
  }, []);

  const handleClearAll = async () => {
    try {
      await clearAllTasks();
      setSuccessMessage('All tasks cleared successfully.');
      fetchTaskStatus();
    } catch (err) {
      setError('Error clearing all tasks');
    }
  };

  const handleClearFinished = async () => {
    try {
      await clearFinishedTasks();
      setSuccessMessage('Finished tasks cleared successfully.');
      fetchTaskStatus();
    } catch (err) {
      setError('Error clearing finished tasks');
    }
  };

  const handleClearFailed = async () => {
    try {
      await clearFailedTasks();
      setSuccessMessage('Failed tasks cleared successfully.');
      fetchTaskStatus();
    } catch (err) {
      setError('Error clearing failed tasks');
    }
  };

  return (
    <Layout title="TASKS" subTitle={'Task Status'}>
      <Box sx={{ padding: '2rem', minHeight: '60vh', backgroundColor: '#f5f5f5' }}>
        {loading ? (
          <CircularProgress />
        ) : (
          <>
            {error && (
              <Typography color="error" sx={{ textAlign: 'center', marginBottom: '1rem' }}>
                {error}
              </Typography>
            )}
            {successMessage && (
              <Typography color="success" sx={{ textAlign: 'center', marginBottom: '1rem' }}>
                {successMessage}
              </Typography>
            )}

            {/* Buttons for clearing tasks */}
            <Box sx={{ marginBottom: '1rem', textAlign: 'center' }}>
              <Button
                variant="contained"
                onClick={handleClearAll}
                sx={{
                  backgroundColor: '#FFCB05',
                  color: '#00274C',
                  textTransform: 'none',
                  padding: '0.3rem 0.8rem',
                  borderRadius: '5px',
                  ':hover': {
                    backgroundColor: '#F9B500',
                  },
                  margin: '0.5rem',
                }}
              >
                Clear All Tasks
              </Button>
              <Button
                variant="contained"
                onClick={handleClearFinished}
                sx={{
                  backgroundColor: '#FFCB05',
                  color: '#00274C',
                  textTransform: 'none',
                  padding: '0.3rem 0.8rem',
                  borderRadius: '5px',
                  ':hover': {
                    backgroundColor: '#F9B500',
                  },
                  margin: '0.5rem',
                }}
              >
                Clear Finished Tasks
              </Button>
              <Button
                variant="contained"
                onClick={handleClearFailed}
                sx={{
                  backgroundColor: '#FFCB05',
                  color: '#00274C',
                  textTransform: 'none',
                  padding: '0.3rem 0.8rem',
                  borderRadius: '5px',
                  ':hover': {
                    backgroundColor: '#F9B500',
                  },
                  margin: '0.5rem',
                }}
              >
                Clear Failed Tasks
              </Button>
            </Box>

            {/* Task Status Lists */}
            {taskStatus && (
              <Box>
                {/* Queued Tasks */}
                <Box sx={{ marginBottom: '2rem' }}>
                  <Typography
                    variant="h6"
                    sx={{ fontWeight: '600', color: '#00274C', marginBottom: '0.5rem' }}
                  >
                    Queued Tasks
                  </Typography>
                  <Box
                    sx={{
                      backgroundColor: '#f9f9f9',
                      borderRadius: '8px',
                      boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)',
                      padding: '1rem',
                    }}
                  >
                    <List>
                      {taskStatus.queued.map((job) => (
                        <ListItem
                          key={job.id}
                          sx={{
                            backgroundColor: '#FFCB05',
                            marginBottom: '0.5rem',
                            borderRadius: '4px',
                            padding: '1rem',
                            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
                            ':hover': {
                              backgroundColor: '#F9B500',
                            },
                          }}
                        >
                          <ListItemText
                            primary={`Task ID: ${job.id}, ${job.description}, Enqueued At: ${job.enqueued_at}`}
                            sx={{ fontSize: '0.9rem', color: '#333' }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                </Box>

                {/* Started Tasks */}
                <Box sx={{ marginBottom: '2rem' }}>
                  <Typography
                    variant="h6"
                    sx={{ fontWeight: '600', color: '#00274C', marginBottom: '0.5rem' }}
                  >
                    Started Tasks
                  </Typography>
                  <Box
                    sx={{
                      backgroundColor: '#f9f9f9',
                      borderRadius: '8px',
                      boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)',
                      padding: '1rem',
                    }}
                  >
                    <List>
                      {taskStatus.started.map((job) => (
                        <ListItem
                          key={job.id}
                          sx={{
                            backgroundColor: '#FFCB05',
                            marginBottom: '0.5rem',
                            borderRadius: '4px',
                            padding: '1rem',
                            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
                            ':hover': {
                              backgroundColor: '#F9B500',
                            },
                          }}
                        >
                          <ListItemText
                            primary={`Task ID: ${job.id}, ${job.description}, Enqueued At: ${job.enqueued_at}`}
                            sx={{ fontSize: '0.9rem', color: '#333' }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                </Box>

                {/* Finished Tasks */}
                <Box sx={{ marginBottom: '2rem' }}>
                  <Typography
                    variant="h6"
                    sx={{ fontWeight: '600', color: '#00274C', marginBottom: '0.5rem' }}
                  >
                    Finished Tasks
                  </Typography>
                  <Box
                    sx={{
                      backgroundColor: '#f9f9f9',
                      borderRadius: '8px',
                      boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)',
                      padding: '1rem',
                    }}
                  >
                    <List>
                      {taskStatus.finished.map((job) => (
                        <ListItem
                          key={job.id}
                          sx={{
                            backgroundColor: '#FFCB05',
                            marginBottom: '0.5rem',
                            borderRadius: '4px',
                            padding: '1rem',
                            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
                            ':hover': {
                              backgroundColor: '#F9B500',
                            },
                          }}
                        >
                          <ListItemText
                            primary={`Task ID: ${job.id}, ${job.description}, Enqueued At: ${job.enqueued_at}`}
                            sx={{ fontSize: '0.9rem', color: '#333' }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                </Box>

                {/* Failed Tasks */}
                <Box sx={{ marginBottom: '2rem' }}>
                  <Typography
                    variant="h6"
                    sx={{ fontWeight: '600', color: '#00274C', marginBottom: '0.5rem' }}
                  >
                    Failed Tasks
                  </Typography>
                  <Box
                    sx={{
                      borderRadius: '8px',
                      boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)',
                      padding: '1rem',
                    }}
                  >
                    <List>
                      {taskStatus.failed.map((job) => (
                        <ListItem
                          key={job.id}
                          sx={{
                            backgroundColor: '#FF6666',
                            marginBottom: '0.5rem',
                            borderRadius: '4px',
                            padding: '1rem',
                            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
                            ':hover': {
                              backgroundColor: '#FF4C4C',
                            },
                          }}
                        >
                          <ListItemText
                            primary={`Task ID: ${job.id}, ${job.description}, Enqueued At: ${job.enqueued_at}`}
                            sx={{ fontSize: '0.9rem', color: '#fff' }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                </Box>
              </Box>
            )}
          </>
        )}
      </Box>
    </Layout>
  );
};

export default TaskStatus;

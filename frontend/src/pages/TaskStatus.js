import React, { useState, useEffect } from 'react';
import { CircularProgress, List, ListItem, ListItemText, Typography, Box } from '@mui/material';
import Layout from '../components/Layout';
import { getTasksStatus } from '../services/api';

const TaskStatus = () => {
  const [taskStatus, setTaskStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchTaskStatus = async () => {
    setLoading(true);
    setError('');
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
            
            {taskStatus && (
              <Box>
                {/* Queued Tasks */}
                <Box sx={{ marginBottom: '2rem'}}>
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
                            primary={`Task ID: ${job.id}, Enqueued At: ${job.enqueued_at}`}
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
                            primary={`Task ID: ${job.id}, Enqueued At: ${job.enqueued_at}`}
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
                            primary={`Task ID: ${job.id}, Enqueued At: ${job.enqueued_at}`}
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
                              backgroundColor: '#990000',
                            },
                          }}
                        >
                          <ListItemText
                            primary={`Task ID: ${job.id}, Enqueued At: ${job.enqueued_at}`}
                            sx={{ fontSize: '0.9rem', color: '#333' }}
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

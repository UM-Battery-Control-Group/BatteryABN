import React, { useState, useEffect } from 'react';
import { CircularProgress, List, ListItem, ListItemText, Typography } from '@mui/material';
import Layout from './Layout';
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
    <Layout title="Task Status">
      {loading ? (
        <CircularProgress />
      ) : (
        <>
          {error && <Typography color="error">{error}</Typography>}
          {taskStatus && (
            <div>
              <Typography variant="h6">Queued Tasks</Typography>
              <List>
                {taskStatus.queued.map((job) => (
                  <ListItem key={job.id}>
                    <ListItemText primary={`Task ID: ${job.id}, Status: ${job.status}, Enqueued At: ${job.enqueued_at}`} />
                  </ListItem>
                ))}
              </List>

              <Typography variant="h6">Started Tasks</Typography>
              <List>
                {taskStatus.started.map((job) => (
                  <ListItem key={job.id}>
                    <ListItemText primary={`Task ID: ${job.id}, Status: ${job.status}, Enqueued At: ${job.enqueued_at}`} />
                  </ListItem>
                ))}
              </List>

              <Typography variant="h6">Finished Tasks</Typography>
              <List>
                {taskStatus.finished.map((job) => (
                  <ListItem key={job.id}>
                    <ListItemText primary={`Task ID: ${job.id}, Status: ${job.status}, Enqueued At: ${job.enqueued_at}`} />
                  </ListItem>
                ))}
              </List>

              <Typography variant="h6">Failed Tasks</Typography>
              <List>
                {taskStatus.failed.map((job) => (
                  <ListItem key={job.id}>
                    <ListItemText primary={`Task ID: ${job.id}, Status: ${job.status}, Enqueued At: ${job.enqueued_at}`} />
                  </ListItem>
                ))}
              </List>
            </div>
          )}
        </>
      )}
    </Layout>
  );
};

export default TaskStatus;

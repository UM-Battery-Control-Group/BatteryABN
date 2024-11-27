import React, { useEffect, useState } from 'react';
import { Box, Button, CircularProgress } from '@mui/material';
import { Link } from 'react-router-dom';
import { getProjects } from '../services/api';
import Layout from '../components/Layout';

const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getProjects()
      .then(response => {
        setProjects(response.data);
        console.log("Projects:", response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching projects:", error);
        setLoading(false);
      });
  }, []);

  return (
    <Layout title="PROJECTS" subTitle={'Project List'}>
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
          {projects.map((project) => (
            <Button
              key={project.project_name}
              component={Link}
              to={`/cells/${project.project_name}`}
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
              {project.project_name}
            </Button>
          ))}
        </Box>
      )}
    </Layout>
  );
};

export default ProjectList;

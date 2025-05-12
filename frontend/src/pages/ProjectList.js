import React, { useEffect, useState } from 'react';
import { Box, Button, CircularProgress } from '@mui/material';
import { Link } from 'react-router-dom';
import { getProjects, getUnlistedProjects } from '../services/api';
import Layout from '../components/Layout';

const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [unlistedProjects, setUnlistedProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getProjects(), getUnlistedProjects()])
      .then(([projectsResponse, unlistedProjectsResponse]) => {
        setProjects(projectsResponse.data);
        setUnlistedProjects(unlistedProjectsResponse.data);
        console.log("Projects:", projectsResponse.data);
        console.log("Unlisted Projects:", unlistedProjectsResponse.data);
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
            flexDirection: 'column',
            gap: '2rem',
            margin: '1rem 0',
          }}
        >
          <Box
            sx={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '1rem',
              justifyContent: 'center',
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

          {unlistedProjects.length > 0 && (
            <Box
              sx={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '1rem',
                justifyContent: 'center',
              }}
            >
              <Box sx={{ width: '100%', textAlign: 'center', marginBottom: '1rem' }}>
                <h3>Unlisted Projects</h3>
              </Box>
              {unlistedProjects.map((projectName) => (
                <Button
                  key={projectName}
                  component={Link}
                  to={`/cells/${projectName}`}
                  sx={{
                    backgroundColor: '#CCCCCC',
                    color: '#000000',
                    textTransform: 'none',
                    padding: '0.5rem 1rem',
                    borderRadius: '5px',
                    ':hover': {
                      backgroundColor: '#AAAAAA',
                    },
                    whiteSpace: 'nowrap',
                  }}
                >
                  {projectName}
                </Button>
              ))}
            </Box>
          )}
        </Box>
      )}
    </Layout>
  );
};

export default ProjectList;

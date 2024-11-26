import React, { useEffect, useState } from 'react';
import { List, ListItem, ListItemText, CircularProgress } from '@mui/material';
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
    <Layout title="Projects">
      {loading ? (
        <CircularProgress />
      ) : (
        <List>
          {projects.map((project) => (
            <ListItem 
              button 
              component={Link} 
              to={`/cells/${project.project_name}`} 
              key={project.project_name}
            >
              <ListItemText primary={project.project_name} />
            </ListItem>
          ))}
        </List>

      )}
    </Layout>
  );
};

export default ProjectList;

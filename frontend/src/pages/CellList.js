import React, { useEffect, useState } from 'react';
import { List, ListItem, ListItemText, CircularProgress } from '@mui/material';
import { Link, useParams } from 'react-router-dom';
import { getCellsByProject } from '../services/api';
import Layout from '../components/Layout';

const CellList = () => {
  const { projectName } = useParams();  
  const [cells, setCells] = useState([]);
  const [loading, setLoading] = useState(true);

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


  return (
    <Layout title={`Cells in Project: ${projectName}`}>
      {loading ? (
        <CircularProgress />
      ) : (
          <List>
            {cells.map(cell => (
              <ListItem 
                button={true} 
                component={Link} 
                to={`/cell/${cell.cell_name}`} 
                key={cell.cell_name}
              >
                <ListItemText primary={cell.cell_name} />
              </ListItem>
            ))}
          </List>
      )}
    </Layout>
  );
};

export default CellList;

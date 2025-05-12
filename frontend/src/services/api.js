import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api';

export const getProjects = () => axios.get(`${API_URL}/projects/`);
export const getProject = (name) => axios.get(`${API_URL}/projects/${name}`);
export const getUnlistedProjects = () => axios.get(`${API_URL}/projects/unlisted`);

export const getCellsByProject = (name) => axios.get(`${API_URL}/cells/project/${name}`);
export const getCellByName = (name) => axios.get(`${API_URL}/cells/${name}`);
export const getCellsByKeyword = (keyword) => axios.get(`${API_URL}/cells/search/${keyword}`);
export const getCellImages = async (name, index) => {
    const response = await axios.get(`${API_URL}/cells/${name}/images/${index}`, {
      responseType: 'blob'  // Tell Axios to expect a Blob response
    });
    return URL.createObjectURL(response.data);  // Create a URL for the image
  };
export const getCellImageHtmls = async (name, index) => {
    const response = await axios.get(`${API_URL}/cells/${name}/htmls/${index}`, {
      responseType: 'blob'
    });
    return URL.createObjectURL(response.data);
  };
export const getCellLatestCellInfo = (name) => axios.get(`${API_URL}/cells/${name}/info/latest`);

export const getTestRecordsByCell = (name) => axios.get(`${API_URL}/trs/cell/${name}`);
export const getTestRecord = ({ name, testType }) => 
  axios.get(`${API_URL}/trs/${name}`, {
    params: { test_type: testType }
  });
  
export const getTestRecordsByKeyword = (keyword) => axios.get(`${API_URL}/trs/search/${keyword}`);

export const getTasksStatus = () => axios.get(`${API_URL}/tasks/status`);
export const enqueueUpdateTask = (cellName) => axios.post(`${API_URL}/tasks/trs/update/${cellName}`);
export const enqueueResetTask = (cellName) => axios.post(`${API_URL}/tasks/trs/reset/${cellName}`);
export const enqueueCreateTask = (cellName) => axios.post(`${API_URL}/tasks/cell/create/${cellName}`);
export const enqueueProcessTask = (cellName) => axios.post(`${API_URL}/tasks/cell/process/${cellName}`);
export const enqueueUpdateProjectTask = (projectName) => axios.post(`${API_URL}/tasks/project/update/${projectName}`);
export const clearAllTasks = () => axios.post(`${API_URL}/tasks/clear`);
export const clearFinishedTasks = () => axios.post(`${API_URL}/tasks/clear/finished`);
export const clearFailedTasks = () => axios.post(`${API_URL}/tasks/clear/failed`);
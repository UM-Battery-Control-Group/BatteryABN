import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProjectList from './pages/ProjectList';
import CellList from './pages/CellList';
import CellDetails from './pages/CellDetails';
import CellImageDetail from './pages/CellImageDetail';
import CellSearch from './pages/CellSearch';
import TestRecordList from './pages/TestRecordList';
import TestRecordDetails from './pages/TestRecordDetails';
import TestRecordSearch from './pages/TestRecordSearch';
import TaskManager from './pages/TaskManager';
import TaskStatus from './pages/TaskStatus';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <main>
          <Routes>
            <Route path="/" element={<ProjectList />} />
            <Route path="/cells" element={<CellSearch />} />
            <Route path="/cells/:projectName" element={<CellList />} />
            <Route path="/cell/:cellName" element={<CellDetails />} />
            <Route path="/cell/:cellName/images/:index" element={<CellImageDetail />} />
            <Route path="/trs" element={<TestRecordSearch />} />
            <Route path="/trs/:cellName" element={<TestRecordList />} />
            <Route path="/tr/:trName" element={<TestRecordDetails />} />
            <Route path="/tasks" element={<TaskManager />} />
            <Route path="/tasks/status" element={<TaskStatus />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

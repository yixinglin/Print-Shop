import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './views/Home.jsx';
import CreateJob from './views/CreateJobView.jsx';
import PrintJobListView from './views/PrintJobListView.jsx';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/create-job" element={<CreateJob />} />
        <Route path="/jobs" element={<PrintJobListView />} />
      </Routes>
    </Router>
  );
};

export default App;

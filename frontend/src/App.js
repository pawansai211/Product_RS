import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Use BrowserRouter
import Signup from './components/SignUp';
import Login from './components/Login';
import Profile from './components/Profile';
import Upload from './services/UploadData';
import Home from './components/Home';

const App = () => {
  return (
    <Router>
      <Routes>
        {/* Use element instead of component */}
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/upload" element={<Upload />} />
      </Routes>
    </Router>
  );
};

export default App;

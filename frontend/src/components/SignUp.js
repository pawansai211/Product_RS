// Signup.js
import React, { useState } from 'react';
import './Signup.css';
import { useNavigate } from 'react-router-dom';
import { signup } from '../services/api';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await signup({ email, username, password });
      if (response) {
        navigate('/login'); // Redirect to login page after successful signup
      }
    } catch (error) {
      setError('Failed to sign up. Please try again.');
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <p>{error}</p>}
        <button type="submit">Sign Up</button>
      </form>
    </div>
    </div>
  );
};

export default Signup;

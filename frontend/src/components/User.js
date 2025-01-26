import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserProfile = ({ setUsername }) => {
  const [username, setUserNameState] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Get the token from localStorage
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Token is missing');
        }

        // Send the token in the Authorization header
        const response = await axios.get('http://127.0.0.1:8000/api/current_user/', {
          headers: {
            'Authorization': `Token ${token}`,  // Include token in the header
          },
        });

        // Set the username (and other user details if needed) in the state
        setUserNameState(response.data.username);
        setUsername(response.data.username);  // Passing the username to the parent component
        setLoading(false);
      } catch (error) {
        console.error('Error fetching user data:', error);
        setLoading(false);
      }
    };

    fetchUserData();
  }, [setUsername]);

  return (
    <div>
      {loading ? (
        <p>Loading user info...</p>
      ) : (
        <div>
          <h2>Welcome, {username}!</h2>  {/* Display the username */}
        </div>
      )}
    </div>
  );
};

export default UserProfile;

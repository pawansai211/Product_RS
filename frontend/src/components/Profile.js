// Profile.js
import React, { useEffect, useState } from 'react';
import { getUserProfile } from '../services/api';

const Profile = () => {
  const [userProfile, setUserProfile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const data = await getUserProfile();
        setUserProfile(data);
      } catch (err) {
        setError('Failed to load user profile.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h2>User Profile</h2>
      {userProfile ? (
        <div>
          <h3>Preferences</h3>
          <p>Preferred Product Type: {userProfile.preferences[0]?.preferred_product_type}</p>
          <p>Preferred Description: {userProfile.preferences[0]?.preferred_description}</p>

          <h3>Interactions</h3>
          <table>
            <thead>
              <tr>
                <th>Product Name</th>
                <th>Description</th>
                <th>Interaction Type</th>
                <th>Interaction Count</th>
              </tr>
            </thead>
            <tbody>
              {userProfile.interactions && userProfile.interactions.length > 0 ? (
                userProfile.interactions.map((interaction, index) => (
                  <tr key={index}>
                    <td>{interaction.product_name}</td>
                    <td>{interaction.description}</td>
                    <td>{interaction.interaction_type}</td>
                    <td>{interaction.interaction_count}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4">No interactions available.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      ) : (
        <p>{error || 'Loading profile...'}</p>
      )}
    </div>
  );
};

export default Profile;

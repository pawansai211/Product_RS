import React, { useEffect, useState } from 'react';
import { getUserProfile, getProductRecommendations } from '../services/api';
import ProductCard from './ProductCard';

const Profile = () => {
  const [userProfile, setUserProfile] = useState(null);
  const [recommendedProducts, setRecommendedProducts] = useState([]); // Initialize as an empty array
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true); // Add loading state to handle async data fetching

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const data = await getUserProfile();
        setUserProfile(data);
      } catch (err) {
        setError('Failed to load user profile.');
      }
    };

    const fetchRecommendations = async () => {
      try {
        const userId = localStorage.getItem('user_id');
        const products = await getProductRecommendations(userId);
        setRecommendedProducts(products);
      } catch (err) {
        setError('Failed to load recommendations.');
      } finally {
        setLoading(false); // Set loading to false after the async tasks finish
      }
    };

    fetchUserProfile();
    fetchRecommendations();
  }, []);

  // Handle loading and error states before rendering the main content
  if (loading) {
    return <p>Loading...</p>; // Show loading message
  }

  return (
    <div>
      <h2>User Profile</h2>
      {userProfile ? (
        <div>
          <h3>Preferences</h3>
          <p>Preferred Product Type: {userProfile.preferred_product_type}</p>
          <p>Preferred Description: {userProfile.preferred_description}</p>

          <h3>Liked Products</h3>
          <ul>
            {userProfile.liked_products && userProfile.liked_products.length > 0 ? (
              userProfile.liked_products.map((product) => (
                <li key={product.id}>{product.name}</li>
              ))
            ) : (
              <p>No liked products available.</p>
            )}
          </ul>

          <h3>Recommended Products</h3>
          <div>
            {Array.isArray(recommendedProducts) && recommendedProducts.length > 0 ? (
              recommendedProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))
            ) : (
              <p>No recommended products available.</p> // Handle empty recommended products
            )}
          </div>
        </div>
      ) : (
        <p>{error || 'Loading profile...'}</p> // Fallback error message or loading message
      )}
    </div>
  );
};

export default Profile;

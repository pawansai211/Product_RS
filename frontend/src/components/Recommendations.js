import './Recommendations.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ProductCard from './ProductCard';

const Recommendations = () => {
  const [recommendedProducts, setRecommendedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const userId = localStorage.getItem('user_id'); // Get the user ID from localStorage

  // Fetch recommended products when the component is mounted
  useEffect(() => {
    const fetchRecommendedProducts = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Token is missing');
        }

        const response = await axios.get(`http://127.0.0.1:8000/api/product_recommendations/${userId}/`, {
          headers: {
            'Authorization': `Token ${token}`,
          },
        });

        // Log the response for debugging
        console.log('Recommended Products:', response.data);

        setRecommendedProducts(response.data);
      } catch (error) {
        setError('Error fetching recommendations.');
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchRecommendedProducts();
    }
  }, [userId]);

  // Handle like and dislike interactions
  const handleInteraction = async (productId, interactionType) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('Token is missing');
      }

      const response = await axios.post(
        'http://127.0.0.1:8000/api/user_interaction/',
        { product_id: productId, interaction_type: interactionType },
        {
          headers: {
            'Authorization': `Token ${token}`,
          },
        }
      );

      console.log(response.data); // Log the response for debugging
    } catch (error) {
      console.error('Error interacting with product:', error.response ? error.response.data : error);
    }
  };

  if (loading) {
    return <p>Loading recommended products...</p>;
  }

  return (
    <div className="recommendations-container">
    <h2>Recommended Products</h2>

    {error && <p className="loading-error">{error}</p>}

    {recommendedProducts && recommendedProducts.length > 0 ? (
      <div className="product-list">
        {recommendedProducts.map((product) => (
          <div key={product.id} className="product-card-container">
            <ProductCard product={product} />
            <div className="interaction-buttons">
              <button onClick={() => handleInteraction(product.id, 'like')}>Like</button>
              <button onClick={() => handleInteraction(product.id, 'dislike')}>Dislike</button>
            </div>
          </div>
        ))}
      </div>
    ) : (
      <p className="no-products">No recommended products available.</p>
    )}
  </div>
  );
};

export default Recommendations;

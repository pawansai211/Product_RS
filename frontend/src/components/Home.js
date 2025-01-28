import React, { useState, useEffect } from 'react';
import './Home.css';
import axios from 'axios';
import UserProfile from './User';

const Home = () => {
  const [username, setUsername] = useState('');
  const [products, setProducts] = useState([]);  // Initialize products as an empty array
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        // Get the token from localStorage
        const token = localStorage.getItem('token');
        
        if (!token) {
          throw new Error('Token is missing');
        }

        // Send the token in the Authorization header
        const response = await axios.get('http://127.0.0.1:8000/api/products/', {
          headers: {
            'Authorization': `Token ${token}`,  // Include token in the header
          },
        });

        console.log(response.data);  // Log the response to see its structure
        setProducts(response.data);  // If the products are in the root of the response
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  // Handle like and dislike interactions
  const handleInteraction = async (productId, interactionType) => {
    try {
      // Get the token from localStorage
      const token = localStorage.getItem('token');

      if (!token) {
        throw new Error('Token is missing');
      }

      // Send the token in the Authorization header
      const response = await axios.post('http://127.0.0.1:8000/api/user_interaction/', {
        product_id: productId,
        interaction_type: interactionType,
      }, {
        headers: {
          'Authorization': `Token ${token}`,  // Include token in the header
        },
      });

      console.log(response.data);
    } catch (error) {
      console.error('Error interacting with product:', error.response ? error.response.data : error);
    }
  };

  return (
    <div>
      <UserProfile setUsername={setUsername} />
      <h2>Product List</h2>

      {/* Product List */}
      {loading ? (
        <p>Loading products...</p>
      ) : (
        <div className="product-list">
          {products && products.length > 0 ? (
            products.map((product) => (
              <div key={product.id} style={{ marginBottom: '20px' }} className="product-item">
                <h3>{product.product_name} ({product.category})</h3>
                <p>{product.description}</p>
                <img
                  src={product.image}
                  alt={product.product_name}
                  style={{ width: '100px', height: '100px' }}
                />
                <div>
                  {/* Like and Dislike Buttons */}
                  <button onClick={() => handleInteraction(product.id, 'like')}>Like</button>
                  <button onClick={() => handleInteraction(product.id, 'dislike')}>Dislike</button>
                </div>
              </div>
            ))
          ) : (
            <p className="no-products">No products found.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Home;

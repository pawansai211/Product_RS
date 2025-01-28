import React from 'react';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      {/* Ensure that the full URL is constructed for the image */}
      <img 
        src={`http://127.0.0.1:8000${product.image}`} 
        alt={product.product_name} 
        className="product-image" 
      />
      <h3>{product.product_name}</h3>
      <p>{product.description}</p>
      {/* Add other product details if necessary */}
    </div>
  );
};

export default ProductCard;

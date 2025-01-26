import React from 'react';

const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      <img src={product.image_url} alt={product.name} />
      <h4>{product.name}</h4>
      <p>{product.description}</p>
    </div>
  );
};

export default ProductCard;
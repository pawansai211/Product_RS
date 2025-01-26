import React, { useState } from 'react';
import axios from 'axios';

const ProductUploadForm = () => {
  const [productData, setProductData] = useState({
    product_name: 'shirt',  // Default value, you can modify the UI to let users choose
    category: 'clothing',    // Default value, you can modify the UI to let users choose
    description: '',
    image: null,
  });
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setProductData({
      ...productData,
      [name]: value,
    });
  };

  const handleFileChange = (e) => {
    setProductData({
      ...productData,
      image: e.target.files[0],
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('product_name', productData.product_name);
    formData.append('category', productData.category);
    formData.append('description', productData.description);
    formData.append('image', productData.image);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/upload_product/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert(response.data.message);
    } catch (error) {
      console.error(error);
      alert('Error uploading product');
    }
  };

  return (
    <div>
      <h2>Upload Product</h2>
      <form onSubmit={handleSubmit}>
        
        <div>
          <label>Product Type:</label>
          <select
            name="product_name"
            value={productData.product_name}
            onChange={handleChange}
            required
          >
            <option value="shirt">Shirt</option>
            <option value="pants">Pants</option>
            <option value="vest">Vest</option>
            <option value="earrings">Earrings</option>
            <option value="necklace">Necklace</option>
            <option value="bangles">Bangles</option>
            <option value="dress">Dress</option>
            <option value="skirt">Skirt</option>
            <option value="shoes">Shoes</option>
          </select>
        </div>
        <div>
          <label>Category:</label>
          <select
            name="category"
            value={productData.category}
            onChange={handleChange}
            required
          >
            <option value="clothing">Clothing</option>
            <option value="accessory">Accessory</option>
          </select>
        </div>
        <div>
          <label>Description:</label>
          <textarea
            name="description"
            value={productData.description}
            onChange={handleChange}
            required
          />
        </div>
        
        <div>
          <label>Image:</label>
          <input type="file" name="image" onChange={handleFileChange} required />
        </div>
        <button type="submit">Upload Product</button>
      </form>
    </div>
  );
};

export default ProductUploadForm;

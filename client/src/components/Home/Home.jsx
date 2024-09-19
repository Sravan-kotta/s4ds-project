import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const [images, setImages] = useState([]);
  const [imageNames, setImageNames] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Load images and image names from local storage when the component mounts
    const storedImages = JSON.parse(localStorage.getItem('images'));
    const storedImageNames = JSON.parse(localStorage.getItem('imageNames'));
    
    if (storedImages && storedImageNames) {
      setImages(storedImages);
      setImageNames(storedImageNames);
    }
  }, []);

  useEffect(() => {
    // Save images and image names to local storage whenever they change
    localStorage.setItem('images', JSON.stringify(images));
    localStorage.setItem('imageNames', JSON.stringify(imageNames));
  }, [images, imageNames]);

  const handlefileUpload = (event) => {
    const files = Array.from(event.target.files);
    const newImages = files.map(file => URL.createObjectURL(file));
    const newImageNames = files.map((_, index) => `Page ${images.length + index + 1}`);

    setImages(images.concat(newImages));
    setImageNames(imageNames.concat(newImageNames));
  };

  const handleDeleteImage = (index) => {
    const newImages = images.slice();
    const newImageNames = imageNames.slice();
    newImages.splice(index, 1);
    newImageNames.splice(index, 1);
    setImages(newImages);
    setImageNames(newImageNames);
  };

  const handleEvaluateClick = () => {
    navigate('/evaluation');
  };

  return (
    <div className="app">
      <div className="upload-section">
        <h2>Upload files</h2>
        <input type="file" id="fileInput" multiple onChange={handlefileUpload} />
        <label htmlFor="fileInput" className="custom-file-upload">Choose files</label>
        
        <div className="image-names">
          {imageNames.map((name, index) => (
            <div key={index} className="image-name">
              <p>{name}</p>
              <button onClick={() => handleDeleteImage(index)}>Delete</button>
            </div>
          ))}
        </div>

        {images.length > 0 && (
          <button className="evaluate-button" onClick={handleEvaluateClick}>Evaluate</button>
        )}
      </div>
      <div className="images-section">
        {images.map((image, index) => (
          <div key={index} className="image-container">
            <img src={image} alt={`Uploaded ${index}`} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;

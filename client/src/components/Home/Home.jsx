import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  /*const [images, setImages] = useState([]);
  const [imageNames, setImageNames] = useState([]);*/
  const navigate = useNavigate(); 

  /*useEffect(() => {
    // Load images and image names from local storage when the component mounts
    const storedImages = JSON.parse(localStorage.getItem('images'));
    const storedImageNames = JSON.parse(localStorage.getItem('imageNames'));
    
    if (storedImages && storedImageNames) {
      setImages(storedImages);
      setImageNames(storedImageNames);
    }
  }, []);*/

  /*useEffect(() => {
    // Save images and image names to local storage whenever they change
    localStorage.setItem('images', JSON.stringify(images));
    localStorage.setItem('imageNames', JSON.stringify(imageNames));
  }, [images, imageNames]);*/
  const handlefileUpload = (e) => {
    setFile(e.target.files[0]);
  };
  const handlefilesubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setMessage('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData, // Send the file in FormData
      });

      const data = await response.json();
      
      if (response.ok) {
        setMessage(`File processed: ${data.result} content: ${data.transcript}`);
      } else {
        setMessage('Error processing file.');
      }
    } catch (error) {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData, // Send the file in FormData
      });
      const data = await response.json();
      console.error('Error during file upload:', error);
      setMessage(`Error during file upload: ${error} content progress: ${data.transcipt}`);
    }
  };

  /*const handleDeleteImage = (index) => {
    const newImages = images.slice();
    const newImageNames = imageNames.slice();
    newImages.splice(index, 1);
    newImageNames.splice(index, 1);
    setImages(newImages);
    setImageNames(newImageNames);
  }; */

  const handleEvaluateClick = () => {
    navigate('/evaluation');
  };

  return (
    <div className="app">
      <div className="upload-section">
        <form onSubmit={handlefilesubmit}>
        <h2>Upload files</h2>
        <input type="file" id="fileInput" onChange={handlefileUpload} />
        <label htmlFor="fileInput" className="custom-file-upload">Choose files</label>
        <button type="submit">Upload</button>
        </form>
        <p>{message}</p>

      {/* <div className="image-names">
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
        ))} */}
        <button className="evaluate-button" onClick={handleEvaluateClick}>Evaluate</button>
      </div> 
    </div>
  );
};

export default Home;

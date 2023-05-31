import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [url, setUrl] = useState('');
  const [isMalicious, setIsMalicious] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (event) => {
    setUrl(event.target.value);
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:5000/backend/endpoint', { url });
      setIsMalicious(response.data.isMalicious);
    } catch (error) {
      console.error(error);
    }
    setIsLoading(false);
  };

  return (
    <div className="app">
      <h1>URL Upload</h1>
      <div className="input-container">
        <input
          type="text"
          placeholder="Enter URL"
          value={url}
          onChange={handleInputChange}
        />
        <button onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? 'Uploading...' : 'Upload'}
        </button>
      </div>
      {isMalicious !== null && (
        <div className={`result ${isMalicious ? 'malicious' : 'safe'}`}>
          {isMalicious ? 'Malicious URL' : 'Safe URL'}
        </div>
      )}
    </div>
  );
};

export default App;

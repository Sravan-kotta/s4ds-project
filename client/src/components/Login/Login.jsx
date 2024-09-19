import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './Login.css';
import logo from './s4ds.jpeg'




const LoginPage = () => {
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();  
        navigate('/home');};
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:5000/login', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ username, password }),
            });
      
            const data = await response.json();
      
            if (response.ok) {
              setMessage(data.message);
            } else {
              setMessage(data.message);
            }
            if (message == "Login successful") {
                navigate('/home');
            }
          } catch (error) {
            console.error('Error during login:', error);
            setMessage('Error during login');
          }
    };

    return (
        <div className="container">
            <div className="login-section">
                <img src= {logo} alt="Logo" className="logo" />
                <h1>Society for Data Science</h1>
                <form onSubmit={handleLogin}>
                    <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)}/>
                    <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>
                    <button type="submit">LOG IN</button>
                </form>
                <a href="#" className="forgot-password">Forgot password?</a>
                <a href="#" className="create-new">Don't have an account? CREATE NEW</a>
                {message && <p>{message}</p>}
            </div>
            <div className="info-section">
                <h1>We are more than just a company</h1>
                <p>Society for Data Science is a collaborative platform for Professional Bodies to promote Innovation around Data Science. Setting standards for the ethical professional practice of data science. Assuring base-level data scientist competency. Advancing data science to serve core values of the scientific method and noblesse oblige.</p>
            </div>
        </div>
    );
};

export default LoginPage;


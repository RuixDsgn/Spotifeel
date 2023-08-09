import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import queryString from 'query-string';
import WelcomePage from './WelcomePage';
import MoodSelectionPage from './MoodSelectionPage';
import AdjectiveSelectionPage from './AdjectiveSelectionPage';
import NewPlaylistPage from './NewPlaylistPage';
import './index.css';

const App = () => {
  const [authUrl, setAuthUrl] = useState('');
  const [accessToken, setAccessToken] = useState('');
  const [mood, setMood] = useState('');
  const [adjectives, setAdjectives] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('/get_auth_url')
      .then(response => {
        console.log('Authentication URL response:', response.data);
        setAuthUrl(response.data.auth_url);
      })
      .catch(error => {
        console.error('Error fetching authentication URL:', error);
      });

    // Check if the URL contains the access token
    const params = queryString.parse(window.location.search);
    const code = params.code;
    if (code) {
      handleAuthCallback(code);
    }
  }, []);

  const handleAuthCallback = (code) => {
    console.log('Handling auth callback with code:', code);
  
    axios.get(`/callback?code=${code}`)
      .then(response => {
        setAccessToken(response.data.access_token);
        console.log("Access Token (Frontend):", response.data.access_token);
        // Remove the access token from the URL to prevent displaying it
        window.history.replaceState({}, document.title, '/');
      })
      .catch(error => {
        console.error('Error fetching access token:', error);
        // Handle the error here (e.g., show an error message to the user)
      });
  };
  
  
  const handleGeneratePlaylist = (adjectives) => {
    // Ensure the user is authenticated before generating the playlist
    if (accessToken) {
      console.log("Selected Adjectives (Frontend):", adjectives); // Log the selected adjectives
      axios.post('/generate', { access_token: accessToken, mood, adjectives, redirect_uri: 'http://localhost:4000/mood' })
        .then(response => {
          setMessage(response.data.message);
          console.log(message);
          const newPlaylistId = response.data.playlist_id;
          // Redirect the user to the NewPlaylistPage with the new playlist ID
          return <Navigate to={`/newplaylist/${newPlaylistId}`} />;
        })
        .catch(error => {
          console.error('Error generating playlist:', error);
        });
    } else {
      // Handle the case where the user is not authenticated yet
      console.log("User is not authenticated. Please log in with Spotify first.");
    }
  };

  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<WelcomePage authUrl={authUrl} />} />
          <Route path="/mood" element={<MoodSelectionPage setMood={setMood} />} />
          <Route path="/adjectives" element={<AdjectiveSelectionPage mood={mood} setAdjectives={setAdjectives} handleGeneratePlaylist={handleGeneratePlaylist} />} />
          <Route path="/generate" element={<NewPlaylistPage accessToken={accessToken} />} />
          <Route path="/newplaylist" element={<NewPlaylistPage accessToken={accessToken} />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

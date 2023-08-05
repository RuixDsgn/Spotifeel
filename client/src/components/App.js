import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useParams } from 'react-router-dom';
import axios from 'axios';
import queryString from 'query-string';
import WelcomePage from './WelcomePage';
import MoodSelectionPage from './MoodSelectionPage';
import AdjectiveSelectionPage from './AdjectiveSelectionPage';

const App = () => {
  const [authUrl, setAuthUrl] = useState('');
  const [accessToken, setAccessToken] = useState('');
  const [mood, setMood] = useState('');
  const [adjectives, setAdjectives] = useState(['', '', '']);
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('/get_auth_url')
      .then(response => {
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
    axios.get(`/callback?code=${code}`)
      .then(response => {
        setAccessToken(response.data.access_token);
        console.log("Access Token (Frontend):", response.data.access_token);
        // Remove the access token from the URL to prevent displaying it
        window.history.replaceState({}, document.title, '/');
      })
      .catch(error => {
        console.error('Error fetching access token:', error);
      });
  };
  
  const handleGeneratePlaylist = () => {
    axios.post('/generate_playlist', { access_token: accessToken, mood, adjectives, redirect_uri: 'http://localhost:4000/callback' })
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('Error generating playlist:', error);
      });
  };

  return (
    <Router>
      <div>
        <h1>Spotify Playlist Generator</h1>
        <Routes>
          <Route path="/" element={<WelcomePage authUrl={authUrl} />} />
          <Route
            path="/mood"
            element={<MoodSelectionPage setMood={setMood} />}
          />
          <Route
            path="/adjectives"
            element={<AdjectiveSelectionPage mood={mood} setAdjectives={setAdjectives} handleGeneratePlaylist={handleGeneratePlaylist} />}
          />
          <Route path="/generate" element={<div>
            <h2>Playlist Generated!</h2>
            <p>{message}</p>
            <p>Choose one of the options below:</p>
            <Link to="/spotify-app">Open in Spotify App</Link>
            <Link to="/spotify-web">Open in Spotify Web Player</Link>
            <Link to="/mood">Start Over</Link>
          </div>} />
          <Route path="/spotify-app" element={<div>
            <h2>Opening in Spotify App...</h2>
          </div>} />
          <Route path="/spotify-web" element={<div>
            <h2>Opening in Spotify Web Player...</h2>
          </div>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

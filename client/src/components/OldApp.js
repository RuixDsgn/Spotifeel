import React, { useState, useEffect } from 'react';
import axios from 'axios';
import queryString from 'query-string';

const App = () => {
  const [authUrl, setAuthUrl] = useState('');
  const [accessToken, setAccessToken] = useState('');
  const [mood, setMood] = useState('');
  const [adjectives, setAdjectives] = useState(['', '', '']);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Fetch the authentication URL when the component mounts
    axios.get('/get_auth_url')
      .then(response => {
        setAuthUrl(response.data.auth_url);
      })
      .catch(error => {
        console.error('Error fetching authentication URL:', error);
      });

    // Check for the OAuth2 callback code in the URL query parameters
    const params = queryString.parse(window.location.search);
    const code = params.code;
    if (code) {
      // Call the handleAuthCallback function to exchange the code for the access token
      handleAuthCallback(code);
    }
  }, []);

  useEffect(() => {
    // This effect should depend on the accessToken state
    if (accessToken) {
      // Call the function to generate the playlist when accessToken changes
      handleGeneratePlaylist();
    }
  }, [accessToken]); // Add accessToken as a dependency here

  // Move handleAuthCallback inside the useEffect callback
  const handleAuthCallback = (code) => {
    // Make the HTTP GET request to the backend /callback endpoint
    axios.get(`/callback?code=${code}`)
      .then(response => {
        // Set the access token in the state
        setAccessToken(response.data.access_token);
        console.log("Access Token (Frontend):", response.data.access_token);

        // After handling the callback, remove the access code from the URL
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
    <div>
      <h1>Spotify Playlist Generator</h1>
      {accessToken ? (
        <div>
          <h2>Welcome! You're logged in.</h2>
          <p>Now you can select your mood and adjectives to generate a playlist.</p>
          <label>
            Mood:
            <input type="text" value={mood} onChange={e => setMood(e.target.value)} />
          </label>
          <br />
          <label>
            Adjective 1:
            <input type="text" value={adjectives[0]} onChange={e => setAdjectives([e.target.value, adjectives[1], adjectives[2]])} />
          </label>
          <br />
          <label>
            Adjective 2:
            <input type="text" value={adjectives[1]} onChange={e => setAdjectives([adjectives[0], e.target.value, adjectives[2]])} />
          </label>
          <br />
          <label>
            Adjective 3:
            <input type="text" value={adjectives[2]} onChange={e => setAdjectives([adjectives[0], adjectives[1], e.target.value])} />
          </label>
          <br />
          <button onClick={handleGeneratePlaylist}>Generate Playlist</button>
          {message && <p>{message}</p>}
        </div>
      ) : (
        <div>
          <h2>Log in with your Spotify account to generate a playlist.</h2>
          <a href={authUrl}>Log in</a>
        </div>
      )}
    </div>
  );
};

export default App;

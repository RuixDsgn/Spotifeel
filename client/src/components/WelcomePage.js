// welcomepage.js (frontend)
import React from 'react';
import { Link } from 'react-router-dom';

const WelcomePage = ({ authUrl }) => {
  const handleLogin = () => {
    window.location.href = authUrl; // Redirect the user to the Spotify authentication URL
  };

  return (
    <div>
      <h2>Welcome to Spotifeel!</h2>
      <p>Spotifeel is a playlist generator that creates personalized playlists based on your mood and adjectives.</p>
      <p>Let's get started!</p>
      {/* Add a button to proceed to the MoodSelectionPage */}
      <button onClick={handleLogin}>Get Started</button>
    </div>
  );
};

export default WelcomePage;

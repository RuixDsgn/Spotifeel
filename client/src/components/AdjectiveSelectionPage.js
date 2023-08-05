import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const AdjectiveSelectionPage = ({ mood, setAdjectives, handleGeneratePlaylist }) => {
  const mood_adjectives = {
    "happy": {
      "adjectives": ["Excited", "Joyful", "Energetic", "Content", "Optimistic", "Playful", "Grateful", "Amused", "Carefree"],
      "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
    },
    "sad": {
      "adjectives": ["Melancholic", "Gloomy", "Heartbroken", "Lonely", "Despairing", "Mournful", "Sorrowful", "Depressed", "Regretful"],
      "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
    },
    "angry": {
      "adjectives": ["Furious", "Irritated", "Enraged", "Annoyed", "Hostile", "Frustrated", "Resentful", "Livid", "Agitated"],
      "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
    },
    "fearful": {
      "adjectives": ["Terrified", "Anxious", "Panicked", "Nervous", "Apprehensive", "Startled", "Timid", "Dreadful", "Jittery"],
      "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
    }
  };

  const [selectedAdjectives, setSelectedAdjectives] = useState([]);

  const navigate = useNavigate();
  const location = useLocation();

  const handleAdjectiveSelection = (adjective) => {
    // Check if the adjective is already selected, and if so, remove it from the selectedAdjectives array.
    if (selectedAdjectives.includes(adjective)) {
      setSelectedAdjectives((prevSelected) => prevSelected.filter((item) => item !== adjective));
    } else {
      // If the adjective is not selected, add it to the selectedAdjectives array.
      setSelectedAdjectives((prevSelected) => [...prevSelected, adjective]);
    }
  };

  const handlePlaylistGeneration = () => {
    if (selectedAdjectives.length === 3) {
      // Assuming you have the logic to set 'accessToken' and 'message' states in App.js
      setAdjectives(selectedAdjectives);
      handleGeneratePlaylist();
      navigate('/generate');
    } else {
      // Show an error message or alert to indicate that the user must select exactly 3 adjectives.
      alert('Please select exactly 3 adjectives to generate the playlist.');
    }
  };

  return (
    <div>
      <h2>Adjective Selection</h2>
      <p>Select adjectives that represent your mood: {mood}</p>
      <ul>
        {mood_adjectives[mood]?.adjectives.map((adjective, index) => (
          <li key={index}>
            <button
              className={selectedAdjectives.includes(adjective) ? 'selected' : ''}
              onClick={() => handleAdjectiveSelection(adjective)}
            >
              {adjective}
            </button>
          </li>
        ))}
      </ul>
      <button onClick={handlePlaylistGeneration}>Generate Playlist</button>
    </div>
  );
};

export default AdjectiveSelectionPage;

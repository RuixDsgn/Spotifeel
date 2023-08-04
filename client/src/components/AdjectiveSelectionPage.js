import React from 'react';
import { useLocation } from 'react-router-dom';

const AdjectiveSelectionPage = ({ mood, setAdjectives, navigate, handleGeneratePlaylist }) => {
  const location = useLocation();

  // Define the adjectives based on the selected mood
  const moodAdjectives = {
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

  // Get the adjectives for the selected mood
  const selectedAdjectives = moodAdjectives[mood]?.adjectives || [];

  const handleAdjectiveChange = (index, adjective) => {
    const updatedAdjectives = [...selectedAdjectives];
    updatedAdjectives[index] = adjective;
    setAdjectives(updatedAdjectives);
  };

  const handleGenerateClick = () => {
    if (selectedAdjectives.length === 3 && selectedAdjectives.every(Boolean)) {
      // All 3 adjectives have been selected, call the handleGeneratePlaylist function
      handleGeneratePlaylist();
    } else {
      alert('Please select 3 adjectives.');
    }
  };

  return (
    <div>
      <h2>Adjective Selection</h2>
      <p>Selected Mood: {mood}</p>
      <p>Select 3 adjectives that represent your current mood:</p>
      <ul>
        {selectedAdjectives.map((adjective, index) => (
          <li key={index}>
            <input
              type="text"
              value={adjective}
              onChange={(e) => handleAdjectiveChange(index, e.target.value)}
            />
          </li>
        ))}
      </ul>
      <button onClick={handleGenerateClick}>Generate Playlist</button>
      <br />
      <button onClick={() => navigate('/mood')}>Back</button>
    </div>
  );
};

export default AdjectiveSelectionPage;

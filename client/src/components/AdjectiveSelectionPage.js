import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

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

  const handleAdjectiveSelection = (adjective) => {
    if (selectedAdjectives.includes(adjective)) {
      setSelectedAdjectives((prevSelected) => prevSelected.filter((item) => item !== adjective));
    } else {
      setSelectedAdjectives((prevSelected) => [...prevSelected, adjective]);
    }
  };

  const handlePlaylistGeneration = () => {
    if (selectedAdjectives.length === 3) {
      setAdjectives(selectedAdjectives); // Set adjectives in the state
      handleGeneratePlaylist(selectedAdjectives); // Pass selectedAdjectives to handleGeneratePlaylist
      console.log(selectedAdjectives)
      navigate('/generate');
    } else {
      alert('Please select exactly 3 adjectives to generate the playlist.');
    }
  };
  
  return (
    <div className='adjective-div'>
      <h2 className='adjective-h2'>If you could describe your mood: {mood}, in using three adjectives, what would they be?</h2><br />
      <div className='adjective-buttons-div'>
  {mood_adjectives[mood]?.adjectives.map((adjective, index) => (
    <button
      id={selectedAdjectives.includes(adjective) ? 'adjective-buttons-active' : 'adjective-buttons'}
      key={index}
      onClick={() => handleAdjectiveSelection(adjective)}
    >
      {adjective}
    </button>
  ))}
</div>
      <br />
      <br />
      <button className='myAdjectiveButton' onClick={handlePlaylistGeneration}>Generate Playlist</button>
    </div>
  );
};

export default AdjectiveSelectionPage;

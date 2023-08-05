import React from 'react';
import { Link } from 'react-router-dom';

const MoodSelectionPage = ({ setMood }) => {
  const handleMoodSelection = (mood) => {
    setMood(mood);
  };

  return (
    <div>
      <h2>Choose Your Mood</h2>
      <Link to="/adjectives" onClick={() => handleMoodSelection('happy')}>Happy</Link>
      <Link to="/adjectives" onClick={() => handleMoodSelection('sad')}>Sad</Link>
      <Link to="/adjectives" onClick={() => handleMoodSelection('angry')}>Angry</Link>
      <Link to="/adjectives" onClick={() => handleMoodSelection('fearful')}>Fearful</Link>
    </div>
  );
};

export default MoodSelectionPage;

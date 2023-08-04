import React from 'react';
import { Link } from 'react-router-dom';

const MoodSelectionPage = () => {
  return (
    <div>
      <h2>Choose Your Mood</h2>
      <Link to="/adjective?mood=happy">Happy</Link>
      <Link to="/adjective?mood=sad">Sad</Link>
      <Link to="/adjective?mood=angry">Angry</Link>
      <Link to="/adjective?mood=fearful">Fearful</Link>
    </div>
  );
};

export default MoodSelectionPage;

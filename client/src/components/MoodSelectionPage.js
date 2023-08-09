import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const MoodSelectionPage = ({ setMood }) => {

  const location = useLocation();
  const access_token = location.state?.code;

  const handleMoodSelection = (mood) => {
    setMood(mood);
  };

  return (
    <div className='mood-div'>
      <h2 className='mood-h2'>How are you feeling today?</h2>
      <Link to="/adjectives" onClick={() => handleMoodSelection('happy')} className='myMoodButton'>Happy</Link><br />
      <Link to="/adjectives" onClick={() => handleMoodSelection('sad')} className='myMoodButton'>Sad</Link><br />
      <Link to="/adjectives" onClick={() => handleMoodSelection('angry')} className='myMoodButton'>Angry</Link><br />
      <Link to="/adjectives" onClick={() => handleMoodSelection('fearful')} className='myMoodButton'>Fearful</Link><br />
    </div>
  );
};

export default MoodSelectionPage;

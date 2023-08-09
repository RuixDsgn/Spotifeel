// welcomepage.js (frontend)
import React from 'react';
import RotatingCircle from './rotateAnimation';

const WelcomePage = ({ authUrl }) => {

  return (
    <div className='welcome-page-div'>
      <div className='App'>
      <RotatingCircle />
      </div>
      <h4>Your Personal Daily Playlist Creator</h4>
      <p className='welcome-page-p'>
        Here's how it works: <br /><br />
         <strong>1.</strong>  Tell us how you're feeling today: Happy, Sad, Angry, or Fearful. <br /><br />
         <strong>2.</strong>  Choose three adjectives that best describe your current mood. <br /><br />
         <strong>3.</strong>  Our advanced algorithm analyzes your selected adjectives, assigning numerical values to each, and matches them with a curated list of genres. <br /><br />

Spotifeel then fetches artists from Spotify who resonate with those genres and adds their best tracks to your brand-new playlist! It's like having a personal DJ crafting the ideal soundtrack for your day.

Experience the power of music tailored to your emotions with Spotifeel. Start your day on the right note – happy, upbeat, or reflective – and let the rhythm of your emotions guide your listening journey.

Discover new tunes, rediscover old favorites, and immerse yourself in the perfect melody for every moment. Spotifeel – where music and emotions harmonize like never before.</p>
      <p><strong>Let's get started!</strong></p>
      {/* Add a button to proceed to the MoodSelectionPage */}
      <a href={authUrl} className='myButton'>Log into Spotify</a>
    </div>
  );
};

export default WelcomePage;

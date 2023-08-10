import React, { useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import axios from 'axios';

const NewPlaylistPage = ({ accessToken }) => {

  return (
    <div className='playlist-div'>
      <h2 className='new-playlist-h2'>Playlist Generated!</h2>
      <p className='new-playlist-p'>Your new playlist is ready.</p>
      <p className='new-playlist-p'>Choose one of the options below:</p>
      <a className='myPlaylistButton' href='https://open.spotify.com'>Open in Spotify Web Player</a>
      <Link className='myPlaylistButton' to='/playlists'>Show me my Playlists</Link> 
      <Link className='myPlaylistButton' to="/mood">Start Over</Link>
    </div>
  );
};

export default NewPlaylistPage;


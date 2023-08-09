import React, { useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import axios from 'axios';

const NewPlaylistPage = ({ accessToken }) => {
  const { playlist_id } = useParams();

  useEffect(() => {
    // Fetch the playlist details using the playlist_id from the URL params
    axios.get(`/playlist-details?access_token=${accessToken}&playlist_id=${playlist_id}`)
      .then(response => {
        // You can handle the playlist details here if needed
      })
      .catch(error => {
        console.error('Error fetching playlist details:', error);
        // Handle the error here (e.g., show an error message to the user)
      });
  }, []);

  return (
    <div className='playlist-div'>
      <h2 className='new-playlist-h2'>Playlist Generated!</h2>
      <p className='new-playlist-p'>Your new playlist is ready.</p>
      <p className='new-playlist-p'>Choose one of the options below:</p>
      <a className='myPlaylistButton' href='https://open.spotify.com'>Open in Spotify Web Player</a>
      {/* <Link to={`/spotify-app/${playlist_id}`}>Open in Spotify App</Link> */}
      <Link className='myPlaylistButton' to="/mood">Start Over</Link>
    </div>
  );
};

export default NewPlaylistPage;


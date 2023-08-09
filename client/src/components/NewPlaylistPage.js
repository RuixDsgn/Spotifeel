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
    <div>
      <h2>Playlist Generated!</h2>
      <p>Your new playlist is ready.</p>
      <p>Choose one of the options below:</p>
      <Link to={`/spotify-app/${playlist_id}`}>Open in Spotify App</Link>
      <Link to={`/spotify-web/${playlist_id}`}>Open in Spotify Web Player</Link>
      <Link to="/mood">Start Over</Link>
    </div>
  );
};

export default NewPlaylistPage;


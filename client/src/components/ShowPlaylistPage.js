import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Playlist from './Playlist';

const ShowPlaylistPage = ({ accessToken }) => {
  const [playlists, setPlaylists] = useState([]);

  useEffect(() => {
    // Fetch user playlists using the access token
    axios
      .get(`/playlists?access_token=${accessToken}`)
      .then(response => {
        console.log(response.data)
        setPlaylists(response.data.playlists.items);
      })
      .catch(error => {
        console.error('Error fetching user playlists:', error);
      });
  }, [accessToken]);

  return (
    <div>
      <h2>Your Playlists</h2>
      <ul>
        <Playlist playlists={playlists}/>
      </ul>
    </div>
  );
};

export default ShowPlaylistPage;

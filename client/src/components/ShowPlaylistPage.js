import React, { useEffect, useState } from 'react';
import axios from 'axios';

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
        {playlists.map(playlist => (
          <li key={playlist.id}>
            <a href={`https://open.spotify.com/playlist/${playlist.id}`} target="_blank" rel="noopener noreferrer">
              {playlist.name}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ShowPlaylistPage;

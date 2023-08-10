import React from 'react'
import PlaylistCard from './PlaylistCard'
import Row from 'react-bootstrap/Row';


const Playlist = ({playlists}) => {

  const renderPlaylist = () => {
    return playlists.map((playlist) => {
      return <PlaylistCard  playlist={playlist}/>
    })
  }
  return (
    <Row xs={1} md={2} lg={4}>
        {renderPlaylist()}
    </Row>
  )
}

export default Playlist


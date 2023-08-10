import React from 'react'
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'

const PlaylistCard = ({playlist}) => {

  return (
        <Col>
            <Card id={playlist.id} style={{ width: '18rem', marginRight: '20px', marginBottom: '10px' }}>
                <Card.Img variant="top" src={playlist.images[0].url}/>
                <Card.Body>
                <Card.Title>{playlist.name}</Card.Title>
                <Card.Text>
                 track items: {playlist.tracks.total} songs
                </Card.Text>
                <Button href={playlist.external_urls.spotify} variant="primary">Listen on Spotify</Button>
                </Card.Body>
          </Card>
        </Col>
  )
}

export default PlaylistCard
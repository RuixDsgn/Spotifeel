from flask import Flask, request, jsonify, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4000"}})
app.secret_key = os.getenv('secret_key') 

# Spotify app credentials
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = 'http://localhost:4000/callback'

# Function to generate the Spotify OAuth2 URL
def get_spotify_oauth_url():
    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-modify-public')
    auth_url = auth_manager.get_authorize_url()
    return auth_url

@app.route('/get_auth_url')
def get_auth_url():
    auth_url = get_spotify_oauth_url()
    return jsonify({'auth_url': auth_url})

@app.route('/callback')
def callback():
    # Handle the Spotify OAuth2 callback and return the access token
    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-modify-public')
    access_token = auth_manager.get_access_token(request.args['code'])
    return jsonify({'access_token': access_token})

@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    access_token = request.json['access_token']
    mood = request.json['mood']
    adjectives = request.json['adjectives']
    redirect_uri = request.json['redirect_uri']  # Add the provided 'redirect_uri'

    # Call the playlist generation method here with the access_token, mood, adjectives, and playlist name
    playlist = generate_spotify_playlist(access_token, mood, adjectives, 'My Playlist')

    if playlist:
        return jsonify({'message': 'Playlist created successfully!'})
    else:
        return jsonify({'error': 'Failed to generate playlist.'})
def fetch_artists_from_spotify(token, genres):
    sp = spotipy.Spotify(auth=token)
    artists = []
    for genre in genres:
        results = sp.search(q=f'genre:{genre}', type='artist', limit=5)
        artists.extend([(artist['name'], artist['id']) for artist in results['artists']['items']])
    return artists

def fetch_tracks_from_spotify(token, artist_ids):
    sp = spotipy.Spotify(auth=token)
    tracks = []
    for artist_id in artist_ids:
        results = sp.artist_top_tracks(artist_id)
        tracks.extend([track['uri'] for track in results['tracks']])
    return tracks

def create_playlist(token, playlist_name, tracks):
    sp = spotipy.Spotify(auth=token)
    playlist = sp.user_playlist_create(sp.me()['id'], playlist_name)
    sp.user_playlist_add_tracks(sp.me()['id'], playlist['id'], tracks)
    return playlist

def generate_spotify_playlist(token, mood, adjectives, playlist_name):
    adjective_genre_mapping = {
            "Excited": ["pop", "dance"],
            "Joyful": ["pop", "indie pop"],
            "Energetic": ["rock", "electronic"],
            "Content": ["chill", "acoustic"],
            "Optimistic": ["pop", "indie pop"],
            "Playful": ["pop", "indie pop"],
            "Grateful": ["chill", "acoustic"],
            "Amused": ["pop", "indie pop"],
            "Carefree": ["pop", "reggae"],

            "Melancholic": ["indie", "folk"],
            "Gloomy": ["alternative", "indie"],
            "Heartbroken": ["indie", "pop"],
            "Lonely": ["indie", "folk"],
            "Despairing": ["alternative", "indie"],
            "Mournful": ["indie", "folk"],
            "Sorrowful": ["indie", "pop"],
            "Depressed": ["alternative", "indie"],
            "Regretful": ["indie", "pop"],

            "Furious": ["metal", "hard rock"],
            "Irritated": ["punk", "alternative"],
            "Enraged": ["metal", "hard rock"],
            "Annoyed": ["punk", "alternative"],
            "Hostile": ["metal", "hard rock"],
            "Frustrated": ["punk", "alternative"],
            "Resentful": ["metal", "hard rock"],
            "Livid": ["punk", "alternative"],
            "Agitated": ["metal", "hard rock"],

            "Terrified": ["ambient", "soundtrack"],
            "Anxious": ["ambient", "soundtrack"],
            "Panicked": ["ambient", "soundtrack"],
            "Nervous": ["ambient", "soundtrack"],
            "Apprehensive": ["ambient", "soundtrack"],
            "Startled": ["ambient", "soundtrack"],
            "Timid": ["ambient", "soundtrack"],
            "Dreadful": ["ambient", "soundtrack"],
            "Jittery": ["ambient", "soundtrack"]        
    }

    mood_adjectives = {
            "happy": {
                "adjectives": ["Excited", "Joyful", "Energetic", "Content", "Optimistic", "Playful", "Grateful", "Amused", "Carefree"],
                "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
            },
            "sad": {
                "adjectives": ["Melancholic", "Gloomy", "Heartbroken", "Lonely", "Despairing", "Mournful", "Sorrowful", "Depressed", "Regretful"],
                "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
            },
            "angry": {
                "adjectives": ["Furious", "Irritated", "Enraged", "Annoyed", "Hostile", "Frustrated", "Resentful", "Livid", "Agitated"],
                "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
            },
            "fearful": {
                "adjectives": ["Terrified", "Anxious", "Panicked", "Nervous", "Apprehensive", "Startled", "Timid", "Dreadful", "Jittery"],
                "numerical_values": [8, 7, 6, 5, 7, 6, 5, 7, 6]
            }
    }

    selected_genres = set()
    selected_adjectives = mood_adjectives.get(mood)
    if selected_adjectives:
        for adjective in adjectives:
            if adjective in selected_adjectives['adjectives']:
                selected_genres.update(adjective_genre_mapping.get(adjective, []))

    artists = fetch_artists_from_spotify(token, selected_genres)
    if not artists:
        return None

    artist_ids = [artist[1] for artist in artists]
    tracks = fetch_tracks_from_spotify(token, artist_ids)
    if not tracks:
        return None

    return create_playlist(token, playlist_name, tracks)

if __name__ == '__main__':
    app.run(debug=True, port=5555)
# from config import app, db, api
# from models import Questionnaire1, Questionnaire2, UserEmotion, UserAdjective1, UserAdjective2, UserAdjective3, Genre1, Genre2, Genre3
# from flask_migrate import Migrate
# from sqlalchemy import func
# from flask import Flask, request, make_response, session, jsonify
# from flask_restful import Resource
# from config import app, db, api
# from algorithm import PlaylistGeneratorß

# class Songs(Resource):
#     def get(self):
#         return songs

# api.add_resource(Songs, '/song')

# class Artist(Resource):
#     def get(self):
#         return result
    
# api.add_resource(Artist, '/artist')

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)

from flask import Flask, request, jsonify, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4000"}})
app.secret_key = 'dullescythe' 

# Spotify app credentials
client_id = 'bcba09cb1f4441edb08d0e5bdf2799a2'
client_secret = 'b264de26c4c74ed784a8a187cdafb085'
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
    print("Access Token:", access_token)
    mood = request.json['mood']
    adjectives = request.json['adjectives']

    # Call the playlist generation method here with the access_token, mood, adjectives, and playlist name
    playlist_name = 'My Playlist'
    playlist = generate_spotify_playlist(access_token, mood, adjectives, playlist_name)

    if playlist:
        return jsonify({'message': 'Playlist created successfully!'})
    else:
        return jsonify({'error': 'Failed to generate playlist.'})

def fetch_artists_from_spotify(token, genres):
    sp = spotipy.Spotify(auth=token)
    artists = []

    try:
        # Get recommended tracks based on the selected genres
        recommended_tracks = sp.recommendations(seed_genres=list(genres), limit=5)['tracks']

        # Extract artists from the recommended tracks
        for track in recommended_tracks:
            artist_name = track['artists'][0]['name']
            artist_id = track['artists'][0]['id']
            artists.append((artist_name, artist_id))
            print(f"Artist '{artist_name}' found in recommended tracks.")
    except spotipy.SpotifyException as e:
        print("An error occurred while fetching artists from Spotify.")
        print("Error message:", e)

    return artists

def fetch_tracks_from_spotify(token, artist_ids):
    sp = spotipy.Spotify(auth=token)
    tracks = []
    for artist_id in artist_ids:
        try:
            results = sp.artist_top_tracks(artist_id)
            tracks.extend([track['uri'] for track in results['tracks']])
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error fetching top tracks for artist: {artist_id}. Reason: {e}")
    return tracks

def create_playlist(token, playlist_name, tracks):
    sp = spotipy.Spotify(auth=token)
    playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, public=True)  # Set the playlist privacy to public
    sp.user_playlist_add_tracks(sp.me()['id'], playlist['id'], tracks)
    print(playlist)
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

    "Furious": ["metal", "hard-rock"],
    "Irritated": ["punk", "alternative"],
    "Enraged": ["metal", "hard-rock"],
    "Annoyed": ["punk", "alternative"],
    "Hostile": ["metal", "hard-rock"],
    "Frustrated": ["punk", "alternative"],
    "Resentful": ["metal", "hard-rock"],
    "Livid": ["punk", "alternative"],
    "Agitated": ["metal", "hard-rock"],

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

    print("Selected Genres:", selected_genres)

    artists = fetch_artists_from_spotify(token, selected_genres)
    if not artists:
        print("No artists found.")
        return None

    artist_ids = [artist[1] for artist in artists]
    tracks = fetch_tracks_from_spotify(token, artist_ids)
    if not tracks:
        print("No tracks found.")
        return None

    print("Creating playlist...")
    playlist = create_playlist(token, playlist_name, tracks)
    if not playlist:
        print("Failed to create playlist.")
        return None

    print("Playlist created successfully!")
    return playlist    
 
if __name__ == '__main__':
    app.run(debug=True, port=5555)
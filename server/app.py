from flask import Flask, request, jsonify, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4000"}})
app.secret_key = os.environ.get('secret_key') 

# Spotify app credentials
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
redirect_uri = 'http://localhost:4000/mood'


CACHE_PATH = os.path.join(os.getcwd(), 'spotify_cache')

# Function to generate the Spotify OAuth2 URL
def get_spotify_oauth_url():
    auth_manager = SpotifyOAuth(
                    client_id=client_id, 
                    client_secret=client_secret, 
                    redirect_uri=redirect_uri, 
                    scope='playlist-modify-public,user-library-read')
    auth_url = auth_manager.get_authorize_url()
    return auth_url

@app.route('/get_auth_url')
def get_auth_url():
    auth_url = get_spotify_oauth_url()
    return jsonify({'auth_url': auth_url})

@app.route('/callback')
def callback():
    # Handle the Spotify OAuth2 callback and respond with the access token
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='playlist-modify-public,user-library-read')

    try:
        access_token = auth_manager.get_access_token(request.args['code'], as_dict=False)
        print("Access Token:", access_token)
        return jsonify({'access_token': access_token})  # Return access token as JSON
    except spotipy.exceptions.SpotifyException as e:
        print("Error fetching access token:", e)
        return jsonify({'error': 'Failed to fetch access token.'}), 500

@app.route('/generate', methods=['POST'])
def generate_playlist():
    access_token = request.json['access_token']
    print("Access Token:", access_token)
    mood = request.json['mood']
    adjectives = request.json['adjectives']

    print("Selected Adjectives (Backend):", adjectives) 

    # Check if the access token is valid
    if not check_access_token(access_token):
        return jsonify({'error': 'Authentication failed. Please check your credentials.'}), 401

    # Call the playlist generation method here with the access_token, mood, adjectives, and playlist name
    playlist_name = f'Mood of the day: {mood}'
    playlist_id = generate_spotify_playlist(access_token, mood, adjectives, playlist_name)

    if playlist_id:
        return jsonify({'playlist_id': playlist_id})
    else:
        return jsonify({'error': 'Failed to generate playlist.'}), 500
    
@app.route('/playlists')
def user_playlists():
    access_token = request.args['access_token']
    playlists = fetch_user_playlists(access_token)
    if playlists:
        return jsonify({'playlists': playlists})
    else:
        return jsonify({'error': 'Failed to fetch user playlists.'}), 500

def fetch_user_playlists(access_token):
    try:
        sp = spotipy.Spotify(auth=access_token)
        playlists = sp.current_user_playlists()
        return playlists
    except spotipy.exceptions.SpotifyException as e:
        print("An error occurred while fetching user playlists.")
        print("Error message:", e)
        return None


# @app.route('/playlist-details')
# def playlist_details():
#     access_token = request.args['access_token']
#     playlist_id = request.args['playlist_id']

#     # Check if the access token is valid
#     if not check_access_token(access_token):
#         return jsonify({'error': 'Authentication failed. Please check your credentials.'}), 401

#     # Fetch the playlist details using the Spotify API
#     playlist = fetch_playlist_details(access_token, playlist_id)

#     if playlist:
#         return jsonify(playlist)
#     else:
#         return jsonify({'error': 'Failed to fetch playlist details.'}), 500

# def fetch_playlist_details(access_token, playlist_id):
#     try:
#         sp = spotipy.Spotify(auth=access_token)
#         playlist = sp.playlist(playlist_id)
#         return playlist
#     except spotipy.exceptions.SpotifyException as e:
#         print("An error occurred while fetching playlist details.")
#         print("Error message:", e)
#         return None
        
def check_access_token(access_token):
    try:
        sp = spotipy.Spotify(auth=access_token)
        sp.user_playlists('me')  # Fetch user playlists using the access token
        return True
    except spotipy.exceptions.SpotifyException as e:
        print("An error occurred while checking the access token.")
        print("Error message:", e)
        return False
    
def fetch_artists_from_spotify(token, genres):
    sp = spotipy.Spotify(auth=token)
    artists = []

    try:
        # Convert the set of genres to a comma-separated string
        seed_genres = ",".join(list(genres))

        # Get recommended tracks based on the selected genres
        recommended_tracks = sp.recommendations(seed_genres=seed_genres, limit=5)['tracks']

        # Extract artists from the recommended tracks
        for track in recommended_tracks:
            artist_name = track['artists'][0]['name']
            artist_id = track['artists'][0]['id']
            artists.append((artist_name, artist_id))
            print(f"Artist '{artist_name}' found in recommended tracks.")
    except spotipy.SpotifyException as e:
        print("An error occurred while fetching artists from Spotify.")
        print("Error message:", e)

    print(artists)
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

def generate_spotify_playlist(access_token, mood, adjectives, playlist_name):

    sp = spotipy.Spotify(auth=access_token)

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

    scope = 'playlist-modify-public'

    # Fetching recommendations with the selected genres
    try:

        recommendations = sp.recommendations(seed_genres=selected_genres, limit=5)
        if not recommendations:
            print("No recommendations found.")
            return None

        # Extracting artist ids from recommendations
        artist_ids = []
        for track in recommendations['tracks']:
            for artist in track['artists']:
                artist_ids.append(artist['id'])

        # Fetching artists' top tracks
        tracks = fetch_tracks_from_spotify(access_token, artist_ids)
        if not tracks:
            print("No tracks found.")
            return None

        print("Creating playlist...")
        playlist = create_playlist(access_token, playlist_name, tracks)
        if not playlist:
            print("Failed to create playlist.")
            return None

        print("Playlist created successfully!")
        return playlist


    except spotipy.exceptions.SpotifyException as e:
        print("An error occurred while fetching recommendations from Spotify.")
        print("Error message:", e)
        return None

if __name__ == '__main__':
    app.run(debug=True, port=5555)
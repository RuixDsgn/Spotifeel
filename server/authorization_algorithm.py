import os
from flask import Flask, request, make_response, session, jsonify, url_for, redirect
from flask_migrate import Migrate
from sqlalchemy import func
from requests import get, post
from dotenv import load_dotenv
import base64
from flask import request
from flask_restful import Resource
from config import app, db, api
import json
import spotipy
from  spotipy.oauth2 import SpotifyOAuth
import time

# O.AUTH2
TOKEN_INFO = 'token_info'

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id,
        client_secret,
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-library-read'
    )

@app.route('/')
def home():
    return 'spotifeel'

@app.route('/spotify-login') 
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

# @app.route('/createPlaylist')
# def createPlaylist():
#     try:
#         token_info = get_user_token()
#     except:
#         print('user not logged in')
#         return redirect(url_for('login', _external=True))

#     sp = spotipy.Spotify(auth=token_info['access_token'])
#     return sp.crurrent_user_saved_tracks(limit=50, offset=0)

def get_user_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception()
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


# WEB_APP TOKEN
load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')


def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = result.json()
    token = json_result['access_token']
    return token

token = get_token()


# MOOD_GENRE MAPPING ALGORITHM
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

def generate_playlist(token, mood, adjectives, playlist_name):
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

# Example usage:
selected_mood = "happy"
selected_adjectives = ["Excited", "Joyful", "Energetic"]
playlist_name = "My Awesome Playlist"
generate_playlist(token, selected_mood, selected_adjectives, playlist_name)

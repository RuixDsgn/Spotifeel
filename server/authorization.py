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

TOKEN_INFO = 'token_info'



load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

# self token access auth
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
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

token = get_token()

# auth header for any api requests
def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}



@app.route('/spotify') 
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# @app.route('/redirect')
# def redirectPage():
#     sp_oauth = create_spotify_oauth()
#     session.clear()
#     code = request.args.get('code')
#     token_info = sp_oauth.get_access_token(code)
#     session[TOKEN_INFO] = token_info
#     return redirect(url_for('getTracks', _external=True))

# @app.route('/getTracks')
# def getTracks():
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
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

# initial o.oath
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id,
        client_secret,
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-library-read'
    )

# self token access auth
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
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

token = get_token()

# auth header for any api requests
def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}

# get req to search for artist
def search_for_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    
    if len(json_result) == 0:
        # print('This artist does not exist.')
        return None
    
    return json_result[0]


# get artists based on a genre
def get_artists_by_genre():
    sp = spotipy.Spotify(auth=token)
    genre = 'pop'
    results = sp.search(q=f'genre:{genre}', type='artist', limit=10)

    artists = [artist['name'] for artist in results['artists']['items']]
    artists_id = [artist['id'] for artist in results['artists']['items']]

    print ('Pop:', artists, artists_id)

# get_artists_by_genre()


# MOOD_GENRE MAPPING ALGORITHM

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

adjective_values = {
            "Excited": 8,
            "Joyful": 7,
            "Energetic": 6,
            "Content": 5,
            "Optimistic": 7,
            "Playful": 6,
            "Grateful": 5,
            "Amused": 7,
            "Carefree": 6,

            "Melancholic": 8,
            "Gloomy": 7,
            "Heartbroken": 6,
            "Lonely": 5,
            "Despairing": 7,
            "Mournful": 6,
            "Sorrowful": 5,
            "Depressed": 7,
            "Regretful": 6,

            "Furious": 8,
            "Irritated": 7,
            "Enraged": 6,
            "Annoyed": 5,
            "Hostile": 7,
            "Frustrated": 6,
            "Resentful": 5,
            "Livid": 7,
            "Agitated": 6,

            "Terrified": 8,
            "Anxious": 7,
            "Panicked": 6,
            "Nervous": 5,
            "Apprehensive": 7,
            "Startled": 6,
            "Timid": 5,
            "Dreadful": 7,
            "Jittery": 6
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


def select_genres_and_artists(mood, adjectives):
        if mood not in ["happy", "sad", "angry", "fearful"]:
            return None, None

        if len(adjectives) != 3:
            return None, None

        # Gets the adjectives and their numerical values associated with the selected mood
        mood_info = mood_adjectives.get(mood)
        if not mood_info:
            return None, None

        selected_adjectives = mood_info["adjectives"]
        adjective_values = mood_info["numerical_values"]

        # Use the adjective-genre mapping to fetch genres based on the adjectives' numerical values
        selected_genres = set()
        for adjective, value in zip(selected_adjectives, adjective_values):
            if adjective in adjectives:
                selected_genres.update(adjective_genre_mapping.get(adjective, []))

        # Fetch artists based on the selected genres from the Spotify Web API
        selected_artists = fetch_artists_from_spotify(selected_genres)

        return list(selected_genres), selected_artists

def get_adjective_value( adjective):
        return adjective_values.get(adjective, 0)

def fetch_artists_from_spotify():
        sp = spotipy.Spotify(auth=token)
        genre = 'pop'
        results = sp.search(q=f'genre:{genre}', type='artist', limit=10)

        artists = [artist['name'] for artist in results['artists']['items']]
        artists_id = [artist['id'] for artist in results['artists']['items']]

        print ('Pop:', artists, artists_id)

fetch_artists_from_spotify()




# # get req to search for songs by artist_id
# def get_songs_by_artist(token, artist_id):
#     url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)['tracks']
#     return json_result


# result = search_for_artist(token, "Madeon")
# artist_id = result['id']
# artist_genre = result['genres']
# songs = get_songs_by_artist(token, artist_id)

# print(artist_genre)

# for idx, song in enumerate(songs):
#     print(f"{idx + 1}. {song['name']}")


# # get req for one track
# def get_one_song(token, track_id):
#     url = f'https://api.spotify.com/v1/tracks/{track_id}'
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)
#     return json_result

# song = get_one_song(token, '5Gggw8WykNhnZsYExUVYxy?si=f39b2f2a54434c55' )
# # print(song)

# # get req to show genres
# def get_genres(token):
#     url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)
#     return json_result

# genres = get_genres(token)

# # for index, genre in enumerate(genres['genres']):
# #     print(f'{index + 1}. {genre}')



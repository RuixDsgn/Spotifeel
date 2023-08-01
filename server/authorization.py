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
        print('This artist does not exist.')
        return None
    
    return json_result[0]


# get req to search for songs by artist_id
def get_songs_by_artist(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result


result = search_for_artist(token, "Madeon")
artist_id = result['id']
artist_genre = result['genres']
songs = get_songs_by_artist(token, artist_id)

print(artist_genre)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")


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



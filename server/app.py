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
from models import User, Questionnaire, Mood, Playlist
import json
import spotipy
from  spotipy.oauth2 import SpotifyOAuth

@app.route('/') 
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    return 'redirect'

# token access auth and o.auth2
load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id,
        client_secret,
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-library-read'
    )

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

# print(artist_genre)

# for idx, song in enumerate(songs):
#     print(f"{idx + 1}. {song['name']}")


# get req for one track
def get_one_song(token, track_id):
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

song = get_one_song(token, '5Gggw8WykNhnZsYExUVYxy?si=f39b2f2a54434c55' )
# print(song)

# get req to show genres
def get_genres(token):
    url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

genres = get_genres(token)

# for index, genre in enumerate(genres['genres']):
#     print(f'{index + 1}. {genre}')



# API Routes
class Songs(Resource):
    def get(self):
        return songs

api.add_resource(Songs, '/song')

class Artist(Resource):
    def get(self):
        return result
    
api.add_resource(Artist, '/artist')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

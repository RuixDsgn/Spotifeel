#!/usr/bin/env python3

# Standard library imports
import os
from flask import Flask, request, make_response, session, jsonify
from flask_migrate import Migrate
from sqlalchemy import func
from requests import get

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import User, Questionnaire, Mood, Playlist

class Songs(Resource):
    def get(self):
        bearer_token = 'BQCZ6Tb9J2i7BcKPWT8a8IdLNaT-mcLJDdJsvq1rKZY6zYnyS4xt8t60fzFts_TVMue4g2ju-wY0S1EDli_sOMNUwFUxTkdyyk2DtluUEBHVQGTtItQ'
        response = get('https://api.spotify.com/v1/tracks/5Tlwkpy7AU3yMXydeFwhCp?si=d6a8dc7941524d56',
                    {'headers': {'Authorization': f'Bearer {bearer_token}'}})
        return response.json()

api.add_resource(Songs, '/song')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

from config import app, db, api
from models import Questionnaire1, Questionnaire2, UserEmotion, UserAdjective1, UserAdjective2, UserAdjective3, Genre1, Genre2, Genre3
from flask_migrate import Migrate
from sqlalchemy import func
from flask import Flask, request, make_response, session, jsonify
from flask_restful import Resource
from config import app, db, api

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

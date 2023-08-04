from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from config import db
import config

class Questionnaire1(db.Model, SerializerMixin):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String)
    emotion_id = db.Column(db.Integer, db.ForeignKey('user_emotion.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserEmotion(db.Model, SerializerMixin):
    __tablename__ = 'user_emotion'
    id = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the one-to-many relationship between UserEmotion and Questionnaire1
    questionnaires = db.relationship('Questionnaire1', backref='user_emotion', lazy=True)

class Questionnaire2(db.Model, SerializerMixin):
    __tablename__ = 'question_2'
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String)
    adjective_1_id = db.Column(db.Integer, db.ForeignKey('user_adjective_1.id'))
    adjective_2_id = db.Column(db.Integer, db.ForeignKey('user_adjective_2.id'))
    adjective_3_id = db.Column(db.Integer, db.ForeignKey('user_adjective_3.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAdjective1(db.Model, SerializerMixin):
    __tablename__ = 'user_adjective_1'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    emotion_id = db.Column(db.Integer, db.ForeignKey('user_emotion.id'))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('question_2.id'))
    meter = db.Column(db.Integer)

class UserAdjective2(db.Model, SerializerMixin):
    __tablename__ = 'user_adjective_2'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    emotion_id = db.Column(db.Integer, db.ForeignKey('user_emotion.id'))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('question_2.id'))
    meter = db.Column(db.Integer)

class UserAdjective3(db.Model, SerializerMixin):
    __tablename__ = 'user_adjective_3'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    emotion_id = db.Column(db.Integer, db.ForeignKey('user_emotion.id'))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('question_2.id'))
    meter = db.Column(db.Integer)

class Genre1(db.Model, SerializerMixin):
    __tablename__ = 'genre_1'
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String) 
    meter = db.Column(db.Integer, db.ForeignKey('user_adjective_1.meter'))

class Genre2(db.Model, SerializerMixin):
    __tablename__ = 'genre_2'
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String) 
    meter = db.Column(db.Integer, db.ForeignKey('user_adjective_2.meter'))

class Genre3(db.Model, SerializerMixin):
    __tablename__ = 'genre_3'
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String) 
    meter = db.Column(db.Integer, db.ForeignKey('user_adjective_3.meter'))

class Playlist(db.Model, SerializerMixin):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    emotion_id = db.Column(db.Integer, db.ForeignKey('user_emotion.id'))
    adjective_1_name = db.Column(db.String, db.ForeignKey('user_adjective_1.name'))
    adjective_2_name = db.Column(db.String, db.ForeignKey('user_adjective_2.name'))
    adjective_3_name = db.Column(db.String, db.ForeignKey('user_adjective_3.name'))
    genre_1_name = db.Column(db.String, db.ForeignKey('genre_1.genre'))
    genre_2_name = db.Column(db.String, db.ForeignKey('genre_2.genre'))
    genre_3_name = db.Column(db.String, db.ForeignKey('genre_3.genre'))

    # Define the many-to-one relationships between Playlist and other tables
    emotion = db.relationship('UserEmotion', backref='playlists', lazy=True)
    adjective_1 = db.relationship('UserAdjective1', backref='playlists', lazy=True, foreign_keys=[adjective_1_name])
    adjective_2 = db.relationship('UserAdjective2', backref='playlists', lazy=True, foreign_keys=[adjective_2_name])
    adjective_3 = db.relationship('UserAdjective3', backref='playlists', lazy=True, foreign_keys=[adjective_3_name])
    genre_1 = db.relationship('Genre1', backref='playlists', lazy=True, foreign_keys=[genre_1_name])
    genre_2 = db.relationship('Genre2', backref='playlists', lazy=True, foreign_keys=[genre_2_name])
    genre_3 = db.relationship('Genre3', backref='playlists', lazy=True, foreign_keys=[genre_3_name])

class Record(db.Model, SerializerMixin):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    questionnaire_1 = db.Column(db.Integer, db.ForeignKey('question.id'))
    emotion_id = db.Column(db.Integer, db.ForeignKey('user_emotion.id'))
    questionnaire_2 = db.Column(db.Integer, db.ForeignKey('question_2.id'))
    adjective_1_id = db.Column(db.Integer, db.ForeignKey('user_adjective_1.id'))
    adjective_2_id = db.Column(db.Integer, db.ForeignKey('user_adjective_2.id'))
    adjective_3_id = db.Column(db.Integer, db.ForeignKey('user_adjective_3.id'))
    genre_1_id = db.Column(db.Integer, db.ForeignKey('genre_1.id'))
    genre_2_id = db.Column(db.Integer, db.ForeignKey('genre_2.id'))
    genre_3_id = db.Column(db.Integer, db.ForeignKey('genre_3.id'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    questionnaire = db.Column(db.Integer, db.ForeignKey('questions.id'))
    mood = db.Column(db.Integer, db.ForeignKey('moods.id'))
    playlist = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Questionnaire(db.Model, SerializerMixin):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question = db.Column(db.String)
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Mood(db.Model, SerializerMixin):
    __tablename__ = 'moods'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mood = db.Column(db.String)


class Playlist(db.Model, SerializerMixin):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

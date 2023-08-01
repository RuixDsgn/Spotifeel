from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from config import db

class Questionnaire1(db.Model, SerializerMixin):
    __tablename__ = 'questions-1'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    emotion_id = db.Column(db.Integer, db.ForeignKey('user-emotions.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserEmotion(db.Model, SerializerMixin):
    __tablename__ = 'user-emotions'
    id = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questions-1.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Questionnaire2(db.Model, SerializerMixin):
    __tablename__ = 'questions-2'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    adjective_id_1 = db.Column(db.Integer, db.ForeignKey('user-emotion-adjectives-1.id'))
    adjective_id_2 = db.Column(db.Integer, db.ForeignKey('user-emotion-adjectives-2.id'))
    adjective_id_3 = db.Column(db.Integer, db.ForeignKey('user-emotion-adjectives-3.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAdjective1(db.Model, SerializerMixin):
    __tablename__ = 'user-emotion-adjectives-1'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    emotion_id = db.Column(db.Integer, db.ForeignKey('user-emotions.id'))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questions-2.id'))
    meter = db.Column(db.Integer)

class UserAdjective2(db.Model, SerializerMixin):
    __tablename__ = 'user-emotion-adjectives-2'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    emotion_id = db.Column(db.Integer, db.ForeignKey('user-emotions.id'))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questions-2.id'))
    meter = db.Column(db.Integer)

class UserAdjective3(db.Model, SerializerMixin):
    __tablename__ = 'user-emotion-adjectives-3'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    emotion_id = db.Column(db.Integer, db.ForeignKey('user-emotions.id'))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questions-2.id'))
    meter = db.Column(db.Integer)

class Genre1(db.Model, SerializerMixin):
    __tablename__ = 'genres-1'
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String) 
    meter = db.Column(db.Integer, db.ForeignKey('user-emotion-adjectives-1.meter'))

class Genre2(db.Model, SerializerMixin):
    __tablename__ = 'genres-2'
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String) 
    meter = db.Column(db.Integer, db.ForeignKey('user-emotion-adjectives-2.meter'))

class Genre3(db.Model, SerializerMixin):
    __tablename__ = 'genres-3'
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String) 
    meter = db.Column(db.Integer, db.ForeignKey('user-emotion-adjectives-3.meter'))

class Record(db.Model, SerializerMixin):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    questionnaire_1 = db.Column(db.Integer, db.ForeignKey('questions-1.id'))
    emotion_id = db.Column(db.Integer, db.ForeignKey('user-emotions.id'))
    questionnaire_2 = db.Column(db.Integer, db.ForeignKey('questions-2.id'))
    adjective_1_id = db.Column(db.Integer, db.ForeignKey('user-emotion-adjectives-1.id'))
    adjective_2_id = db.Column(db.Integer, db.ForeignKey('user-emotion-adjectives-2.id'))
    adjective_3_id = db.Column(db.Integer, db.ForeignKey('user-emotion-adjectives-3.id'))
    genre_1_id = db.Column(db.Integer, db.ForeignKey('genres-1.id'))
    genre_2_id = db.Column(db.Integer, db.ForeignKey('genres-2.id'))
    genre_3_id = db.Column(db.Integer, db.ForeignKey('genres-3.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


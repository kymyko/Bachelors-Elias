from flask_login import UserMixin
from sqlalchemy import JSON

from app import db
from datetime import datetime, timezone


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(255), default='No address provided')
    password_hash = db.Column(db.Text, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    account_status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    articles = db.relationship('Articles', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='user', lazy=True)
    ratings = db.relationship('Ratings', backref='user', lazy=True)
    appointments = db.relationship('Appointments', backref='user', lazy=True)
    chats = db.relationship('Chats', backref='user', lazy=True)
    psychologist = db.relationship('Psychologists', backref='user', uselist=False)


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    comments = db.relationship('Comments', backref='article', lazy=True)
    ratings = db.relationship('Ratings', backref='article', lazy=True)


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Ratings(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)


class Psychologists(db.Model):
    __tablename__ = 'psychologists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    location = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    working_hours = db.Column(db.JSON, nullable=False, default={})  # Store working hours as JSON

    def __repr__(self):
        return f'<Psychologist {self.user_id}>'


class Appointments(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    psychologist_id = db.Column(db.Integer, db.ForeignKey('psychologists.id'), nullable=False)
    appointment_time = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Chats(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chat_log = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'chat_log': self.chat_log,
            'created_at': self.created_at.isoformat()
        }

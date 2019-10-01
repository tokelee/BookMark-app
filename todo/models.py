from sqlalchemy import desc, asc, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from todo import db, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Bookmark(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    url=db.Column(db.Text, nullable=False)
    date=db.Column(db.DateTime, default=datetime.utcnow)
    description=db.Column(db.String(300))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    #the many side get the foreign key

    @staticmethod
    def newest():
        return Bookmark.query.order_by(desc(Bookmark.date))

    def __str__(self):
        return f'<Bookmark {self.description}:{self.url}'



class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True)
    email=db.Column(db.String(120),unique=True)
    bookmarks=db.relationship('Bookmark',backref='user',lazy='dynamic')
    password_hash=db.Column(db.String(300))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.secret_key, expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @property
    def password(self):
        raise AttributeError('password: write only-field')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()
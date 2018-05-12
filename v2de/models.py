import hashlib
from . import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    nodes = db.relationship('Node',backref='tag',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'))
    posts = db.relationship('Post',backref='node',lazy='dynamic')

    def __repr__(self):
        return '<Node %r>' % self.name


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    repies = db.Column(db.Integer,default=0)
    chick = db.Column(db.Integer,default=0)
    node_id = db.Column(db.Integer,db.ForeignKey('nodes.id'))
    publish_time = db.Column(db.DateTime,default=datetime.now())
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True,index=True)
    avatar = db.Column(db.String(64))
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    avatar_hash = db.Column(db.String(64))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def gravatar(self, size=100, default='monsterid', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        if self.avatar_hash:
            hash = self.avatar_hash
        else:
            hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
            self.avatar_hash = hash
            db.session.add(self)
            db.session.commit()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)


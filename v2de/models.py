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
    def collection(self,user):
        return CollecTag.query.filter_by(tag_id=self.id,user_id=user.id).first()
class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'))
    posts = db.relationship('Post',backref='node',lazy='dynamic')
    header = db.Column(db.String(128))
    avatar = db.Column(db.String(64))
    users = db.relationship('CollectNode',backref='node',lazy='dynamic')

    def __repr__(self):
        return '<Node %r>' % self.name
    def collection(self,user):
        if not user.is_authenticated:
            return False
        return CollectNode.query.filter_by(node_id=self.id,user_id=user.id).first()

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
    comments = db.relationship('Comment',backref='posts',lazy='dynamic')

    def chicking(self):
        self.chick = self.chick + 1
        db.session.add(self)
        db.session.commit()

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    publish_time = db.Column(db.DateTime,default=datetime.now())
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True,index=True)
    avatar = db.Column(db.String(64))
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    avatar_hash = db.Column(db.String(64))
    comments = db.relationship('Comment',backref='author',lazy='dynamic')
    collectnodes = db.relationship('CollectNode',backref='users',lazy='dynamic')
    collectags = db.relationship('CollecTag',backref='users',lazy='dynamic')


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

class CollectNode(db.Model):
    __tablename__ = 'collactnode'
    id = db.Column(db.Integer,primary_key=True)
    node_id = db.Column(db.Integer,db.ForeignKey('nodes.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    time = db.Column(db.DateTime,default=datetime.now())


class CollecTag(db.Model):
    __tablename__ = 'collactag'
    id = db.Column(db.Integer,primary_key=True)
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    time = db.Column(db.DateTime,default=datetime.now())


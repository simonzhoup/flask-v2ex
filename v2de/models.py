from . import db

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    nodes = db.relationship('Node',backref='tag')

    def __repr__(self):
        return '<Role %r>' % self.name

class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'))

    def __repr__(self):
        return '<Node %r>' % self.name

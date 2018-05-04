from . import main
from flask import render_template,request
from ..models import Tag,Node, Post


@main.route('/')
def index():
    tag_list = [t.name for t in Tag.query.order_by(Tag.id)]
    tag = request.args.get('tag','技术')
    t = Tag.query.filter_by(name=tag).first()
    posts = Post.query.join(Node,Node.id==Post.node_id).filter(Node.tag_id==t.id).all()
    return render_template('index.html',tag_list=tag_list,node_list=t.nodes,tag=tag,posts=posts)
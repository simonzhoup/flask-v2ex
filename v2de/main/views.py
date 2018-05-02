from . import main
from flask import render_template,request
from ..models import Tag,Node

@main.route('/')
def index():
    tag_list = [t.name for t in Tag.query.all()]
    tag = request.args.get('tag','')
    if tag:
        node_list = Tag.query.filter_by(name=tag).first().nodes
    else:
        node_list = Tag.query.filter_by(id=1).first().nodes
    return render_template('index.html',tag_list=tag_list,node_list=node_list,tag=tag)
from . import main
from flask import render_template,request,url_for,redirect,flash,make_response,jsonify
from ..models import Tag,Node, Post,User,Comment,CollecTag,CollectNode
from .forms import RegisterForm,LoginForm
from .. import db
from flask_login import login_user,login_required,logout_user,current_user
from datetime import datetime
from markdown import markdown
import bleach
import json

def sort_post(post):
    for p in post:
        return p.comments.count()

@main.route('/')
def index():
    tag_list = [t.name for t in Tag.query.order_by(Tag.id)]
    tag = request.args.get('tag','')
    t = Tag.query.filter_by(name=tag).first()
    if tag and tag != request.cookies.get('tag',''):
        return index_cookie(tag)
    else:
        tag = request.cookies.get('tag','技术')
    t = Tag.query.filter_by(name=tag).first()
    hot_posts = [p for p in Post.query.all() if (datetime.now() - p.publish_time).days == 0]
    hot_posts.sort(key=lambda x: x.comments.count(), reverse=True)
    if tag == '最热':
        posts = hot_posts
    elif tag == '全部':
        posts = Post.query.all()[::-1]
        # hot_posts = [p for p in Post.query.all() if (datetime.now()-p.publish_time).days == 0]
        posts.sort(key=lambda x: x.comments.count())
    else:
        posts = Post.query.join(Node,Node.id==Post.node_id).filter(Node.tag_id==t.id).order_by(Post.publish_time.desc()).all()
        posts.sort(key=lambda x: x.comments.count())
    return render_template('index.html',tag_list=tag_list,node_list=t.nodes,tag=tag,posts=posts[:10],hot_posts=hot_posts)

def index_cookie(tag):
    resp = make_response(redirect(url_for('main.index',tag=tag)))
    resp.set_cookie('tag',tag,max_age=24*60*60)
    return resp

@main.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('user_register.html',form=form)

@main.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名/密码错误')
    return render_template('user_login.html',form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/member/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html',user=user)

@main.route('/go/<name>',methods=['POST','GET'])
def node(name):
    node = Node.query.filter_by(name=name).first()
    if request.method == 'POST':
        file = request.files.get('avatar','')
        if file:
            file.save('v2de/static/img/node/%s.jpg' % node.name)
            node.avatar = '%s.jpg' %node.name
        header = request.form.get('header','')
        if header:
            node.header = header
        db.session.add(node)
        db.session.commit()
        return redirect(url_for('main.node',name=node.name))
    page = request.args.get('page', 1, type=int)
    pageination =Post.query.filter_by(node_id=node.id).order_by(Post.publish_time.desc()).paginate(page, per_page=10,error_out=False)
    posts = pageination.items
    endpoint = 'main.node'
    return render_template('node.html',node=node,posts=posts,pageination=pageination,endpoint=endpoint)

def content_clean(c):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc']
    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'p','img','figure']
    content = bleach.linkify(bleach.clean(
        markdown(c, output_format='html5',extensions=exts),
        tags=allowed_tags, strip=True))
    return content

def title_clean(t):
    allowed_tags = []
    title = bleach.linkify(bleach.clean(
        markdown(t, output_format='html'),
        tags=allowed_tags, strip=True))
    return title


@main.route('/p/<int:id>',methods=['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        content = request.form.get('comment-content','')
        if not content:
            pass
        comment = Comment(user_id=current_user.id,post_id=post.id,content=content_clean(content))
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.post',id=post.id))
    post.chicking()
    comments = post.comments.all()
    last_comment = post.comments.order_by(Comment.publish_time.desc()).first()
    return render_template('post.html',post=post,comments=comments,last_comment=last_comment)


@main.route('/collect/node/')
@login_required
def collect_node():
    node_id = request.args.get('node_id','')
    if node_id:
        node = Node.query.filter_by(id=node_id).first()
        if node:
            c = CollectNode.query.filter_by(node_id=node_id,user_id=current_user.id).first()
            if c:
                db.session.delete(c)
                db.session.commit()
                return '加入收藏'
            else:
                c =CollectNode(node_id=node.id,user_id=current_user.id)
                db.session.add(c)
                db.session.commit()
                return '取消收藏'
    return '加入收藏'


@main.route('/new',methods=['GET','POST'])
@login_required
def new_post():
    nodes = Node.query.all()
    hot_nodes = sorted(nodes,key=lambda x: x.posts.count(),reverse=True)[:15]
    if request.method == 'POST':
        title =request.form.get('title')
        content = request.form.get('content')
        node_id = request.form.get('node_id')
        p = Post(title=title_clean(title),content=content_clean(content),node_id=int(node_id),author_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        return jsonify({'result':'ok'})
    return render_template('new_post.html',nodes=nodes,hot_nodes=hot_nodes)

@main.route('/view/post')
@login_required
def view_post():
    content = request.args.get('content','')
    return content_clean(content)
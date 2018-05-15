from . import main
from flask import render_template,request,url_for,redirect,flash,make_response
from ..models import Tag,Node, Post,User,Comment
from .forms import RegisterForm,LoginForm
from .. import db
from flask_login import login_user,login_required,logout_user,current_user

from markdown import markdown
import bleach

@main.route('/')
def index():
    tag_list = [t.name for t in Tag.query.order_by(Tag.id)]
    tag = request.args.get('tag','')
    if tag and tag != request.cookies.get('tag',''):
        return index_cookie(tag)
    else:
        tag = request.cookies.get('tag','技术')
    t = Tag.query.filter_by(name=tag).first()
    posts = Post.query.join(Node,Node.id==Post.node_id).filter(Node.tag_id==t.id).order_by(Post.publish_time.desc()).all()
    return render_template('index.html',tag_list=tag_list,node_list=t.nodes,tag=tag,posts=posts)

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
    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'p','img']
    content = bleach.linkify(bleach.clean(
        markdown(c, output_format='html'),
        tags=allowed_tags, strip=True))
    return content


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
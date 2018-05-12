from . import main
from flask import render_template,request,url_for,redirect,flash
from ..models import Tag,Node, Post,User
from .forms import RegisterForm,LoginForm
from .. import db
from flask_login import login_user,login_required,logout_user,current_user

@main.route('/')
def index():
    tag_list = [t.name for t in Tag.query.order_by(Tag.id)]
    tag = request.args.get('tag','技术')
    t = Tag.query.filter_by(name=tag).first()
    posts = Post.query.join(Node,Node.id==Post.node_id).filter(Node.tag_id==t.id).all()
    return render_template('index.html',tag_list=tag_list,node_list=t.nodes,tag=tag,posts=posts)

@main.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return render_template(url_for('main.index'))
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
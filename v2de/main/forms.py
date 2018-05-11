from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SelectField,SubmitField,ValidationError
from wtforms.validators import Email,Length,Regexp,EqualTo
from ..models import User

class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, numbers, dots or underscores')])
    email = StringField('邮箱',validators=[Length(1,64),Email()])
    password = PasswordField('密码',validators=[EqualTo('password2',message='密码不一致')])
    password2 = PasswordField('重复密码')
    submit = SubmitField('提交')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已被使用')

    def validate_username(self,filed):
        if User.query.filter_by(username=filed.data).first():
            raise ValidationError('重复用户名')




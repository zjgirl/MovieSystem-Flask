
# use wtf web, use wtf.quick_form() to render template
# no need to define form in the html

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('用户名', validators = [DataRequired()])
    password = PasswordField('密码', validators = [DataRequired()])
    remember_me = BooleanField('记住我')

    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators = [DataRequired()])
    email = StringField('邮箱')
    password = PasswordField('密码', validators = [DataRequired(), EqualTo('password_confirm', message='密码必须一致！')])
    password_confirm = PasswordField('确认密码', validators = [DataRequired()])

    submit = SubmitField('注册')
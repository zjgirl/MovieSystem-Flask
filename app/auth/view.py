from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from . import auth
from .form import LoginForm, RegisterForm
from ..model import User


@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():   
        if User.query.filter_by(username=form.username.data).first():
            flash('该用户名已被注册！')
            return render_template('auth/register.html', form=form)
        User.addUser(form.username.data, form.password.data, form.email.data)
        flash('注册成功！')
        return redirect(url_for('auth.login'))   
    return render_template('auth/register.html', form=form)
            
@auth.route('/login', methods = ['GET', 'POST']) 
def login():
    form = LoginForm()
    if form.validate_on_submit(): # check post data and get can't go in
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data) #record the current user in session
            next = request.args.get('next') # if the login operation is mandatory, once login, go to that page directly
            if not next:
                next = url_for('main.index')
            return redirect(next)
        flash('用户名或密码错误！')
    return render_template('auth/login.html', form=form)


@auth.route('/logout') 
@login_required
def logout():
    logout_user() #remove the record about the user
    flash('您已退出登录')
    return redirect(url_for('auth.login'))

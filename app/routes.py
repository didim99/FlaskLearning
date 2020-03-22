# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.forms import AuthForm
from app.models import User
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth'))
    return render_template('index.html', title="Система шифрования RSA")


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AuthForm()

    if form.validate_on_submit():
        user = User.load_user(form.login.data)
        if user is None or not user.check_password(form.passw.data):
            flash('Invalid username or password')
            return redirect(url_for('auth'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('auth.html', title="Авторизация", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

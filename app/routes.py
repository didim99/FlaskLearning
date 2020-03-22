# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app.forms import ATTR_MANAGER, ATTR_ACTION
from app.forms import ACTION_GEN_KEY, ACTION_SET_KEY, ACTION_GO
from app.forms import AuthForm, KeyGenForm, KeySetForm
from app.models import User
from app import app
from encryption import CryptoManager
from encryption.rsa import RSAKey


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth'))

    if ATTR_MANAGER not in app.extensions:
       app.extensions[ATTR_MANAGER] = CryptoManager()
    manager = app.extensions[ATTR_MANAGER]

    action = None
    keygenform = KeyGenForm()
    keysetform = KeySetForm()
    if ATTR_ACTION in request.values:
        action = request.values[ATTR_ACTION]
    if manager.key:
        keysetform.keyE.data = manager.key.e
        keysetform.keyD.data = manager.key.d
        keysetform.keyN.data = manager.key.n

    if action == ACTION_GEN_KEY:
        if keygenform.validate_on_submit():
            manager.key = RSAKey.generate(keygenform.length.data)
            keysetform.keyE.data = manager.key.e
            keysetform.keyD.data = manager.key.d
            keysetform.keyN.data = manager.key.n
        if keygenform.length.errors:
            flash('Invalid key length', 'error')
    elif action == ACTION_SET_KEY:
        if keysetform.validate_on_submit():
            manager.key = RSAKey(keysetform.e.data, keysetform.d.data, keysetform.n.data)
        if keysetform.length.errors:
            flash('Invalid key parameters', 'error')
    elif action == ACTION_GO:
        pass

    return render_template('index.html', title="Система шифрования RSA", manager=manager,
                           keyGenForm=keygenform, keySetForm=keysetform)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AuthForm()

    if form.validate_on_submit():
        user = User.load_user(form.login.data)
        if user is None or not user.check_password(form.passw.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('auth.html', title="Авторизация", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

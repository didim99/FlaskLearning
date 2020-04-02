# -*- coding: utf-8 -*-
import json
from base64 import b64decode
from urllib.parse import urlencode
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app.forms import ATTR_MANAGER, ATTR_ACTION, ATTR_DATA
from app.forms import ACTION_GEN_KEY, ACTION_SET_KEY, ACTION_GO, ACTION_POST
from app.forms import AuthForm, KeyGenForm, KeySetForm, MessageForm
from app.models import User
from app import app
from vkapi import VKAPI
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
    messageform = MessageForm()
    if ATTR_ACTION in request.values:
        action = request.values[ATTR_ACTION]
    if not action == ACTION_POST:
        manager.clear()
    if manager.key:
        keysetform.keyE.data = manager.key.e
        keysetform.keyD.data = manager.key.d
        keysetform.keyN.data = manager.key.n
    if manager.message:
        messageform.message.data = manager.message

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
        if keysetform.keyE.errors or keysetform.keyD.errors or keysetform.keyN.errors:
            flash('Invalid key parameters', 'error')
    elif action == ACTION_GO:
        if messageform.validate_on_submit():
            message = messageform.message.data
            file = messageform.inFile.data

            if not manager.key:
                flash('Key not defined', 'error')
            elif not message and not file.filename:
                flash('Empty message', 'error')
            else:
                if message:
                    manager.message = message
                else:
                    manager.load_file(file)
                manager.process()
    elif action == ACTION_POST:
        flash('Запись на стену отправлена', 'info')

    return render_template('index.html', title="Система шифрования RSA",
                           manager=manager, keyGenForm=keygenform,
                           keySetForm=keysetform, messageForm=messageform)


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

    vkapi = urlencode(app.config['VKAPI'])
    return render_template('auth.html', title="Авторизация",
                           form=form, vkapi=vkapi)


@app.route('/vkauth')
def vkauth():
    if ATTR_DATA in request.values:
        data = json.loads(b64decode(request.values[ATTR_DATA]))
        if VKAPI.KEY_TOKEN in data:
            try:
                user = User(data)
                login_user(user)
            except IOError as e:
                flash(e, 'error')
            return redirect(url_for('index'))
        elif VKAPI.KEY_ERR_DESC in data:
            flash(data[VKAPI.KEY_ERR_DESC], 'error')
    return redirect(url_for('auth'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

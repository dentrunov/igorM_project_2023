from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from urllib.parse import urlsplit

from .forms import AuthForm, RegistrationForm
from app import app, db
from .models import User, Pupils


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/enter', methods=['GET', 'POST'])
def enter():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AuthForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.pasw.data):
            flash('Invalid username or password')
            return redirect(url_for('enter'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('enter.html', title='Вход', form=form)

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляю, пользователь зарегистрирован')
        return redirect(url_for('enter'))
    return render_template('reg.html', title="Регистрация пользователя", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/check')
@login_required
def check():
    return 'third_page'
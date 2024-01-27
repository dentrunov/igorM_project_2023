from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from urllib.parse import urlsplit

from datetime import datetime as dt

from .forms import AuthForm, RegistrationForm, CreatePupilsForm, CreateCodesForm, CreateTGIDForm
from app import app, db
from .models import User, Pupils, NewUsers
from .data import generate_pupils, generate_codes


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

@app.route('/check', methods=['GET', 'POST'])
@login_required
def check():
    gen_pupils_form = CreatePupilsForm()
    codes_form = CreateCodesForm()
    pupils_list = Pupils.query.all()
    q = len(pupils_list)
    tg_forms = [CreateTGIDForm() for i in range(q)]
    if codes_form.submit_code.data and codes_form.validate_on_submit():
        
        codes = generate_codes(q)
        for i in range(q):
            pupils_list[i].last_generated_code = codes[i]
            pupils_list[i].last_generated_code_date = dt.now()
        db.session.commit()
        return redirect(url_for('check'))
    if gen_pupils_form.submit.data and gen_pupils_form.validate_on_submit():
        names = [Pupils(**row) for row in generate_pupils(gen_pupils_form.count.data)]
        db.session.add_all(names)
        db.session.commit()
        flash('Список создан')
        return redirect(url_for('check'))
    if CreateTGIDForm().tgid_submit.data and CreateTGIDForm().validate_on_submit():
        pupil_id = request.form["tg_hidden"]
        update_pupil = Pupils.query.filter_by(pupil_id=pupil_id).first()
        print(2)
        update_pupil.tg_id = request.form["tgid_input"]
        db.session.commit()
        return redirect(url_for('check'))
 
    
    # return render_template('check.html', title="Проверка", codes_form=codes_form, pupils_list=pupils_list)
    return render_template('check.html', title="Проверка", gen_pupils_form=gen_pupils_form, codes_form=codes_form, pupils_list=pupils_list, tg_forms=tg_forms)

@app.route('/new_users', methods=['GET', 'POST'])
@login_required
def new_users():
    new_users = NewUsers.query.all()
    return render_template('new_users.html', title="Новые пользователи", new_users=new_users)
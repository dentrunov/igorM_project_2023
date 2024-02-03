from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from urllib.parse import urlsplit

from datetime import datetime as dt

from .forms import *
from app import app, db
from .models import User, Pupils, NewUsers
from .data import generate_pupils, generate_codes

import pandas as pd
import os

ALLOWED_EXTENSIONS = ["xlsx", ]

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    """ главная страница """
    return render_template('index.html')

@app.route('/enter', methods=['GET', 'POST'])
def enter():
    """ функция входа пользователя """
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
    """ регистрация пользователя"""
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
    """ функция выхода пользователя """
    logout_user()
    return redirect(url_for('index'))

@app.route('/check', methods=['GET', 'POST'])
@login_required
def check():
    """ функция просмотра учеников """
    gen_pupils_form = CreatePupilsForm()
    codes_form = CreateCodesForm()
    add_pulils_form = AddPupilsFromFileForm()
    pupils_list = Pupils.query.all()
    all_list = []
    for pupil in pupils_list:
        new_pupil = {key:value for key, value in dict(pupil.__dict__).items()}
        if pupil.last_visit is not None:
            new_pupil["last_visit"] = pupil.last_visit.strftime("%d.%m.%Y %H:%M:%S")
        if pupil.out_time is not None:
            new_pupil["out_time"] = pupil.out_time.strftime("%d.%m.%Y %H:%M:%S")
        all_list.append(new_pupil)
    q = len(pupils_list)
    tg_forms = [CreateTGIDForm() for i in range(q)]
    ren_forms = [RenamePupilsForm() for i in range(q)]
    del_forms = [DeletePupilsForm() for i in range(q)]

    if codes_form.submit_code.data and codes_form.validate_on_submit():
        # запуск генерирования кодов для учеников
        codes = generate_codes(q)
        pupils_list_codes = Pupils.query.all()
        for i in range(q):
            pupils_list_codes[i].last_generated_code = codes[i]
            pupils_list_codes[i].last_generated_code_date = dt.now()
        db.session.commit()
        return redirect(url_for('check'))
    
    if gen_pupils_form.submit.data and gen_pupils_form.validate_on_submit():
        names = [Pupils(**row) for row in generate_pupils(gen_pupils_form.count.data)]
        db.session.add_all(names)
        db.session.commit()
        flash('Список создан')
        return redirect(url_for('check'))
    
    if add_pulils_form.addpupil_submit.data and add_pulils_form.validate_on_submit():
        print(request.files)
        if 'addpupil_file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        else:
            file = request.files['addpupil_file']
            if file.filename == '':
                flash('Нет выбранного файла')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                
                filename = file.filename
                file.save(filename)
                df= pd.read_excel(filename)
                mylist = df.to_dict()
                pupils = mylist["Фамилии"].values()
                names = [Pupils(pupil_name=pupil) for pupil in pupils]
                db.session.add_all(names)
                db.session.commit()
                os.remove(filename)
                flash('Список создан')
                return redirect(url_for('check'))

    
    if CreateTGIDForm().tgid_submit.data and CreateTGIDForm().validate_on_submit():
        # сохранение TG ID для ученика
        pupil_id = request.form["tg_hidden"]
        update_pupil = Pupils.query.filter_by(pupil_id=pupil_id).first()
        update_pupil.tg_id = request.form["tgid_input"]
        db.session.commit()
        return redirect(url_for('check'))
    
    if DeletePupilsForm().deletepupil_submit.data and DeletePupilsForm().validate_on_submit():
        # удаление ученика
        pupil_id = request.form["delete_hidden"]
        delete_pupil = Pupils.query.filter_by(pupil_id=pupil_id).first()
        db.session.delete(delete_pupil)
        db.session.commit()
        return redirect(url_for('check'))
    
    if RenamePupilsForm().renamepupil_submit.data and RenamePupilsForm().validate_on_submit():
        # удаление ученика
        pupil_id = request.form["rename_hidden"]
        rename_pupil = Pupils.query.filter_by(pupil_id=pupil_id).first()
        rename_pupil.pupil_name = request.form["rename"]
        db.session.commit()
        # return redirect(url_for('check'))
 
    return render_template('check.html', title="Проверка", 
                           gen_pupils_form=gen_pupils_form, 
                           codes_form=codes_form, 
                           pupils_list=all_list, 
                           tg_forms=tg_forms,
                           add_pulils_form=add_pulils_form,
                           ren_forms=ren_forms,
                           del_forms=del_forms,
                           )

@app.route('/new_users', methods=['GET', 'POST'])
@login_required
def new_users():
    """ функция просмотра новых пользователей бота"""
    new_users = NewUsers.query.all()
    for user in new_users:
        if user.new_user_datetime is not None:
            user.new_user_datetime = user.new_user_datetime.strftime("%d.%m.%Y %H:%M:%S")
    return render_template('new_users.html', title="Новые пользователи", new_users=new_users)
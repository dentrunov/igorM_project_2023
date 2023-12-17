from flask import Flask, render_template, request
from forms import AuthForm
from app import app

@app.route('/', methods=["POST", "GET"])
def hello_world():
    error = ''
    form = AuthForm()
    if form.is_submitted():
        username = request.form["username"]
        pasw = request.form["pass"]
        if username == "111" and pasw == '222':
            return render_template('success.html', name='Успешная авторизация')
        else:
            error = 'Неверные данные'
    return render_template('index.html', name='Главная страница', error=error, form=form)

@app.route('/second_page')
def second_page():
    return 'second_page'
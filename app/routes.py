from flask import render_template, request
from .forms import AuthForm
from app import app
from flask_login import login_required

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/enter')
def enter():
    return render_template('enter.html')

@app.route('/check')
@login_required
def check():
    return 'third_page'
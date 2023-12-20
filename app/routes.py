from flask import render_template, request
from .forms import AuthForm
from app import app

@app.route('/')
@app.route('/index')
def index():
    
    return render_template('index.html')

@app.route('/enter')
def enter():
    return 'second_page'

@app.route('/check')
def check():
    return 'third_page'
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """ Таблица БД пользователей сайта"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    tg_id = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Pupils(db.Model):
    """ Таблица БД учеников"""
    pupil_id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.BigInteger, index=True, default=0)
    pupil_name = db.Column(db.String(64), index=True)
    last_visit = db.Column(db.DateTime)
    last_generated_code = db.Column(db.String(64), index=True, default=0)
    last_generated_code_date = db.Column(db.DateTime)
    at_school = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Pupil {}>'.format(self.pupil_name)
    
class NewUsers(db.Model):
    """ Таблица новых пользователей бота для просмотра TG ID"""
    new_user_id = db.Column(db.Integer, primary_key=True)
    new_user_name = db.Column(db.String(64), index=True)
    new_user_tg_id = db.Column(db.Integer, index=True, unique=True)
    new_user_datetime = db.Column(db.DateTime)

    def __repr__(self):
        return '<NewUser {}>'.format(self.new_user_name)
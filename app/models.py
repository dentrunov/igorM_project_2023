from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
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
    pupil_id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.Integer, index=True, unique=True)
    pupil_name = db.Column(db.String(64), index=True, unique=True)
    last_visit = db.Column(db.DateTime)
    last_generated_code = db.Column(db.String(64), index=True, unique=True)
    last_generated_code_date = db.Column(db.DateTime)
    at_school = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Pupil {}>'.format(self.username)

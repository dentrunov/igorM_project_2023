from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tg_id = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username) 
    
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
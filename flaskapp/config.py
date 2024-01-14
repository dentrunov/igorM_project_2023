import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'a-08sgy-0ug-0sdf9ug=0sdfug=s0dfjs=0df9jhs[doifgjsdl;fk;sdlfhs;dfghs;dlkfghwpoieithg[owfe;lskdf'
    # SQLALCHEMY_DATABASE_URI = "postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev"
    # SQL_HOST=db
    # SQL_PORT=5432
    # DATABASE="hello_flask_dev"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
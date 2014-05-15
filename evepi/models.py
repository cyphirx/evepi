from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.Text, unique=True)
    pwdhash = db.Column(db.Text, unique=False)
    last_login = db.Column(db.DateTime, unique=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class APIs(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    keyID = db.Column(db.Integer, unique=True)
    vCode = db.Column(db.Text, unique=True)
    user_id = db.Column(db.Integer, unique=False)

class Character(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    characterID = db.Column(db.Integer, unique=True)

def initial_db():
    from flask import Flask
    from sqlalchemy import exists

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cache.db'
    db.init_app(app)
    with app.test_request_context():
        db.create_all(app=app)
        db.session.commit()


if __name__ == "__main__":
    initial_db()
    exit(0)

# vim: set ts=4 sw=4 et :
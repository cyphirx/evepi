from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Table(db.Model):
    Value1 = db.Column(db.Integer, unique=True, primary_key=True)
    Value2 = db.Column(db.Text, unique=False)


class APIs(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    keyID = db.Column(db.Integer, unique=True)
    vCode = db.Column(db.Text, unique=True)

class character(db.Model):
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
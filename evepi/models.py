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


class SkillPack(db.Model):
    __tablename__ = "pack_main"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, unique=True)
    filename = db.Column(db.Text, unique=False)
    status = db.Column(db.Boolean)



class SkillAttr(db.Model):
    __tablename__ = "pack_attr"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    pack_id = db.Column(db.Integer, unique=False)
    skill_id = db.Column(db.Integer, unique=False)
    skill_name = db.Column(db.Text, unique=False)
    priority = db.Column(db.Integer, unique=False)
    value = db.Column(db.Integer, unique=False)


class Api(db.Model):
    __tablename__ = "char_api"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    keyID = db.Column(db.Integer, unique=True)
    vCode = db.Column(db.Text, unique=True)
    keyType = db.Column(db.Text)
    accessMask = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    last_checked = db.Column(db.DateTime)

class Character(db.Model):
    __tablename__ = "char_main"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    api_id = db.Column(db.Integer)
    characterID = db.Column(db.Integer)
    characterName = db.Column(db.Text)
    corpID = db.Column(db.Integer)
    corporationName = db.Column(db.Text)
    allianceID = db.Column(db.Integer)
    allianceName = db.Column(db.Text)
    cloneSP = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    charisma = db.Column(db.Integer)
    perception = db.Column(db.Integer)
    willpower = db.Column(db.Integer)

    last_checked = db.Column(db.Integer)


class CharacterSkills(db.Model):
    __tablename__ = "char_skills"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    characterID = db.Column(db.Integer, unique=False)
    skillID = db.Column(db.Integer, unique=False)
    skillpoints = db.Column(db.Integer, unique=False)
    level = db.Column(db.Integer, unique=False)


class SkillRef(db.Model):
    __tablename__ = 'ref_skills'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    skillID = db.Column(db.Integer, unique=True)
    skillName = db.Column(db.Text)
    groupID = db.Column(db.Integer)
    rank = db.Column(db.Float)


class SkillGroup(db.Model):
    __tablename__ = 'ref_groups'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    groupID = db.Column(db.Integer, unique=True)
    groupName = db.Column(db.Text)

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
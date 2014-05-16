from flask import Flask

app = Flask(__name__)

app.secret_key = "Some key used for creating hidden tags"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cache.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set('xml')


from models import db
db.init_app(app)

import evepi.routes



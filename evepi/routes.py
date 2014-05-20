import pprint
from evepi import app
import os
from evepi.forms import SigninForm, SignupForm, ApiForm
import xml.etree.ElementTree as ET
from models import db, initial_db, User, Api, SkillPack, SkillAttr
from flask import render_template, flash, Markup, session, redirect, url_for, request, jsonify, abort, \
    send_from_directory
from werkzeug.utils import secure_filename

from ConfigParser import ConfigParser


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


Config = ConfigParser()
Config.read("settings.ini")
cached_time = ""
ALLOWED_EXTENSIONS = set(['txt', 'xml'])
initial_db()

if os.path.isfile('settings.ini'):
    apiURL = ConfigSectionMap("general")['apiurl']
    debug = ConfigSectionMap("general")['debug']
    interface = ConfigSectionMap("general")['interface']
    port = int(os.environ.get("PORT", 5000))

    # stopgap until we can get connected to Auth
    user = ConfigSectionMap("users")['user']
    password = ConfigSectionMap("users")['password']

else:
    apiURL = os.environ['eve_api_url']
    debug = os.environ['app_debug']
    interface = os.environ['app_binding_address']
    port = int(os.environ.get("PORT", 5000))

    # stopgap until we can get connected to Auth
    user = os.environ['app_admin_user']
    password = os.environ['app_admin_password']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def pull_character(keyID, vCode):
    pass


def pull_apis(keyID, vCode):
    pass


def update_characters(characterID):
    print characterID
    pass


def update_apis():
    pass


@app.route('/')
def default_display():
    return render_template('index.html')


# API Management section
@app.route('/api', methods=['GET', 'POST'])
def display_apis():
    form = ApiForm()

    if 'username' not in session:
        return redirect(url_for('default_display'))

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required!')
        else:
            url = apiURL + ""

            newapi = Api(keyID=form.keyID.data,vCode=form.vCode.data,user_id=session['id'],status=True)
            db.session.add(newapi)
            db.session.commit()
            update_apis()

    apis = Api.query.filter_by(user_id=session['id']).all()
    content = ""
    #TODO Add API update, delete functions
    for api in apis:
        content += "<tr>"
        content += "<td>" + str(api.keyID) + "</td>"
        content += "<td>" + api.vCode + "</td>"
        content += "<td>" + str(api.last_checked) + "</td>"
        content += "<td>Things</td>"
        content += "</tr>"


    return render_template('api.html', form=form, apis=Markup(content))


# Skill browser section
@app.route('/packs')
def display_skillpacks():
    return render_template('skillpacks.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']

    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Kick off processing routine
        #f = open(app.config['UPLOAD_FOLDER'] + "\\" + filename, 'r')
        #read = f.read()
        lookup = ET.parse(app.config['UPLOAD_FOLDER'] + "\\" + filename)
        lookup_root = lookup.getroot()

        # Get plan name
        plan = lookup_root.get('name')
        print plan

        skill_plan = SkillPack(name=plan,filename=filename,status=True)
        db.session.add(skill_plan)
        db.session.commit()

        print skill_plan.id

        # Skill attributes
        for child in lookup_root:
            if child.tag != "entry":
                continue
            skill = child.get('skill')
            priority = child.get('priority')
            skillID = child.get('skillID')
            level = child.get('level')

            skill_attrib = SkillAttr(pack_id=skill_plan.id, skill_id=skillID, priority=priority,skill_name=skill,value=level)
            db.session.add(skill_attrib)

        db.session.commit()
        return redirect(url_for('uploaded_file',
                                filename=filename))

@app.route('/testing')
def test_query():
    sql = '''select skill_name , MAX(case when priority <= 10 then value end) AS required, MAX(case when priority > 10 then value end) AS recommended
from skill_attr
where
  pack_id = 1
group by skill_name
'''
    skills = db.engine.execute(sql).fetchall()

    for skill in skills:
        if not skill.required:
            required = 0
        else:
            required = skill.required
        if not skill.recommended:
            recommended = required
        else:
            recommended = skill.recommended
        print skill.skill_name, required, recommended

    return "hi"



# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/signout')
def signout():
    if 'username' not in session:
        return redirect(url_for('signin'))

    session.pop('username', None)
    return redirect(url_for('default_display'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.username.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['username'] = newuser.username

            return redirect(url_for('default_display'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()

    if 'username' in session:
        return redirect(url_for('default_display'))

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                session['username'] = user.username
                session['id'] = user.id
            return redirect(url_for('default_display'))

    elif request.method == 'GET':
        return render_template('signin.html', form=form)



        # vim: set ts=4 sw=4 et :
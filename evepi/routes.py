from evepi import app
import os
from evepi.forms import SigninForm, SignupForm, ApiForm

from models import db, initial_db, User, Api
from flask import render_template, Markup, session, redirect, url_for, request, jsonify, abort

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
        newapi = Api(keyID=form.keyID.data,vCode=form.vCode.data,user_id=session['id'],status=True)
        db.session.add(newapi)
        db.session.commit()

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



# Registration Section

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
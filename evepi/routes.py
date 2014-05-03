from evepi import app
import os
from evepi.forms import SigninForm

from models import db, Table, initial_db
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


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()

    if 'email' in session:
        return redirect(url_for('hello_world'))

    if request.method == 'POST':
        if form.name.data == user and form.password.data == password:
            session['email'] = form.name.data
            return redirect(url_for('default_display'))
        else:
            return render_template('signin.html', form=form)

    elif request.method == 'GET':
        return render_template('signin.html', form=form)



    # vim: set ts=4 sw=4 et :
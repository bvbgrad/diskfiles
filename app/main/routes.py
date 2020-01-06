from datetime import datetime
from flask import render_template, current_app
from flask_login import current_user, login_required

from app import db
from app.main import bp

import subprocess
import os


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    current_app.logger.info('index')
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('main/index.html', admin_type=current_user.admin_type,  posts=posts)


@bp.route('/vol')
def vol():
    current_app.logger.info('vol')
    volCmd = "vol e:"
    volData = os.system(volCmd)
    if (volData == 0):
        stream = os.popen(volCmd)
        volName = stream.readline()
        volSerialNumber = stream.readline()
        print("volume: ", volName)
        print("Serial: ", volSerialNumber)
        return render_template('main/vol.html', volName=volName, volSerialNumber=volSerialNumber)
    else:
        no_data = "No disk data"
        print(no_data)
        return render_template('main/vol.html', volName=no_data)

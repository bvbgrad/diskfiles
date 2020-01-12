from datetime import datetime
import os

from flask import render_template, current_app
from flask_login import current_user, login_required

from app import db
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    current_app.logger.info('Enter main/index')

    return render_template('main/index.html', admin_type=current_user.admin_type)


@bp.route('/vol')
@login_required
def vol():
    current_app.logger.info("Enter: main/vol")
    volCmd = "vol e:"
        # todo os.system execution echos Stdout system command output 
    volData = os.system(volCmd)
    if (volData == 0):
        stream = os.popen(volCmd)
        volName = stream.readline()[22:].rstrip('\n ')
        volSerialNumber = stream.readline()[25:].rstrip('\n ')
        current_app.logger.info\
            ("main/vol Volume info: Serial: " + volSerialNumber + ", Name: " + volName)
        return render_template\
            ('main/vol.html', volName=volName, volSerialNumber=volSerialNumber)
    else:
        current_app.logger.info("main/vol Device not ready or no volume data")
        return render_template('main/vol.html', volName="No disk data")

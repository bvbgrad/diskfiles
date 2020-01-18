from datetime import datetime
import os

from flask import render_template, current_app
from flask_login import current_user, login_required

from app import db
from app.main import bp


@bp.before_app_request
def before_request():
    """
        Add timestamp to user object for every route access
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """
        Home page
    """
    current_app.logger.info('Enter main/index')

    return render_template('main/index.html', admin_type=current_user.admin_type)


@bp.route('/vol')
@login_required
def vol():
    """
        stub route to test disk vol command
    """
    current_app.logger.info("Enter: main/vol")
    vol_cmd = "vol e:"
    vol_data = os.system(vol_cmd)
    if vol_data != 0: # disk read failure
        current_app.logger.info("main/vol Device not ready or no volume data")
        return render_template('main/vol.html', volName="No disk data")

    stream = os.popen(vol_cmd) # os.popen execution echos system command output to stdout
    vol_name = stream.readline()[22:].rstrip('\n ')
    vol_serial_number = stream.readline()[25:].rstrip('\n ')
    current_app.logger.info(
        "main/vol Volume info: Serial: " + vol_serial_number + ", Name: " + vol_name)
    return render_template(
        'main/vol.html', volName=vol_name, volSerialNumber=vol_serial_number)

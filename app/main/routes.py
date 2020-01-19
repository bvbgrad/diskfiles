"""
    Routes for Main application
"""
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
    volume_info = __vol_info__('e:')
    if len(volume_info) == 0:
        return render_template('main/vol.html', volName="No disk data")

    disk_files = []
    disk_files.append(("serial number", "volume name", "file name"))
    disk_files.append((volume_info["serial_number"], volume_info["name"], "file 1"))
    disk_files.append((volume_info["serial_number"], volume_info["name"], "file 2"))

    return render_template(
        'main/vol.html', disk_files=disk_files,
        volName=volume_info["name"],
        volSerialNumber=volume_info["serial_number"])


def __vol_info__(volume_letter):
    current_app.logger.info("Enter: main/__vol_info__")
    vol_cmd = "vol " + volume_letter
    vol_data = os.system(vol_cmd)
    if vol_data != 0: # disk read failure
        volume_info = {}
        current_app.logger.info("main/vol Device not ready or no volume data")
    else:
        stream = os.popen(vol_cmd) # os.popen execution echos system command output to stdout
        vol_name = stream.readline()[22:].rstrip('\n ')
        vol_serial_number = stream.readline()[25:].rstrip('\n ')
        volume_info = {"name":vol_name, "serial_number":vol_serial_number}
        current_app.logger.info(
            "main/__vol_info__: Volume info: " +
            "Serial: " + volume_info["serial_number"] +
            ", Name: " + volume_info["name"])

    return volume_info

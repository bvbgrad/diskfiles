"""
    Routes for Main application
"""
import os
from datetime import datetime
from pathlib import Path

from flask import current_app, render_template
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
    volume_letter = 'E:'
    volume_info = __vol_info__(volume_letter)
    if len(volume_info) == 0:
        return render_template('main/vol.html', volName="No disk data")

    disk_files = __create_disk_list__(volume_letter)
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


def __create_disk_list__(current_dir):
    current_app.logger.info("Enter: main/__create_disk_list__ from volume: " + current_dir)

    disk_files = []
    disk_files.append(("Path", "Size", "Created"))

    current_path = Path(current_dir)
    for path in sorted(current_path.rglob('*')):
        if path.is_file():
            filepath = path.drive / path.parent / path.name
            filename = str(filepath)[2:] # get rid of drive letter
            created = datetime.fromtimestamp(path.stat().st_ctime)
            disk_files.append((filename, path.stat().st_size,\
                            f"{created:%Y%m%d-%H:%M:%S}"))
        else:
            # print(path.name)
            pass

    current_app.logger.info(
        f"Exit: main/__create_disk_list__ found {len(disk_files) - 1} files")
    return disk_files

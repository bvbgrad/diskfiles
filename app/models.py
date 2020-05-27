"""
    Data model - persistent data objects
"""
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    """ User object """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    admin_type = db.Column(db.String(20), default="none")
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    disks = db.relationship('Disk', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<Username {}, email: {}, Admin type: {}>'\
            .format(self.username, self.email, self.admin_type)

    def __init__(self, username, email, admin_type):
        self.username = username
        self.email = email
        self.admin_type = admin_type

    def set_password(self, password):
        """ One way hash of password string """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
            check if clear text password will generate the same hash
            that is stored in database for the 'current' password
        """
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    """ Check if user is logged-in on every page load """
    return User.query.get(int(user_id))


class Disk(db.Model):
    """ Disks in the catalog """

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(9), index=True, unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, default='NA')
    seq = db.Column(db.String(2), default='00')
    description = db.Column(db.Text, default='TBD')
    loc_type = db.Column(db.String(20), default='TBD')
    loc_seq = db.Column(db.String(2), default='00')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    files = db.relationship('File', backref='Disk', lazy='dynamic')

    def __repr__(self):
        return '<Serial: {}, name:Sequence = {}:{}>'\
                .format(self.serial_number, self.name, self.seq)

    def __init__(self, serial_number, name, description):
        self.serial_number = serial_number
        self.name = name
        self.description = description

    def set_name(self, name, seq):
        """ Update the disk name and seqence number """
        self.name = name
        self.seq = seq

    def set_location(self, loc_type, loc_seq):
        """ Update the location type and seqence number """
        self.loc_type = loc_type
        self.loc_seq = loc_seq

    def set_user_id(self, user_id):
        """ Update user id reference """
        self.user_id = user_id

class File(db.Model):
    """ All files """
    id = db.Column(db.Integer, primary_key=True)
    disk_id = db.Column(db.Integer, db.ForeignKey('disk.id'))
    filepath = db.Column(db.String(255))
    filename = db.Column(db.String(100))
    size = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    file_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<filename: {}, size = {}>'\
                .format(self.filename, self.size)

    def __init__(self, disk_id, filepath, filename, size, created):
        self.disk_id = disk_id
        self.filepath = filepath
        self.filename = filename
        self.size = size
        self.created = created

    def set_disk_id(self, disk_id):
        """ Update the disk_id """
        self.disk_id = disk_id

    def set_filepathname(self, filepath, filename):
        """ Update the file path and file name """
        self.filepath = filepath
        self.filename = filename

    def set_file_size(self, size):
        """ Update the size """
        self.size = size

    def set_file_created(self, created):
        """ Update the created timestamp """
        self.created = created

    def set_file_hash(self, file_hash):
        """ Update the file_hash """
        self.file_hash = file_hash

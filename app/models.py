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
    email = db.Column(db.String(120), index=True, unique=True)
    admin_type = db.Column(db.String(20), default="none")
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

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

""" Entry point """
from app import create_app, db
from app.models import User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """ Register the items in the shell session """
    return {'db': db, 'User': User}

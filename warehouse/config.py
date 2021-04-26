import binascii
import logging
import os

from flask import Flask, send_file

from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger(__name__)

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

static_dir = os.path.join(root_dir, "web", "build")


# Initialize the application.
app = Flask(__name__, static_url_path="/", static_folder=static_dir)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", binascii.hexlify(os.urandom(20)))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.url_map.strict_slashes = False


@app.errorhandler(Exception)
def handle_internal_failure(error):
    """
    Serve error page in case of internal failure.
    """
    if not hasattr(error, "code") or type(error.code) != int:
        logger.error(error)
        error = send_file(os.path.join(static_dir, "error.html")), 500
    return error


@app.teardown_appcontext
def close_connection(exception=None):
    """
    Terminate connection after HTTP request.
    """
    db.session.remove()


# Initialize the database.
db = SQLAlchemy(app)
db.reflect()

with app.app_context():
    # Sync tables from models.
    from . import models  # noqa F401

    db.create_all()
    db.session.commit()


# Register routes.
from . import views  # noqa F401

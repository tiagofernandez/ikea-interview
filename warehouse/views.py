import os

from flask import send_file

from sqlalchemy.sql import text

from .config import app, db, static_dir


@app.route("/")
def index():
    """
    Return the landing page.
    """
    return send_file(os.path.join(static_dir, "index.html"))


@app.route("/api/health-check")
def health_check():
    """
    Get the operational status of this application and an indication
    of its ability to connect to downstream dependent services.
    """
    db.session.query(text("1")).from_statement(text("SELECT 1")).all()
    return {}

from functools import wraps
from flask import session, redirect, flash, url_for


def login_required(f):
    @wraps(f)
    def decorate(*args, **kwargs):
        if not "username" in session:
            flash("First, you need to login in")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorate

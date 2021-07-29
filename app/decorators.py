from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f): 
    @wraps(f)
    def decorated_function(*args, **kwargs): 
        if not current_user.is_admin:
            flash("You cannot access this page.")
            return redirect(url_for("general.index"))
        return f(*args, **kwargs)
    return decorated_function

def editor_required(f): 
    @wraps(f)
    def decorated_function(*args, **kwargs): 
        if not current_user.is_editor:
            flash("You cannot access this page.")
            return redirect(url_for("general.index"))
        return f(*args, **kwargs)
    return decorated_function
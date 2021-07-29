from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required

from app.decorators import admin_required

mod = Blueprint("admin", __name__, url_prefix="/admin")

@mod.route("/")
@login_required 
@admin_required
def render_admin():
    return render_template(
        "pages/admin.html"
    )

#manage users
#remove users, change their details except passwords


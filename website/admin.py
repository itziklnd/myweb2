from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

admin = Blueprint('admin', __name__)

@admin.route('/admin-page')
@login_required
def admin_page():
    return render_template('admin_page.html', user=current_user, users=User)

@admin.route('/admin-logout')
def admin_logout():
    current_id = current_user.id
    user = User.query.get(current_id)
    user.is_admin = False
    db.session.commit()
    return redirect(url_for('views.home'))

@admin.route('/block-user/<int:user_id>')
def block_user(user_id):
    print(f'user id: {user_id} condition: blocked')
    user = User.query.filter_by(id=user_id).first()
    user.is_allowed = False
    db.session.commit()
    # כאן תוכל לבצע את החסימה של המשתמש
    return redirect(url_for('admin.admin_page'))

@admin.route('/allow-user/<int:user_id>')
def allow_user(user_id):
    print(f'user id: {user_id} condition: allowed')
    user = User.query.filter_by(id=user_id).first()
    user.is_allowed = True
    db.session.commit()
    # כאן תוכל לבצע את החסימה של המשתמש
    return redirect(url_for('admin.admin_page'))


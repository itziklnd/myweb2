from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)

@admin.route('/admin-page')
@login_required
def admin_page():
    users = User.query.all()  # שינוי: הבאת כל המשתמשים מהמסד
    return render_template('admin_page.html', user=current_user, users=users)

@admin.route('/admin-logout')
@login_required
def admin_logout():
    current_id = current_user.id
    user = User.query.get(current_id)
    if user:
        user.is_admin = False
        db.session.commit()
        flash('You have been logged out from admin.', category='success')
    else:
        flash('User not found.', category='error')
    return redirect(url_for('views.home'))

@admin.route('/block-user/<int:user_id>')
@login_required
def block_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_allowed = False
        db.session.commit()
        flash('User has been blocked.', category='success')
    else:
        flash('User not found.', category='error')
    return redirect(url_for('admin.admin_page'))

@admin.route('/allow-user/<int:user_id>')
@login_required
def allow_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_allowed = True
        db.session.commit()
        flash('User has been unblocked.', category='success')
    else:
        flash('User not found.', category='error')
    return redirect(url_for('admin.admin_page'))

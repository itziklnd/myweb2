from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)

# פונקציה לבדיקה אם האימייל תקין
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# טיפול בשגיאות בצורה כללית
@auth.app_context_processor
def inject_user():
    return dict(user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    print('Login')
    if request.method == 'POST':
        password = request.form.get('password')
        username = request.form.get('username')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/log_out')
def log_out():
    print("Attempting to log out")  # לוג כדי לבדוק שהפונקציה מופעלת
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))



@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists.', category='error')
        elif not is_valid_email(email):
            flash('Invalid email address.', category='error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            try:
                new_user = User(username=username, email=email, password=generate_password_hash(password1, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()

                # חיבור המשתמש החדש לאחר יצירת החשבון
                login_user(new_user, remember=True)
                flash('Account created and logged in!', category='success')
                return redirect(url_for('views.home'))
            except Exception as e:
                db.session.rollback()
                flash('There was an error creating your account. Please try again.', category='error')
                print(f"Error: {e}")

    return render_template("sign_up.html", user=current_user)

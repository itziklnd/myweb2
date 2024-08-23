from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
from flask_login import login_user, login_required, current_user
from .models import Task, User
from . import db
import json
from werkzeug.security import generate_password_hash, check_password_hash

ADMIN_PASSWORD = '1234'

views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    print(current_user.is_admin)
    if request.method == 'POST':
        task_desc = request.form.get('task-desc')
        task_points = request.form.get('task-points')

        if task_desc and task_points:
            try:
                task_points = int(task_points)
                if len(task_desc) > 0 and task_points > 0:
                    new_task = Task(data=task_desc, points=task_points)
                    db.session.add(new_task)
                    db.session.commit()
                    flash('Task added!', category='success')
                else:
                    flash('Invalid input!', category='error')
            except ValueError:
                flash('Points must be a number!', category='error')

    notes = Task.query.all()
    users = User.query.all()  # Fetch all users for the points board
    return render_template("home.html", notes=notes, users=users, user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = json.loads(request.data)
    task_id = data.get('noteId')
    
    # Fetch the task from the database
    task = Task.query.get(task_id)
    
    if task:
        # Update the current user's points
        current_user.points += task.points
        
        # Remove the task from the database
        db.session.delete(task)
        db.session.commit()
        
        # Save the updated points for the user
        db.session.add(current_user)
        db.session.commit()
        
        return jsonify({'success': True})
    
    return jsonify({'success': False})


@views.route('/admin-login', methods=['POST'])
def admin_login():
    print(ADMIN_PASSWORD)
    password = request.form.get('admin-password')
    print(password)

    if password == ADMIN_PASSWORD:
        user = User.query.filter_by(id=current_user.id).first()
        if user:
            user.is_admin = True
            db.session.commit()
            return redirect(url_for('views.home'))

# @views.route('/reset-points', methods=['POST'])
# @login_required
# def reset_points():
#     if not session.get('admin', False):
#         return jsonify({'success': False})

#     users = User.query.all()
#     for user in users:
#         user.points = 0

#     db.session.commit()
#     return jsonify({'success': True})

# @views.route('/reset-database', methods=['POST'])
# @login_required
# def reset_database():
#     if not session.get('admin', False):
#         flash('Unauthorized', category='error')
#         return redirect(url_for('views.home'))

#     # Delete all tasks and users
#     try:
#         Task.query.delete()
#         User.query.delete()
#         db.session.commit()
#         flash('Database has been reset!', category='success')
#         return jsonify({'success': True})
#     except Exception as e:
#         db.session.rollback()
#         flash(f'Error resetting database: {str(e)}', category='error')
#         return jsonify({'success': False})

# @views.route('/logout-admin', methods=['POST'])
# @login_required
# def logout_admin():
#     session.pop('admin', None)  # Remove admin from session
#     return jsonify({'success': True})

# @views.route('/login')
# def login():
#     # Implement login logic here
#     return render_template("login.html")

@views.route('/add-task', methods=['POST'])
@login_required
def add_task():
    task_desc = request.form.get('task-desc')
    task_points = request.form.get('task-points')
    
    if task_desc and task_points:
        try:
            task_points = int(task_points)
            if len(task_desc) > 0 and task_points > 0:
                new_task = Task(data=task_desc, points=task_points)
                db.session.add(new_task)
                db.session.commit()
                flash('Task added!', category='success')
            else:
                flash('Invalid input!', category='error')
        except ValueError:
            flash('Points must be a number!', category='error')
    
    return redirect('/')
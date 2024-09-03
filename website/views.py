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
    
    return redirect(url_for('views.home'))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SESSION_PROTECTION'] = 'strong'  # חיזוק ניהול הסשנים
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    from .models import User  # ייבוא של המודל

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = User.query.get(int(id))
        return user
    return app

def create_database(app):
    if not path.exists(path.join(app.instance_path, DB_NAME)):
        with app.app_context():
            db.create_all()
        print('Created Database!')

def split_data(data, delimiter=':', max_splits=None):
    parts = data.split(delimiter, max_splits)
    return parts


def update_user_column(user_id, new_item):
    from .models import User  # ייבוא של המודל
    user = User.query(User).filter_by(id=user_id).one_or_none()
        
    if user is None:
        print(f"משתמש עם ID {user_id} לא נמצא.")
        return
    
    # חילוק המחרוזת לחלקים
    data =user.data  # הנחה שהעמודה שלך נקראת data
    parts = data.split(';')
    
    # הוספת הפריט החדש לרשימה
    parts.append(str(new_item))
    
    # חיבור הרשימה חזרה למחרוזת
    updated_data = ';'.join(parts)
    
    # עדכון השדה בעמודה
    user.data = updated_data
    db.session.commit()
    
    # שמירה של השינויים בבסיס הנתונים
    print(f"העמודה עודכנה בהצלחה עבור משתמש עם ID {user.id}.")
    print(user.data)
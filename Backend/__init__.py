from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'Quizziotest1.db'

def create_app():

  # Calculate the base directory (one level up from the Backend folder)
  base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Use absolute paths for static and template folders
  app = Flask(__name__,
              static_folder=os.path.join(base_dir, 'Frontend', 'static'),
              template_folder=os.path.join(base_dir, 'Frontend', 'templates'))
  
  app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)
  
  from .views import views
  from .auth import auth
  
  

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  

  from .models import User

  create_database(app)

  return app


def create_database(app):
  if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', DB_NAME)):
    with app.app_context():
      db.create_all()
    print('Created Database!')
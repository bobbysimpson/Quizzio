from flask import Flask
import os


def create_app():
  app = Flask(__name__, template_folder=os.path.abspath("./Frontend/templates"))
  app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
  #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  

  #from .views import views
  from .auth import auth

  #app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  return app
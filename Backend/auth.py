from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os


auth = Blueprint('auth', __name__, template_folder=os.path.abspath("./Frontend/templates"))

@auth.route('/login', methods=['GET', 'POST'])
def login():
  # debug: print('reached login page') #REACHED
  if request.method == 'POST':
    # debug: print('received POST request') #NOT REACHED
    username = request.form.get('login-username')
    #debug: print('got username')
    password = request.form.get('login-password')

    user = User.query.filter_by(username=username).first()
    if user:
      if check_password_hash(user.password, password):
        print("Log in successful") #NEED TO IMPLEMENT FLASH MESSAGES HERE
        #login_user(user, remember=True)
        return redirect(url_for('index.html'))
      else:
        print('Incorrect password') #HERE
    else:
      print('User does not exist.') #HERE

  return render_template('login.html', user=current_user)

@auth.route('/sign-up')
def sign_up():
  return render_template('signup.html')
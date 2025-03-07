from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os


auth = Blueprint('auth', __name__, template_folder=os.path.abspath("./Frontend/templates"))

@auth.route('/', methods=['GET', 'POST'])
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

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('signup-email')
    username = request.form.get('signup-username')
    password = request.form.get('signup-password')
    

    user = User.query.filter_by(email=email).first()
    if user:
      flash('Email already exists', category='error')

    if len(email) < 4:
      flash('Email must be greater than 3 characters', category='error')
    elif len(username) < 2:
      flash('Username must be greater than 1 character', category='error')
    elif len(password) < 7:
      flash('Password must be at least 7 characters', category='error')
    else:
      new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
      db.session.add(new_user)
      db.session.commit()
      #login_user(user, remember=True)
      flash('Account created!', category='success')
      return redirect(url_for('views.home')) #logs them in and redirects them to welcome page

  return render_template('signup.html', user=current_user)
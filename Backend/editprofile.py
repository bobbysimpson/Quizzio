from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import current_user
import os
import json


editprofile = Blueprint('editprofile', __name__, template_folder=os.path.abspath('./Frontend/templates'), static_folder=os.path.abspath('./Frontend/static'))

@editprofile.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)

@editprofile.route('/edit', methods = ['GET', 'POST'])
def edit():
    print(User.query.filter_by(username=current_user.username).first())
    if request.method == 'POST':
        jsonData = request.get_json()
        newUsername = jsonData['username']
        newEmail = jsonData['email']
        newPassword = jsonData['password']
        if len(newUsername) != 0:
            # need to add validation to make sure new username is not taken
            current_user.username = newUsername
        if len(newEmail) != 0:
            # email validation will go here
            current_user.email = newEmail
        if len(newPassword) != 0:
            current_user.password = generate_password_hash(newPassword, method='pbkdf2:sha256')
        db.session.commit()
        print("User data saved successfully") # need to flash a message here
    return User.query.filter_by(username=current_user.username).first()

    

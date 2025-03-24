from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from .models import User
from werkzeug.security import generate_password_hash
from flask_login import current_user
import os
import json


editprofile = Blueprint('editprofile', __name__)

@editprofile.route('/profile')
def profile():
    return render_template('profile.html')

@editprofile.route('/edit', methods = ['GET', 'POST'])
def edit():
    supabase = current_app.config["SUPABASE_CLIENT"]
    print(User.query.filter_by(username=current_user.username).first())
    if request.method == 'POST':
        jsonData = request.get_json()
        newUsername = jsonData['username']
        newEmail = jsonData['email']
        newPassword = jsonData['password']
        updateData = {}
        if len(newUsername) != 0:
            response = supabase.table("users").select("*").eq("username", newUsername).execute()
            if len(response.data) != 0:
                flash("Error: Username already in use.")
            else:
                updateData['username'] = newUsername
        if len(newEmail) != 0:
            response = supabase.table("users").select("*").eq("email", newEmail).execute()
            if len(response.data) != 0:
                flash("Error: Email already in use")
            else:
                updateData['email'] = newEmail
        if len(newPassword) != 0:
            updateData['password'] = generate_password_hash(newPassword, method='pbkdf2:sha256')
        
        response = supabase.table("users").update(json.dumps(updateData)).eq("username", session["username"]).execute()
        print("User data saved successfully") # need to flash a message here
    return User.query.filter_by(username=current_user.username).first()

    

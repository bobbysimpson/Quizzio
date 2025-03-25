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
    if request.method == 'POST':
        newUsername = request.form['newUsername']
        newEmail = request.form['newEmail']
        newPassword = request.form['newPassword']
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
        response = supabase.table("users").update(updateData).eq("username", session["username"]).execute()
       # print(response.data)
        if not response.data or len(response.data) == 0:
        #    flash("Error: Nothing happened", "error")
            print("Didn't work")
        else:
         #   flash("User data saved successfully", "success") # need to flash a message here
              print("Did work")
              if len(newUsername) != 0:
                  session["username"] = newUsername
    return render_template('profile.html')

    

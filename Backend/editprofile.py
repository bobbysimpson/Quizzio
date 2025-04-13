from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from .models import User
from werkzeug.security import generate_password_hash
from flask_login import current_user
import os
import json


editprofile = Blueprint('editprofile', __name__)

@editprofile.route('/profile')
def profile():
    #session['_flashes'].clear() # note this breaks all flashed messages on this page, need to fix this later
    supabase = current_app.config["SUPABASE_CLIENT"]
    response = supabase.table("users").select("email").eq("username", current_user.username).execute()
    email = response.data[0]
    email = email.get("email")
    return render_template('profile.html', username=current_user.username, email=email)

@editprofile.route('/edit', methods = ['GET', 'POST'])
def edit():
    supabase = current_app.config["SUPABASE_CLIENT"]
    if request.method == 'POST':
        newUsername = request.form['newUsername']
        newEmail = request.form['newEmail']
        newPassword = request.form['newPassword']

        updateData = {}
# checks for each possible field to update so that blank values don't accidentally get passed over. Can probably be consolidated into simpler statements than this.
        if len(newUsername) != 0:
            response = supabase.table("users").select("*").eq("username", newUsername).execute()
            if len(response.data) != 0:
                flash("Error: Username already in use.", "error")
            else:
                updateData['username'] = newUsername
        if len(newEmail) != 0:
            response = supabase.table("users").select("*").eq("email", newEmail).execute()
            if len(response.data) != 0:
                flash("Error: Email already in use")
            else:
                updateData['email'] = newEmail
        if len(newPassword) != 0:
            updateData['password'] = generate_password_hash(newPassword)
        response = supabase.table("users").update(updateData).eq("username", current_user.username).execute()
       # print(response.data)
        if not response.data or len(response.data) == 0:
            flash("Error: Nothing happened", "error")
            print("Didn't work")
        else:
            flash("User data saved successfully", "success") # need to flash a message here
            print("Did work")
            if len(newUsername) != 0:
                current_user.username = newUsername
    response = supabase.table("users").select("email").eq("username", current_user.username).execute()
    email = response.data[0]
    email = email.get("email")
    return render_template('profile.html', username=current_user.username, email=email)
    

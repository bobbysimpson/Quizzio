import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('views.index'))

    supabase = current_app.config["SUPABASE_CLIENT"]
    if request.method == "POST":
        email = request.form.get("email").lower() 
        username = request.form.get("username").lower()
        password = request.form.get("password")

        #new signup form validation
        if not email or not username or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('auth.signup'))


        existing_user = supabase.table("users").select("email").eq("email", email).execute()
        if existing_user.data:
            flash("Email already exists. Please use a different email.", "error")
            return redirect(url_for('auth.signup'))

        existing_username = supabase.table("users").select("username").eq("username", username).execute()
        if existing_username.data:
            flash("Username already exists. Please choose a different username.", "error")
            return redirect(url_for('auth.signup'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.", "error")
            return redirect(url_for('auth.signup'))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return redirect(url_for('auth.signup'))

        password_hash = generate_password_hash(password)

        response = supabase.table("users").insert({
            "email": email,
            "username": username,
            "password_hash": password_hash
        }).execute()

        user_obj = User.from_dict(response.data[0])
        login_user(user_obj, remember=True)
        flash("Account created successfully!", "success")
        return redirect(url_for('views.index')) 

    return render_template("signup.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('views.index'))

    supabase = current_app.config["SUPABASE_CLIENT"]
    if request.method == "POST":
        username = request.form.get("username").lower()  
        password = request.form.get("password")


        if not username or not password:
            flash("Please provide both username and password.", "error")
            return redirect(url_for('auth.login'))


        response = supabase.table("users").select("*").eq("username", username).execute()


        if not response.data or len(response.data) == 0:
            flash("Invalid username or password.", "error")
            return redirect(url_for('auth.login'))

        user = response.data[0]


        if check_password_hash(user["password_hash"], password):
            user_obj = User.from_dict(user)
            login_user(user_obj, remember=True)
            flash("Logged in successfully!", "success")
            return redirect(url_for('views.index'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('auth.login'))

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('auth.login'))

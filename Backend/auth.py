from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    supabase = current_app.config["SUPABASE_CLIENT"]
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not email or not username or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('auth.signup'))
        
        # NEED TO ADD CODE WHICH checks if email already exists
        # ADD CODE WHICH VALIDATES EMAIL AND PASSWORD E.G. if password > 3 chars etc
        
        password_hash = generate_password_hash(password)
        
        # Insert new user into Supabase 'users' table
        response = supabase.table("users").insert({
            "email": email,
            "username": username,
            "password_hash": password_hash
        }).execute()

        user_obj = User.from_dict(response.data[0])
        login_user(user_obj, remember=True)
        
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('auth.login'))
    
    return render_template("signup.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    supabase = current_app.config["SUPABASE_CLIENT"]
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            flash("Please provide both username and password.", "error")
            return redirect(url_for('auth.login'))
        
        # Query the 'users' table by username
        response = supabase.table("users").select("*").eq("username", username).execute()
        
        
        if not response.data or len(response.data) == 0:
            flash("Invalid username or password.", "error")
            return redirect(url_for('auth.login'))
        
        user = response.data[0]
        
        if check_password_hash(user["password_hash"], password):
            # Optionally, store user info in the session
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            flash("Logged in successfully!", "success")
            user_obj = User.from_dict(user)
            login_user(user_obj, remember=True) # BUG MIGHT BE HERE SO LOOK INTO THIS NEXT TIME
            return redirect(url_for('views.index'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('auth.login'))
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required  # this decorator makes sure the user is logged in before they can access the route. If not, they'll be redirected to the login page. 
def logout():
  logout_user()
  return redirect(url_for('auth.login'))
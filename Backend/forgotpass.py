from flask import Flask, request, render_template, url_for, redirect, flash, session, current_app, Blueprint
import smtplib
from email.mime.text import MIMEText
import secrets
from werkzeug.security import generate_password_hash
from supabase import create_client, Client
import os

forgotpass = Blueprint('forgotpass', __name__)
#app.secret_key = 'MY_SUPER_SECRET_KEY'  # Replace with a strong secret key

# Set up Supabase credentials (ideally use environment variables in production)
#SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ymspflrxipjlipncgzyy.supabase.co")
#SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inltc3BmbHJ4aXBqbGlwbmNnenl5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE2OTcxMzYsImV4cCI6MjA1NzI3MzEzNn0.jNFsla4rFX1WWiyS7Iu0GBYQQG8iMv2YLQ-3aHaWRGs")
#supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# In-memory storage for reset tokens (for demonstration pxurposes)
reset_tokens = {}  # Format: {token: email}

# SMTP configuration for Gmail
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'quizzioreset@gmail.com'  # Replace with actual sender email
EMAIL_PASSWORD = 'zbsj yrpo qdnk wwvn'      # Replace with actual app password

def send_reset_email(recipient_email, token):
    reset_url = url_for('forgotpass.reset_password', token=token, _external=True)
    subject = "Password Reset Request"
    body = f"Click the following link to reset your password: {reset_url}"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
        print("IT SENT")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@forgotpass.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    supabase = current_app.config["SUPABASE_CLIENT"]
    if request.method == "GET":
        # Render the forgot password page (forgotpass.html)
        return render_template("forgotpass.html")
    else:
        # Process the form submission
        email = request.form.get("email")
        
        # Query Supabase to check if the email exists in the "users" table
        response = supabase.table("users").select("*").eq("email", email).execute()
        
        # Check if any data was returned; if not, flash "Invalid email."
        if not response.data or len(response.data) == 0:
            flash("Invalid email.", "error")
            return redirect(url_for("forgotpass.forgot_password"))
        
        # Email exists: generate a unique token for password reset and store it
        token = secrets.token_urlsafe(16)
        reset_tokens[token] = email

        # Send the reset email and flash a message accordingly
        if send_reset_email(email, token):
            flash("Reset email sent.", "success")
        else:
            flash("Failed to send password reset email. Please try again later.", "error")

        # Redirect to login page after processing
        return redirect(url_for("auth.login"))

@forgotpass.route("/reset_password/<token>", methods = ["GET", "POST"])
def reset_password(token):
    supabase = current_app.config["SUPABASE_CLIENT"]
    email = reset_tokens.get(token)
    print(email)
    if not email:
        flash("Invalid or expired reset link.", "error")
        return redirect(url_for("auth.login"))
    else:
        if request.method == "POST":
                newPassword = request.form.get("password")
                if len(newPassword) != 0:
                    newPassword = generate_password_hash(newPassword)
                    updateData = {"password_hash" : newPassword}
                    response = supabase.table("users").update(updateData).eq("email", email).execute() # hacky way of making sure it affects the right account
                    print(response)
                    if not response or len(response.data) == 0:
                        print("Something didn't work")
                    else:
                        print("Password changed.") # add message flash here
                    return redirect(url_for("auth.login"))
    return render_template("reset_pass.html", email=email)

@forgotpass.route("/login")
def login():
    return render_template("login.html")

#if __name__ == "__main__":
 #   app.run(debug=True)
from flask import Flask, request, render_template, url_for, redirect, flash
import smtplib
from email.mime.text import MIMEText
import secrets

app = Flask(__name__)
app.secret_key = 'MY_SUPER_SECRET_KEY'  # Replace with your own secure key

# In-memory token storage (for demo purposes only)
reset_tokens = {}  # Format: {token: email}

# In-memory "user database" for demonstration purposes.
# In production, use a real database and hash passwords.
users = {
    'testuser': {
        'username': 'testuser',
        'password': 'testpassword',  # For demo only (plain text)
        'email': 'rahulmehra4@aol.co.uk'
    }
}

# SMTP configuration for Gmail
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'quzzioreset@gmail.com'         # Replace with your Gmail address
EMAIL_PASSWORD = 'jnnk mehw tymv msat' 

def send_reset_email(recipient_email, token):
    reset_url = url_for('reset_password', token=token, _external=True)
    subject = "Password Reset Request"
    body = f"Click the following link to reset your password:\n{reset_url}\nIf you did not request a password reset, please ignore this email."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            flash("Login successful!")
            return redirect(url_for('dashboard'))
        else:
            flash("Username and password not accepted")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the Dashboard! (This is a placeholder)"

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    # For testing, we hardcode the recipient email to your test email.
    # In production, use: email = request.form.get('email')
    email = 'rahulmehra4@aol.co.uk'
    if not email:
        flash("Please enter a valid email address.")
        return redirect(url_for('login'))
    token = secrets.token_urlsafe(16)
    reset_tokens[token] = email
    try:
        send_reset_email(email, token)
        flash("A password reset email has been sent. Please check your inbox.")
    except Exception as e:
        flash("There was an error sending the reset email. Please try again later.")
        print("SMTP error:", e)
    return redirect(url_for('login'))

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = reset_tokens.get(token)
    if not email:
        flash("Invalid or expired token.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_password = request.form.get('password')
        # Update the password in our in-memory database
        for user in users.values():
            if user['email'] == email:
                user['password'] = new_password
                break
        del reset_tokens[token]
        flash("Your password has been updated.")
        return redirect(url_for('login'))
    return render_template('reset_password.html', token=token)

if __name__ == '__main__':
    app.run(debug=True)
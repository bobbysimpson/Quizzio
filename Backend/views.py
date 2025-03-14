from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def index():
    print(f"User authenticated: {current_user.is_authenticated}")
    return render_template("index.html", user=current_user)



@views.route('/guides', methods=['GET', 'POST'])
def guides():
    return render_template("welcome.html")
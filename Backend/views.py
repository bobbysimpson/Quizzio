from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def index():
    #print(f"User authenticated: {current_user.is_authenticated}")
    return render_template("index.html", user=current_user)



@views.route('/guides', methods=['GET', 'POST'])
def guides():
    return render_template("welcome.html")

@views.route('/create')
def create():
    return render_template("create.html")

@views.route('/english')
def english():
    return render_template("English.html")

@views.route('/language')
def language():
    return render_template("Language.html")

@views.route('/maths')
def maths():
    return render_template("Maths.html")

@views.route('/science')
def science():
    return render_template("Science.html")

@views.route('/computing')
def computing():
    return render_template("Computing.html")

@views.route('/other')
def other():
    return render_template("Other.html")

@views.route('/library')
def library():
    return render_template("library.html")

#github shite
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request, jsonify

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def index():
    #print(f"User authenticated: {current_user.is_authenticated}")
    return render_template("index.html", user=current_user)



@views.route('/guides', methods=['GET', 'POST'])
def guides():
    return render_template("Welcome.html")

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

@views.route('/api/quizzes', methods=['POST'])
@login_required
def save_quiz():
    data = request.get_json()
    title = data.get('title')
    category = data.get('category')
    flashcards = data.get('flashcards', [])

    try:
        # Just print the data for now (until Supabase integration is added)
        print("QUIZ TITLE:", title)
        print("CATEGORY:", category)
        print("FLASHCARDS:", flashcards)

        return jsonify({"message": "Received successfully"}), 201
    except Exception as e:
        print("Error saving quiz:", str(e))
        return jsonify({"error": "Something went wrong"}), 500
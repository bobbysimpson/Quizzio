from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request, jsonify, current_app

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

    supabase = current_app.config["SUPABASE_CLIENT"]
    print("CATEGORY RECEIVED:", category)

    try:
        inserts = []
        for card in flashcards:
            inserts.append({
                "user_id": current_user.id,
                "set_title": title,
                "category": category,
                "front_text": card["name"],
                "back_text": card["content"]
            })

        response = supabase.table("flashcards").insert(inserts).execute()

        if response.data is None:
            print("Supabase insert failed:", response)
            return jsonify({"error": "Database insert failed"}), 500

        return jsonify({"message": "Flashcards saved successfully"}), 201
    
    except Exception as e:
        print("Error saving to Supabase:", str(e))
        return jsonify({"error": "Server error"}), 500
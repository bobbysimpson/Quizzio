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
@login_required
def library():
    supabase = current_app.config["SUPABASE_CLIENT"]
    response = supabase.table("flashcard_sets").select("*").eq("user_id", current_user.id).execute()
    quizzes = response.data if response.data else []
    return render_template("library.html", quizzes=quizzes)

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
        # Step 1: Create a new flashcard set
        set_response = supabase.table("flashcard_sets").insert({
            "user_id": current_user.id,
            "title": title,
            "category": category
        }).execute()

        set_id = set_response.data[0]["set_id"]

        # Step 2: Insert flashcards with that set_id
        inserts = []
        for card in flashcards:
            inserts.append({
                "user_id": current_user.id,
                "set_id": set_id,
                "front_text": card["name"],
                "back_text": card["content"]
            })

        flashcard_response = supabase.table("flashcards").insert(inserts).execute()

        if flashcard_response.data is None:
            print("Supabase insert failed:", flashcard_response)
            return jsonify({"error": "Database insert failed"}), 500

        return jsonify({"message": "Flashcard set saved successfully"}), 201
    
    except Exception as e:
        print("Error saving to Supabase:", str(e))
        return jsonify({"error": "Server error"}), 500
    
@views.route('/api/sets', methods=['GET'])
@login_required
def get_flashcard_sets():
    supabase = current_app.config["SUPABASE_CLIENT"]

    try:
        response = supabase.table("flashcard_sets") \
            .select("id", "title", "category", "created_at") \
            .eq("user_id", current_user.id) \
            .execute()

        return jsonify(response.data), 200

    except Exception as e:
        print("Error fetching sets:", str(e))
        return jsonify({"error": "Could not fetch sets"}), 500
    
@views.route('/quiz_detail/<int:quiz_id>')
def quiz_detail(quiz_id):
    supabase = current_app.config["SUPABASE_CLIENT"]
    response = supabase.table("flashcard_sets").select("*").eq("id", quiz_id).execute()
    quiz = response.data[0] if response.data else None
    return render_template("quiz_detail.html", quiz=quiz)
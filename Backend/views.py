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
    supabase = current_app.config["SUPABASE_CLIENT"]
    
    # Fetches quizzes in the a category
    response = supabase.table("flashcard_sets")\
        .select("set_id, title, category, created_at, user_id, users(username)")\
        .ilike("category", "%English%")\
        .execute()
    quizzes = response.data if response.data else []
    
    # Fetches bookmarked flashcard_ids
    bookmarked_flashcards = supabase.table("bookmarks") \
        .select("flashcard_id") \
        .eq("user_id", current_user.id) \
        .execute()
    bookmarked_flashcard_ids = [item['flashcard_id'] for item in bookmarked_flashcards.data]
    
    if bookmarked_flashcard_ids:
        bookmarked_sets_response = supabase.table("flashcards") \
            .select("set_id") \
            .in_("flashcard_id", bookmarked_flashcard_ids) \
            .execute()
        bookmarked_set_ids = list(set(item['set_id'] for item in bookmarked_sets_response.data))
    else:
        bookmarked_set_ids = []
    
    for quiz in quizzes:
        quiz['is_bookmarked'] = quiz['set_id'] in bookmarked_set_ids

    return render_template("English.html", quizzes=quizzes)

@views.route('/language')
def language():
    supabase = current_app.config["SUPABASE_CLIENT"]
    
    response = supabase.table("flashcard_sets")\
        .select("set_id, title, category, created_at, user_id, users(username)")\
        .ilike("category", "%Language%")\
        .execute()
    quizzes = response.data if response.data else []
    
    bookmarked_flashcards = supabase.table("bookmarks") \
        .select("flashcard_id") \
        .eq("user_id", current_user.id) \
        .execute()
    bookmarked_flashcard_ids = [item['flashcard_id'] for item in bookmarked_flashcards.data]
    
    if bookmarked_flashcard_ids:
        bookmarked_sets_response = supabase.table("flashcards") \
            .select("set_id") \
            .in_("flashcard_id", bookmarked_flashcard_ids) \
            .execute()
        bookmarked_set_ids = list(set(item['set_id'] for item in bookmarked_sets_response.data))
    else:
        bookmarked_set_ids = []
    
    for quiz in quizzes:
        quiz['is_bookmarked'] = quiz['set_id'] in bookmarked_set_ids

    return render_template("Language.html", quizzes=quizzes)

@views.route('/maths')
def maths():
    supabase = current_app.config["SUPABASE_CLIENT"]
    
    response = supabase.table("flashcard_sets")\
        .select("set_id, title, category, created_at, user_id, users(username)")\
        .ilike("category", "%Maths%")\
        .execute()
    quizzes = response.data if response.data else []
    
    bookmarked_flashcards = supabase.table("bookmarks") \
        .select("flashcard_id") \
        .eq("user_id", current_user.id) \
        .execute()
    bookmarked_flashcard_ids = [item['flashcard_id'] for item in bookmarked_flashcards.data]
    
    if bookmarked_flashcard_ids:
        bookmarked_sets_response = supabase.table("flashcards") \
            .select("set_id") \
            .in_("flashcard_id", bookmarked_flashcard_ids) \
            .execute()
        bookmarked_set_ids = list(set(item['set_id'] for item in bookmarked_sets_response.data))
    else:
        bookmarked_set_ids = []
    
    for quiz in quizzes:
        quiz['is_bookmarked'] = quiz['set_id'] in bookmarked_set_ids

    return render_template("Maths.html", quizzes=quizzes)

@views.route('/science')
@login_required
def science():
    supabase = current_app.config["SUPABASE_CLIENT"]
    
    response = supabase.table("flashcard_sets")\
        .select("set_id, title, category, created_at, user_id, users(username)")\
        .ilike("category", "%Science%")\
        .execute()
    quizzes = response.data if response.data else []
    
    bookmarked_flashcards = supabase.table("bookmarks") \
        .select("flashcard_id") \
        .eq("user_id", current_user.id) \
        .execute()
    bookmarked_flashcard_ids = [item['flashcard_id'] for item in bookmarked_flashcards.data]
    
    if bookmarked_flashcard_ids:
        bookmarked_sets_response = supabase.table("flashcards") \
            .select("set_id") \
            .in_("flashcard_id", bookmarked_flashcard_ids) \
            .execute()
        bookmarked_set_ids = list(set(item['set_id'] for item in bookmarked_sets_response.data))
    else:
        bookmarked_set_ids = []
    
    for quiz in quizzes:
        quiz['is_bookmarked'] = quiz['set_id'] in bookmarked_set_ids
    
    return render_template("Science.html", quizzes=quizzes)

@views.route('/computing')
def computing():
    supabase = current_app.config["SUPABASE_CLIENT"]
    
    response = supabase.table("flashcard_sets")\
        .select("set_id, title, category, created_at, user_id, users(username)")\
        .ilike("category", "%Computing%")\
        .execute()
    quizzes = response.data if response.data else []
    
    bookmarked_flashcards = supabase.table("bookmarks") \
        .select("flashcard_id") \
        .eq("user_id", current_user.id) \
        .execute()
    bookmarked_flashcard_ids = [item['flashcard_id'] for item in bookmarked_flashcards.data]
    
    if bookmarked_flashcard_ids:
        bookmarked_sets_response = supabase.table("flashcards") \
            .select("set_id") \
            .in_("flashcard_id", bookmarked_flashcard_ids) \
            .execute()
        bookmarked_set_ids = list(set(item['set_id'] for item in bookmarked_sets_response.data))
    else:
        bookmarked_set_ids = []
    
    for quiz in quizzes:
        quiz['is_bookmarked'] = quiz['set_id'] in bookmarked_set_ids

    return render_template("Computing.html", quizzes=quizzes)

@views.route('/other')
@login_required 
def other():
    supabase = current_app.config["SUPABASE_CLIENT"]
    
    response = supabase.table("flashcard_sets")\
        .select("set_id, title, category, created_at, user_id, users(username)")\
        .ilike("category", "%Other%")\
        .execute()
    quizzes = response.data if response.data else []
    
    bookmarked_flashcards = supabase.table("bookmarks") \
        .select("flashcard_id") \
        .eq("user_id", current_user.id) \
        .execute()
    bookmarked_flashcard_ids = [item['flashcard_id'] for item in bookmarked_flashcards.data]
    
    if bookmarked_flashcard_ids:
        bookmarked_sets_response = supabase.table("flashcards") \
            .select("set_id") \
            .in_("flashcard_id", bookmarked_flashcard_ids) \
            .execute()
        bookmarked_set_ids = list(set(item['set_id'] for item in bookmarked_sets_response.data))
    else:
        bookmarked_set_ids = []
    
    for quiz in quizzes:
        quiz['is_bookmarked'] = quiz['set_id'] in bookmarked_set_ids
    
    return render_template("Other.html", quizzes=quizzes)

@views.route('/library')
@login_required
def library():
    supabase = current_app.config["SUPABASE_CLIENT"]

    # Get bookmarked flashcard IDs for the current user
    bookmarked_flashcards = supabase.table("bookmarks") \
        .select("flashcard_id") \
        .eq("user_id", current_user.id) \
        .execute()
    bookmarked_flashcard_ids = [item['flashcard_id'] for item in bookmarked_flashcards.data]

    if not bookmarked_flashcard_ids:
        quizzes = []
    else:
        # Get set IDs from bookmarked flashcards
        sets_response = supabase.table("flashcards") \
            .select("set_id") \
            .in_("flashcard_id", bookmarked_flashcard_ids) \
            .execute()
        set_ids = list(set(item['set_id'] for item in sets_response.data))

        # Fetch flashcard sets with bookmarked flashcards
        response = supabase.table("flashcard_sets") \
            .select("set_id, title, category, created_at, user_id, users(username)") \
            .in_("set_id", set_ids) \
            .execute()
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

    try:
        # Create the flashcard set
        set_response = supabase.table("flashcard_sets").insert({
            "user_id": current_user.id,
            "title": title,
            "category": category
        }).execute()
        set_id = set_response.data[0]["set_id"]

        # Insert flashcards
        flashcard_inserts = [
            {
                "user_id": current_user.id,
                "set_id": set_id,
                "front_text": card["name"],
                "back_text": card["content"]
            } for card in flashcards
        ]
        flashcard_response = supabase.table("flashcards").insert(flashcard_inserts).execute()

        if not flashcard_response.data:
            return jsonify({"error": "Failed to insert flashcards"}), 500

        # Automatically bookmark all flashcards for the creator
        flashcard_ids = [fc["flashcard_id"] for fc in flashcard_response.data]
        bookmark_inserts = [
            {"user_id": current_user.id, "flashcard_id": fc_id}
            for fc_id in flashcard_ids
        ]
        supabase.table("bookmarks").insert(bookmark_inserts).execute()

        return jsonify({"message": "Quiz saved and bookmarked successfully"}), 201

    except Exception as e:
        print(f"Error saving quiz: {str(e)}")
        return jsonify({"error": "Server error"}), 500
    
@views.route('/api/sets', methods=['GET'])
@login_required
def get_flashcard_sets():
    supabase = current_app.config["SUPABASE_CLIENT"]

    try:
        response = supabase.table("flashcard_sets") \
            .select("set_id", "title", "category", "created_at", "users(username)") \
            .eq("user_id", current_user.id) \
            .execute()

        return jsonify(response.data), 200

    except Exception as e:
        print("Error fetching sets:", str(e))
        return jsonify({"error": "Could not fetch sets"}), 500
    
@views.route('/quiz_detail/<int:quiz_id>')
@login_required
def quiz_detail(quiz_id):
    supabase = current_app.config["SUPABASE_CLIENT"]
    response = supabase.table("flashcard_sets").select("*").eq("set_id", quiz_id).execute()
    quiz = response.data[0] if response.data else None
    return render_template("quiz_detail.html", quiz=quiz)

@views.route('/flashcard')
def flashcard():
    # Get the quiz_id and quiz_title from the URL parameters.
    quiz_id = request.args.get('quiz_id')
    quiz_title = request.args.get('quiz_title', 'Quiz Title')
    
    # Optionally, you can do additional processing here if needed,
    # such as querying Supabase for additional quiz details to pass along.
    
    return render_template('flashcard.html', quiz_id=quiz_id, quiz_title=quiz_title)

@views.route('/api/sets/<int:set_id>', methods=['DELETE'])
@login_required
def delete_set(set_id):
    supabase = current_app.config["SUPABASE_CLIENT"]
    try:
        # check user
        response = supabase.table("flashcard_sets").select("user_id").eq("set_id", set_id).execute()
        if not response.data or response.data[0]["user_id"] != current_user.id:
            return jsonify({"error": "Unauthorized or set not found"}), 403

        # delete
        supabase.table("flashcards").delete().eq("set_id", set_id).execute()
        
        supabase.table("flashcard_sets").delete().eq("set_id", set_id).execute()
        
        return jsonify({"message": "Set deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting set: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@views.route('/api/bookmark_set/<int:set_id>', methods=['POST'])
@login_required
def bookmark_set(set_id):
    supabase = current_app.config["SUPABASE_CLIENT"]
    try:
        flashcards_response = supabase.table("flashcards") \
            .select("flashcard_id") \
            .eq("set_id", set_id) \
            .execute()
        if not flashcards_response.data:
            return jsonify({"error": "No flashcards found in the set"}), 404

        bookmark_inserts = [
            {"user_id": current_user.id, "flashcard_id": fc["flashcard_id"]}
            for fc in flashcards_response.data
        ]
        supabase.table("bookmarks").insert(bookmark_inserts).execute()

        return jsonify({"message": "Set bookmarked successfully"}), 200
    except Exception as e:
        print(f"Error bookmarking set: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@views.route('/api/unbookmark_set/<int:set_id>', methods=['DELETE'])
@login_required
def unbookmark_set(set_id):
    supabase = current_app.config["SUPABASE_CLIENT"]
    try:
        flashcards_response = supabase.table("flashcards") \
            .select("flashcard_id") \
            .eq("set_id", set_id) \
            .execute()
        if not flashcards_response.data:
            return jsonify({"error": "No flashcards found in the set"}), 404

        flashcard_ids = [fc["flashcard_id"] for fc in flashcards_response.data]

        # Delete all bookmarks for these flashcards for the current user
        supabase.table("bookmarks") \
            .delete() \
            .eq("user_id", current_user.id) \
            .in_("flashcard_id", flashcard_ids) \
            .execute()

        return jsonify({"message": "Set unbookmarked successfully"}), 200
    except Exception as e:
        print(f"Error unbookmarking set: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@views.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    supabase = current_app.config["SUPABASE_CLIENT"]

    # Search in the title (you can add more fields if needed)
    response = supabase.table("flashcard_sets") \
        .select("set_id, title, category, created_at, user_id, users(username)") \
        .ilike("title", f"%{query}%") \
        .execute()

    quizzes = response.data if response.data else []
    return render_template("search_results.html", quizzes=quizzes, query=query)

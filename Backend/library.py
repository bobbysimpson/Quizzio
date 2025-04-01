
from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user

library_bp = Blueprint('library', __name__)

@library_bp.route('/library')
@login_required
def library():
    supabase = current_app.config["SUPABASE_CLIENT"]
    response = supabase.table("quizzes").select("*").eq("user_id", current_user.id).execute()
    quizzes = response.data if response.data else []
    return render_template("library.html", quizzes=quizzes)
from flask import Flask
from flask_login import LoginManager
import os
from os import path
from supabase import create_client, Client

def create_app():
    # Calculate the base directory (one level up from the Backend folder)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Create the Flask app with absolute paths for static and template folders
    app = Flask(__name__,
                static_folder=os.path.join(base_dir, 'Frontend', 'static'),
                template_folder=os.path.join(base_dir, 'Frontend', 'templates'))
    
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    
    # Set up Supabase credentials (replace with environment variables in production)
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ymspflrxipjlipncgzyy.supabase.co")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inltc3BmbHJ4aXBqbGlwbmNnenl5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE2OTcxMzYsImV4cCI6MjA1NzI3MzEzNn0.jNFsla4rFX1WWiyS7Iu0GBYQQG8iMv2YLQ-3aHaWRGs")
    
    # Initialize the Supabase client and store it in app config
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    app.config["SUPABASE_CLIENT"] = supabase

    # Register blueprints for your views and authentication routes
    from .views import views
    from .auth import auth
    from .editprofile import editprofile
    from .forgotpass import forgotpass
    from .library import library_bp  # NEW: import the library blueprint

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(editprofile, url_prefix='/')
    app.register_blueprint(forgotpass, url_prefix='/')
    app.register_blueprint(library_bp, url_prefix='/')  # NEW: register library blueprint
    
    # Import the User model to support user loading
    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Access the Supabase client from app config
        supabase = app.config["SUPABASE_CLIENT"]
        # Query the 'users' table by user_id
        response = supabase.table("users").select("*").eq("user_id", user_id).execute()
        if not response.data:
            return None
        user_data = response.data[0]
        return User.from_dict(user_data)
    
    return app
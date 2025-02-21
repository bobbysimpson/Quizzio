
# from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'testtest'
app.config['MYSQL_DB'] = 'sgbsimp2'

mysql = MySQL(app)

#################################
#          USER ROUTES          #
#################################

# Render a simple signup page (if needed)
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    hashed_password = generate_password_hash(password)
    
    try:
        cur = mysql.connection.cursor()
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        cur.execute(query, (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cur = mysql.connection.cursor()
        query = "SELECT user_id, username, password_hash FROM users WHERE username = %s"
        cur.execute(query, (username,))
        user = cur.fetchone()
        cur.close()
        
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        
        user_id, username, password_hash = user
        if check_password_hash(password_hash, password):
            return jsonify({'message': 'Login successful', 'user_id': user_id}), 200
        else:
            return jsonify({'error': 'Invalid password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#################################
#     FLASHCARD SET ROUTES      #
#################################

# Retrieve Public Flashcard Sets
@app.route('/flashcard_sets', methods=['GET'])
def get_flashcard_sets():
    try:
        cur = mysql.connection.cursor()
        query = "SELECT set_id, user_id, title, description, is_public FROM flashcard_sets WHERE is_public = TRUE"
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        
        flashcard_sets = [{
            'set_id': row[0],
            'user_id': row[1],
            'title': row[2],
            'description': row[3],
            'is_public': row[4]
        } for row in result]
        
        return jsonify(flashcard_sets), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create a New Flashcard Set
@app.route('/flashcard_sets', methods=['POST'])
def create_flashcard_set():
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    description = data.get('description', '')
    is_public = data.get('is_public', True)
    
    if not user_id or not title:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        cur = mysql.connection.cursor()
        query = "INSERT INTO flashcard_sets (user_id, title, description, is_public) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (user_id, title, description, is_public))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Flashcard set created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#################################
#       FLASHCARD ROUTES        #
#################################

# Retrieve Flashcards for a Given Set
@app.route('/flashcards/<int:set_id>', methods=['GET'])
def get_flashcards(set_id):
    try:
        cur = mysql.connection.cursor()
        query = "SELECT flashcard_id, question, answer FROM flashcards WHERE set_id = %s"
        cur.execute(query, (set_id,))
        result = cur.fetchall()
        cur.close()
        
        flashcards = [{
            'flashcard_id': row[0],
            'question': row[1],
            'answer': row[2]
        } for row in result]
        
        return jsonify(flashcards), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add a New Flashcard to a Set
@app.route('/flashcards', methods=['POST'])
def add_flashcard():
    data = request.get_json()
    set_id = data.get('set_id')
    question = data.get('question')
    answer = data.get('answer')
    
    if not set_id or not question or not answer:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        cur = mysql.connection.cursor()
        query = "INSERT INTO flashcards (set_id, question, answer) VALUES (%s, %s, %s)"
        cur.execute(query, (set_id, question, answer))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Flashcard added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#################################
#     USER PROGRESS & BOOKMARKS #
#################################

# Record User Progress on a Flashcard
@app.route('/user_progress', methods=['POST'])
def add_user_progress():
    data = request.get_json()
    user_id = data.get('user_id')
    flashcard_id = data.get('flashcard_id')
    is_correct = data.get('is_correct')
    
    if user_id is None or flashcard_id is None or is_correct is None:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        cur = mysql.connection.cursor()
        query = "INSERT INTO user_progress (user_id, flashcard_id, is_correct) VALUES (%s, %s, %s)"
        cur.execute(query, (user_id, flashcard_id, is_correct))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User progress recorded successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add a Bookmark for a Flashcard
@app.route('/bookmarks', methods=['POST'])
def add_bookmark():
    data = request.get_json()
    user_id = data.get('user_id')
    flashcard_id = data.get('flashcard_id')
    
    if not user_id or not flashcard_id:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        cur = mysql.connection.cursor()
        query = "INSERT INTO bookmarks (user_id, flashcard_id) VALUES (%s, %s)"
        cur.execute(query, (user_id, flashcard_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Bookmark added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#################################
#         RUN THE APP           #
#################################
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
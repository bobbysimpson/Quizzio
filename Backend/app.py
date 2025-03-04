from flask import Flask,render_template, request,make_response
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'testtest'
app.config['MYSQL_DB'] = 'sgbsimp2'
 
mysql = MySQL(app)

@app.route('/login.html')
@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('login.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    error = None
    if request.method == 'GET':
        return f"????"
    if request.method == 'POST':
        username = request.form['username']
        password_hash = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT username, password_hash FROM users WHERE username = %s''', [username])
        userRecord = cursor.fetchall()
        if len(userRecord) == 0:
            error = "User does not exist"
        else:
            if password_hash != userRecord[0][1]:
                error = "Incorrect password"
            else:
                resp = make_response()
                resp.set_cookie(username, userRecord[0][0])
                return render_template('index.html', username = userRecord[0][0])
        return render_template('login.html', error=error)

@app.route('/adduser', methods = ['POST', 'GET'])
def adduser():
    error = None
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        username = request.form['username']
        password_hash = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT username, email FROM users WHERE username = %s OR email = %s''', [username, email])
        record = cursor.fetchall()
        if len(record) != 0:
            error = "User already exists"
        else:
            cursor.execute(''' INSERT INTO users (username, password_hash, email) VALUES(%s,%s,%s)''',(username,password_hash, email))
            mysql.connection.commit()
            cursor.close()
            resp = make_response()
            resp.set_cookie(username, username)
            return render_template("index.html", username = username)
        return render_template('login.html', error=error)
app.run(host='localhost', port=5000)
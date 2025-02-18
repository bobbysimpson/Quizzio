from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'testtest'
app.config['MYSQL_DB'] = 'quizziotest'
 
mysql = MySQL(app)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/adduser', methods = ['POST', 'GET'])
def adduser():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO users VALUES(%s,%s,%s)''',(username,password, email))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
 
app.run(host='localhost', port=5000)
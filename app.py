
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import hashlib

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'xyzsdfg'  # Ensure to replace with a strong key in production

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root@123'  # Your MySQL password (empty here for localhost with no password)
app.config['MYSQL_DB'] = 'data'  # Make sure your database name is 'data'

# Initialize MySQL
mysql = MySQL(app)

# Function to hash passwords securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Hash the input password
        hashed_password = hash_password(password)
        
        # Fetch the user based on email and hashed password
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, hashed_password))
        user = cursor.fetchone()
        
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Logged in successfully!'
            return redirect(url_for('user'))
        else:
            message = 'Incorrect email or password!'
    
    return render_template('login.html', message=message)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''  # Corrected typo from 'mesage' to 'message'
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Check if the email already exists
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            # Hash the password before storing
            hashed_password = hash_password(password)
            
            # Insert new user record. Use NULL for `userid` so that MySQL will auto-generate it.
            cursor.execute('INSERT INTO user (name, email, password) VALUES (%s, %s, %s)', (userName, email, hashed_password))
            mysql.connection.commit()
            message = 'You have successfully registered!'
            return redirect(url_for('login'))  # Redirect to login after successful registration
    
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    
    return render_template('register.html', message=message)


@app.route('/user')
def user():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user')
        users = cursor.fetchall()
        return render_template('user.html', users=users)
    return redirect(url_for('login'))  # Redirect to login if not logged in


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

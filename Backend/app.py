from flask import Flask, render_template, request, session, redirect, url_for  
  
app = Flask(__name__)  
app.secret_key = 'secret-key' # this should be a long, random string  
  
# Mock user database  
users = {  
    'john': 'password',  
    'jane': 'password'  
}  
  
# Login route  
@app.route('/login', methods=['GET', 'POST'])  
def login():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password']  
        if username in users and users[username] == password:  
            session['username'] = username  
            return redirect(url_for('dashboard'))  
        else:  
            return render_template('login.html', error='Invalid username or password')  
    else:  
        return render_template('login.html')  
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get data from the form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate the input
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return render_template('register.html')

        # Hash the password
        hashed_password = hash_password(password)

        # Save the user to the database
        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, hashed_password),
            )
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'danger')
        finally:
            conn.close()

    # Render the registration page for GET requests
    return render_template('register.html')

  
# Dashboard route  
@app.route('/dashboard')  
def dashboard():  
    if 'username' in session:  
        username = session['username']  
        return render_template('index.html', username=username)  
    else:  
        return redirect(url_for('login'))  
  
# Logout route  
@app.route('/logout')  
def logout():  
    session.pop('username', None)  
    return redirect(url_for('login'))  
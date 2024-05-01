from flask import Flask, render_template, request, redirect, session, jsonify
from database_connection import db_connect
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a secure secret key

# Establish database connection
db = db_connect()
cursor = db.cursor()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        position = request.form['position']
        number = request.form['number']
        
        # Save player data to the database
        cursor.execute("INSERT INTO players (firstname, lastname, email, password, position, number) VALUES (%s, %s, %s, %s, %s, %s)",
                       (firstname, lastname, email, password, position, number))
        db.commit()
        return redirect('/login')  # Redirect to login page after registration
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check if player exists in the database
        cursor.execute("SELECT * FROM players WHERE email = %s AND password = %s", (email, password))
        player = cursor.fetchone()
        if player:
            session['email'] = email
            return redirect('/player_list')  # Redirect to player list page
        else:
            return "Invalid email or password"
    return render_template('login.html')

@app.route('/player_list')
def player_list():
    if 'email' not in session:
        return redirect('/login')
    # Fetch player details from the database
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    return render_template('player_list.html', players=players)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

@app.route('/delete_player/<email>', methods=['POST'])
def delete_player(email):
    if 'email' not in session or session['email'] != email:
        return jsonify({'error': 'Unauthorized access!'}), 401
    try:
        # Delete the player from the database
        cursor.execute("DELETE FROM players WHERE email = %s", (email,))
        db.commit()
        # Return a success response
        return jsonify({'success': True}), 200
    except Exception as e:
        # Return an error response if deletion fails
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

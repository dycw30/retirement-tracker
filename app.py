from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mysecret')

# Database connection (PostgreSQL via Railway)
def get_db_connection():
    return psycopg2.connect(
        dbname=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        host=os.environ['PGHOST'],
        port=os.environ['PGPORT']
    )

# ------------------------- Routes -------------------------
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and check_password_hash(user[0], password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, category, activity, objective, frequency, notes, rating, last_updated FROM goals ORDER BY category")
    goals = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('dashboard.html', goals=goals)

@app.route('/update', methods=['POST'])
def update():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    goal_id = request.form['goal_id']
    notes = request.form['notes']
    rating = request.form['rating']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE goals SET notes = %s, rating = %s, last_updated = %s WHERE id = %s
    """, (notes, rating, timestamp, goal_id))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

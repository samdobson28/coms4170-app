import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_journey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load quiz data from JSON file
def load_quiz_data():
    try:
        with open('static/data/quiz.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        app.logger.error(f"Error loading quiz data: {str(e)}")
        return None

QUIZ_DATA = load_quiz_data()

# Database Models
class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_part = db.Column(db.String(10), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class SavedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(50), nullable=False)
    item_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Load data
with open('static/data/lessons.json') as f:
    data = json.load(f)
    foods = data['foods']
    phrases = data['phrases']
    places = data['places']

# Database setup
def init_db():
    conn = sqlite3.connect('user_progress.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_answers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question_id TEXT,
                  answer TEXT,
                  is_correct INTEGER,
                  timestamp DATETIME)''')
    c.execute('''CREATE TABLE IF NOT EXISTS page_visits
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  page TEXT,
                  timestamp DATETIME)''')
    c.execute('''CREATE TABLE IF NOT EXISTS saved_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  item_type TEXT,
                  item_id TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('user_progress.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/learn/<section>')
def learn(section):
    # Record page visit
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO page_visits (page, timestamp) VALUES (?, ?)',
              (f'learn/{section}', datetime.now()))
    conn.commit()
    conn.close()

    if section == 'culture':
        return render_template('culture.html', foods=foods)
    elif section == 'language':
        return render_template('language.html')
    elif section == 'map':
        return render_template('map.html', places=places)
    else:
        return redirect(url_for('home'))

@app.route('/food/<food_id>')
def food_details(food_id):
    food = next((f for f in foods if f['id'] == food_id), None)
    if food:
        return render_template('food_details.html', food=food)
    return redirect(url_for('culture'))

@app.route('/quiz')
@app.route('/quiz/<int:question_number>')
def quiz(question_number=1):
    # Record page visit
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO page_visits (page, timestamp) VALUES (?, ?)',
              (f'quiz/{question_number}', datetime.now()))
    conn.commit()
    conn.close()

    if not QUIZ_DATA:
        return render_template('error.html', message="Quiz data is currently unavailable. Please try again later."), 503
    
    # Ensure question_number is within bounds
    total_questions = len(QUIZ_DATA['questions'])
    if question_number < 1:
        return redirect(url_for('quiz', question_number=1))
    elif question_number > total_questions:
        return redirect(url_for('quiz', question_number=total_questions))
    
    return render_template('quiz.html', 
                         quiz_data=QUIZ_DATA,
                         current_question=question_number,
                         total_questions=total_questions)

@app.route('/quiz/part1')
def quiz_part1():
    if not QUIZ_DATA or 'part1' not in QUIZ_DATA:
        return render_template('error.html', message="Quiz part 1 is currently unavailable. Please try again later."), 503
    return render_template('quiz.html', quiz_data=QUIZ_DATA['part1'])

@app.route('/quiz/part2')
def quiz_part2():
    if not QUIZ_DATA or 'part2' not in QUIZ_DATA:
        return render_template('error.html', message="Quiz part 2 is currently unavailable. Please try again later."), 503
    return render_template('quiz.html', quiz_data=QUIZ_DATA['part2'])

@app.route('/save_quiz_answer', methods=['POST'])
def save_quiz_answer():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO quiz_answers (question_id, answer, is_correct, timestamp) VALUES (?, ?, ?, ?)',
              (data['question_id'], str(data['answer']), data['is_correct'], datetime.now()))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/save_item', methods=['POST'])
def save_item():
    try:
        data = request.get_json()
        item_type = data.get('type')
        item_id = data.get('id')
        
        if not item_type or not item_id:
            return jsonify({'error': 'Invalid data provided'}), 400
        
        conn = get_db()
        c = conn.cursor()
        c.execute('INSERT INTO saved_items (item_type, item_id, timestamp) VALUES (?, ?, ?)',
                  (item_type, item_id, datetime.now()))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Item saved successfully'})
    except Exception as e:
        app.logger.error(f"Error saving item: {str(e)}")
        return jsonify({'error': 'Failed to save item'}), 500

@app.route('/guidebook')
def guidebook():
    # Record page visit
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO page_visits (page, timestamp) VALUES (?, ?)',
              ('guidebook', datetime.now()))
    conn.commit()
    
    # Get saved items
    c.execute('SELECT * FROM saved_items')
    saved_items = c.fetchall()
    conn.close()

    saved_foods = [f for f in foods if f['id'] in [i['item_id'] for i in saved_items if i['item_type'] == 'food']]
    saved_phrases = [p for p in phrases if p['spanish'] in [i['item_id'] for i in saved_items if i['item_type'] == 'phrase']]
    saved_places = []
    for category in places.values():
        saved_places.extend([p for p in category if p['name'] in [i['item_id'] for i in saved_items if i['item_type'] == 'place']])
    
    return render_template('guidebook.html',
                         foods=saved_foods,
                         phrases=saved_phrases,
                         places=saved_places)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', message="An internal server error occurred"), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
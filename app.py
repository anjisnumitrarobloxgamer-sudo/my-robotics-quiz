import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Secret key required to keep admin login sessions secure
app.secret_key = "super_secret_quiz_key_123"

# Render provides a permanent hard drive folder called '/data/' if you attach a disk.
# If running locally on your computer, it saves to your current folder.
if os.path.exists("/data"):
    QUESTIONS_FILE = "/data/robotics_quiz.json"
else:
    QUESTIONS_FILE = "robotics_quiz.json"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "robotics2026"

# Base default questions if the storage file is empty
DEFAULT_QUESTIONS = [
    {"id": 0, "question": "Which keyword is used to define a function in Python?", "options": ["func", "define", "def", "lambda"], "correct": "def"},
    {"id": 1, "question": "What does 'AI' stand for?", "options": ["Automated Internet", "Artificial Intelligence", "Advanced Integration", "Algorithmic Index"], "correct": "Artificial Intelligence"}
]

def load_questions():
    """Loads questions from our permanent storage file."""
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r") as file:
                return json.load(file)
        except Exception:
            return DEFAULT_QUESTIONS
    return DEFAULT_QUESTIONS

def save_questions(questions_list):
    """Saves updated questions permanently."""
    with open(QUESTIONS_FILE, "w") as file:
        json.dump(questions_list, file, indent=4)

@app.route('/')
def home():
    questions = load_questions()
    return render_template('quiz.html', quiz=questions)

@app.route('/submit', methods=['POST'])
def submit():
    questions = load_questions()
    score = 0
    total = len(questions)
    user_answers = {}
    
    for item in questions:
        question_id = str(item["id"])
        selected_option = request.form.get(question_id)
        user_answers[item["id"]] = selected_option
        if selected_option == item["correct"]:
            score += 1

    return render_template('result.html', score=score, total=total, quiz=questions, answers=user_answers)

# --- NEW ADMIN PANEL ROUTES ---

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # If already logged in, show the question manager dashboard
    if session.get('logged_in'):
        questions = load_questions()
        return render_template('admin.html', quiz=questions)
        
    # Handle Login Form submission
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Invalid Credentials!")
            
    return render_template('login.html')

@app.route('/admin/add', methods=['POST'])
def add_question():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
        
    questions = load_questions()
    
    # Calculate next clean ID number
    next_id = max([q["id"] for q in questions]) + 1 if questions else 0
    
    new_q = {
        "id": next_id,
        "question": request.form.get('question'),
        "options": [
            request.form.get('option1'),
            request.form.get('option2'),
            request.form.get('option3'),
            request.form.get('option4')
        ],
        "correct": request.form.get('correct')
    }
    
    questions.append(new_q)
    save_questions(questions)
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:q_id>')
def delete_question(q_id):
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
        
    questions = load_questions()
    # Keep all questions except the one we want to delete
    questions = [q for q in questions if q["id"] != q_id]
    save_questions(questions)
    return redirect(url_for('admin'))

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)


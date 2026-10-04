import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Secret key required to keep admin login sessions secure
app.secret_key = "super_secret_quiz_key_123"

# Render provides a permanent hard drive folder called '/data/' if you attach a disk.
if os.path.exists("/data"):
    QUESTIONS_FILE = "/data/robotics_quiz.json"
else:
    QUESTIONS_FILE = "robotics_quiz.json"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "robotics2026"

# Pre-loaded with your 20 custom technical questions!
DEFAULT_QUESTIONS = [
    # --- PYTHON QUESTIONS ---
    {"id": 0, "question": "Which keyword is used to define a function in Python?", "options": ["func", "define", "def", "lambda"], "correct": "def"},
    {"id": 1, "question": "What is the correct file extension for Python files?", "options": [".pt", ".py", ".pyt", ".pyw"], "correct": ".py"},
    {"id": 2, "question": "Which data type is used to store a sequence of true or false values?", "options": ["String", "Integer", "Boolean", "Float"], "correct": "Boolean"},
    {"id": 3, "question": "How do you start a single-line comment in Python?", "options": ["//", "/*", "#", "--"], "correct": "#"},
    {"id": 4, "question": "Which of these is used to add an item to the end of a list?", "options": ["add()", "append()", "insert()", "extend()"], "correct": "append()"},
    {"id": 5, "question": "What does the len() function do in Python?", "options": ["Changes case", "Generates numbers", "Counts list items/characters", "Deletes data"], "correct": "Counts list items/characters"},
    
    # --- ARTIFICIAL INTELLIGENCE QUESTIONS ---
    {"id": 6, "question": "What does 'AI' stand for?", "options": ["Automated Internet", "Artificial Intelligence", "Advanced Integration", "Algorithmic Index"], "correct": "Artificial Intelligence"},
    {"id": 7, "question": "What type of learning uses labeled training data?", "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Deep Learning"], "correct": "Supervised Learning"},
    {"id": 8, "question": "What is the name of the test used to determine if a machine can think like a human?", "options": ["Turing Test", "Einstein Test", "Tesla Test", "Binary Test"], "correct": "Turing Test"},
    {"id": 9, "question": "Which neural network architecture is famously used for analyzing images?", "options": ["RNN", "CNN", "LSTM", "GAN"], "correct": "CNN"},
    {"id": 10, "question": "What is the primary goal of Machine Learning?", "options": ["To build faster hardware", "To let computers learn from data without explicit programming", "To make web pages look modern", "To secure cloud storage networks"], "correct": "To let computers learn from data without explicit programming"},
    {"id": 11, "question": "What does 'NLP' stand for in AI engineering?", "options": ["Network Layer Protocol", "Natural Language Processing", "Neural Logical Program", "Node Location Point"], "correct": "Natural Language Processing"},
    {"id": 12, "question": "Which math field is most critical for adjusting weights in deep learning?", "options": ["Calculus", "Geometry", "Trigonometry", "Algebra"], "correct": "Calculus"},

    # --- ROBOTICS QUESTIONS ---
    {"id": 13, "question": "What is the primary purpose of an 'actuator' in a robot?", "options": ["To process sensory information", "To move or control a mechanism", "To store backup battery power", "To write data logs"], "correct": "To move or control a mechanism"},
    {"id": 14, "question": "What type of sensor helps a robot measure distance using high-frequency sound waves?", "options": ["Infrared Sensor", "Ultrasonic Sensor", "Gyroscope", "Lidar"], "correct": "Ultrasonic Sensor"},
    {"id": 15, "question": "What does 'DOF' stand for in robotics movement?", "options": ["Direction of Flight", "Degrees of Freedom", "Depth of Field", "Digital Output Frame"], "correct": "Degrees of Freedom"},
    {"id": 16, "question": "Which framework is a popular open-source middleware used for writing robot software?", "options": ["ROS (Robot Operating System)", "Linux-Bot", "RoboCraft", "Flask-Bot"], "correct": "ROS (Robot Operating System)"},
    {"id": 17, "question": "What robot component acts like its 'eyes' or 'ears' to gather information from the environment?", "options": ["Actuator", "Sensor", "Microcontroller", "Chassis"], "correct": "Sensor"},
    {"id": 18, "question": "What is a robot arm's 'hand' or claw mechanism technically called?", "options": ["Linkage", "Joint", "End Effector", "Manipulator"], "correct": "End Effector"},
    {"id": 19, "question": "Which component functions as the main administrative 'brain' of a simple small-scale hobbyist robot?", "options": ["Battery Pack", "Microcontroller", "DC Motor", "Gearbox"], "correct": "Microcontroller"}
]

def load_questions():
    """Loads questions from permanent storage file, falls back to our 20 default questions if empty."""
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

# --- ADMIN PANEL ROUTES ---

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('logged_in'):
        questions = load_questions()
        return render_template('admin.html', quiz=questions)
        
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
    questions = [q for q in questions if q["id"] != q_id]
    save_questions(questions)
    return redirect(url_for('admin'))

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)



from flask import Flask, render_template, request

app = Flask(__name__)

# 20 High-Quality Questions about Robotics, AI, and Python built right into the code!
QUIZ_DATA = [
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

@app.route('/')
def home():
    # Feeds the fixed 20 questions directly to the web view
    return render_template('quiz.html', quiz=QUIZ_DATA)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    total = len(QUIZ_DATA)
    user_answers = {}
    
    for item in QUIZ_DATA:
        question_id = str(item["id"])
        selected_option = request.form.get(question_id)
        user_answers[item["id"]] = selected_option
        if selected_option == item["correct"]:
            score += 1

    return render_template('result.html', score=score, total=total, quiz=QUIZ_DATA, answers=user_answers)

if __name__ == '__main__':
    app.run(debug=True)

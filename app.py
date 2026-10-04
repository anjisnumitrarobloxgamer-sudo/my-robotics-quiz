import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Secret key required to keep user login sessions secure
app.secret_key = "super_secure_5_subjects_key_2026_final"

# Determine path for the persistent SQLite Database file on Render
if os.path.exists("/data"):
    DB_FILE = "/data/quiz_platform.db"
else:
    DB_FILE = "quiz_platform.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the secure user registration tracking table inside SQLite."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database file right away
init_db()

# COMPREHENSIVE 5-SUBJECT COURSE LIBRARY (EXACTLY 20 HARD QUESTIONS EACH)
SUBJECT_QUIZZES = {
    "cricket": [
        {"id": 0, "question": "Who scored the first-ever double century in One Day International (ODI) cricket history?", "options": ["Sachin Tendulkar", "Virender Sehwag", "Rohit Sharma", "Chris Gayle"], "correct": "Sachin Tendulkar"},
        {"id": 1, "question": "What is the standard weight range of a men's professional cricket ball?", "options": ["4.75 to 5.25 ounces", "5.5 to 5.75 ounces", "5.0 to 5.5 ounces", "5.75 to 6.25 ounces"], "correct": "5.5 to 5.75 ounces"},
        {"id": 2, "question": "Which bowler holds the record for taking the most wickets in Test match cricket history?", "options": ["Shane Warne", "Muttiah Muralitharan", "James Anderson", "Anil Kumble"], "correct": "Muttiah Muralitharan"},
        {"id": 3, "question": "What is the standard length of a professional cricket pitch between the two sets of wickets?", "options": ["20 yards", "22 yards", "24 yards", "18 yards"], "correct": "22 yards"},
        {"id": 4, "question": "Which country won the inaugural ICC T20 World Cup tournament back in 2007?", "options": ["India", "Pakistan", "Australia", "West Indies"], "correct": "India"},
        {"id": 5, "question": "What is the maximum allowed width of a standard professional cricket bat?", "options": ["4.25 inches", "4.5 inches", "4.0 inches", "4.75 inches"], "correct": "4.25 inches"},
        {"id": 6, "question": "Who is the only player to score 400 runs in a single innings of a Test match?", "options": ["Brian Lara", "Don Bradman", "Matthew Hayden", "Mahela Jayawardene"], "correct": "Brian Lara"},
        {"id": 7, "question": "Which umpire is famously known for his signature 'crooked finger' out signal style?", "options": ["Billy Bowden", "Steve Bucknor", "Aleem Dar", "David Shepherd"], "correct": "Billy Bowden"},
        {"id": 8, "question": "What term describes a batsman being dismissed because they obstructed the field defensively?", "options": ["Obstructing the field", "Timed out", "Hit the ball twice", "Handling the ball"], "correct": "Obstructing the field"},
        {"id": 9, "question": "Which bowler has taken the fastest 300 wickets in Test cricket history (in terms of matches)?", "options": ["Ravichandran Ashwin", "Dennis Lillee", "Muttiah Muralitharan", "Dale Steyn"], "correct": "Ravichandran Ashwin"},
        {"id": 10, "question": "What is the maximum height allowed for a cricket stump above the ground?", "options": ["28 inches", "30 inches", "26 inches", "32 inches"], "correct": "28 inches"},
        {"id": 11, "question": "Which ground is universally referred to as the historic 'Home of Cricket'?", "options": ["Lord's Cricket Ground", "Melbourne Cricket Ground", "Eden Gardens", "The Oval"], "correct": "Lord's Cricket Ground"},
        {"id": 12, "question": "Who was the captain of the Indian cricket team during their historic 1983 World Cup victory?", "options": ["Kapil Dev", "Sunil Gavaskar", "Ravi Shastri", "Mohinder Amarnath"], "correct": "Kapil Dev"},
        {"id": 13, "question": "How many minutes does an incoming batsman get to arrive at the crease before being declared 'Timed Out'?", "options": ["3 minutes", "2 minutes", "5 minutes", "4 minutes"], "correct": "3 minutes"},
        {"id": 14, "question": "Which fielding position stands directly behind the batsman on the off side to catch deflections?", "options": ["Slip", "Gully", "Point", "Cover"], "correct": "Slip"},
        {"id": 15, "question": "Who holds the record for scoring the fastest century in ODI history in 31 balls?", "options": ["AB de Villiers", "Corey Anderson", "Shahid Afridi", "Glenn Maxwell"], "correct": "AB de Villiers"},
        {"id": 16, "question": "What technology tracks the trajectory of a moving ball for LBW reviews?", "options": ["Hawk-Eye", "Snickometer", "Hot Spot", "LED Stumps"], "correct": "Hawk-Eye"},
        {"id": 17, "question": "Which country won three consecutive ICC Cricket World Cups between 1999 and 2007?", "options": ["Australia", "India", "West Indies", "Sri Lanka"], "correct": "Australia"},
        {"id": 18, "question": "What term describes a bowler delivering a ball that bounces cleanly above the batsman's waist line height without pitching?", "options": ["Beamer", "Bouncer", "Yorker", "Full Toss"], "correct": "Beamer"},
        {"id": 19, "question": "Who is the legendary Australian cricketer famously known to have finished his career with a Test batting average of 99.94?", "options": ["Don Bradman", "Ricky Ponting", "Shane Warne", "Allan Border"], "correct": "Don Bradman"}
    ],
    "science": [
        {"id": 0, "question": "What is the approximate speed of light travelling through a complete space vacuum environment?", "options": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"], "correct": "300,000 km/s"},
        {"id": 1, "question": "Which chemical element holds the absolute lowest atomic weight number on the Periodic Table layout?", "options": ["Hydrogen", "Helium", "Lithium", "Oxygen"], "correct": "Hydrogen"},
        {"id": 2, "question": "What primary gas compound makes up the absolute largest percentage share of Earth's atmosphere?", "options": ["Nitrogen", "Oxygen", "Carbon Dioxide", "Argon"], "correct": "Nitrogen"},
        {"id": 3, "question": "Which planet holds the title of the densest and largest rock-based planet inside our Solar System?", "options": ["Earth", "Mars", "Venus", "Mercury"], "correct": "Earth"},
        {"id": 4, "question": "What basic unit scales evaluate absolute zero thermal energy baseline registers?", "options": ["Kelvin", "Celsius", "Fahrenheit", "Rankine"], "correct": "Kelvin"},
        {"id": 5, "question": "What core component particles carry negative electrical charges inside atomic structure clouds?", "options": ["Electrons", "Protons", "Neutrons", "Quarks"], "correct": "Electrons"},
        {"id": 6, "question": "Which rock category forms directly from cooled volcanic magma or lava flow collections?", "options": ["Igneous", "Sedimentary", "Metamorphic", "Basaltic"], "correct": "Igneous"},
        {"id": 7, "question": "What force prevents objects from floating off into space, holding planets in orbital paths?", "options": ["Gravity", "Magnetism", "Friction", "Centrifugal Force"], "correct": "Gravity"},
        {"id": 8, "question": "Which layer of Earth's atmosphere contains the vital ozone layer block filter?", "options": ["Stratosphere", "Troposphere", "Mesosphere", "Thermosphere"], "correct": "Stratosphere"},
        {"id": 9, "question": "What process describes a solid changing directly into a gas phase, skipping the liquid state?", "options": ["Sublimation", "Evaporation", "Condensation", "Melting"], "correct": "Sublimation"},
        {"id": 10, "question": "Which gland inside the human body is frequently referred to as the master system endocrine director?", "options": ["Pituitary Gland", "Thyroid Gland", "Adrenal Gland", "Pancreas"], "correct": "Pituitary Gland"},
        {"id": 11, "question": "What is the chemical formula for standard hydrogen peroxide disinfectant compounds?", "options": ["H2O2", "H2O", "HO2", "H3O"], "correct": "H2O2"},
        {"id": 12, "question": "Which subatomic particles are composed of combinations of fundamental elements named quarks?", "options": ["Protons and Neutrons", "Electrons", "Photons", "Neutrinos"], "correct": "Protons and Neutrons"},
        {"id": 13, "question": "What law states that an object at rest will remain at rest unless acted upon by an external force?", "options": ["Newton's First Law", "Newton's Second Law", "Newton's Third Law", "Law of Thermodynamics"], "correct": "Newton's First Law"},
        {"id": 14, "question": "Which wave variant requires a physical material substance medium to propagate across spaces?", "options": ["Mechanical Wave", "Electromagnetic Wave", "Light Wave", "Radio Wave"], "correct": "Mechanical Wave"},
        {"id": 15, "question": "What chemical element is represented by the uppercase symbol 'K' on the Periodic Table?", "options": ["Potassium", "Krypton", "Calcium", "Phosphorus"], "correct": "Potassium"},
        {"id": 16, "question": "What process occurs when unstable atomic nuclei lose energy by emitting ionizing particles?", "options": ["Radioactive Decay", "Nuclear Fusion", "Chemical Synthesis", "Ionization"], "correct": "Radioactive Decay"},
        {"id": 17, "question": "Which planet is the hottest in our Solar System due to a dense, runaway greenhouse gas atmosphere?", "options": ["Venus", "Mercury", "Mars", "Jupiter"], "correct": "Venus"},
        {"id": 18, "question": "What values represent absolute neutral parameters on standard logarithmic pH scaling arrays?", "options": ["7", "0", "14", "5"], "correct": "7"},
        {"id": 19, "question": "What force opposes the relative motion of solid surfaces sliding against one another?", "options": ["Friction", "Inertia", "Tension", "Elasticity"], "correct": "Friction"}
    ],



"math": [
{"id": 0, "question": "What is the numerical value of the mathematical constant pi rounded to four decimal places?", "options": ["3.1416", "3.1412", "3.1418", "3.1420"], "correct": "3.1416"},
{"id": 1, "question": "What is the total sum of all interior angles inside a standard geometric hexagon shape?", "options": ["720 degrees", "540 degrees", "360 degrees", "900 degrees"], "correct": "720 degrees"},
{"id": 2, "question": "Which formula is used to solve for the hypotenuse side length of a right-angled triangle framework?", "options": ["Pythagorean Theorem", "Quadratic Formula", "Euler's Formula", "Sine Rule"], "correct": "Pythagorean Theorem"},
{"id": 3, "question": "What mathematical field uses derivatives and integrals to analyze dynamic rates of change?", "options": ["Calculus", "Algebra", "Topology", "Statistics"], "correct": "Calculus"},
{"id": 4, "question": "What is the exact square root value of the integer number 225?", "options": ["15", "13", "25", "12"], "correct": "15"},
{"id": 5, "question": "Which term describes a whole number greater than 1 that has no positive divisors other than 1 and itself?", "options": ["Prime Number", "Composite Number", "Integer", "Rational Number"], "correct": "Prime Number"},
{"id": 6, "question": "What is the value of any non-zero real number raised to the exponential power of 0?", "options": ["1", "0", "Infinity", "Undefined"], "correct": "1"},
{"id": 7, "question": "What type of triangle features three completely unequal side lengths and angles?", "options": ["Scalene Triangle", "Isosceles Triangle", "Equilateral Triangle", "Right Triangle"], "correct": "Scalene Triangle"},
{"id": 8, "question": "What formula resolves equations structured in the standard layout format ax² + bx + c = 0?", "options": ["Quadratic Formula", "Binomial Theorem", "Determinant Method", "Logarithmic Law"], "correct": "Quadratic Formula"},
{"id": 9, "question": "Which Greek mathematician is widely honored as the definitive historical 'Father of Geometry'?", "options": ["Euclid", "Pythagoras", "Archimedes", "Aristotle"], "correct": "Euclid"},
{"id": 10, "question": "What statistical value represents the exact middle number inside a sequentially sorted dataset array?", "options": ["Median", "Mean", "Mode", "Variance"], "correct": "Median"},
{"id": 11, "question": "What geometric term defines a straight line segment that connects two border points of a circle while crossing through its center?", "options": ["Diameter", "Radius", "Chord", "Tangent"], "correct": "Diameter"},
{"id": 12, "question": "What is the logarithm value of 1000 calculated using a base number of 10?", "options": ["3", "2", "4", "10"], "correct": "3"},
{"id": 13, "question": "What geometric shape parameters scale by squaring a radius value and multiplying by pi?", "options": ["Area of a Circle", "Circumference of a Circle", "Volume of a Sphere", "Surface Area of a Cylinder"], "correct": "Area of a Circle"},
{"id": 14, "question": "Which term describes angles whose exact sum combines together to equal exactly 90 degrees?", "options": ["Complementary Angles", "Supplementary Angles", "Obtuse Angles", "Reflex Angles"], "correct": "Complementary Angles"},
{"id": 15, "question": "What is the factorial value calculation output of the integer number 5 (written as 5!)?", "options": ["120", "60", "24", "100"], "correct": "120"},
{"id": 16, "question": "Which line segment shares only one exact touch coordinate point along a circle's outer curvature boundary?", "options": ["Tangent Line", "Secant Line", "Chord", "Radius"], "correct": "Tangent Line"},
{"id": 17, "question": "What algebraic matrix calculation scales output vectors away from zero space parameters?", "options": ["Determinant", "Transpose", "Inverse Matrix", "Dot Product"], "correct": "Determinant"},
{"id": 18, "question": "What mathematical law balances operations across statements using parentheses, exponents, multiplication, division, addition, subtraction?", "options": ["Order of Operations", "Commutative Property", "Distributive Law", "Associative Rule"], "correct": "Order of Operations"},
{"id": 19, "question": "What branch of mathematics analyzes shapes, spaces, and the properties that remain unchanged under continuous deformations?", "options": ["Topology", "Trigonometry", "Calculus", "Arithmetic"], "correct": "Topology"}
],
"robotics_ai": [
{"id": 0, "question": "Which framework is a popular open-source middleware used globally for writing modular robot software ecosystems?", "options": ["ROS (Robot Operating System)", "Linux-Bot", "RoboCraft", "Flask-Bot"], "correct": "ROS (Robot Operating System)"},
{"id": 1, "question": "Which mathematical technique is primarily used to adjust weights and biases back through layers in deep neural networks?", "options": ["Backpropagation", "Linear Regression", "Matrix Inversion", "Fourier Transform"], "correct": "Backpropagation"},
{"id": 2, "question": "What neural network architecture uses recurrence and gates like LSTM to process sequential text data streams?", "options": ["RNN", "CNN", "GAN", "Transformer"], "correct": "RNN"},
{"id": 3, "question": "What robot component functions as its physical 'hand' or mechanical gripping mechanism tool?", "options": ["End Effector", "Actuator", "Chassis", "Sensor"], "correct": "End Effector"},
{"id": 4, "question": "Which Python keyword is explicitly reserved to generate a generator function stream instead of returning a static value?", "options": ["yield", "return", "lambda", "global"], "correct": "yield"},
{"id": 5, "question": "What algorithm utilizes probability graphs to predict hidden state trajectories in simultaneous localization and mapping (SLAM)?", "options": ["Extended Kalman Filter", "A* Search", "Dijkstra Algorithm", "Gradient Descent"], "correct": "Extended Kalman Filter"},
{"id": 6, "question": "Which term describes the number of independent parameters or directions a robot mechanism can safely move within?", "options": ["Degrees of Freedom", "Actuation Ratio", "Kinematic Axis", "Linkage Count"], "correct": "Degrees of Freedom"},
{"id": 7, "question": "What subfield of AI focuses on enabling machines to comprehend, parse, and process structural human languages?", "options": ["NLP", "Computer Vision", "Reinforcement Learning", "Expert Systems"], "correct": "NLP"},
{"id": 8, "question": "Which type of machine learning lets an agent discover ideal behaviors using rewards and structural punishments?", "options": ["Reinforcement Learning", "Supervised Learning", "Unsupervised Learning", "Clustering"], "correct": "Reinforcement Learning"},
{"id": 9, "question": "What is the primary function of a convolutional layer inside a CNN image analysis network framework?", "options": ["Feature Extraction", "Data Flattening", "Weight Initialization", "Dimensionality Expansion"], "correct": "Feature Extraction"},
{"id": 10, "question": "Which metric evaluates structural model errors by computing squared distances between coordinates?", "options": ["Mean Squared Error", "Cross-Entropy Loss", "F1 Score", "Accuracy"], "correct": "Mean Squared Error"},
{"id": 11, "question": "Which hardware processor is uniquely optimized for running heavy matrix-multiplication operations in parallel AI algorithms?", "options": ["GPU", "CPU", "Hard Drive", "Sound Card"], "correct": "GPU"},
{"id": 12, "question": "What problem occurs when an AI model memorizes training data so perfectly that it fails on fresh incoming data sets?", "options": ["Overfitting", "Underfitting", "Data Leakage", "Bias Drift"], "correct": "Overfitting"},
{"id": 13, "question": "What sensor uses laser light reflections to accurately map out physical environments in 3D cloud spaces?", "options": ["Lidar", "Ultrasonic Sensor", "Infrared Sensor", "Barometer"], "correct": "Lidar"},
{"id": 14, "question": "What component translates electronic signals into physical motor forces, acting as the muscles of a robot?", "options": ["Actuator", "Microcontroller", "Sensor", "Bus Transceiver"], "correct": "Actuator"},
{"id": 15, "question": "Which activation function outputs values strictly between 0 and 1, mapping features onto binary probabilities?", "options": ["Sigmoid", "ReLU", "Tanh", "Softmax"], "correct": "Sigmoid"},
{"id": 16, "question": "What optimization method uses derivatives to find the lowest error point on a neural loss surface topology?", "options": ["Gradient Descent", "Random Search", "Binary Partitioning", "Matrix Expansion"], "correct": "Gradient Descent"},
{"id": 17, "question": "Which Python library provides highly optimized multidimensional array operations critical for AI data math packages?", "options": ["NumPy", "Flask", "Django", "Requests"], "correct": "NumPy"},
{"id": 18, "question": "What concept ensures that a robotic arm can calculate exactly where its joints must rotate to reach a static 3D target coordinate?", "options": ["Inverse Kinematics", "Forward Kinematics", "Dead Reckoning", "Telemetry Scaling"], "correct": "Inverse Kinematics"},
{"id": 19, "question": "What is the main objective of unsupervised machine learning clustering algorithms?", "options": ["To group unlabeled data by hidden patterns", "To predict continuous target variables", "To classify text onto labels", "To secure server databases"], "correct": "To group unlabeled data by hidden patterns"}
],
"java": [
{"id": 0, "question": "What memory area handles object allocations in Java?", "options": ["Heap Space", "Stack Memory", "Method Area", "Register Cache"], "correct": "Heap Space"},

{"id": 1, "question": "Which keyword prevents a class from being inherited or sub-classed by another class?", "options": ["final", "static", "abstract", "private"], "correct": "final"},
{"id": 2, "question": "Which interface must a class implement to allow its instances to be sorted using Collections.sort()?", "options": ["Comparable", "Comparator", "Serializable", "Cloneable"], "correct": "Comparable"},
{"id": 3, "question": "What exception is thrown when a program tries to access an object reference that hasn't been initialized?", "options": ["NullPointerException", "ArrayIndexOutOfBoundsException", "IllegalArgumentException", "IOException"], "correct": "NullPointerException"},
{"id": 4, "question": "Which collection class guarantees insertion order maintenance using an underlying linked chain?", "options": ["LinkedHashSet", "HashSet", "TreeSet", "ArrayList"], "correct": "LinkedHashSet"},
{"id": 5, "question": "What mechanism allows a subclass to provide a specific implementation of a method already defined in its superclass?", "options": ["Method Overriding", "Method Overloading", "Encapsulation", "Polymorphism"], "correct": "Method Overriding"},
{"id": 7, "question": "Which block guarantees execution regardless of whether an exception is thrown or caught during a try cycle?", "options": ["finally", "catch", "throw", "finalized"], "correct": "finally"},
{"id": 6, "question": "Which keyword is used to establish an inheritance relationship between classes in Java?", "options": ["extends", "implements", "inherits", "super"], "correct": "extends"},
{"id": 8, "question": "What data structure handles execution tracking and local primitive variable storage for methods?", "options": ["Stack Memory", "Heap Space", "Garbage Collector", "PermGen"], "correct": "Stack Memory"},
{"id": 9, "question": "Which keyword forces a method or variable to belong to the class itself rather than individual instances?", "options": ["static", "public", "volatile", "transient"], "correct": "static"},
{"id": 10, "question": "Which design mechanism allows code packages to bundle variables and methods together while hiding internal details?", "options": ["Encapsulation", "Inheritance", "Abstraction", "Overloading"], "correct": "Encapsulation"},
{"id": 11, "question": "What background thread automatically reclaims memory by deleting unreferenced objects?", "options": ["Garbage Collector", "Compiler", "JVM Monitor", "Defragmenter"], "correct": "Garbage Collector"},
{"id": 12, "question": "Which modifier allows variables to be accessed only within the exact same class definition boundaries?", "options": ["private", "protected", "public", "default"], "correct": "private"},
{"id": 13, "question": "What is the primary purpose of the 'super' keyword inside a subclass constructor function?", "options": ["To call the parent class constructor", "To initialize static attributes", "To destroy duplicate references", "To throw custom exceptions"], "correct": "To call the parent class constructor"},
{"id": 14, "question": "Which container utility provides a thread-safe implementation of a map without locking the entire structure?", "options": ["ConcurrentHashMap", "HashMap", "Hashtable", "TreeMap"], "correct": "ConcurrentHashMap"},
{"id": 15, "question": "What concept describes creating multiple methods in the same class with identical names but different parameter lists?", "options": ["Method Overloading", "Method Overriding", "Dynamic Binding", "Interface Mapping"], "correct": "Method Overloading"},
{"id": 16, "question": "Which keyword identifies variables that should be skipped during object serialization sequences?", "options": ["transient", "volatile", "synchronized", "native"], "correct": "transient"},
{"id": 17, "question": "What runtime environment tool interprets Java bytecodes so they can execute on local operating systems?", "options": ["JVM", "JDK", "JRE", "JVC"], "correct": "JVM"},
{"id": 18, "question": "Which operator performs an explicit type check to confirm whether an object belongs to a specific class layout?", "options": ["instanceof", "typeof", "is", "cast"], "correct": "instanceof"},
{"id": 19, "question": "Which synchronization modifier ensures that changes made to a variable are always flushed immediately to main memory?", "options": ["volatile", "synchronized", "final", "abstract"], "correct": "volatile"}
]
}

@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return render_template("portal_landing.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template(
                "user_signup.html",
                error="Please fill in all fields."
            )

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template(
                "user_signup.html",
                error="This email address is already registered!"
            )
        finally:
            conn.close()

        return redirect(
            url_for("login", success="Account created successfully! Please log in.")
        )

    return render_template("user_signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    success_msg = request.args.get("success")

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("dashboard"))

        return render_template(
            "user_login.html",
            error="Incorrect email or password."
        )

    return render_template("user_login.html", success=success_msg)


@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        subjects=SUBJECT_QUIZZES.keys()
    )


@app.route("/quiz/<subject>")
def quiz(subject):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    if subject not in SUBJECT_QUIZZES:
        return redirect(url_for("dashboard"))

    return render_template(
        "quiz.html",
        quiz=SUBJECT_QUIZZES[subject],
        subject_name=subject
    )


@app.route("/submit/<subject>", methods=["POST"])
def submit(subject):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    questions = SUBJECT_QUIZZES.get(subject)

    if questions is None:
        return redirect(url_for("dashboard"))

    score = 0
    total = len(questions)
    user_answers = {}

    for item in questions:
        question_id = str(item["id"])
        selected_option = request.form.get(question_id)

        user_answers[item["id"]] = selected_option

        if selected_option == item["correct"]:
            score += 1

    return render_template(
        "result.html",
        score=score,
        total=total,
        quiz=questions,
        answers=user_answers
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )

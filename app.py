
import os
import sqlite3
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

# Secret key used for Flask sessions
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "super_secure_5_subjects_key_2026"
)


# ============================================================
# DATABASE
# ============================================================

# Use /data when it exists (useful for some hosting platforms).
# Otherwise keep the database beside app.py.
if os.path.isdir("/data"):
    DB_FILE = "/data/quiz_platform.db"
else:
    DB_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "quiz_platform.db"
    )


def get_db_connection():
    """Create and return a SQLite database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the users table if it does not already exist."""
    conn = get_db_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


init_db()


# ============================================================
# QUIZ LIBRARY
# 5 SUBJECTS × 20 QUESTIONS = 100 QUESTIONS
# ============================================================

SUBJECT_QUIZZES = {

    # ========================================================
    # CRICKET
    # ========================================================

    "cricket": [
        {
            "id": 0,
            "question": "Who scored the first-ever double century in One Day International (ODI) cricket history?",
            "options": [
                "Sachin Tendulkar",
                "Virender Sehwag",
                "Rohit Sharma",
                "Chris Gayle"
            ],
            "correct": "Sachin Tendulkar"
        },
        {
            "id": 1,
            "question": "What is the standard weight range of a men's professional cricket ball?",
            "options": [
                "4.75 to 5.25 ounces",
                "5.5 to 5.75 ounces",
                "5.0 to 5.5 ounces",
                "5.75 to 6.25 ounces"
            ],
            "correct": "5.5 to 5.75 ounces"
        },
        {
            "id": 2,
            "question": "Which bowler holds the record for taking the most wickets in Test match cricket history?",
            "options": [
                "Shane Warne",
                "Muttiah Muralitharan",
                "James Anderson",
                "Anil Kumble"
            ],
            "correct": "Muttiah Muralitharan"
        },
        {
            "id": 3,
            "question": "What is the standard length of a professional cricket pitch between the two sets of wickets?",
            "options": [
                "20 yards",
                "22 yards",
                "24 yards",
                "18 yards"
            ],
            "correct": "22 yards"
        },
        {
            "id": 4,
            "question": "Which country won the inaugural ICC T20 World Cup tournament back in 2007?",
            "options": [
                "India",
                "Pakistan",
                "Australia",
                "West Indies"
            ],
            "correct": "India"
        },
        {
            "id": 5,
            "question": "What is the maximum allowed width of a standard professional cricket bat?",
            "options": [
                "4.25 inches",
                "4.5 inches",
                "4.0 inches",
                "4.75 inches"
            ],
            "correct": "4.25 inches"
        },
        {
            "id": 6,
            "question": "Who is the only player to score 400 runs in a single innings of a Test match?",
            "options": [
                "Brian Lara",
                "Don Bradman",
                "Matthew Hayden",
                "Mahela Jayawardene"
            ],
            "correct": "Brian Lara"
        },
        {
            "id": 7,
            "question": "Which umpire is famously known for his signature 'crooked finger' out signal style?",
            "options": [
                "Billy Bowden",
                "Steve Bucknor",
                "Aleem Dar",
                "David Shepherd"
            ],
            "correct": "Billy Bowden"
        },
        {
            "id": 8,
            "question": "What term describes a batsman being dismissed because they obstructed the field defensively?",
            "options": [
                "Obstructing the field",
                "Timed out",
                "Hit the ball twice",
                "Handling the ball"
            ],
            "correct": "Obstructing the field"
        },
        {
            "id": 9,
            "question": "Which bowler has taken the fastest 300 wickets in Test cricket history (in terms of matches)?",
            "options": [
                "Ravichandran Ashwin",
                "Dennis Lillee",
                "Muttiah Muralitharan",
                "Dale Steyn"
            ],
            "correct": "Ravichandran Ashwin"
        },
        {
            "id": 10,
            "question": "What is the maximum height allowed for a cricket stump above the ground?",
            "options": [
                "28 inches",
                "30 inches",
                "26 inches",
                "32 inches"
            ],
            "correct": "28 inches"
        },
        {
            "id": 11,
            "question": "Which ground is universally referred to as the historic 'Home of Cricket'?",
            "options": [
                "Lord's Cricket Ground",
                "Melbourne Cricket Ground",
                "Eden Gardens",
                "The Oval"
            ],
            "correct": "Lord's Cricket Ground"
        },
        {
            "id": 12,
            "question": "Who was the captain of the Indian cricket team during their historic 1983 World Cup victory?",
            "options": [
                "Kapil Dev",
                "Sunil Gavaskar",
                "Ravi Shastri",
                "Mohinder Amarnath"
            ],
            "correct": "Kapil Dev"
        },
        {
            "id": 13,
            "question": "How many minutes does an incoming batsman get to arrive at the crease before being declared 'Timed Out'?",
            "options": [
                "3 minutes",
                "2 minutes",
                "5 minutes",
                "4 minutes"
            ],
            "correct": "3 minutes"
        },
        {
            "id": 14,
            "question": "Which fielding position stands directly behind the batsman on the off side to catch deflections?",
            "options": [
                "Slip",
                "Gully",
                "Point",
                "Cover"
            ],
            "correct": "Slip"
        },
        {
            "id": 15,
            "question": "Who holds the record for scoring the fastest century in ODI history in 31 balls?",
            "options": [
                "AB de Villiers",
                "Corey Anderson",
                "Shahid Afridi",
                "Glenn Maxwell"
            ],
            "correct": "AB de Villiers"
        },
        {
            "id": 16,
            "question": "What technology tracks the trajectory of a moving ball for LBW reviews?",
            "options": [
                "Hawk-Eye",
                "Snickometer",
                "Hot Spot",
                "LED Stumps"
            ],
            "correct": "Hawk-Eye"
        },
        {
            "id": 17,
            "question": "Which country won three consecutive ICC Cricket World Cups between 1999 and 2007?",
            "options": [
                "Australia",
                "India",
                "West Indies",
                "Sri Lanka"
            ],
            "correct": "Australia"
        },
        {
            "id": 18,
            "question": "What term describes a bowler delivering a ball that reaches the batsman's waist without pitching?",
            "options": [
                "Beamer",
                "Bouncer",
                "Yorker",
                "Full Toss"
            ],
            "correct": "Beamer"
        },
        {
            "id": 19,
            "question": "Who is the legendary Australian cricketer famous for finishing his career with a Test batting average of 99.94?",
            "options": [
                "Don Bradman",
                "Ricky Ponting",
                "Shane Warne",
                "Allan Border"
            ],
            "correct": "Don Bradman"
        }
    ],


    # ========================================================
    # SCIENCE
    # ========================================================

    "science": [
        {
            "id": 0,
            "question": "What is the approximate speed of light travelling through a vacuum?",
            "options": [
                "300,000 km/s",
                "150,000 km/s",
                "450,000 km/s",
                "600,000 km/s"
            ],
            "correct": "300,000 km/s"
        },
        {
            "id": 1,
            "question": "Which chemical element has the lowest atomic number on the Periodic Table?",
            "options": [
                "Hydrogen",
                "Helium",
                "Lithium",
                "Oxygen"
            ],
            "correct": "Hydrogen"
        },
        {
            "id": 2,
            "question": "Which gas makes up the largest percentage of Earth's atmosphere?",
            "options": [
                "Nitrogen",
                "Oxygen",
                "Carbon Dioxide",
                "Argon"
            ],
            "correct": "Nitrogen"
        },
        {
            "id": 3,
            "question": "Which is the densest and largest rocky planet in our Solar System?",
            "options": [
                "Earth",
                "Mars",
                "Venus",
                "Mercury"
            ],
            "correct": "Earth"
        },
        {
            "id": 4,
            "question": "Which temperature scale uses absolute zero as its baseline?",
            "options": [
                "Kelvin",
                "Celsius",
                "Fahrenheit",
                "Rankine"
            ],
            "correct": "Kelvin"
        },
        {
            "id": 5,
            "question": "Which particles carry negative electrical charges inside atoms?",
            "options": [
                "Electrons",
                "Protons",
                "Neutrons",
                "Quarks"
            ],
            "correct": "Electrons"
        },
        {
            "id": 6,
            "question": "Which rock category forms from cooled volcanic magma or lava?",
            "options": [
                "Igneous",
                "Sedimentary",
                "Metamorphic",
                "Basaltic"
            ],
            "correct": "Igneous"
        },
        {
            "id": 7,
            "question": "What force prevents objects from floating away from Earth?",
            "options": [
                "Gravity",
                "Magnetism",
                "Friction",
                "Centrifugal Force"
            ],
            "correct": "Gravity"
        },
        {
            "id": 8,
            "question": "Which layer of Earth's atmosphere contains the ozone layer?",
            "options": [
                "Stratosphere",
                "Troposphere",
                "Mesosphere",
                "Thermosphere"
            ],
            "correct": "Stratosphere"
        },
        {
            "id": 9,
            "question": "What process describes a solid changing directly into a gas?",
            "options": [
                "Sublimation",
                "Evaporation",
                "Condensation",
                "Melting"
            ],
            "correct": "Sublimation"
        },
        {
            "id": 10,
            "question": "Which gland is commonly called the master gland of the endocrine system?",
            "options": [
                "Pituitary Gland",
                "Thyroid Gland",
                "Adrenal Gland",
                "Pancreas"
            ],
            "correct": "Pituitary Gland"
        },
        {
            "id": 11,
            "question": "What is the chemical formula for hydrogen peroxide?",
            "options": [
                "H2O2",
                "H2O",
                "HO2",
                "H3O"
            ],
            "correct": "H2O2"
        },
        {
            "id": 12,
            "question": "Which subatomic particles are made from combinations of quarks?",
            "options": [
                "Protons and Neutrons",
                "Electrons",
                "Photons",
                "Neutrinos"
            ],
            "correct": "Protons and Neutrons"
        },
        {
            "id": 13,
            "question": "What law states that an object at rest remains at rest unless acted upon by an external force?",
            "options": [
                "Newton's First Law",
                "Newton's Second Law",
                "Newton's Third Law",
                "Law of Thermodynamics"
            ],
            "correct": "Newton's First Law"
        },
        {
            "id": 14,
            "question": "Which type of wave requires a physical medium to propagate?",
            "options": [
                "Mechanical Wave",
                "Electromagnetic Wave",
                "Light Wave",
                "Radio Wave"
            ],
            "correct": "Mechanical Wave"
        },
        {
            "id": 15,
            "question": "What element is represented by the symbol K?",
            "options": [
                "Potassium",
                "Krypton",
                "Calcium",
                "Phosphorus"
            ],
            "correct": "Potassium"
        },
        {
            "id": 16,
            "question": "What process occurs when unstable atomic nuclei lose energy by emitting radiation?",
            "options": [
                "Radioactive Decay",
                "Nuclear Fusion",
                "Chemical Synthesis",
                "Ionization"
            ],
            "correct": "Radioactive Decay"
        },
        {
            "id": 17,
            "question": "Which planet is the hottest in our Solar System?",
            "options": [
                "Venus",
                "Mercury",
                "Mars",
                "Jupiter"
            ],
            "correct": "Venus"
        },
        {
            "id": 18,
            "question": "What pH value represents a neutral solution at standard conditions?",
            "options": [
                "7",
                "0",
                "14",
                "5"
            ],
            "correct": "7"
        },
        {
            "id": 19,
            "question": "What force opposes the relative motion of solid surfaces sliding against each other?",
            "options": [
                "Friction",
                "Inertia",
                "Tension",
                "Elasticity"
            ],
            "correct": "Friction"
        }
    ],


    # ========================================================
    # MATHEMATICS
    # ========================================================

    "math": [
        {
            "id": 0,
            "question": "What is the numerical value of pi rounded to four decimal places?",
            "options": [
                "3.1416",
                "3.1412",
                "3.1418",
                "3.1420"
            ],
            "correct": "3.1416"
        },
        {
            "id": 1,
            "question": "What is the sum of all interior angles of a hexagon?",
            "options": [
                "720 degrees",
                "540 degrees",
                "360 degrees",
                "900 degrees"
            ],
            "correct": "720 degrees"
        },
        {
            "id": 2,
            "question": "Which theorem is used to find the hypotenuse of a right-angled triangle?",
            "options": [
                "Pythagorean Theorem",
                "Quadratic Formula",
                "Euler's Formula",
                "Sine Rule"
            ],
            "correct": "Pythagorean Theorem"
        },
        {
            "id": 3,
            "question": "What mathematical field uses derivatives and integrals?",
            "options": [
                "Calculus",
                "Algebra",
                "Topology",
                "Statistics"
            ],
            "correct": "Calculus"
        },
        {
            "id": 4,
            "question": "What is the square root of 225?",
            "options": [
                "15",
                "13",
                "25",
                "12"
            ],
            "correct": "15"
        },
        {
            "id": 5,
            "question": "Which term describes a whole number greater than 1 that has no positive divisors other than 1 and itself?",
            "options": [
                "Prime Number",
                "Composite Number",
                "Integer",
                "Rational Number"
            ],
            "correct": "Prime Number"
        },
        {
            "id": 6,
            "question": "What is the value of any non-zero real number raised to the power 0?",
            "options": [
                "1",
                "0",
                "Infinity",
                "Undefined"
            ],
            "correct": "1"
        },
        {
            "id": 7,
            "question": "What type of triangle has three unequal sides?",
            "options": [
                "Scalene Triangle",
                "Isosceles Triangle",
                "Equilateral Triangle",
                "Right Triangle"
            ],
            "correct": "Scalene Triangle"
        },
        {
            "id": 8,
            "question": "Which formula solves equations of the form ax² + bx + c = 0?",
            "options": [
                "Quadratic Formula",
                "Binomial Theorem",
                "Determinant Method",
                "Logarithmic Law"
            ],
            "correct": "Quadratic Formula"
        },
        {
            "id": 9,
            "question": "Which Greek mathematician is widely known as the Father of Geometry?",
            "options": [
                "Euclid",
                "Pythagoras",
                "Archimedes",
                "Aristotle"
            ],
            "correct": "Euclid"
        },
        {
            "id": 10,
            "question": "Which statistical value represents the middle number of a sorted dataset?",
            "options": [
                "Median",
                "Mean",
                "Mode",
                "Variance"
            ],
            "correct": "Median"
        },
        {
            "id": 11,
            "question": "What is a line segment through the center of a circle connecting two points on the circle?",
            "options": [
                "Diameter",
                "Radius",
                "Chord",
                "Tangent"
            ],
            "correct": "Diameter"
        },
        {
            "id": 12,
            "question": "What is log10(1000)?",
            "options": [
                "3",
                "2",
                "4",
                "10"
            ],
            "correct": "3"
        },
        {
            "id": 13,
            "question": "Which formula calculates the area of a circle?",
            "options": [
                "Area of a Circle",
                "Circumference of a Circle",
                "Volume of a Sphere",
                "Surface Area of a Cylinder"
            ],
            "correct": "Area of a Circle"
        },
        {
            "id": 14,
            "question": "What are angles whose sum is exactly 90 degrees called?",
            "options": [
                "Complementary Angles",
                "Supplementary Angles",
                "Obtuse Angles",
                "Reflex Angles"
            ],
            "correct": "Complementary Angles"
        },
        {
            "id": 15,
            "question": "What is 5!?",
            "options": [
                "120",
                "60",
                "24",
                "100"
            ],
            "correct": "120"
        },
        {
            "id": 16,
            "question": "Which line touches a circle at exactly one point?",
            "options": [
                "Tangent Line",
                "Secant Line",
                "Chord",
                "Radius"
            ],
            "correct": "Tangent Line"
        },
        {
            "id": 17,
            "question": "Which matrix calculation can indicate whether a square matrix is invertible?",
            "options": [
                "Determinant",
                "Transpose",
                "Inverse Matrix",
                "Dot Product"
            ],
            "correct": "Determinant"
        },
        {
            "id": 18,
            "question": "Which mathematical rule determines the order in which operations are performed?",
            "options": [
                "Order of Operations",
                "Commutative Property",
                "Distributive Law",
                "Associative Rule"
            ],
            "correct": "Order of Operations"
        },
        {
            "id": 19,
            "question": "Which branch of mathematics studies shapes and spaces under continuous deformation?",
            "options": [
                "Topology",
                "Trigonometry",
                "Calculus",
                "Arithmetic"
            ],
            "correct": "Topology"
        }
    ],


    # ========================================================
    # ROBOTICS & AI
    # ========================================================

    "robotics_ai": [
        {
            "id": 0,
            "question": "Which framework is a popular open-source middleware used for writing modular robot software?",
            "options": [
                "ROS (Robot Operating System)",
                "Linux-Bot",
                "RoboCraft",
                "Flask-Bot"
            ],
            "correct": "ROS (Robot Operating System)"
        },
        {
            "id": 1,
            "question": "Which mathematical technique adjusts weights and biases backward through neural network layers?",
            "options": [
                "Backpropagation",
                "Linear Regression",
                "Matrix Inversion",
                "Fourier Transform"
            ],
            "correct": "Backpropagation"
        },
        {
            "id": 2,
            "question": "Which neural network architecture uses recurrence and gates such as LSTM?",
            "options": [
                "RNN",
                "CNN",
                "GAN",
                "Transformer"
            ],
            "correct": "RNN"
        },
        {
            "id": 3,
            "question": "What robot component functions as its physical hand or gripping mechanism?",
            "options": [
                "End Effector",
                "Actuator",
                "Chassis",
                "Sensor"
            ],
            "correct": "End Effector"
        },
        {
            "id": 4,
            "question": "Which Python keyword is used to produce values from a generator?",
            "options": [
                "yield",
                "return",
                "lambda",
                "global"
            ],
            "correct": "yield"
        },
        {
            "id": 5,
            "question": "Which algorithm can be used to estimate state in robotic localization?",
            "options": [
                "Extended Kalman Filter",
                "A* Search",
                "Dijkstra Algorithm",
                "Gradient Descent"
            ],
            "correct": "Extended Kalman Filter"
        },
        {
            "id": 6,
            "question": "What term describes the number of independent directions a robot mechanism can move?",
            "options": [
                "Degrees of Freedom",
                "Actuation Ratio",
                "Kinematic Axis",
                "Linkage Count"
            ],
            "correct": "Degrees of Freedom"
        },
        {
            "id": 7,
            "question": "Which AI field focuses on understanding and processing human language?",
            "options": [
                "NLP",
                "Computer Vision",
                "Reinforcement Learning",
                "Expert Systems"
            ],
            "correct": "NLP"
        },
        {
            "id": 8,
            "question": "Which type of machine learning uses rewards and penalties to learn behavior?",
            "options": [
                "Reinforcement Learning",
                "Supervised Learning",
                "Unsupervised Learning",
                "Clustering"
            ],
            "correct": "Reinforcement Learning"
        },
        {
            "id": 9,
            "question": "What is the primary function of a convolutional layer in a CNN?",
            "options": [
                "Feature Extraction",
                "Data Flattening",
                "Weight Initialization",
                "Dimensionality Expansion"
            ],
            "correct": "Feature Extraction"
        },
        {
            "id": 10,
            "question": "Which metric calculates the average squared difference between predicted and actual values?",
            "options": [
                "Mean Squared Error",
                "Cross-Entropy Loss",
                "F1 Score",
                "Accuracy"
            ],
            "correct": "Mean Squared Error"
        },
        {
            "id": 11,
            "question": "Which processor is highly optimized for parallel matrix operations used in AI?",
            "options": [
                "GPU",
                "CPU",
                "Hard Drive",
                "Sound Card"
            ],
            "correct": "GPU"
        },
        {
            "id": 12,
            "question": "What problem occurs when an AI model memorizes training data and performs poorly on new data?",
            "options": [
                "Overfitting",
                "Underfitting",
                "Data Leakage",
                "Bias Drift"
            ],
            "correct": "Overfitting"
        },
        {
            "id": 13,
            "question": "Which sensor uses laser reflections to create detailed 3D maps?",
            "options": [
                "Lidar",
                "Ultrasonic Sensor",
                "Infrared Sensor",
                "Barometer"
            ],
            "correct": "Lidar"
        },
        {
            "id": 14,
            "question": "What component converts electronic signals into physical movement in a robot?",
            "options": [
                "Actuator",
                "Microcontroller",
                "Sensor",
                "Bus Transceiver"
            ],
            "correct": "Actuator"
        },
        {
            "id": 15,
            "question": "Which activation function produces values between 0 and 1?",
            "options": [
                "Sigmoid",
                "ReLU",
                "Tanh",
                "Softmax"
            ],
            "correct": "Sigmoid"
        },
        {
            "id": 16,
            "question": "Which optimization method uses derivatives to minimize error?",
            "options": [
                "Gradient Descent",
                "Random Search",
                "Binary Partitioning",
                "Matrix Expansion"
            ],
            "correct": "Gradient Descent"
        },
        {
            "id": 17,
            "question": "Which Python library provides optimized multidimensional arrays for scientific and AI computing?",
            "options": [
                "NumPy",
                "Flask",
                "Django",
                "Requests"
            ],
            "correct": "NumPy"
        },
        {
            "id": 18,
            "question": "What allows a robotic arm to calculate the joint movements needed to reach a target position?",
            "options": [
                "Inverse Kinematics",
                "Forward Kinematics",
                "Dead Reckoning",
                "Telemetry Scaling"
            ],
            "correct": "Inverse Kinematics"
        },
        {
            "id": 19,
            "question": "What is the main objective of unsupervised clustering?",
            "options": [
                "To group unlabeled data by hidden patterns",
                "To predict continuous target variables",
                "To classify text onto labels",
                "To secure server databases"
            ],
            "correct": "To group unlabeled data by hidden patterns"
        }
    ],


    # ========================================================
    # JAVA
    # ========================================================

    "java": [
        {
            "id": 0,
            "question": "What memory area handles object allocations in Java?",
            "options": [
                "Heap Space",
                "Stack Memory",
                "Method Area",
                "Register Cache"
            ],
            "correct": "Heap Space"
        },
        {
            "id": 1,
            "question": "Which keyword prevents a class from being inherited?",
            "options": [
                "final",
                "static",
                "abstract",
                "private"
            ],
            "correct": "final"
        },
        {
            "id": 2,
            "question": "Which interface allows objects to be sorted using their natural ordering?",
            "options": [
                "Comparable",
                "Comparator",
                "Serializable",
                "Cloneable"
            ],
            "correct": "Comparable"
        },
        {
            "id": 3,
            "question": "What exception occurs when a program accesses an object reference containing null?",
            "options": [
                "NullPointerException",
                "ArrayIndexOutOfBoundsException",
                "IllegalArgumentException",
                "IOException"
            ],
            "correct": "NullPointerException"
        },
        {
            "id": 4,
            "question": "Which collection maintains insertion order using a linked structure?",
            "options": [
                "LinkedHashSet",
                "HashSet",
                "TreeSet",
                "ArrayList"
            ],
            "correct": "LinkedHashSet"
        },
        {
            "id": 5,
            "question": "What allows a subclass to provide a specific implementation of a superclass method?",
            "options": [
                "Method Overriding",
                "Method Overloading",
                "Encapsulation",
                "Polymorphism"
            ],
            "correct": "Method Overriding"
        },
        {
            "id": 6,
            "question": "Which keyword establishes inheritance between Java classes?",
            "options": [
                "extends",
                "implements",
                "inherits",
                "super"
            ],
            "correct": "extends"
        },
        {
            "id": 7,
            "question": "Which block executes regardless of whether an exception occurs?",
            "options": [
                "finally",
                "catch",
                "throw",
                "finalized"
            ],
            "correct": "finally"
        },
        {
            "id": 8,
            "question": "Which memory area stores method execution frames and local variables?",
            "options": [
                "Stack Memory",
                "Heap Space",
                "Garbage Collector",
                "PermGen"
            ],
            "correct": "Stack Memory"
        },
        {
            "id": 9,
            "question": "Which keyword makes a method or variable belong to the class rather than individual objects?",
            "options": [
                "static",
                "public",
                "volatile",
                "transient"
            ],
            "correct": "static"
        },
        {
            "id": 10,
            "question": "Which concept bundles data and methods while restricting direct access to implementation details?",
            "options": [
                "Encapsulation",
                "Inheritance",
                "Abstraction",
                "Overloading"
            ],
            "correct": "Encapsulation"
        },
        {
            "id": 11,
            "question": "What automatically reclaims memory occupied by unreachable objects?",
            "options": [
                "Garbage Collector",
                "Compiler",
                "JVM Monitor",
                "Defragmenter"
            ],
            "correct": "Garbage Collector"
        },
        {
            "id": 12,
            "question": "Which modifier allows access only within the same class?",
            "options": [
                "private",
                "protected",
                "public",
                "default"
            ],
            "correct": "private"
        },
        {
            "id": 13,
            "question": "What is the primary purpose of super inside a subclass constructor?",
            "options": [
                "To call the parent class constructor",
                "To initialize static attributes",
                "To destroy duplicate references",
                "To throw custom exceptions"
            ],
            "correct": "To call the parent class constructor"
        },
        {
            "id": 14,
            "question": "Which map implementation is designed for concurrent access without locking the entire map?",
            "options": [
                "ConcurrentHashMap",
                "HashMap",
                "Hashtable",
                "TreeMap"
            ],
            "correct": "ConcurrentHashMap"
        },
        {
            "id": 15,
            "question": "What concept describes multiple methods having the same name but different parameter lists?",
            "options": [
                "Method Overloading",
                "Method Overriding",
                "Dynamic Binding",
                "Interface Mapping"
            ],
            "correct": "Method Overloading"
        },
        {
            "id": 16,
            "question": "Which keyword prevents a field from being included in standard Java serialization?",
            "options": [
                "transient",
                "volatile",
                "synchronized",
                "native"
            ],
            "correct": "transient"
        },
        {
            "id": 17,
            "question": "What Java component executes Java bytecode?",
            "options": [
                "JVM",
                "JDK",
                "JRE",
                "JVC"
            ],
            "correct": "JVM"
        },
        {
            "id": 18,
            "question": "Which operator checks whether an object is an instance of a particular class?",
            "options": [
                "instanceof",
                "typeof",
                "is",
                "cast"
            ],
            "correct": "instanceof"
        },
        {
            "id": 19,
            "question": "Which keyword ensures that reads of a variable observe the latest value written by another thread?",
            "options": [
                "volatile",
                "synchronized",
                "final",
                "abstract"
            ],
            "correct": "volatile"
        }
    ]
}


# ============================================================
# LOGIN REQUIRED DECORATOR
# ============================================================

def login_required(function):
    """Protect pages that require a logged-in user."""

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not session.get("user_id"):
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():

    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    return render_template("portal_landing.html")


# ============================================================
# SIGN UP
# ============================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Basic validation
        if not name or not email or not password:
            return render_template(
                "user_signup.html",
                error="Please fill in all fields."
            )

        # Hash password instead of storing it as plain text
        password_hash = generate_password_hash(password)

        conn = get_db_connection()

        try:

            conn.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, password_hash)
            )

            conn.commit()
            conn.close()

            return redirect(
                url_for(
                    "login",
                    success="Account created successfully! Please log in."
                )
            )

        except sqlite3.IntegrityError:

            conn.close()

            return render_template(
                "user_signup.html",
                error="This email address is already registered!"
            )

    return render_template("user_signup.html")


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    success_msg = request.args.get("success")

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        return render_template(
            "user_login.html",
            error="Incorrect email or password."
        )

    return render_template(
        "user_login.html",
        success=success_msg
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        subjects=SUBJECT_QUIZZES.keys()
    )


# ============================================================
# QUIZ
# ============================================================

@app.route("/quiz/<subject>")
@login_required
def quiz(subject):

    if subject not in SUBJECT_QUIZZES:
        return redirect(url_for("dashboard"))

    return render_template(
        "quiz.html",
        quiz=SUBJECT_QUIZZES[subject],
        subject_name=subject
    )


# ============================================================
# SUBMIT QUIZ
# ============================================================

@app.route("/submit/<subject>", methods=["POST"])
@login_required
def submit(subject):

    if subject not in SUBJECT_QUIZZES:
        return redirect(url_for("dashboard"))

    questions = SUBJECT_QUIZZES[subject]

    score = 0
    total = len(questions)

    user_answers = {}

    for item in questions:

        question_id = str(item["id"])

        selected_option = request.form.get(question_id)

        user_answers[item["id"]] = selected_option

        if selected_option == item["correct"]:
            score += 1

    percentage = 0

    if total > 0:
        percentage = round((score / total) * 100, 2)

    return render_template(
        "result.html",
        score=score,
        total=total,
        percentage=percentage,
        quiz=questions,
        answers=user_answers,
        subject_name=subject
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "user_login.html",
        error="The requested page was not found."
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return """
    <h1>Internal Server Error</h1>
    <p>Something went wrong on the server.</p>
    """, 500


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )


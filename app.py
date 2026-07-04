from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import PyPDF2
import os
import sqlite3
load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Registration Successful!"
        })

    except sqlite3.IntegrityError:

        return jsonify({
            "success": False,
            "message": "Email already exists!"
        })
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({
            "success": True,
            "message": "Login Successful!"
        })

    return jsonify({
        "success": False,
        "message": "Invalid Email or Password!"
    })
# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return "Welcome to Resumora AI Backend"

# ---------------- RESUME ANALYZER ---------------- #

@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    resume_text = ""

    if file.filename.lower().endswith(".pdf"):

        with open(filepath, "rb") as pdf_file:

            reader = PyPDF2.PdfReader(pdf_file)

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    resume_text += text

    else:
        return jsonify({
            "error": "Only PDF files are supported."
        }), 400

    prompt = f"""
You are an ATS Resume Analyzer.

Analyze this resume and provide:

ATS Score

Strengths

Missing Skills

Suggestions

Resume:
{resume_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({
        "message": "Resume analyzed successfully!",
        "analysis": response.text
    })

# ---------------- INTERVIEW QUESTIONS ---------------- #

@app.route("/interview", methods=["POST"])
def interview():

    data = request.get_json()

    role = data.get("role")

    prompt = f"""
You are an expert interviewer.

Generate 10 interview questions for a {role}.

Include:

1. HR Questions

2. Technical Questions

3. Coding Questions

Number each question.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({
        "questions": response.text
    })

# ---------------- FEEDBACK ---------------- #

@app.route("/feedback", methods=["POST"])
def feedback():

    data = request.get_json()

    answer = data.get("answer")

    prompt = f"""
Evaluate this interview answer.

Provide:

Rating /10

Strengths

Weaknesses

Suggestions

Answer:

{answer}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({
        "feedback": response.text
    })

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
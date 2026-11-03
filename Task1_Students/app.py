from flask import Flask, jsonify, request
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("students.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)

def student_dict(row):
    return dict(row) if row else None

@app.get("/students")
def get_students():
    with get_db() as db:
        rows = db.execute("SELECT * FROM students ORDER BY id").fetchall()
    return jsonify([student_dict(row) for row in rows])

@app.get("/students/<int:student_id>")
def get_student(student_id):
    with get_db() as db:
        row = db.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student_dict(row))

@app.post("/students")
def add_student():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    department = str(data.get("department", "")).strip()
    email = str(data.get("email", "")).strip()
    if not all([name, department, email]):
        return jsonify({"error": "name, department and email are required"}), 400
    try:
        with get_db() as db:
            cur = db.execute(
                "INSERT INTO students(name, department, email) VALUES (?, ?, ?)",
                (name, department, email)
            )
            row = db.execute("SELECT * FROM students WHERE id=?", (cur.lastrowid,)).fetchone()
        return jsonify(student_dict(row)), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists"}), 409

@app.put("/students/<int:student_id>")
def update_student(student_id):
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    department = str(data.get("department", "")).strip()
    email = str(data.get("email", "")).strip()
    if not all([name, department, email]):
        return jsonify({"error": "name, department and email are required"}), 400
    try:
        with get_db() as db:
            cur = db.execute(
                "UPDATE students SET name=?, department=?, email=? WHERE id=?",
                (name, department, email, student_id)
            )
            if cur.rowcount == 0:
                return jsonify({"error": "Student not found"}), 404
            row = db.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
        return jsonify(student_dict(row))
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists"}), 409

@app.delete("/students/<int:student_id>")
def delete_student(student_id):
    with get_db() as db:
        cur = db.execute("DELETE FROM students WHERE id=?", (student_id,))
    if cur.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Student deleted successfully"})

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5001, debug=True)

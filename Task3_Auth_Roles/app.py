from flask import Flask, jsonify, request, g
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import sqlite3
import os
from pathlib import Path
from functools import wraps

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("employees.db")
SECRET_KEY = os.environ.get("SECRET_KEY", "classroom-only-change-this-secret-before-deployment")
serializer = URLSafeTimedSerializer(SECRET_KEY, salt="employee-api-auth")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('employee', 'admin'))
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        # Classroom demo accounts only. Change/remove these before deployment.
        for username, password, role in [
            ("admin", "Admin123!", "admin"),
            ("employee", "Employee123!", "employee")
        ]:
            exists = db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
            if not exists:
                db.execute(
                    "INSERT INTO users(username, password_hash, role) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), role)
                )

def employee_dict(row):
    return dict(row) if row else None

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Bearer token is required"}), 401
        token = auth.split(" ", 1)[1].strip()
        try:
            payload = serializer.loads(token, max_age=3600)
        except SignatureExpired:
            return jsonify({"error": "Token expired; please log in again"}), 401
        except BadSignature:
            return jsonify({"error": "Invalid token"}), 401
        g.user = payload
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    @token_required
    def wrapper(*args, **kwargs):
        if g.user.get("role") != "admin":
            return jsonify({"error": "Administrator role required"}), 403
        return fn(*args, **kwargs)
    return wrapper

@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = data.get("password", "")
    if not username or not isinstance(password, str):
        return jsonify({"error": "username and password are required"}), 400
    with get_db() as db:
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid username or password"}), 401
    token = serializer.dumps({"user_id": user["id"], "username": user["username"], "role": user["role"]})
    return jsonify({"message": "Login successful", "access_token": token,
                    "token_type": "Bearer", "role": user["role"]})

@app.get("/employees")
@token_required
def list_employees():
    with get_db() as db:
        rows = db.execute("SELECT * FROM employees ORDER BY id").fetchall()
    return jsonify([employee_dict(row) for row in rows])

@app.get("/employees/<int:employee_id>")
@token_required
def get_employee(employee_id):
    with get_db() as db:
        row = db.execute("SELECT * FROM employees WHERE id=?", (employee_id,)).fetchone()
    if not row:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(employee_dict(row))

@app.post("/employees")
@admin_required
def add_employee():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    department = str(data.get("department", "")).strip()
    email = str(data.get("email", "")).strip()
    if not all([name, department, email]):
        return jsonify({"error": "name, department and email are required"}), 400
    try:
        with get_db() as db:
            cur = db.execute(
                "INSERT INTO employees(name, department, email) VALUES (?, ?, ?)",
                (name, department, email)
            )
            row = db.execute("SELECT * FROM employees WHERE id=?", (cur.lastrowid,)).fetchone()
        return jsonify(employee_dict(row)), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

@app.put("/employees/<int:employee_id>")
@admin_required
def update_employee(employee_id):
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    department = str(data.get("department", "")).strip()
    email = str(data.get("email", "")).strip()
    if not all([name, department, email]):
        return jsonify({"error": "name, department and email are required"}), 400
    try:
        with get_db() as db:
            cur = db.execute(
                "UPDATE employees SET name=?, department=?, email=? WHERE id=?",
                (name, department, email, employee_id)
            )
            if cur.rowcount == 0:
                return jsonify({"error": "Employee not found"}), 404
            row = db.execute("SELECT * FROM employees WHERE id=?", (employee_id,)).fetchone()
        return jsonify(employee_dict(row))
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

@app.delete("/employees/<int:employee_id>")
@admin_required
def delete_employee(employee_id):
    with get_db() as db:
        cur = db.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    if cur.rowcount == 0:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"message": "Employee deleted successfully"})

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5003, debug=False)

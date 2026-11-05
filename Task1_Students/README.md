# Task 1 — Database-Driven Flask API with Streamlit Interface

### Features
- SQLite database and `students` table (`id`, `name`, `department`, `email`).
- `GET /students` — retrieve all students.
- `GET /students/<id>` — retrieve one student.
- `POST /students` — add a student.
- `PUT /students/<id>` — update a student.
- `DELETE /students/<id>` — delete a student.
- Streamlit interface displays records, adds, updates, deletes, and refreshes after operations.

### Run

Terminal 1:

```bash
pip install -r requirements.txt
python app.py
```

Terminal 2:

```bash
streamlit run streamlit_app.py
```

Open the Streamlit URL shown in the terminal (normally `http://localhost:8501`).

### cURL examples

```bash
curl http://127.0.0.1:5001/students
curl http://127.0.0.1:5001/students/1
curl -X POST http://127.0.0.1:5001/students -H "Content-Type: application/json" -d "{\"name\":\"Ali Khan\",\"department\":\"CS\",\"email\":\"ali@example.com\"}"
curl -X PUT http://127.0.0.1:5001/students/1 -H "Content-Type: application/json" -d "{\"name\":\"Ali Khan\",\"department\":\"Software Engineering\",\"email\":\"ali@example.com\"}"
curl -X DELETE http://127.0.0.1:5001/students/1
```

### Video demonstration
Add your public video URL here: `https://drive.google.com/file/d/1M-R_TV-xwreIlzvB-w2T7ZQdq_4F8DyL/view?usp=sharing`

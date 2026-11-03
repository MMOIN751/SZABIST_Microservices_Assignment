# SZABIST University Larkana — Assignment 1
## Developing custom APIs to provide your Microservice

This repository contains working implementations for all three tasks in the assignment.

## Project structure

- `Task1_Students/` — Flask + SQLite CRUD API and Streamlit user interface.
- `Task2_API_Keys/` — Flask text-processing API protected by three API keys.
- `Task3_Auth_Roles/` — Flask employee API with login, authentication, and role-based authorization.

Each task is independent and has its own README and `requirements.txt`.

## General setup

Use Python 3.10 or newer. Open a terminal in the relevant task folder:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

Run the commands in that task's README. Start each task in a separate terminal if you want to demonstrate them together.

## Important security notes

- Task 2 keys are generated locally. Do not upload real keys, `.env` files, passwords, or screenshots containing secrets to a public repository.
- Task 3 demo accounts are for classroom testing only. Change their passwords and set a long random `SECRET_KEY` before any real deployment.
- The SQLite databases are created automatically when each application starts.

## Suggested submission

1. Push this project to your own public GitHub repository (without secrets or generated databases).
2. Put your repository URL in the required `.txt` submission file.
3. Record a short video showing each task working and add its public link to the matching task folder/README.
4. Replace the video placeholders with your actual public video URLs.

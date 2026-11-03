# Task 3 — Authentication and Authorization in a Flask API

### Roles and permissions

| Operation | Employee | Administrator |
|---|---:|---:|
| View all employees | Yes | Yes |
| View one employee | Yes | Yes |
| Add employee | No | Yes |
| Update employee | No | Yes |
| Delete employee | No | Yes |

### Security features
- `/login` checks username and a securely hashed password.
- A signed, time-limited Bearer token is returned after successful login.
- All employee endpoints require a valid token.
- Add, update, and delete routes additionally require the `admin` role.
- Passwords are stored as Werkzeug password hashes, not plain text.
- Tokens expire after one hour.

### Run

```bash
pip install -r requirements.txt
```

Set a long random secret before starting.

Windows PowerShell:

```powershell
$env:SECRET_KEY="replace-with-a-long-random-secret"
python app.py
```

macOS/Linux:

```bash
export SECRET_KEY="replace-with-a-long-random-secret"
python app.py
```

Server runs at `http://127.0.0.1:5003`.

### Demo login accounts

For classroom testing only:

- Administrator: `admin` / `Admin123!`
- Employee: `employee` / `Employee123!`

Change these before any real deployment.

### cURL testing

1. Login as administrator and copy `access_token` from the response:

```bash
curl -X POST http://127.0.0.1:5003/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"Admin123!\"}"
```

2. Use the copied token in the following commands:

```bash
curl http://127.0.0.1:5003/employees -H "Authorization: Bearer PASTE_TOKEN"
curl -X POST http://127.0.0.1:5003/employees -H "Authorization: Bearer PASTE_TOKEN" -H "Content-Type: application/json" -d "{\"name\":\"Sara Ali\",\"department\":\"IT\",\"email\":\"sara@example.com\"}"
curl -X PUT http://127.0.0.1:5003/employees/1 -H "Authorization: Bearer PASTE_TOKEN" -H "Content-Type: application/json" -d "{\"name\":\"Sara Ali\",\"department\":\"Software Engineering\",\"email\":\"sara@example.com\"}"
curl -X DELETE http://127.0.0.1:5003/employees/1 -H "Authorization: Bearer PASTE_TOKEN"
```

3. Login as the employee user and use that token for a POST/PUT/DELETE request. It should return `403 Forbidden`. A request without a token should return `401 Unauthorized`.

### Authentication vs Authorization

- **Authentication:** verifies who the user is (login and password).
- **Authorization:** checks what the logged-in user is allowed to do (employee or admin role).

### Video demonstration
Add your public video URL here: `PASTE_TASK_3_VIDEO_LINK`

# Task 2 — API Key Generation and Sharing

### Features
- Flask `POST /process` endpoint accepts JSON text and returns uppercase text.
- Three separate random keys can be generated for three consumers.
- Each request must include its key in the `X-API-Key` header.
- Missing or invalid keys are rejected with HTTP `401`.
- Keys are read from the environment, not hard-coded in source code.
- Uses constant-time comparison (`hmac.compare_digest`) for key checks.

### Generate keys

```bash
pip install -r requirements.txt
python generate_keys.py
```

Copy the three generated values. Set them in the environment in the same terminal where the server will run.

Windows PowerShell:

```powershell
$env:API_KEYS="PASTE_KEY_1,PASTE_KEY_2,PASTE_KEY_3"
python app.py
```

macOS/Linux:

```bash
export API_KEYS="PASTE_KEY_1,PASTE_KEY_2,PASTE_KEY_3"
python app.py
```

Never put real keys in GitHub, source code, screenshots, or public video. Share each key privately with its assigned tester.

### Test with cURL

Replace `PASTE_KEY_1` with one of your generated keys:

```bash
curl -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -H "X-API-Key: PASTE_KEY_1" -d "{\"text\":\"hello root software\"}"
```

Invalid-key test:

```bash
curl -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -H "X-API-Key: wrong-key" -d "{\"text\":\"hello\"}"
```

Missing-key test:

```bash
### Test with cURL

Replace `PASTE_KEY_1` with one of your generated keys:

```bash
curl -X POST http://127.0.0.1:5002/process \
-H "Content-Type: application/json" \
-H "X-API-Key: PASTE_KEY_1" \
-d "{\"text\":\"hello root software\"}"
```

Invalid-key test:

```bash
curl -X POST http://127.0.0.1:5002/process \
-H "Content-Type: application/json" \
-H "X-API-Key: wrong-key" \
-d "{\"text\":\"hello\"}"
```

Missing-key test:

```bash
curl -X POST http://127.0.0.1:5002/process \
-H "Content-Type: application/json" \
-d "{\"text\":\"hello root software\"}"
```

### Video demonstration

[Watch Task 2 Video Demonstration](https://drive.google.com/file/d/1oYbiDGhBoZa0193_5asuYMLsEepcchYU/view?usp=sharing)


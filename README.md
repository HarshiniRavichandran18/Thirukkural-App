**Thirukkural — Royal Digital Manuscript**

A premium Flask web application that allows users to explore the timeless wisdom of **Thiruvalluvar**. Search Thirukkural by **Kural Number**, **Athikaram**, or **Kural Title**, with all data fetched directly from the Thirukkural REST API.

## Features

- Royal manuscript-inspired mobile-first UI
- Search by Kural Number (1–1330)
- Search by Athikaram
- Search by Kural Title / Keyword
- Fetches data directly from the Thirukkural REST API
- No SQL, SQLite, or local database
- Elegant error handling for invalid searches

---

## Project Structure

```text
Thirukkural-App/
├── app.py
├── README.md
├── requirements.md
├── templates/
│   └── index.html
└── static/
    ├── style.css/
    └── app.js/
```

---


<img width="1600" height="899" alt="WhatsApp Image 2026-08-14 at 12 07 29 AM" src="https://github.com/user-attachments/assets/db91a527-a0cd-4a12-bd8d-206771654774" />

## Run Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd thirukkural-app
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask requests
```

### 4. Run the application

```bash
python app.py
```

### Expected Output

```text
* Serving Flask app 'app'
* Debug mode: off
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### 5. Open in your browser

```
http://127.0.0.1:5000
```

## How It Works

```text
        User
          │
          ▼
 Royal Web Interface
          │
          ▼
      Flask App
          │
          ▼
 Thirukkural REST API
          │
          ▼
     JSON Response
          │
          ▼
 Beautiful Kural Display
```

The user searches using a **Kural Number**, **Athikaram**, or **Kural Title**. Flask receives the request, fetches the matching Kural from the external Thirukkural REST API, and renders the result in a royal manuscript-style interface.

---

## Built With

- Python
- Flask
- HTML5
- CSS3
- Vanilla JavaScript
- REST API

---

## Author

**Harshini K R**

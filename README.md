# Online Feedback Collector with Admin Dashboard

A small Flask project that collects feedback from users, stores it in SQLite,
and displays the results in an admin dashboard.

## Project Structure

```text
OnlineFeedbackCollector/
│
├── app.py
├── requirements.txt
├── database.db
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── index.html
│   ├── admin.html
│   └── layout.html
│
└── README.md
```

## Features

- Feedback form with name, email, rating and comments
- Flask POST route for submitting feedback
- SQLite database
- Admin dashboard
- Total feedback count
- Average rating
- Rating distribution chart
- All feedback displayed in a table
- CSV export
- JSON API at `/api/feedback`
- Bootstrap-based responsive UI
- Simple JavaScript form validation

## How to Run

### 1. Open the project folder

```bash
cd OnlineFeedbackCollector
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install the required package

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

The application will normally run at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

## Pages

- Home / Feedback Form: `/`
- Admin Dashboard: `/admin-dashboard`
- CSV Export: `/export-csv`
- JSON API: `/api/feedback`

## Database

The application creates the `Feedback` table automatically the first time
the Flask application starts.

The table contains:

- id
- name
- email
- rating
- comments
- date_submitted

## Notes

The admin dashboard is intended for the internship project demonstration.
For a production application, proper authentication, CSRF protection,
environment variables and deployment configuration should be added.

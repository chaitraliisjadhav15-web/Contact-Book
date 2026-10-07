from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
import sqlite3
import csv
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = "feedback-project-secret-key"

DATABASE = "database.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS Feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comments TEXT NOT NULL,
            date_submitted TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    comments = request.form.get("comments", "").strip()
    rating = request.form.get("rating", "").strip()

    if not name or not email or not rating or not comments:
        flash("Please fill in all the fields.")
        return redirect(url_for("home"))

    try:
        rating = int(rating)
    except ValueError:
        flash("Please select a valid rating.")
        return redirect(url_for("home"))

    if rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5.")
        return redirect(url_for("home"))

    connection = get_db_connection()
    connection.execute(
        """
        INSERT INTO Feedback
        (name, email, rating, comments, date_submitted)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            email,
            rating,
            comments,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    connection.commit()
    connection.close()

    flash("Thank you! Your feedback has been submitted.")
    return redirect(url_for("home"))


@app.route("/admin-dashboard")
def admin_dashboard():
    connection = get_db_connection()

    feedback = connection.execute(
        "SELECT * FROM Feedback ORDER BY id DESC"
    ).fetchall()

    total_feedback = connection.execute(
        "SELECT COUNT(*) FROM Feedback"
    ).fetchone()[0]

    average_rating = connection.execute(
        "SELECT AVG(rating) FROM Feedback"
    ).fetchone()[0]

    rating_rows = connection.execute(
        """
        SELECT rating, COUNT(*) AS count
        FROM Feedback
        GROUP BY rating
        ORDER BY rating
        """
    ).fetchall()

    connection.close()

    rating_counts = [0, 0, 0, 0, 0]
    for row in rating_rows:
        rating_counts[row["rating"] - 1] = row["count"]

    return render_template(
        "admin.html",
        feedback=feedback,
        total_feedback=total_feedback,
        average_rating=round(average_rating, 2) if average_rating else 0,
        rating_counts=rating_counts,
    )


@app.route("/export-csv")
def export_csv():
    connection = get_db_connection()
    feedback = connection.execute(
        "SELECT * FROM Feedback ORDER BY id DESC"
    ).fetchall()
    connection.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(
        ["ID", "Name", "Email", "Rating", "Comments", "Date Submitted"]
    )

    for row in feedback:
        writer.writerow(
            [
                row["id"],
                row["name"],
                row["email"],
                row["rating"],
                row["comments"],
                row["date_submitted"],
            ]
        )

    response = Response(
        output.getvalue(),
        mimetype="text/csv",
    )
    response.headers["Content-Disposition"] = (
        "attachment; filename=feedback.csv"
    )
    return response


@app.route("/api/feedback")
def feedback_api():
    connection = get_db_connection()
    rows = connection.execute(
        "SELECT * FROM Feedback ORDER BY id DESC"
    ).fetchall()
    connection.close()

    data = [dict(row) for row in rows]
    return jsonify(data)


if __name__ == "__main__":
    create_table()
    app.run(debug=True)

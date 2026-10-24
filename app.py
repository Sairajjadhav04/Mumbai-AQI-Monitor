from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
import sqlite3
import re
import os
import csv
from backend.aqi_category import get_aqi_category
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
app = Flask(__name__)
app.config["SECRET_KEY"] = (
    os.environ.get("FLASK_SECRET_KEY") or os.urandom(32).hex()
)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "users.db"
AQI_FILE = BASE_DIR / "backend" / "data" / "aqi_data.csv"
def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialize_database():
    """Create required tables without deleting existing records."""
    with get_db() as db:
        # Existing public user accounts
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        # Admin accounts
        db.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Main Head account
        db.execute("""
            CREATE TABLE IF NOT EXISTS main_head (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Stations assigned to individual admins
        db.execute("""
            CREATE TABLE IF NOT EXISTS station_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER NOT NULL,
                city TEXT NOT NULL,
                station TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                UNIQUE (admin_id, city, station),
                FOREIGN KEY (admin_id) REFERENCES admins(id)
            )
        """)
        # Latest AQI readings
        db.execute("""
            CREATE TABLE IF NOT EXISTS aqi_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                station TEXT NOT NULL,
                aqi REAL NOT NULL,
                pm25 REAL NOT NULL,
                pm10 REAL NOT NULL,
                updated_by INTEGER,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (city, station),
                FOREIGN KEY (updated_by) REFERENCES admins(id)
            )
        """)
        # History of AQI updates
        db.execute("""
            CREATE TABLE IF NOT EXISTS aqi_update_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER NOT NULL,
                city TEXT NOT NULL,
                station TEXT NOT NULL,
                old_aqi REAL,
                new_aqi REAL NOT NULL,
                old_pm25 REAL,
                new_pm25 REAL NOT NULL,
                old_pm10 REAL,
                new_pm10 REAL NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (admin_id) REFERENCES admins(id)
            )
        """)
        # Daily update status
        db.execute("""
            CREATE TABLE IF NOT EXISTS daily_update_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER NOT NULL,
                city TEXT NOT NULL,
                station TEXT NOT NULL,
                update_date TEXT NOT NULL,
                submitted_at TEXT,
                status TEXT NOT NULL DEFAULT 'PENDING',
                UNIQUE (admin_id, city, station, update_date),
                FOREIGN KEY (admin_id) REFERENCES admins(id)
            )
        """)
        # Admin alerts
        db.execute("""
            CREATE TABLE IF NOT EXISTS admin_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER NOT NULL,
                alert_type TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                email_sent INTEGER NOT NULL DEFAULT 0,
                acknowledged INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (admin_id) REFERENCES admins(id)
            )
        """)
# Initialize database when the application starts
initialize_database()
def load_aqi_data():
    aqi_data = []

    if not AQI_FILE.exists():
        return aqi_data

    with open(AQI_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row.get("aqi"):
                continue

            row["category"] = get_aqi_category(row["aqi"])
            aqi_data.append(row)

    return aqi_data
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        with get_db() as db:
            user = db.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()
        if user and check_password_hash(
            user["password_hash"], password
        ):
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        error = "Invalid email or password."
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        if not full_name or not email or not phone:
            error = "Please complete all fields."
        elif not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", email
        ):
            error = "Enter a valid email address."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            try:
                with get_db() as db:
                    db.execute("""
                        INSERT INTO users
                        (full_name, email, phone, password_hash)
                        VALUES (?, ?, ?, ?)
                    """, (
                        full_name,
                        email,
                        phone,
                        generate_password_hash(password)
                    ))
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                error = "An account with this email already exists."
    return render_template("register.html", error=error)
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    with get_db() as db:
        user = db.execute(
            """
            SELECT full_name, email
            FROM users
            WHERE id = ?
            """,
            (session["user_id"],)
        ).fetchone()

    if user is None:
        session.clear()
        return redirect(url_for("login"))

    # Currently, dashboard data comes from the CSV file.
    aqi_data = load_aqi_data()

    if aqi_data:
        highest = max(
            aqi_data,
            key=lambda row: float(row["aqi"])
        )

        lowest = min(
            aqi_data,
            key=lambda row: float(row["aqi"])
        )

        average_aqi = round(
            sum(float(row["aqi"]) for row in aqi_data)
            / len(aqi_data)
        )

    else:
        highest = None
        lowest = None
        average_aqi = None

    return render_template(
        "dashboard.html",
        user=user,
        aqi_data=aqi_data,
        highest=highest,
        lowest=lowest,
        average_aqi=average_aqi
    )
# --------------------------------------------------
# AQI CATEGORY ANALYSIS
# --------------------------------------------------

@app.route("/aqi-analysis")
def aqi_analysis():

    # Only logged-in users can access analysis
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Load existing station data
    aqi_data = load_aqi_data()

    # Official Indian AQI category order
    categories = [
        "Good",
        "Satisfactory",
        "Moderate",
        "Poor",
        "Very Poor",
        "Severe"
    ]

    # Initially, every category has zero stations
    counts = {category: 0 for category in categories}

    # Count stations in each category
    for row in aqi_data:
        category = row.get("category", "").strip()

        if category in counts:
            counts[category] += 1

    # Prepare graph output path
    chart_path = BASE_DIR / "static" / "aqi_category_chart.png"
    chart_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate bar graph
    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        categories,
        [counts[category] for category in categories]
    )

    plt.title("AQI Station Analysis by Category")
    plt.xlabel("AQI Category")
    plt.ylabel("Number of Stations")
    plt.xticks(rotation=20)

    # Display count above each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(int(height)),
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.savefig(chart_path, dpi=150)
    plt.close()

    return render_template(
        "aqi_analysis.html",
        counts=counts
    )
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
import sqlite3
import re
app = Flask(__name__)

app.config["SECRET_KEY"] = "a12efdef5223752eca4e5cc3c33130fc12a22c4905f8926fe05f9c4ff31d3ef8"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "users.db"


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)


initialize_database()


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

        if user and check_password_hash(user["password_hash"], password):
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

        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            error = "Enter a valid email address."

        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            try:
                with get_db() as db:
                    db.execute(
                        """INSERT INTO users
                           (full_name, email, phone, password_hash)
                           VALUES (?, ?, ?, ?)""",
                        (
                            full_name,
                            email,
                            phone,
                            generate_password_hash(password)
                        )
                    )
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
            "SELECT full_name, email FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()
    if user is None:
        session.clear()
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)

import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash  # type: ignore
from flask_login import (  # type: ignore
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import check_password_hash

DB_PATH = "users.db"

app = Flask(__name__)

# In production, set SECRET_KEY as a real environment variable instead
# of relying on the fallback below.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-key")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT id, username FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return User(id=row["id"], username=row["username"])


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db_connection()
        row = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        conn.close()

        if row is not None and check_password_hash(row["password_hash"], password):
            user = User(id=row["id"], username=row["username"])
            login_user(user)
            return redirect(url_for("home"))

        flash("Incorrect username or password.")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/tools")
@login_required
def tools():
    return render_template("tools.html")


@app.route("/submit", methods=["POST"])
@login_required
def submit():
    name = request.form["name"]
    issue = request.form["issue"]

    print("New Log:")
    print("Name:", name)
    print("Issue:", issue)

    return f"Log saved!<br>Name: {name}<br>Issue: {issue}"


if __name__ == "__main__":
    app.run(debug=True)
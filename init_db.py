"""
Run this once to create the database and your admin account:

    python init_db.py

It will ask for a username and password, hash the password, and store
the account in users.db. Re-running this script is safe — it will not
create a duplicate table, but it WILL let you add another user if you
want a second account later.
"""

import sqlite3
import getpass
from werkzeug.security import generate_password_hash

DB_PATH = "users.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def create_user():
    username = input("Username: ").strip()
    if not username:
        print("Username can't be empty.")
        return

    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Confirm password: ")

    if password != confirm:
        print("Passwords don't match. Try again.")
        return

    if len(password) < 8:
        print("Password should be at least 8 characters.")
        return

    password_hash = generate_password_hash(password)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        conn.commit()
        print(f"User '{username}' created.")
    except sqlite3.IntegrityError:
        print(f"A user named '{username}' already exists.")
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    create_user()
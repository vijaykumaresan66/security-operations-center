from functools import wraps

from flask import (
    session,
    redirect,
    url_for,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from modules.database import database_connection


# ==========================================
# CREATE USER
# ==========================================

def create_user(username, password, role="analyst"):

    password_hash = generate_password_hash(password)

    try:

        with database_connection() as connection:

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO users (
                    username,
                    password_hash,
                    role
                )
                VALUES (?, ?, ?)
            """, (
                username,
                password_hash,
                role
            ))

            return True

    except Exception as error:

        print(f"User creation error: {error}")

        return False


# ==========================================
# AUTHENTICATE USER
# ==========================================

def authenticate_user(username, password):

    with database_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                username,
                password_hash,
                role
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        if not user:
            return None

        if check_password_hash(
            user["password_hash"],
            password
        ):

            return {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }

        return None


# ==========================================
# LOGIN USER
# ==========================================

def login_user(user):

    session.clear()

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role"] = user["role"]

    session.permanent = True


# ==========================================
# LOGOUT USER
# ==========================================

def logout_user():

    session.clear()


# ==========================================
# CHECK LOGIN
# ==========================================

def is_logged_in():

    return "user_id" in session


# ==========================================
# GET CURRENT USER
# ==========================================

def get_current_user():

    if not is_logged_in():
        return None

    return {
        "id": session.get("user_id"),
        "username": session.get("username"),
        "role": session.get("role")
    }


# ==========================================
# LOGIN REQUIRED DECORATOR
# ==========================================

def login_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not is_logged_in():

            flash(
                "Please login to access this page.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        return function(*args, **kwargs)

    return decorated_function


# ==========================================
# ROLE REQUIRED DECORATOR
# ==========================================

def role_required(required_role):

    def decorator(function):

        @wraps(function)
        def decorated_function(*args, **kwargs):

            if not is_logged_in():

                flash(
                    "Please login first.",
                    "warning"
                )

                return redirect(
                    url_for("login")
                )

            current_role = session.get("role")

            if current_role != required_role:

                flash(
                    "You do not have permission to access this page.",
                    "danger"
                )

                return redirect(
                    url_for("dashboard")
                )

            return function(*args, **kwargs)

        return decorated_function

    return decorator
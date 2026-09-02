from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

import os

from werkzeug.utils import secure_filename

from config import Config

from modules.database import (
    initialize_database,
    get_dashboard_statistics,
    get_all_logs,
    get_all_alerts,
    update_alert_status
)

from modules.auth import (
    create_user,
    authenticate_user,
    login_user,
    logout_user,
    login_required
)

from modules.log_parser import (
    parse_log_file
)

from modules.alerts import (
    generate_alerts
)


# ==========================================
# APPLICATION
# ==========================================

app = Flask(__name__)

app.config.from_object(Config)


# ==========================================
# UPLOAD CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = (
    5 * 1024 * 1024
)


# ==========================================
# INITIALIZE DATABASE
# ==========================================

initialize_database()


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    if "user_id" in session:

        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
    )


# ==========================================
# LOGIN
# ==========================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if not username or not password:

            flash(
                "Username and password are required.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        user = authenticate_user(
            username,
            password
        )

        if user:

            login_user(user)

            flash(
                "Login successful.",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid username or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():

    statistics = get_dashboard_statistics()

    logs = get_all_logs()

    alerts = get_all_alerts()

    return render_template(
        "dashboard.html",
        statistics=statistics,
        logs=logs,
        alerts=alerts
    )
# ==========================================
# SYSTEM / ABOUT PROJECT
# ==========================================

@app.route("/system")
@login_required
def system():

    return render_template(
        "system.html"
    )


# ==========================================
# UPDATE ALERT STATUS
# ==========================================

@app.route(
    "/alerts/<int:alert_id>/status",
    methods=["POST"]
)
@login_required
def update_status(alert_id):

    status = request.form.get(
        "status",
        ""
    ).strip()

    # --------------------------------------
    # ALLOWED STATUSES
    # --------------------------------------

    allowed_statuses = [
        "Open",
        "Investigating",
        "Resolved"
    ]

    if status not in allowed_statuses:

        flash(
            "Invalid alert status.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    # --------------------------------------
    # UPDATE DATABASE
    # --------------------------------------

    success = update_alert_status(
        alert_id,
        status
    )

    if success:

        flash(
            f"Alert #{alert_id} updated to {status}.",
            "success"
        )

    else:

        flash(
            "Alert could not be updated.",
            "danger"
        )

    return redirect(
        url_for("dashboard")
    )


# ==========================================
# LOG UPLOAD
# ==========================================

@app.route(
    "/upload",
    methods=["GET", "POST"]
)
@login_required
def upload():

    if request.method == "POST":

        # --------------------------------------
        # GET UPLOADED FILE
        # --------------------------------------

        uploaded_file = request.files.get(
            "log_file"
        )

        # --------------------------------------
        # CHECK FILE
        # --------------------------------------

        if not uploaded_file:

            flash(
                "Please select a log file.",
                "danger"
            )

            return redirect(
                url_for("upload")
            )

        if uploaded_file.filename == "":

            flash(
                "No file selected.",
                "danger"
            )

            return redirect(
                url_for("upload")
            )

        # --------------------------------------
        # SECURE FILE NAME
        # --------------------------------------

        filename = secure_filename(
            uploaded_file.filename
        )

        # --------------------------------------
        # CHECK EXTENSION
        # --------------------------------------

        if not filename.lower().endswith(".txt"):

            flash(
                "Only .txt log files are supported.",
                "danger"
            )

            return redirect(
                url_for("upload")
            )

        # --------------------------------------
        # CREATE UPLOAD DIRECTORY
        # --------------------------------------

        os.makedirs(
            app.config["UPLOAD_FOLDER"],
            exist_ok=True
        )

        # --------------------------------------
        # CREATE FILE PATH
        # --------------------------------------

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        # --------------------------------------
        # SAVE FILE
        # --------------------------------------

        try:

            uploaded_file.save(
                file_path
            )

        except Exception as error:

            flash(
                f"File upload failed: {error}",
                "danger"
            )

            return redirect(
                url_for("upload")
            )

        # --------------------------------------
        # PARSE LOG FILE
        # --------------------------------------

        try:

            logs = parse_log_file(
                file_path
            )

        except Exception as error:

            flash(
                f"Log parsing failed: {error}",
                "danger"
            )

            return redirect(
                url_for("upload")
            )

        # --------------------------------------
        # CHECK PARSED LOGS
        # --------------------------------------

        if not logs:

            flash(
                "No valid security logs were found in the file.",
                "warning"
            )

            return redirect(
                url_for("upload")
            )

        # --------------------------------------
        # GENERATE ALERTS
        # --------------------------------------

        try:

            alerts = generate_alerts(
                logs
            )

        except Exception as error:

            flash(
                f"Alert generation failed: {error}",
                "danger"
            )

            return redirect(
                url_for("upload")
            )

        # --------------------------------------
        # SUCCESS MESSAGE
        # --------------------------------------

        flash(
            f"{len(logs)} logs processed and "
            f"{len(alerts)} alerts generated.",
            "success"
        )

        # --------------------------------------
        # RETURN TO DASHBOARD
        # --------------------------------------

        return redirect(
            url_for("dashboard")
        )

    # ======================================
    # GET REQUEST
    # ======================================

    return render_template(
        "upload.html"
    )


# ==========================================
# CREATE INITIAL ADMIN
# ==========================================

def create_initial_admin():

    username = "admin"

    password = "Admin@12345"

    success = create_user(
        username,
        password,
        "admin"
    )

    if success:

        print(
            "Initial admin user created."
        )

        print(
            "Username: admin"
        )

        print(
            "Password: Admin@12345"
        )

    else:

        print(
            "Admin user already exists."
        )


# ==========================================
# APPLICATION START
# ==========================================

if __name__ == "__main__":

    create_initial_admin()

    app.run(
        debug=True
    )
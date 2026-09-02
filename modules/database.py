import sqlite3
from pathlib import Path
from contextlib import contextmanager

# ==========================================
# UPDATE ALERT STATUS
# ==========================================

def update_alert_status(alert_id, status):

    allowed_statuses = [
        "Open",
        "Investigating",
        "Resolved"
    ]

    if status not in allowed_statuses:
        return False

    with database_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE alerts
            SET status = ?
            WHERE id = ?
        """, (
            status,
            alert_id
        ))

        return cursor.rowcount > 0
# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "soc.db"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=30
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# DATABASE CONTEXT MANAGER
# ==========================================

@contextmanager
def database_connection():

    connection = get_connection()

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# CREATE TABLES
# ==========================================

def initialize_database():

    with database_connection() as connection:

        cursor = connection.cursor()

        # --------------------------------------
        # USERS TABLE
        # --------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                role TEXT NOT NULL DEFAULT 'analyst',

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        # --------------------------------------
        # LOGS TABLE
        # --------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT,

                source_ip TEXT,

                destination_ip TEXT,

                username TEXT,

                event_type TEXT,

                message TEXT,

                severity TEXT,

                risk_score INTEGER DEFAULT 0,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        # --------------------------------------
        # ALERTS TABLE
        # --------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                log_id INTEGER,

                alert_type TEXT NOT NULL,

                severity TEXT NOT NULL,

                risk_score INTEGER DEFAULT 0,

                description TEXT,

                status TEXT DEFAULT 'Open',

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (log_id)
                    REFERENCES logs(id)

            )
        """)

        print("Database initialized successfully.")


# ==========================================
# INSERT LOG
# ==========================================

def insert_log(
    timestamp,
    source_ip,
    destination_ip,
    username,
    event_type,
    message,
    severity,
    risk_score
):

    with database_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO logs (

                timestamp,
                source_ip,
                destination_ip,
                username,
                event_type,
                message,
                severity,
                risk_score

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            timestamp,
            source_ip,
            destination_ip,
            username,
            event_type,
            message,
            severity,
            risk_score

        ))

        return cursor.lastrowid


# ==========================================
# INSERT ALERT
# ==========================================

def insert_alert(
    log_id,
    alert_type,
    severity,
    risk_score,
    description
):

    with database_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO alerts (

                log_id,
                alert_type,
                severity,
                risk_score,
                description

            )

            VALUES (?, ?, ?, ?, ?)
        """, (

            log_id,
            alert_type,
            severity,
            risk_score,
            description

        ))

        return cursor.lastrowid


# ==========================================
# GET ALL LOGS
# ==========================================

def get_all_logs():

    with database_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM logs
            ORDER BY id DESC
        """)

        return cursor.fetchall()


# ==========================================
# GET ALL ALERTS
# ==========================================

def get_all_alerts():

    with database_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                alerts.*,
                logs.source_ip,
                logs.destination_ip,
                logs.event_type,
                logs.username,
                logs.message

            FROM alerts

            LEFT JOIN logs
                ON alerts.log_id = logs.id

            ORDER BY alerts.id DESC
        """)

        return cursor.fetchall()


# ==========================================
# DASHBOARD STATISTICS
# ==========================================

def get_dashboard_statistics():

    with database_connection() as connection:

        cursor = connection.cursor()

        # Total logs
        cursor.execute("""
            SELECT COUNT(*)
            FROM logs
        """)

        total_logs = cursor.fetchone()[0]

        # Critical alerts
        cursor.execute("""
            SELECT COUNT(*)
            FROM alerts
            WHERE severity = 'Critical'
        """)

        critical_alerts = cursor.fetchone()[0]

        # High alerts
        cursor.execute("""
            SELECT COUNT(*)
            FROM alerts
            WHERE severity = 'High'
        """)

        high_alerts = cursor.fetchone()[0]

        # Medium alerts
        cursor.execute("""
            SELECT COUNT(*)
            FROM alerts
            WHERE severity = 'Medium'
        """)

        medium_alerts = cursor.fetchone()[0]

        # Low alerts
        cursor.execute("""
            SELECT COUNT(*)
            FROM alerts
            WHERE severity = 'Low'
        """)

        low_alerts = cursor.fetchone()[0]

        # Open alerts
        cursor.execute("""
            SELECT COUNT(*)
            FROM alerts
            WHERE status = 'Open'
        """)

        open_alerts = cursor.fetchone()[0]

        return {

            "total_logs": total_logs,

            "critical_alerts": critical_alerts,

            "high_alerts": high_alerts,

            "medium_alerts": medium_alerts,

            "low_alerts": low_alerts,

            "open_alerts": open_alerts

        }
    # ==========================================
# UPDATE ALERT STATUS
# ==========================================

def update_alert_status(alert_id, status):

    allowed_statuses = [
        "Open",
        "Investigating",
        "Resolved"
    ]

    if status not in allowed_statuses:
        return False

    with database_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE alerts
            SET status = ?
            WHERE id = ?
        """, (
            status,
            alert_id
        ))

        return cursor.rowcount > 0
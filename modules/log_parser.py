from datetime import datetime

from modules.database import insert_log


# ==========================================
# SEVERITY CALCULATION
# ==========================================

def calculate_severity(event_type, message):

    event = event_type.lower()
    text = message.lower()

    # --------------------------------------
    # CRITICAL
    # --------------------------------------

    if (
        "ransomware" in text
        or "data breach" in text
        or "privilege escalation" in text
    ):

        return "Critical", 90


    # --------------------------------------
    # HIGH
    # --------------------------------------

    if (
        "malware" in text
        or "brute force" in text
        or "unauthorized access" in text
        or "sql injection" in text
    ):

        return "High", 75


    # --------------------------------------
    # MEDIUM
    # --------------------------------------

    if (
        "failed login" in text
        or "suspicious" in text
        or "port scan" in text
        or "multiple login" in text
    ):

        return "Medium", 50


    # --------------------------------------
    # LOW
    # --------------------------------------

    if (
        "login" in event
        or "logout" in event
        or "connection" in event
    ):

        return "Low", 20


    # --------------------------------------
    # DEFAULT
    # --------------------------------------

    return "Low", 10


# ==========================================
# PARSE SINGLE LOG
# ==========================================

def parse_log(
    source_ip,
    destination_ip,
    username,
    event_type,
    message,
    timestamp=None
):

    # --------------------------------------
    # TIMESTAMP
    # --------------------------------------

    if timestamp is None:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


    # --------------------------------------
    # CALCULATE RISK
    # --------------------------------------

    severity, risk_score = calculate_severity(
        event_type,
        message
    )


    # --------------------------------------
    # INSERT INTO DATABASE
    # --------------------------------------

    log_id = insert_log(

        timestamp=timestamp,

        source_ip=source_ip,

        destination_ip=destination_ip,

        username=username,

        event_type=event_type,

        message=message,

        severity=severity,

        risk_score=risk_score

    )


    return {

        "id": log_id,

        "timestamp": timestamp,

        "source_ip": source_ip,

        "destination_ip": destination_ip,

        "username": username,

        "event_type": event_type,

        "message": message,

        "severity": severity,

        "risk_score": risk_score

    }


# ==========================================
# PARSE LOG FILE
# ==========================================

def parse_log_file(file_path):

    parsed_logs = []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:

                continue


            # ----------------------------------
            # EXPECTED FORMAT
            # ----------------------------------

            parts = line.split("|")


            if len(parts) < 6:

                continue


            timestamp = parts[0].strip()

            source_ip = parts[1].strip()

            destination_ip = parts[2].strip()

            username = parts[3].strip()

            event_type = parts[4].strip()

            message = "|".join(
                parts[5:]
            ).strip()


            # ----------------------------------
            # PARSE LOG
            # ----------------------------------

            log = parse_log(

                source_ip=source_ip,

                destination_ip=destination_ip,

                username=username,

                event_type=event_type,

                message=message,

                timestamp=timestamp

            )


            parsed_logs.append(log)


    return parsed_logs
from modules.database import insert_alert


# ==========================================
# ALERT RULES
# ==========================================

ALERT_RULES = {

    "Critical": {
        "minimum_risk_score": 80,
        "alert_type": "Critical Security Incident"
    },

    "High": {
        "minimum_risk_score": 70,
        "alert_type": "High Risk Security Event"
    },

    "Medium": {
        "minimum_risk_score": 40,
        "alert_type": "Suspicious Activity"
    },

    "Low": {
        "minimum_risk_score": 100,
        "alert_type": "Informational Event"
    }

}


# ==========================================
# GENERATE ALERT
# ==========================================

def generate_alert(log):

    severity = log.get(
        "severity",
        "Low"
    )

    risk_score = int(
        log.get(
            "risk_score",
            0
        )
    )

    event_type = log.get(
        "event_type",
        "Unknown Event"
    )

    message = log.get(
        "message",
        ""
    )

    log_id = log.get(
        "id"
    )


    # --------------------------------------
    # FIND ALERT RULE
    # --------------------------------------

    rule = ALERT_RULES.get(
        severity
    )

    if not rule:

        return None


    minimum_score = rule[
        "minimum_risk_score"
    ]


    # --------------------------------------
    # CHECK RISK SCORE
    # --------------------------------------

    if risk_score < minimum_score:

        return None


    # --------------------------------------
    # CREATE DESCRIPTION
    # --------------------------------------

    description = (
        f"Security event detected: "
        f"{event_type}. "
        f"{message}"
    )


    # --------------------------------------
    # INSERT ALERT
    # --------------------------------------

    alert_id = insert_alert(

        log_id=log_id,

        alert_type=rule[
            "alert_type"
        ],

        severity=severity,

        risk_score=risk_score,

        description=description

    )


    return {

        "id": alert_id,

        "log_id": log_id,

        "alert_type": rule[
            "alert_type"
        ],

        "severity": severity,

        "risk_score": risk_score,

        "description": description,

        "status": "Open"

    }


# ==========================================
# PROCESS MULTIPLE LOGS
# ==========================================

def generate_alerts(logs):

    alerts = []


    for log in logs:

        alert = generate_alert(
            log
        )

        if alert:

            alerts.append(
                alert
            )


    return alerts
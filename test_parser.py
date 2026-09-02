from modules.log_parser import parse_log_file
from modules.alerts import generate_alerts


# ==========================================
# PARSE LOG FILE
# ==========================================

logs = parse_log_file(
    "uploads/test_logs.txt"
)


# ==========================================
# GENERATE ALERTS
# ==========================================

alerts = generate_alerts(
    logs
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print()

print("=" * 60)

print("SOC ALERT ENGINE TEST")

print("=" * 60)


print()

print(
    f"Logs Processed: {len(logs)}"
)

print(
    f"Alerts Generated: {len(alerts)}"
)


# ==========================================
# DISPLAY ALERTS
# ==========================================

for alert in alerts:

    print()

    print("-" * 60)

    print(
        f"Alert ID    : {alert['id']}"
    )

    print(
        f"Alert Type  : {alert['alert_type']}"
    )

    print(
        f"Severity    : {alert['severity']}"
    )

    print(
        f"Risk Score  : {alert['risk_score']}"
    )

    print(
        f"Status      : {alert['status']}"
    )

    print(
        f"Description : {alert['description']}"
    )


print()

print("=" * 60)

print("ALERT ENGINE TEST COMPLETED")

print("=" * 60)
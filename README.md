# 🛡️ AI SOC Analyst Dashboard

A dynamic Security Operations Center (SOC) Analyst Dashboard built with Python and Flask for collecting, parsing, monitoring, and analyzing security logs.

This project simulates a real-world SOC environment where security logs are processed and suspicious activities are converted into security alerts based on predefined detection rules.

---

## 🚀 Features

- 🔐 Secure login system
- 📂 Security log file upload
- 🔍 Automatic log parsing
- 🚨 Security alert generation
- 📊 Dynamic SOC dashboard
- ⚠️ Severity classification
- 🎯 Risk scoring
- 📋 Security log management
- 🔔 Alert management
- 💾 SQLite database integration
- 📈 Dashboard statistics
- 🌐 Flask web interface
- 🧩 Modular Python architecture

---

## 🏗️ Project Structure

```text
AI-SOC-Analyst-Dashboard/
│
├── app.py
│
├── modules/
│   ├── __init__.py
│   ├── database_manager.py
│   ├── log_parser.py
│   ├── alerts.py
│   ├── alert_manager.py
│   ├── auth.py
│   ├── network.py
│   └── scanner.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── index.html
│   ├── alerts.html
│   └── logs.html
│
├── static/
│   └── css/
│       └── dashboard.css
│
├── database/
│   └── database.db
│
├── sample_logs.txt
├── requirements.txt
└── README.md
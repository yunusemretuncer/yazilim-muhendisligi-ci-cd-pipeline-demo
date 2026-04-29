"""
Mini DevSecOps demo app.
Bilerek 3 zafiyet içerir:
  1) Hardcoded AWS access key (gitleaks yakalar)
  2) SQL injection - string concat ile sorgu (bandit yakalar)
  3) Eski/zafiyetli Flask versiyonu (pip-audit yakalar)
"""
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# VULN #1: Hardcoded secret
AWS_ACCESS_KEY = "AKIA4QHZB5VTM8XNK3PR"
AWS_SECRET_KEY = "j7Hk3PQm9bR2nT5wX8vC4dY6gZ1fA0eS+L/qNuVB"


@app.route("/user")
def get_user():
    user_id = request.args.get("id", "1")
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    # VULN #2: SQL Injection
    query = "SELECT * FROM users WHERE id = " + user_id
    cur.execute(query)

    return {"result": cur.fetchall()}


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) # nosec B104 - container deployment

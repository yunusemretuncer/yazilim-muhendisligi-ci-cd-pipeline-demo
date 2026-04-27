"""
Mini DevSecOps demo app.
Bilerek 2 zafiyet içerir:
  1) Hardcoded AWS access key (gitleaks yakalar)
  2) SQL injection - string concat ile sorgu (bandit yakalar)
"""
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# VULN #1: Hardcoded secret - gitleaks bunu commit'te yakalar
AWS_ACCESS_KEY = "AKIAZ7K3YQXVN4PW2L5R"
AWS_SECRET_KEY = "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"


@app.route("/user")
def get_user():
    user_id = request.args.get("id", "1")
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    # VULN #2: SQL Injection - bandit B608 yakalar
    query = "SELECT * FROM users WHERE id = " + user_id
    cur.execute(query)

    return {"result": cur.fetchall()}


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

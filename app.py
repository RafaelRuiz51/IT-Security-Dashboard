from flask import Flask, render_template, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        message TEXT,
        severity TEXT,
        timestamp TEXT,
        resolved INTEGER DEFAULT 0
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        status TEXT DEFAULT 'Open',
        created TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        department TEXT,
        status TEXT DEFAULT 'Active',
        last_login TEXT
    )''')
    
    conn.commit()
    conn.close()

# --- SEED FAKE DATA ---
def seed_data():
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM alerts")
    if c.fetchone()[0] == 0:
        alerts = [
            ('Brute Force', 'SERVER01: 47 failed logins from IP 192.168.1.105', 'High', '2026-05-29 08:14:22'),
            ('Account Lockout', 'User jsmith locked out after 5 failed attempts', 'Medium', '2026-05-29 09:31:05'),
            ('Unauthorized Access', 'Attempted RDP connection blocked from 10.0.0.88', 'High', '2026-05-29 10:02:44'),
            ('Password Reset', 'Admin password reset performed outside business hours', 'Medium', '2026-05-29 11:15:30'),
            ('Port Scan', 'Nmap scan detected from 192.168.1.200', 'Low', '2026-05-29 12:44:10'),
        ]
        c.executemany("INSERT INTO alerts (type, message, severity, timestamp) VALUES (?,?,?,?)", alerts)
    
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        users = [
            ('jsmith', 'Finance', 'Locked', '2026-05-29 08:10:00'),
            ('mrodriguez', 'HR', 'Active', '2026-05-29 09:00:00'),
            ('tlee', 'IT', 'Active', '2026-05-29 07:55:00'),
            ('kpatel', 'Operations', 'Active', '2026-05-28 17:30:00'),
            ('bjohnson', 'Finance', 'Disabled', '2026-05-27 12:00:00'),
        ]
        c.executemany("INSERT INTO users (username, department, status, last_login) VALUES (?,?,?,?)", users)
    
    c.execute("SELECT COUNT(*) FROM tickets")
    if c.fetchone()[0] == 0:
        tickets = [
            ('Brute Force Detected - SERVER01', 'Auto-generated: 47 failed logins detected. Investigate IP 192.168.1.105.', 'Open', '2026-05-29 08:14:22'),
            ('Account Lockout - jsmith', 'User locked out. Verify identity before unlocking.', 'In Progress', '2026-05-29 09:31:05'),
            ('RDP Block - 10.0.0.88', 'Unauthorized RDP attempt blocked. Review firewall logs.', 'Open', '2026-05-29 10:02:44'),
        ]
        c.executemany("INSERT INTO tickets (title, description, status, created) VALUES (?,?,?,?)", tickets)
    
    conn.commit()
    conn.close()

# --- ROUTES ---
@app.route('/')
def dashboard():
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    c.execute("SELECT * FROM alerts WHERE resolved=0 ORDER BY timestamp DESC")
    alerts = c.fetchall()
    c.execute("SELECT COUNT(*) FROM alerts WHERE severity='High' AND resolved=0")
    high_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM alerts WHERE resolved=0")
    total_alerts = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'")
    open_tickets = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE status='Active'")
    active_users = c.fetchone()[0]
    conn.close()
    return render_template('dashboard.html', alerts=alerts, high_count=high_count,
                           total_alerts=total_alerts, open_tickets=open_tickets,
                           active_users=active_users)

@app.route('/tickets')
def tickets():
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tickets ORDER BY created DESC")
    tickets = c.fetchall()
    conn.close()
    return render_template('tickets.html', tickets=tickets)

@app.route('/users')
def users():
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/resolve/<int:alert_id>')
def resolve_alert(alert_id):
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    c.execute("UPDATE alerts SET resolved=1 WHERE id=?", (alert_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()
    seed_data()
    app.run(debug=True)
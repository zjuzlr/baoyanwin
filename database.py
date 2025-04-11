
import sqlite3
import os

DB_NAME = "records.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    password_hash TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    school_name TEXT,
                    interview_date TEXT,
                    assessment_process TEXT,
                    lessons_learned TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    conn.close()

def insert_record(user_id, school, date, process, lesson):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO records (user_id, school_name, interview_date, assessment_process, lessons_learned) VALUES (?, ?, ?, ?, ?)',
              (user_id, school, date, process, lesson))
    record_id = c.lastrowid
    conn.commit()
    conn.close()
    return record_id

def get_user_records(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM records WHERE user_id=? ORDER BY timestamp DESC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(id=row[0], user_id=row[1], school_name=row[2], interview_date=row[3], assessment_process=row[4], lessons_learned=row[5]) for row in rows]

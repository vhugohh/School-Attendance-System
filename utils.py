import sqlite3
import pandas as pd
from datetime import datetime
import qrcode
from io import BytesIO
import os

DB_NAME = "attendance.db"

def init_db():
    """Initializes the SQLite database with students and attendance tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Students table
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            group_name TEXT NOT NULL
        )
    ''')
    
    # Attendance table
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            timestamp DATETIME,
            date TEXT,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def register_student(student_id, name, group_name):
    """Registers a student or updates their info if they exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO students (id, name, group_name)
        VALUES (?, ?, ?)
    ''', (student_id, name, group_name))
    conn.commit()
    conn.close()

def record_attendance(student_id):
    """Records attendance for a student. Returns success boolean and message."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if student exists
    c.execute('SELECT name FROM students WHERE id = ?', (student_id,))
    student = c.fetchone()
    
    if not student:
        conn.close()
        return False, "Estudiante no encontrado/registrado."
    
    student_name = student[0]
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    
    # Check if already marked present today
    c.execute('''
        SELECT id FROM attendance 
        WHERE student_id = ? AND date = ?
    ''', (student_id, today_str))
    
    if c.fetchone():
        conn.close()
        return False, f"Asistencia ya registrada hoy para {student_name}."
    
    c.execute('''
        INSERT INTO attendance (student_id, timestamp, date)
        VALUES (?, ?, ?)
    ''', (student_id, now, today_str))
    
    conn.commit()
    conn.close()
    return True, f"Asistencia registrada: {student_name}"

def get_attendance_data():
    """Returns a pandas DataFrame with attendance records."""
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT a.timestamp, s.id, s.name, s.group_name
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        ORDER BY a.timestamp DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def generate_qr(data):
    """Generates a QR code image from string data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes for download
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr # Returns bytes

# Initialize DB on load ensures tables exist
if not os.path.exists(DB_NAME):
    init_db()
else:
    # Always try to init to ensure tables exist even if file exists (e.g. empty file)
    init_db()

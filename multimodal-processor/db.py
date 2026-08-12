import pymysql
import datetime
import streamlit as st

def get_connection():
    return pymysql.connect(
        host=st.secrets["mysql"]["host"],
        port=int(st.secrets["mysql"]["port"]),
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        charset="utf8mb4"
    )

def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME,
                mode VARCHAR(10) NOT NULL,
                action VARCHAR(50) NOT NULL,
                input_data TEXT,
                output_data TEXT,
                email VARCHAR(100) NULL
            )
        """)
        try:
            cursor.execute("ALTER TABLE history ADD COLUMN email VARCHAR(100) NULL")
            conn.commit()
        except Exception:
            pass
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NULL,
                name VARCHAR(100) NOT NULL,
                profile_pic VARCHAR(255),
                auth_provider VARCHAR(20) DEFAULT 'local',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(100) NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                auth_provider VARCHAR(20) NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Failed to initialize database: {e}")

def load_history_from_db(email=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if email:
            cursor.execute(
                "SELECT timestamp, mode, action, input_data, output_data FROM history WHERE email=%s ORDER BY timestamp ASC",
                (email,)
            )
        else:
            cursor.execute("SELECT timestamp, mode, action, input_data, output_data FROM history WHERE email IS NULL ORDER BY timestamp ASC")
        rows = cursor.fetchall()
        history = []
        for row in rows:
            history.append({
                "timestamp": str(row[0]),
                "mode": row[1],
                "action": row[2],
                "input": row[3],
                "output": row[4]
            })
        cursor.close()
        conn.close()
        return history
    except Exception as e:
        return []

def add_to_history_db(mode, action, input_data, output_data, email=None):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (timestamp, mode, action, input_data, output_data, email) VALUES (%s, %s, %s, %s, %s, %s)",
            (now, mode, action, input_data, output_data, email)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        pass

def clear_history_db(email=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if email:
            cursor.execute("DELETE FROM history WHERE email=%s", (email,))
        else:
            cursor.execute("DELETE FROM history WHERE email IS NULL")
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        return False

def authenticate_user(email, password):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT email, name, profile_pic, auth_provider FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        return None

def register_user(email, password, name, auth_provider="local", profile_pic=None):
    if not profile_pic:
        profile_pic = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=0D8ABC&color=fff&size=128"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "User with this email already exists."
        
        cursor.execute(
            "INSERT INTO users (email, password, name, auth_provider, profile_pic) VALUES (%s, %s, %s, %s, %s)",
            (email, password, name, auth_provider, profile_pic)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Registration successful!"
    except Exception as e:
        return False, f"Registration failed: {e}"

def record_login_in_db(email, auth_provider):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO login_history (email, auth_provider) VALUES (%s, %s)",
            (email, auth_provider)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        pass

def register_or_login_google(email, name, profile_pic):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT email, name, profile_pic, auth_provider FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        
        if not user:
            cursor.execute(
                "INSERT INTO users (email, password, name, auth_provider, profile_pic) VALUES (%s, NULL, %s, 'google', %s)",
                (email, name, profile_pic)
            )
            conn.commit()
            cursor.execute("SELECT email, name, profile_pic, auth_provider FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        return None

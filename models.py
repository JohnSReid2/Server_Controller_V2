import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = "database.db"

# Initialize the database and create the users table if it doesn't exist
def init_db():
    with sqlite3.connect(DB_PATH) as conn: # Create or open the database, auto-closing it after the block by using with
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

# Create a user with a hashed password
def create_user(username, password, is_admin=False):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        hashed_pw = generate_password_hash(password) # Hash the password using werkzeug's security module 
        c.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, hashed_pw, int(is_admin)))
        conn.commit()

# Retrieve a user by username
def get_user(username):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username))
        return c.fetchone()
    
# Retrieve a user by ID
def get_user_by_id(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return c.fetchone()
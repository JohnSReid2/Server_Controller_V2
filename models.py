import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from exceptions import UserAlreadyExists, UserNotFound, AuthenticationError

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
                is_admin INTEGER DEFAULT 0,
                theme_preference TEXT DEFAULT 'light'
            )
        ''')
        conn.commit()

# get user by username
def get_user(username):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()

    if user is None:
        raise UserNotFound(f"User with username '{username}' not found.")
    
    return user

# Get user by ID
def get_user_by_id(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()

    if user is None:
        raise UserNotFound(f"User with ID '{user_id}' not found.")
    
    return user
    
# Create a user with a hashed password
def create_user(username, password, is_admin):
    password = generate_password_hash(password)  # Hash the password
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)',
            (username, password, int(is_admin))
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: users.username" in str(e):
            raise UserAlreadyExists(f"User '{username}' already exists.")
        else:
            raise
    finally:
        conn.close()


# Update a user's theme preference
def update_user_theme(user_id, theme):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('UPDATE users SET theme_preference = ? WHERE id = ?',(theme, user_id))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        conn.close()

# Get a user's theme preference
def get_user_theme(user_id):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT theme_preference FROM users WHERE id = ?', (user_id,))
        theme = c.fetchone()
        if theme is None:
            raise UserNotFound(f"User with ID '{user_id}' not found.")
        return theme[0]
    except sqlite3.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        conn.close()
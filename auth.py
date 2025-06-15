from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import check_password_hash
from forms import LoginForm, CreateUserForm
from functools import wraps
import models
from logger import logger
from exceptions import UserNotFound, AuthenticationError

# Blueprint for auth-related routes (e.g., login, logout)
auth = Blueprint('auth', __name__)

# Initialize Flask-Login's LoginManager
login_manager = LoginManager()

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id_, username, is_admin):
        self.id = id_
        self.username = username
        self.is_admin = is_admin

    # Helper to construct a User from DB row tuple
    @staticmethod
    def from_db(user_row):
        return User(id_=user_row[0], username=user_row[1], is_admin=bool(user_row[3]))


# Flask-Login callback to load a user from the session by ID.
# Called automatically by Flask-Login to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    try:
        user = models.get_user_by_id(user_id)
        return User.from_db(user)
    except UserNotFound:
        logger.warning(f"[AUTH] Tried to load unknown user ID: {user_id}")
        return None


# Route for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        try:
            user = models.get_user(username)

            # Verify the password
            if not check_password_hash(user[2], password):
                raise AuthenticationError("Incorrect password.")
            
            # Create a User object and log them in
            user_obj = User.from_db(user)
            login_user(user_obj)
            flash("Logged in successfully.", "success")
            logger.info(f"User {username} logged in")
            return redirect(url_for('dashboard'))
        
        except UserNotFound:
            flash("User does not exist.", "error")
            logger.warning(f"Failed login: unknown user '{username}'")
        except AuthenticationError:
            flash("Incorrect password.", "error")
            logger.warning(f"Failed login: incorrect password for user '{username}'")
        except Exception as e:
            flash("An unexpected error occurred.", "error")
            logger.error(f"[LOGIN ERROR] {str(e)}")

    return render_template('login.html', form=form)

# Route for user logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
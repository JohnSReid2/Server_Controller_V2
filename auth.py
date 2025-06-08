from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import check_password_hash
import models

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id_, username, is_admin):
        self.id = id_
        self.username = username
        self.is_admin = is_admin

    @staticmethod
    def from_db(user_row):
        return User(id_=user_row[0], username=user_row[1], is_admin=bool(user_row[3]))

@login_manager.user_loader
def load_user(user_id):
    user_row = models.get_user_by_id(user_id)
    return User.from_db(user_row) if user_row else None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = models.get_user(username)
        if user and check_password_hash(user[2], password):
            login_user(User.from_db(user))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials.")
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
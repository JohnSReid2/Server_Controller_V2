from flask import Flask, render_template
from flask_login import login_required, current_user
from flask_wtf import CSRFProtect
import models
from auth import auth, login_manager
from admin import admin_bp
from settings import settings_bp
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CSRFProtect(app) # Enable CSRF protection globally

# Register auth module and init login
app.register_blueprint(auth)
app.register_blueprint(settings_bp)
app.register_blueprint(admin_bp)

login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# Root url, redirect to dashboard if logged in
@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username, is_admin=current_user.is_admin)

if __name__ == "__main__":
    models.init_db()
    app.run(debug=True)


    

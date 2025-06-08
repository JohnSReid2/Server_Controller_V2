from flask import Flask, render_template
from flask_login import login_required, current_user
import models
from auth import auth, login_manager

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Register auth module and init login
app.register_blueprint(auth)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username, is_admin=current_user.is_admin)

if __name__ == "__main__":
    models.init_db()
    app.run(debug=True)
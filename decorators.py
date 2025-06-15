from functools import wraps
from flask import abort
from flask_login import current_user
from logger import logger

# Decorator to restrict access to admin users only
def admin_required(f):
    @wraps(f)  # Preserves original function metadata
    def decorated_function(*args, **kwargs):
        # Check if user is logged in and has admin rights
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Return HTTP 403 Forbidden if not allowed
        return f(*args, **kwargs)  # Proceed to route handler if authorized
    return decorated_function

# Decorator to log when a route is accessed
def log_access(label=None):
    def decorator(f):
        @wraps(f)  # Preserves original function metadata
        def decorated_function(*args, **kwargs):
            # Get username if user is logged in, otherwise log as 'Anonymous'
            user = current_user.username if current_user.is_authenticated else "Anonymous"
            # Log access with a label or the function's name
            logger.info(f"[ACCESS] {user} accessed {label or f.__name__}")
            return f(*args, **kwargs)  # Proceed to route handler
        return decorated_function
    return decorator
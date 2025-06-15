
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from forms import CreateUserForm
import models
from decorators import admin_required, log_access
from logger import logger
from exceptions import UserAlreadyExists


# Define a Blueprint specific to admin-related routes
admin_bp = Blueprint("admin", __name__)


# Admin Panel Route
@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
@log_access("Admin Panel")
def admin_panel():
    form = CreateUserForm()

    # Check if form was submitted and is valid
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        is_admin = form.is_admin.data

        try:
            # Attempt to create the user in the database
            models.create_user(username, password, is_admin)
            flash("User created successfully.", "success")
            logger.info(
                f"[ADMIN] Created user: {username}, Admin: {is_admin} by {current_user.username}"
            )

        except UserAlreadyExists as e:
            # Handle specific case: username already taken
            flash(str(e), "error")
            logger.warning(f"[ADMIN] {e}")

        except Exception as e:
            # Catch any other unexpected error
            flash("Unexpected error occurred.", "error")
            logger.error(f"[ADMIN ERROR] Failed to create user: {str(e)}")

        # Refresh the page regardless of outcome to avoid form resubmission
        return redirect(url_for('admin.admin_panel'))

    # Render the admin panel template with the user creation form
    return render_template("admin.html", form=form)
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from decorators import admin_required, log_access
from logger import logger
from models import update_user_theme
from flask import request, jsonify

# Define a Blueprint specific to settings-related routes
settings_bp = Blueprint("settings", __name__)

# Route to change user theme preference, accessible only to logged-in users
@settings_bp.route('/api/set-theme', methods=['POST'])
@login_required
def set_theme_preference():
    theme = request.json.get("theme")
    if theme not in ["light", "dark", "system"]:
        logger.warning(f"[SETTINGS] {current_user.username} attempted to set invalid theme: {theme}")
        return jsonify({"error": "Invalid theme"}), 400
    update_user_theme(current_user.id, theme)
    logger.info(f"[SETTINGS] {current_user.username} updated theme to {theme}")
    return jsonify({"status": "ok"})
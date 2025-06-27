from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

main_bp = Blueprint('main', __name__, template_folder='../templates')


# -------------------------------
#  Home Page
# -------------------------------
@main_bp.route('/')
@main_bp.route('/home')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        current_app.logger.exception("Error loading home page")
        flash("Failed to load home page.", "danger")
        return redirect(url_for('auth.login'))


# -------------------------------
#  Catch-all 404 Handler
# -------------------------------
@main_bp.app_errorhandler(404)
def fallback_to_home(error):
    current_app.logger.warning("404 Not Found: %s", request.path)
    flash("Invalid URL. Redirected to home page.", "warning")
    return redirect(url_for('main.home'))

import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_jwt_extended import create_access_token, unset_jwt_cookies, set_access_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db

auth_bp = Blueprint('auth', __name__, template_folder='../templates')


# -------------------------------
#  Validation Helpers
# -------------------------------
def is_valid_username(username):
    """Valid username: 3–20 characters, letters, numbers, underscores."""
    return re.fullmatch(r'^\w{3,20}$', username) is not None

def is_valid_password(password):
    """Valid password: 8+ chars, 1 uppercase, 1 digit, 1 special char."""
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )


# -------------------------------
#  Register
# -------------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if not is_valid_username(username):
                flash('Username must be 3–20 characters long and contain only letters, numbers, and underscores.', 'danger')
                return redirect(url_for('auth.register'))

            if not is_valid_password(password):
                flash('Password must be at least 8 characters long and include one uppercase letter, one number, and one special character.', 'danger')
                return redirect(url_for('auth.register'))

            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'warning')
                return redirect(url_for('auth.register'))

            # Save user
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('auth.login'))

        return render_template('register.html')

    except Exception as e:
        db.session.rollback()
        current_app.logger.error("Registration error: %s", str(e))
        flash('An error occurred during registration.', 'danger')
        return redirect(url_for('auth.register'))


# -------------------------------
#  Login
# -------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                access_token = create_access_token(identity=str(user.id))
                session['username'] = user.username

                response = redirect(url_for('main.home'))
                set_access_cookies(response, access_token)

                flash('Login successful!', 'success')
                return response

            flash('Invalid credentials.', 'danger')
            return redirect(url_for('auth.login'))

        return render_template('login.html')

    except Exception as e:
        current_app.logger.error("Login error: %s", str(e))
        flash('An error occurred during login.', 'danger')
        return redirect(url_for('auth.login'))


# -------------------------------
#  Logout
# -------------------------------
@auth_bp.route('/logout')
def logout():
    try:
        response = redirect(url_for('auth.login'))
        unset_jwt_cookies(response)
        session.clear()

        flash('You have been logged out.', 'info')
        return response

    except Exception as e:
        current_app.logger.error("Logout error: %s", str(e))
        flash('An error occurred during logout.', 'danger')
        return redirect(url_for('main.home'))


# -------------------------------
#  Catch-All Route Handler
# -------------------------------
@auth_bp.route('/<path:subpath>')
def catch_all_auth(subpath):
    if subpath.startswith('register'):
        flash(f"Invalid path '/auth/{subpath}'. Redirected to Register.", "warning")
        return redirect(url_for('auth.register'))
    elif subpath.startswith('login'):
        flash(f"Invalid path '/auth/{subpath}'. Redirected to Login.", "warning")
        return redirect(url_for('auth.login'))
    else:
        flash(f"Invalid auth path '/auth/{subpath}'. Redirected to Login.", "warning")
        return redirect(url_for('auth.login'))

from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

from Models.user import User
from Models.database import db
from app import app

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username and password are correct
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

        # If the username and password are incorrect, show an error message
        error_message = 'Invalid username or password'
        return render_template('login.html', error_message=error_message)

    # If the request method is GET, render the login page
    return render_template('login.html')

@auth.route('/logout')
def logout():
    # Clear the user session and redirect to the login page
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route('/users')
def view_users():
    # Check if the user is logged in and has admin privileges
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if not user.is_admin:
        return "You do not have permission to view this page."

    # Get all the users from the database
    users = User.query.all()

    return render_template('users.html', users=users)

@auth.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        is_admin = request.form.get('is_admin')

        # Check if the passwords match
        if password != confirm_password:
            error_message = 'Passwords do not match'
            return render_template('create_user.html', error_message=error_message)

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error_message = 'Username is already taken'
            return render_template('create_user.html', error_message=error_message)

        # Create a new user object and add it to the database
        user = User(username=username, password=generate_password_hash(password), is_admin=is_admin)
        db.session.add(user)
        db.session.commit()

        # Redirect the user to the dashboard
        return redirect(url_for('dashboard'))

    # If the request method is GET, render the create user page
    return render_template('create_user.html')


@auth.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Get the user object
    user = User.query.get(user_id)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        is_admin = request.form.get('is_admin')

        # Check if the passwords match
        if password != confirm_password:
            error_message = 'Passwords do not match'
            return render_template('edit_user.html', user=user, error_message=error_message)

        # Update the user object with the new data
        user.username = username
        user.password = generate_password_hash(password)
        user.is_admin = is_admin
        db.session.commit()

        # Redirect the user to the dashboard
        return redirect(url_for('dashboard'))

    # If the request method is GET, render the edit user page
    return render_template('edit_user.html', user=user)


@auth.route('/users/delete/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    # Get the user object
    user = User.query.get(user_id)

    # Delete the user object from the database
    db.session.delete(user)
    db.session.commit()

    # Redirect the user to the dashboard
    return redirect(url_for('dashboard'))

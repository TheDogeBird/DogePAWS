# views/auth.py
# Routes for authentication and user management
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

from Models.user import User, is_admin
from Models.database import db

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
def get_all_users():
    # Get all users
    users = User.query.all()

    # Render the users page with the list of users
    return render_template('users.html', users=users)


@auth.route('/users/<int:user_id>')
def get_user(user_id):
    # Get the user object
    user = User.query.get(user_id)

    # Render the user page with the user object
    return render_template('user.html', user=user)


@auth.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Get the form data
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        # Create the user object
        new_user = User(username=username, password=generate_password_hash(password), role=role)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the users page
        return redirect(url_for('auth.get_all_users'))

    # If the request method is GET, render the create user page
    return render_template('create_user.html')


@auth.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Get the user object
    user = User.query.get(user_id)

    if request.method == 'POST':
        # Get the form data
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        # Update the user object
        user.username = username
        user.password = generate_password_hash(password)
        user.role = role

        # Update the user in the database
        db.session.commit()

        # Redirect to the user page
        return redirect(url_for('auth.get_user', user_id=user_id))

    # If the request method is GET, render the edit user page
    return render_template('edit_user.html', user=user)


# Delete a user by ID
@auth.route('/users/delete/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    # Check if the user is logged in and an administrator
    if 'user_id' not in session or not is_admin():
        return redirect(url_for('auth.login'))

    # Get the user object
    user = User.query.get(user_id)

    # If the user doesn't exist, show an error message
    if not user:
        error_message = f"User with ID {user_id} not found"
        return render_template('error.html', error_message=error_message)

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    # Redirect to the user list page
    return redirect(url_for('auth.user_list'))

from flask import Blueprint, render_template, request, redirect, session
from Models.user import User
# from Models.database import Session, get_db
# from config import settings

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/home')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.authenticate(username, password)
        if user is not None:
            session['username'] = user.username
            return redirect('/home')
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')
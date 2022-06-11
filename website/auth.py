from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()

        if(user):
            if(check_password_hash(user.password, password)):
                flash('Logged In', category = 'success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again', category = 'error')
        else:
            flash('Username does not exist, try again', category = 'error')


    return render_template("login.html", user = current_user)

@auth.route('/', methods = ['GET', 'POST'])
def redir():
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if(request.method == 'POST'):
        email = request.form.get('email')
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confPassword = request.form.get('confPassword')

        CheckForUsername = User.query.filter_by(username = username).first()
        CheckForEmail = User.query.filter_by(email = email).first()

        if(CheckForUsername):
            flash('Username not available', category = 'error')
        elif(CheckForEmail):
            flash('User Exists with the given email', category = 'error')
        elif(password != confPassword):
            flash('Passwords do not match', category = 'error')
        else:
            new_user = User(email = email, name = name, username = username, password = generate_password_hash(password, method = 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            flash('New Account Created!!!', category = 'success')
            
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user = current_user)
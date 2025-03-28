from flask import Blueprint, render_template, request, redirect, flash, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        check_username = User.query.filter_by(username= username).first()
        
        if check_username:
            if check_password_hash(check_username.password, password):
                flash("Login Successfully", category='success')
                login_user(check_username, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password", category='error')
        else:
            flash('Username not found', category='error')        
    
    
    return render_template('login.html')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        check_username = User.query.filter_by(username= username).first()
        check_email = User.query.filter_by(email= email).first()
        
        
        if check_email:
            flash('Email is already exist, try again', category='error')
        elif check_username:
            flash('Username is already exist, try again', category='error')
        elif password1 != password2:
            flash('Password doest not match', category='error')
        elif not password1:  # Check if password is None or empty string first
            flash('Password is required', category='error')    
        elif len(password1) < 3 :
            flash('Password must be 3 characters above', category='error')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method= 'pbkdf2:sha256'))  
            db.session.add(new_user)
            db.session.commit()
            
            flash('Username Successfully Created', category='success')
            
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
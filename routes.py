# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, bcrypt

# Create a Blueprint
main = Blueprint('main', __name__)

# Signup Route
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already registered!")
            return redirect(url_for('main.signup'))
        
        new_user = User(full_name=full_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please login.")
        return redirect(url_for('main.login'))

    return render_template('signup.html')

# Login Route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Login successful!")
            return redirect(url_for('main.home'))
        else:
            flash("Invalid email or password")
            return redirect(url_for('main.login'))

    return render_template('login.html')

# Home Route
@main.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    return "Welcome to FitTrack!"

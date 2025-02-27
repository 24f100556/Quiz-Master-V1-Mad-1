from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import db, User, Course, Chapter, Quiz, Question, Option, Score
from datetime import datetime 
from flask_login import login_user , login_required , logout_user, current_user





@app.route('/')
@login_required
def index():
    return render_template('index.html',user = current_user)



@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '' or password == '':
        flash('Username or password cannot be empty.', category= 'error')
        return redirect(url_for('login'))
    user = User.query.filter_by(username=username).first()
    
    if not user :
        flash('User does not exist',category='error')
        return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Incorrect password',category='error')
        return redirect(url_for('login'))
    flash('Logged in successfully!', category='success')
    login_user(user, remember= True)
    return redirect(url_for('index'))

 

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    dob_str = request.form.get('dob') 
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
    level = request.form.get('level')
    if username == '' or password == '':
        flash('User name or password cannot be empty.',category='error')
        return redirect(url_for('register'))
    if User.query.filter_by(username=username).first():
        flash('Oops! That username is taken. You can try adding numbers or a unique word',category='error')
        return redirect(url_for('register'))
    if User.query.filter_by(email=email).first():
        flash('Oops! An account with this email already exists. Please use a different email.',category='error')
        return redirect(url_for('register'))
    user = User( email = email, username = username, password = password, name = name,  level = level,dob = dob) 
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered.',category='success')
    login_user(user, remember= True)
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    
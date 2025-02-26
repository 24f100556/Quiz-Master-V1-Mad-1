from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import db, User, Course, Chapter, Quiz, Question, Option, Score
# from datetime import datetime 






@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '' or password == '':
        flash('User name or password cannot be empty.')
        return redirect(url_for('login'))
    user = User.query.filter_by(username=username).first()
    if not user :
        flash('User does not exist')
        return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Incorrect password')
        return redirect(url_for('login'))
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
    # dob = request.form.get('dob')
   




    level = request.form.get('level')
    if username == '' or password == '':
        flash('User name or password cannot be empty.')
        return redirect(url_for('register'))
    if User.query.filter_by(username=username).first():
        flash('Oops! That username is taken. You can try adding numbers or a unique word')
        return redirect(url_for('register'))
    user = User( email = email, username = username, password = password, name = name,  level = level) #dob = dob, add after
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered.')
    return redirect(url_for('login'))
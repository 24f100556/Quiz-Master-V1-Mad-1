from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import db, User, Course, Chapter, Quiz, Question, Option, Score
from datetime import datetime 
from flask_login import login_user , login_required , logout_user, current_user
import sqlite3




@app.route('/')
@login_required
def index():
    user = current_user
    if user.is_admin:
        return redirect(url_for('admin'))
    else:
         return render_template('index.html',user = current_user)
    


@app.route('/admin')
@login_required
def admin():
    user = current_user
    if not user.is_admin:
        flash('YOU ARE NOT AUTHORIZED TO VIEW THIS PAGE.',category = 'error')
        return redirect(url_for('index'))
    return render_template('admin/admin.html',user = current_user, total_users = User.query.count())





@app.route('/login')
def login():
    return render_template('login.html', user = current_user)


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
    return redirect(url_for('index',user = current_user))

 
@app.route('/register')
def register():
    return render_template('register.html',user = current_user)

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
    if current_user.is_authenticated and current_user.is_admin:
            flash('User registered successfully!', 'success')
            return redirect(url_for('manage_users'))
    login_user(user, remember= True)
    flash('Registration successful!', 'success')
    return redirect(url_for('index',user = current_user))

 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)




@app.route('/profile/edit', methods=['GET','POST'])
@login_required
def edit_profile():
    if request.method == 'POST' :

        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        current_user.name = request.form.get('name')
        current_user.level = request.form.get('level')

        dob_str = request.form.get('dob')  
        if dob_str:
            current_user.dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

        
        existing_user = User.query.filter_by(username=current_user.username).first()
        if existing_user and existing_user.id != current_user.id:
            flash('Oops! That username is taken.', category='error')
            return redirect(url_for('edit_profile'))

        existing_email = User.query.filter_by(email=current_user.email).first()
        if existing_email and existing_email.id != current_user.id:
            flash('Oops! An account with this email already exists.', category='error')
            return redirect(url_for('edit_profile'))

        
        cpassword = request.form.get('cpassword')
        if not current_user.check_password(cpassword):  
            flash('Incorrect current password', category='error')
            return redirect(url_for('edit_profile'))


        new_password = request.form.get('password')
        if new_password:
            current_user.password = new_password  

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html',user = current_user)

@app.route('/dashboard')
@login_required  
def dashboard():
    return render_template('dashboard.html',user=current_user) 


@app.route('/manage_users')
@login_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html',users=users,user=current_user)

@app.route('/add_user')
@login_required
def add_user():
    return redirect(url_for('register'))

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required  
def admin_edit_user(user_id):
  
    user = User.query.get_or_404(user_id)  
    
    if request.method == 'POST':
      
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.name = request.form.get('name')
        user.level = request.form.get('level')
        dob_str = request.form.get('dob')  
        if dob_str:
            user.dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

        db.session.commit()
        flash('User profile updated successfully!', 'success')
        return redirect(url_for('manage_users')) 

    return render_template('admin/edit_user.html', user=user)


@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
  
    return redirect(url_for('manage_users'))  


    
    

    
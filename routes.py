from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import db, User, Course, Chapter, Quiz, Question, Option, Score
from datetime import datetime 
from flask_login import login_user , login_required , logout_user, current_user





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
    quizzes = Quiz.query.all()

    if not user.is_admin:
        flash('YOU ARE NOT AUTHORIZED TO VIEW THIS PAGE.',category = 'error')
        return redirect(url_for('index'))
    return render_template('admin/admin.html',user = current_user, total_users = User.query.count(),quizzes = quizzes)





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


    
    

@app.route('/admin/courses')
def manage_courses():
    courses = Course.query.all()
    return render_template('admin/courses.html', courses=courses,user = current_user)

@app.route('/admin/coursses/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['name']
        description = request.form['description']
        if course_name:
            new_course = Course(name=course_name,description=description)
            description = description if description else None 
            db.session.add(new_course)
            db.session.commit()
            flash('Course added successfully!', 'success')
            return redirect(url_for('manage_courses'))
    return render_template('admin/add_course.html',user = current_user)

@app.route('/admin/courses/delete/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
  
    return redirect(url_for('manage_courses'))  






@app.route('/admin/course/<int:course_id>/add_chapter', methods=['GET', 'POST'])
def add_chapter(course_id):
    course = Course.query.get_or_404(course_id)
    chapters = Chapter.query.filter_by(course_id=course_id).all()
    if request.method == 'POST':
        chapter_name = request.form['name']
        description = request.form['description']
        if chapter_name:
            new_chapter = Chapter(name=chapter_name, description=description, course=course)
            db.session.add(new_chapter)
            db.session.commit()
            flash('Chapter added successfully!', 'success')
            return redirect(url_for('manage_courses'))
    return render_template('admin/add_chapter.html',chapters = chapters, course=course,user = current_user)



@app.route('/chapter/<int:chapter_id>/delete', methods=['POST'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    course_id = chapter.course_id  
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter  deleted successfully!', 'success')
  

    return redirect(url_for('add_chapter', course_id=course_id))







@app.route('/admin/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    chapters = Chapter.query.all()  

    if request.method == 'POST':
        quiz_name = request.form.get('name')
        quiz_date_str = request.form.get('date')
        quiz_time_str = request.form.get('time')
        chapter_id = request.form.get('chapter_id')

        quiz_date = datetime.strptime(quiz_date_str, "%Y-%m-%d").date()
        quiz_time = datetime.strptime(quiz_time_str, "%H:%M").time()    

        
        new_quiz = Quiz(
            name=quiz_name,
            date=quiz_date,
            time=quiz_time,
            chapter_id=chapter_id
        )

        db.session.add(new_quiz)
        db.session.commit()

        flash('Quiz created successfully!', 'success')
        return redirect(url_for('add_quiz'))

   
    quizzes = Quiz.query.all()
    return render_template('admin/add_quiz.html', quizzes=quizzes, chapters=chapters, user=current_user)


@app.route('/admin/quiz/delete/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('add_quiz'))



@app.route('/admin/quiz/<int:quiz_id>/add_question', methods=['GET', 'POST'])
def add_question(quiz_id):
    quiz = Quiz.query.get(quiz_id)

    if request.method == 'POST':
     
        statement = request.form['statement']
        marks = request.form['marks']

        question = Question(
            statement=statement,
            marks=marks,
            quiz_id=quiz_id
        )
        db.session.add(question)
        db.session.commit()  

        
        options = [
            request.form['option1'],
            request.form['option2'],
            request.form.get('option3'),
            request.form.get('option4')
        ]

  
        correct_option = int(request.form['correct_option']) - 1

        for index, option_text in enumerate(options):
            if option_text:
                option = Option(
                    option_text=option_text,
                    is_correct=(index == correct_option),
                    ques_id=question.id
                )
                db.session.add(option)

        db.session.commit()

        flash('Question added!', 'success')
        return redirect(url_for('add_question', quiz_id=quiz_id))

    return render_template('admin/add_question.html', quiz=quiz,user = current_user)

@app.route('/delete_question/<int:question_id>', methods=['POST', 'GET'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id  


    for option in question.options:
        db.session.delete(option)

    db.session.delete(question)
    db.session.commit()

    flash('Question deleted successfully!', 'success')
    return redirect(url_for('quiz_details', quiz_id=quiz_id,user=current_user))



@app.route('/admin/quiz/<int:quiz_id>')
def quiz_details(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('admin/quiz_details.html', quiz=quiz,user = current_user)

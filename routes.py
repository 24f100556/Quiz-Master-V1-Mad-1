from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import db, User, Course, Chapter, Quiz, Question, Option, Score
from datetime import datetime,timedelta
from flask_login import login_user , login_required , logout_user, current_user





    

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
        return redirect(url_for('profile'))
    return render_template('edit_profile.html',show_nav=False,user = current_user)

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


@app.route('/admin/courses/update/<int:course_id>', methods=['GET', 'POST'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        course.name = request.form.get('name')
        course.description = request.form.get('description') 
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('manage_courses'))
    return render_template('admin/update_course.html', course=course,user = current_user) 













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
            return redirect(url_for('add_chapter', course_id=course_id))
    return render_template('admin/add_chapter.html',chapters = chapters, course=course,user = current_user)



@app.route('/admin/chapter/<int:chapter_id>/add_chapter/update', methods=['GET', 'POST'])
def update_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    if request.method == 'POST':
        chapter.name = request.form.get('name')
        chapter.description = request.form.get('description')
        db.session.commit()
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('add_chapter', course_id=chapter.course_id))
    return render_template('admin/update_chapter.html', chapter=chapter,user = current_user)






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
        quiz_time = datetime.strptime(request.form.get('time') , "%I:%M %p").time()

        chapter_id = request.form.get('chapter_id')

        quiz_date = datetime.strptime(quiz_date_str, "%Y-%m-%d").date()
        duration_minutes = request.form.get('duration_minutes')



        
        new_quiz = Quiz(
            name=quiz_name,
            date=quiz_date,
            time=quiz_time,
            chapter_id=chapter_id,
            duration_minutes=duration_minutes
        )

        db.session.add(new_quiz)
        db.session.commit()

        flash('Quiz created successfully!', 'success')
        return redirect(url_for('add_quiz'))

   
    quizzes = Quiz.query.all()
    return render_template('admin/add_quiz.html', quizzes=quizzes, chapters=chapters, user=current_user)


@app.route('/admin/quiz/update/<int:quiz_id>', methods=['GET', 'POST'])
def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapters = Chapter.query.all()

    if request.method == 'POST':
        quiz.name = request.form.get('name')
        quiz.date = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date()
        quiz.time = datetime.strptime(request.form.get('time') , "%I:%M %p").time()
        quiz.duration_minutes = request.form.get('duration_minutes')
        quiz.chapter_id = request.form.get('chapter_id')
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('quiz_details', quiz_id=quiz.id))

    return render_template('admin/update_quiz.html', quiz=quiz, chapters=chapters,user = current_user)




@app.route('/admin/quiz/delete/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('add_quiz'))


@app.route('/admin/quiz/<int:quiz_id>')
def quiz_details(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
   
    return render_template('admin/quiz_details.html', quiz=quiz,user = current_user)



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
        return redirect(url_for('quiz_details', quiz_id=quiz_id))

    return render_template('admin/add_question.html', quiz=quiz,user = current_user)




@app.route('/admin/question/<int:question_id>/update', methods=['GET', 'POST'])
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    options = Option.query.filter_by(ques_id=question.id).all()
    if request.method == 'POST':
        question.statement = request.form.get('statement')
        question.marks = request.form.get('marks')
     
        for option in options:
            option_text = request.form.get(f'option_{option.id}')
            is_correct = request.form.get(f'is_correct_{option.id}') == 'on'
            option.option_text = option_text
            option.is_correct = is_correct
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('quiz_details', quiz_id=question.quiz_id))

    return render_template('admin/update_question.html', question=question,user = current_user, quiz=question.quiz,options=options)




@app.route('/admin/delete_question/<int:question_id>', methods=['POST', 'GET'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id  


    for option in question.options:
        db.session.delete(option)

    db.session.delete(question)
    db.session.commit()

    flash('Question deleted successfully!', 'success')
    return redirect(url_for('quiz_details', quiz_id=quiz_id,user=current_user))




#-------------------------User Routes------------------------------------------------



@app.route('/')
@login_required
def index():
    user = current_user
    quizzes = Quiz.query.all()

    available_quizzes = []
    upcoming_quizzes = []
    ended_quizzes = []

    now = datetime.now()

    for quiz in quizzes:
        quiz_start = datetime.combine(quiz.date, quiz.time)

        # Validate duration_minutes
        try:
            duration = float(quiz.duration_minutes)
            quiz_end = quiz_start + timedelta(minutes=duration)
        except (TypeError, ValueError):
            duration = None
            quiz_end = None

        # Upcoming quiz: starts after now
        if quiz_start > now:
            upcoming_quizzes.append({
                'quiz': quiz,
                'start': quiz_start,
                'end': quiz_end
            })

        # Ended quiz: quiz_end exists AND now is after quiz_end
        elif quiz_end and now > quiz_end:
            ended_quizzes.append({
                'quiz': quiz,
                'start': quiz_start,
                'end': quiz_end
            })

        # Available quiz: already started and either no end time or still ongoing
        elif quiz_start <= now and (quiz_end is None or now <= quiz_end):
            available_quizzes.append({
                'quiz': quiz,
                'start': quiz_start,
                'end': quiz_end
            })

    if user.is_admin:
        return redirect(url_for('admin'))

    return render_template(
        'index.html',
        user=user,
        available_quizzes=available_quizzes,
        upcoming_quizzes=upcoming_quizzes,
        ended_quizzes=ended_quizzes
    )














# @app.route('/start_quiz/<int:quiz_id>', methods=['GET', 'POST'])
# @login_required
# def start_quiz(quiz_id):
#     quiz = Quiz.query.get_or_404(quiz_id)

#     # Step 1: Calculate quiz start and end datetimes
#     quiz_start = datetime.combine(quiz.date, quiz.time)

#     # Validate and convert duration_minutes
#     duration_minutes = int(quiz.duration_minutes) if quiz.duration_minutes and str(quiz.duration_minutes).isdigit() else None

#     quiz_end = quiz_start + timedelta(minutes=duration_minutes) if duration_minutes else None
  


#     # Step 2: Get current time
#     current_time = datetime.now()

#     # Step 3: Validate time window
#     if current_time < quiz_start:
#         flash(f"The quiz hasn't started yet! Starts at {quiz_start.strftime('%Y-%m-%d %I:%M %p')}.", "warning")
#         return redirect(url_for('index'))

#     if quiz_end and current_time > quiz_end:
#         flash("The quiz has already ended!", "danger")
#         return redirect(url_for('index'))

#     # Step 4: Handle form submission (when user submits answers)
#     if request.method == 'POST':
#         scored_marks = 0
#         total_marks = 0

#         for question in quiz.questions:
#             total_marks += question.marks
#             selected_option_id = request.form.get(f'question_{question.id}')
            
#             if selected_option_id:
#                 selected_option = Option.query.get(int(selected_option_id))

#                 if selected_option and selected_option.is_correct:
#                     scored_marks += question.marks

#         percentage_score = (scored_marks / total_marks) * 100 if total_marks > 0 else 0

#         new_score = Score(
#             user_id=current_user.id,
#             quiz_id=quiz.id,
#             total_score=scored_marks,
#         )
#         db.session.add(new_score)
#         db.session.commit()

#         flash(f'You scored {scored_marks}/{total_marks} ({percentage_score:.2f}%)', 'success')
#         return redirect(url_for('index'))

#     # Step 5: Render quiz attempt page if within allowed time window
#     return render_template('start_quiz.html', quiz=quiz, user=current_user, quiz_start=quiz_start, quiz_end=quiz_end)




@app.route('/start_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Step 1: Calculate quiz start and end datetimes
    quiz_start = datetime.combine(quiz.date, quiz.time)

    # Validate and convert duration_minutes (SAME AS OLD)
    duration_minutes = int(quiz.duration_minutes) if quiz.duration_minutes and str(quiz.duration_minutes).isdigit() else None

    quiz_end = quiz_start + timedelta(minutes=duration_minutes) if duration_minutes else None

    # Step 2: Get current time
    current_time = datetime.now()

    # Step 3: Validate time window
    if current_time < quiz_start:
        flash(f"The quiz hasn't started yet! Starts at {quiz_start.strftime('%Y-%m-%d %I:%M %p')}.", "warning")
        return redirect(url_for('index'))

    if quiz_end and current_time > quiz_end:
        flash("The quiz has already ended!", "danger")
        return redirect(url_for('index'))

    # Prepare feedback data
    feedback = []
    scored_marks = 0
    total_marks = 0
    percentage_score = 0

    # Step 4: Handle form submission (when user submits answers)
    if request.method == 'POST':
        for question in quiz.questions:
            total_marks += question.marks
            selected_option_id = request.form.get(f'question_{question.id}')

            selected_option = None
            is_correct = False

            if selected_option_id:
                selected_option = Option.query.get(int(selected_option_id))
                if selected_option and selected_option.is_correct:
                    scored_marks += question.marks
                    is_correct = True

            feedback.append({
                'question': question,
                'selected_option': selected_option,
                'is_correct': is_correct,
                'accepted_options': [opt for opt in question.options if opt.is_correct],
                'score': question.marks if is_correct else 0
            })

        percentage_score = (scored_marks / total_marks) * 100 if total_marks > 0 else 0

        new_score = Score(
            user_id=current_user.id,
            quiz_id=quiz.id,
            total_score=scored_marks,
        )
        db.session.add(new_score)
        db.session.commit()

        flash(f'You scored {scored_marks}/{total_marks} ({percentage_score:.2f}%)', 'success')

        # ✅ Instead of redirecting, show feedback on the same page
        return render_template(
            'start_quiz.html',
            quiz=quiz,
            user=current_user,
            quiz_start=quiz_start,
            quiz_end=quiz_end,
            feedback=feedback,
            scored_marks=scored_marks,
            total_marks=total_marks,
            percentage_score=percentage_score
        )

    # Step 5: Render quiz attempt page if within allowed time window
    return render_template(
        'start_quiz.html',
        quiz=quiz,
        user=current_user,
        quiz_start=quiz_start,
        quiz_end=quiz_end
    )



















































@app.route('/progress')
@login_required
def user_progress():
    scores = Score.query.filter_by(user_id=current_user.id).all()

    progress_data = []
    total_percentage = 0

    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)

        # Count number of questions
        num_questions = len(quiz.questions)

        # Calculate total marks by summing up all question marks
        total_marks = sum([question.marks for question in quiz.questions])

        # Calculate percentage score based on user's score
        percentage_score = (score.total_score / total_marks) * 100 if total_marks > 0 else 0

        total_percentage += percentage_score  # Add to total for averaging

        progress_data.append({
            'quiz_name': quiz.name,
            'num_questions': num_questions,
            'total_marks': total_marks,
            'user_score': score.total_score,
            'percentage': round(percentage_score, 2),
            'date': score.timestamp
        })

    # Calculate average score
    if len(scores) > 0:
        average_score = round(total_percentage / len(scores), 2)
    else:
        average_score = 0

    return render_template('user_progress.html', 
                           progress_data=progress_data, 
                           scores=scores, 
                           average_score=average_score,
                           user=current_user)



@app.route('/view_quiz/<int:quiz_id>')
@login_required
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Subject is the Course name via the Chapter
    subject = quiz.chapter.course.name if quiz.chapter and quiz.chapter.course else "N/A"

    # Chapter name
    chapter = quiz.chapter.name if quiz.chapter else "N/A"

    # Number of questions
    num_questions = len(quiz.questions)

    # Scheduled Date
    scheduled_date = quiz.date.strftime('%d/%m/%Y') if quiz.date else "Not Scheduled"

    # Duration in minutes
    duration = quiz.duration_minutes

    quiz_details = {
        'id': quiz.id,
        'subject': subject,
        'chapter': chapter,
        'num_questions': num_questions,
        'scheduled_date': scheduled_date,
        'time': quiz.time.strftime('%I:%M %p') if quiz.time else "Not Scheduled",
        'duration': duration
    }

    return render_template('view_quiz.html', quiz=quiz_details,user=current_user)






@app.route('/search')
@login_required
def search():
    query = request.args.get('query', '').strip()
    filter_by = request.args.get('filter', 'all')  # default to 'all' if nothing is selected

    if not query:
        return render_template('search_results.html', results={}, query=query, user=current_user)

    # For Admin users
    if current_user.is_admin:
        results = {}

        if filter_by in ['users', 'all']:
            users = User.query.filter(User.username.ilike(f'%{query}%')).all()
            results['users'] = users

        if filter_by in ['subjects', 'all']:
            courses = Course.query.filter(Course.name.ilike(f'%{query}%')).all()
            results['courses'] = courses

        if filter_by in ['quizzes', 'all']:
            quizzes = Quiz.query.filter(Quiz.name.ilike(f'%{query}%')).all()
            results['quizzes'] = quizzes

        if filter_by in ['questions', 'all']:
            questions = Question.query.filter(Question.statement.ilike(f'%{query}%')).all()
            results['questions'] = questions

    # For Normal users
    else:
        results = {}

        if filter_by in ['subjects', 'all']:
            courses = Course.query.filter(Course.name.ilike(f'%{query}%')).all()
            results['courses'] = courses

        if filter_by in ['quizzes', 'all']:
            quizzes = Quiz.query.filter(Quiz.name.ilike(f'%{query}%')).all()
            results['quizzes'] = quizzes

    return render_template('search_results.html', results=results, query=query, user=current_user)




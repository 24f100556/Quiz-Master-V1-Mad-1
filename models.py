from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate



db = SQLAlchemy(app)  

migrate = Migrate(app, db)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passhash = db.Column(db.String(600), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    level = db.Column(db.String(100))
    dob = db.Column(db.Date, nullable=True)
    is_admin = db.Column(db.Boolean, nullable = False , default = False)
    scores = db.relationship('Score', backref='user', lazy=True)
    


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.passhash = generate_password_hash(password)



    def check_password(self, password):
        return check_password_hash(self.passhash, password)
        




class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    chapters = db.relationship('Chapter', backref='course',cascade="all, delete-orphan", lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    description = db.Column(db.Text)
    quizzes = db.relationship('Quiz', backref='chapter',cascade="all, delete-orphan", lazy=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=True,default=10)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz',cascade="all, delete-orphan", lazy=True)
    scores = db.relationship('Score', backref='quiz', cascade="all, delete-orphan", lazy=True)
    

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    statement = db.Column(db.Text, nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    options = db.relationship('Option', backref='question',cascade="all, delete-orphan", lazy=True)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ques_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    option_text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
   

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username = 'admin').first()
    if not admin :
        admin = User(username='admin',email = 'admin@gmail.com',password = 'admin', name = 'admin', is_admin = True)
        db.session.add(admin)
        db.session.commit()

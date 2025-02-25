# from flask import render_template, request, redirect, url_for, flash, session

# from app import app

# from models import db, User, Course, Chapter, Quiz, Question, Option, Score




# @app.route('/')
# def home():
#     return render_template('index.html')


from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import  User, Course, Chapter, Quiz, Question, Option, Score

@app.route('/')
def home():
    return render_template('index.html')


from dotenv import load_dotenv 
from os import getenv


from app import app
import os
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 

from flask_login import LoginManager
from models import User  

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)  

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  



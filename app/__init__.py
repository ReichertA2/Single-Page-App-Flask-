from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager




# INITALIZING 
app=Flask(__name__)
app.config.from_object(Config)

# Register Plug-ins
login = LoginManager(app)

# init my Database Manager
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# Configure some settings
login.login_view='login'
login.login_message = 'Please log in'
login.login_message_category = 'warning'

from app import routes, models
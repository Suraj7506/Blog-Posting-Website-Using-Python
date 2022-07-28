from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login  import LoginManager
from astroid import manager



app = Flask(__name__,template_folder="f")
app.config['SECRET_KEY']= 'd4a06c98e74b895cc08c6a56991b8494'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.db'
db = SQLAlchemy(app)
encode = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from management import route
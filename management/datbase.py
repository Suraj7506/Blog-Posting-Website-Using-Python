from importlib.util import LazyLoader
from management import db , login_manager
from datetime import datetime
from flask_login import UserMixin






class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(120) , unique = True , nullable = False)
    email = db.Column(db.String(120) , unique = True , nullable = False)
    image_file = db.Column(db.Text , nullable = False , default = 'default.jpg')
    bio = db.Column(db.Text , nullable = False)
    password = db.Column(db.String(60) , nullable = False)
    review = db.relationship('Post' , backref = 'author' ,lazy='dynamic')
    

    def __repr__(self):
        return f"User({self.username} , {self.email} ,{self.image_file})"


class Admin(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    admin = db.Column(db.String(120) , unique = True , nullable = False)
    email = db.Column(db.String(120) , unique = True , nullable = False)
    password = db.Column(db.String(60) , nullable = False)

    def __repr__(self):
        return f"Admin({self.admin} , {self.email})"


class Post(db.Model):
    id =  db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(100) , nullable= False)
    date_post = db.Column(db.DateTime , nullable= False , default = datetime.utcnow)
    data = db.Column(db.Text , nullable= False)
    uid = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)

    def __repr__(self):
        return f"Post({self.title} , {self.data})"
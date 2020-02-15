from syblogpost import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# UserMixing is used to check functionalities like is authenticated, is active ,offline
# created 2 classes Users and Blogspot which should also serve as a table in the database
class Users(db.Model,UserMixin):
    id            = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(128), nullable=False, default = 'default_picture.png')
    email         = db.Column(db.String(64), unique=True, index=True)
    username      = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
# linking up the database as a user will also be an author of a post on the blog 
    posts = db.relationship('Blogpost',backref='author',lazy=True)
# intializing the created tables and also hashing the password 
    def __init__(self,email,username,password):
        self.email    = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username is {self.username}"

class Blogpost(db.Model):
    user    = db.relationship(Users)
    id      = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date    = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)
    title   = db.Column(db.String(140),nullable=False)
    text    = db.Column(db.Text, nullable = False)

    def __init__(self,title,text,user_id):
        self.title   = title
        self.text    = text
        self.user_id = user_id

    def __repr__(self):
        return f"POST ID :{self.id} --- {self.date}-- {self.title}"

db.create_all()
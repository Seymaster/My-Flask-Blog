from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__,instance_relative_config=True)

# both config.py instantiation
app.config.from_object('config')
app.config.from_pyfile('config.py')

#database setup 
app.config['SQLACHEMY_DATABASE_URI'] = 'mysql://root@localhost/test'
app.config['SQLACHEMY_TRACK_MODIFICATIONS']

db = SQLAlchemy(app)
Migrate(db,app)

#login manager config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

from syblogpost.core.views import core
from syblogpost.users.views import users
from syblogpost.error_handler.views import error_pages
from syblogpost.blogpost.views import blog
app.register_blueprint(blog)
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)

#templates requirement 
app.config['CSRF_ENABLED']
app.config['CSRF_SECRET_KEY']
app.config['SECRET_KEY']


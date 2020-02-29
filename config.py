DEBUG = True
# Globally database configuration

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/test'
SQLACHEMY_TRACK_MODIFICATIONS = True

# Enabling protection against cross-site forgery REQUIRED
CSRF_ENABLED = True
CSRF_SECRET_KEY = 'codded'
SECRET_KEY = 'password'

#creating the bleuprint for the HomePage
# /app/task1/__init__.py
from flask import Blueprint

login_bp = Blueprint('Login', 
                        __name__,
                        url_prefix='/Login',
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/static/admin')

from . import routes


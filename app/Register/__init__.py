#creating the bleuprint for the HomePage
# /app/task1/__init__.py
from flask import Blueprint

register_bp = Blueprint('Register', 
                        __name__,
                        url_prefix='/Register',
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/static/admin')

from . import routes


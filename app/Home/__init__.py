#creating the bleuprint for the HomePage
# /app/task1/__init__.py
from flask import Blueprint

homepage_bp = Blueprint('Home', 
                        __name__,
                        url_prefix='/',
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/static/admin')

from . import routes


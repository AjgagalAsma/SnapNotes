#creating the bleuprint for the NotePage
# /app/task1/__init__.py
from flask import Blueprint

notepage_bp = Blueprint('Note', 
                        __name__,
                        url_prefix='/Note',
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/static/admin')

from . import routes


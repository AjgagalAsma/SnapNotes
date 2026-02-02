#Registering the blue print

# /app/__init__.py
from flask import Flask
from transformers import AutoProcessor, AutoModelForCausalLM 
import torch
from .Home import homepage_bp  # Import Home Page blueprint  
from .Login import login_bp  # Import Login Page blueprint 
from .Register import register_bp  # Import Register Page blueprint 
from .Notes import notes_bp  # Import Notes Page blueprint 
from .Note import notepage_bp    
#from .extensions import mysql
from flask_mysqldb import MySQL



def create_app():
    app = Flask(__name__) 
    app.secret_key = 'your_secret_key'
     
    # Configurations de la base de données MySQL
    app.config['MYSQL_HOST'] = 'localhost'  #localhost pour xampp!!!!!!!!!!!!!!!!
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'hd_db'
    app.config['MYSQL_PORT'] = 3308

    #mysql.init_app(app)

    # Initialisation de MySQL
    # from flask_mysqldb import MySQL
    mysql = MySQL(app) 

    # Global model and processor initialization to avoid loading them on each request
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Load model and processor once at app startup
    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Florence-2-base", torch_dtype=torch_dtype, trust_remote_code=True
    ).to(device)
    processor = AutoProcessor.from_pretrained("microsoft/Florence-2-base", trust_remote_code=True)

    # Make model and processor available globally
    app.config['MODEL'] = model
    app.config['PROCESSOR'] = processor
    app.config['DEVICE'] = device
    app.config['TORCH_DTYPE'] = torch_dtype


    # Register each blueprint with the app
    app.register_blueprint(homepage_bp)
    app.register_blueprint(login_bp)

    app.register_blueprint(register_bp)
    app.register_blueprint(notepage_bp)
    app.register_blueprint(notes_bp)

    return app

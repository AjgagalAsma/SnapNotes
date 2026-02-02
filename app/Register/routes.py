# /app/$HomePage/routes.py
from . import register_bp  # Import the Blueprint object

#importing packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import bcrypt
from flask import session


 # Import the Blueprint object


app = Flask(__name__)

 # Ensure this line is included
app.secret_key = 'your_secret_key'  # Remplacez ceci par une clé secrète sécurisée


mysql = MySQL(app)

@register_bp.route('/', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            return render_template('register.html',error="Passwords do not match!")

        # Vérifier si l'email existe déjà
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user WHERE email = %s", [email])
            user = cur.fetchone()

            if user:
                return render_template('register.html',error="Email already exists!")

            # Hachage du mot de passe
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insérer les données dans la base de données
            cur.execute(
                "INSERT INTO user (nom, prenom, email, phone_number, password) VALUES (%s, %s, %s, %s, %s)",
                (first_name, last_name, email, phone_number, hashed_password)
            )
            mysql.connection.commit()
            cur.close()

            #return redirect(url_for('Login.Login'))
            return render_template('register.html', sucess="You have successfully registered! Please login to continue.")
        except Exception as e:
            return render_template('register.html', error="Error! Please try later.")
    return render_template('register.html')  # Affiche le formulaire d'inscription






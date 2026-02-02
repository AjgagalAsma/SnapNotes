# /app/$HomePage/routes.py
from . import login_bp  # Import the Blueprint object

#importing packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import bcrypt
from flask import session


 # Import the Blueprint object


app = Flask(__name__)  # Ensure this line is included

app.secret_key = 'your_secret_key'  # Remplacez ceci par une clé secrète sécurisée

mysql = MySQL(app)

@login_bp.route('/',methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Vérifier l'existence de l'utilisateur
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user is None:
            # L'utilisateur n'existe pas
            return render_template('login.html', error="No account found with that email address.")
        elif not bcrypt.checkpw(password.encode('utf-8'), user[5].encode('utf-8')):  # user[5] correspond à la colonne du mot de passe
            # Le mot de passe est incorrect
            return render_template('login.html', error="Incorrect password, please try again.")
        
        
        # Connexion réussie - stocker l'ID de l'utilisateur dans la session
        session['user_id'] = user[0]  # Assumons que l'ID de l'utilisateur est dans la première colonne (index 0)
        print(session['user_id'])
        return redirect('/Note')  # Redirige vers la page d'accueil

    return render_template('login.html')  # Affiche le formulaire de connexion






# /app/$HomePage/routes.py
from . import notes_bp # Import the Blueprint object

#importing packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import bcrypt
from flask import session


 # Import the Blueprint object


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Remplacez ceci par une clé secrète sécurisée

mysql = MySQL(app)

# Route de logout
@notes_bp.route('/logout')
def Logout():
    session.clear()  # Supprime toutes les données de session
    return redirect(url_for('Login.Login'))  # Redirige vers la page de connexion

@notes_bp.route('/',)
def Notes():
    cur = mysql.connection.cursor()
    

    if 'user_id' not in session:
        return redirect(url_for('Login.Login'))
    # ID de l'utilisateur à filtrer
    user_id = session.get('user_id')  # Récupère l'ID de l'utilisateur depuis la session
    cur.execute("SELECT nom FROM user WHERE id_user = %s", [user_id])
    result = cur.fetchone()
    user_name = result[0]  
    # Nombre de notes par page
    per_page = 4
    # Récupérer la page actuelle et le terme de recherche
    page = int(request.args.get('page', 1))
    query = request.args.get('query', '')  # Récupérer le terme de recherche (vide par défaut)
    
    # Calculer l'index de départ des notes pour cette page
    start = (page - 1) * per_page

    # Si un terme de recherche est fourni, on filtre les notes
    if query:
        cur.execute(f"""
            SELECT n.id_note, n.texte, n.image, n.date_creation, 
                   u.nom AS user_name, GROUP_CONCAT(t.nom) AS tags, n.nom_txt
            FROM note n
            JOIN user u ON n.id_user = u.id_user
            LEFT JOIN note_Tag nt ON n.id_note = nt.id_note
            LEFT JOIN tag t ON nt.id_tag = t.id_tag
            WHERE n.id_user = %s AND (n.texte LIKE %s OR t.nom LIKE %s OR n.nom_txt LIKE %s)
            GROUP BY n.id_note
           LIMIT {start}, {per_page}
        """, (user_id, '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        # Si aucun terme de recherche n'est donné, afficher toutes les notes pour cet utilisateur
        cur.execute(f"""
            SELECT n.id_note, n.texte, n.image, n.date_creation, 
                   u.nom AS user_name, GROUP_CONCAT(t.nom) AS tags, n.nom_txt
            FROM note n
            JOIN user u ON n.id_user = u.id_user
            LEFT JOIN note_Tag nt ON n.id_note = nt.id_note
            LEFT JOIN tag t ON nt.id_tag = t.id_tag
            WHERE n.id_user = %s
            GROUP BY n.id_note
            LIMIT {start}, {per_page}
        """, (user_id,))

    notes = cur.fetchall()  # Récupérer les notes filtrées ou toutes les notes
    cur.close()

    # Calculer le nombre total de notes correspondant à la recherche
    cur = mysql.connection.cursor()
    if query:
        cur.execute("""
            SELECT COUNT(*) 
            FROM note n
            JOIN user u ON n.id_user = u.id_user
            LEFT JOIN note_Tag nt ON n.id_note = nt.id_note
            LEFT JOIN tag t ON nt.id_tag = t.id_tag
            WHERE n.id_user = %s AND (n.texte LIKE %s OR t.nom LIKE %s OR n.nom_txt LIKE %s)
        """, (user_id, '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        cur.execute("""
            SELECT COUNT(*) 
            FROM note n
            JOIN user u ON n.id_user = u.id_user
            LEFT JOIN note_Tag nt ON n.id_note = nt.id_note
            LEFT JOIN tag t ON nt.id_tag = t.id_tag
            WHERE n.id_user = %s
        """, (user_id,))
    total_notes = cur.fetchone()[0]
    cur.close()

    # Calculer le nombre total de pages
    total_pages = (total_notes // per_page)  + (1 if total_notes % per_page > 0 else 0)

    # Passer les notes, la page actuelle et le nombre total de pages au template
    return render_template('notes.html', notes=notes, page=page, total_pages=total_pages, query=query,user_name=user_name)
    
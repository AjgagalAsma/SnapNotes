#from . import notepage_bp  # Import the Blueprint object
from time import sleep
from app.Note import notepage_bp 
from flask import Flask, request, current_app, session, url_for, redirect
#from app.extensions import mysql  # Importez MySQL depuis app/__init__.py
import os
import requests
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM, pipeline 
from datetime import datetime
from flask_mysqldb import MySQL


zero_shot_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

from flask import render_template
app = Flask(__name__)

 # Ensure this line is included
app.secret_key = 'your_secret_key'  # Remplacez ceci par une clé secrète sécurisée


mysql = MySQL(app)


def delete_files_in_folder(folder_path, file_pattern='*'):
    # List all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

@notepage_bp.route('/')
def render_note():
    ##Open the connexion with database to get user_name
    cur = mysql.connection.cursor()
    cur.execute("SELECT nom FROM user WHERE id_user = %s", [session.get('user_id')])
    result = cur.fetchone()
    user_name = result[0]
    session['user_name'] = user_name    
    cur.close()
    return render_template('note.html',user_name = session.get('user_name'))

@notepage_bp.route('/upload', methods=['GET', 'POST'])
def UploadImage():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('note.html', error='No file part')
        file = request.files['image']
        if file.filename == '':
            return render_template('note.html', error='No file selected')
        
        """upload_folder = os.path.join('app', 'upload')
        os.makedirs(upload_folder, exist_ok=True)
        file_name = file.filename
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)



        # # Sauvegarde temporaire du fichier"""
        upload_folder = os.path.join('app', 'Note', 'static', 'temp')
        file_name = file.filename
        file_path = os.path.join(upload_folder, file.filename)
        #delete_files_in_folder(upload_folder)  # Supprimer les anciens fichiers
        file.save(file_path)

        # Extraction de texte après l'upload
        
        #try:
        img_path = os.path.join(upload_folder, file_name)
        prompt = "<OCR>"

        image = Image.open(img_path)
        #image = image.convert("RGB")
        inputs = current_app.config['PROCESSOR'](
            text=prompt, images=image, return_tensors="pt"
        ).to(current_app.config['DEVICE'], current_app.config['TORCH_DTYPE'])

        generated_ids = current_app.config['MODEL'].generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            do_sample=False,
            num_beams=3,
        )
        generated_text = current_app.config['PROCESSOR'].batch_decode(
            generated_ids, skip_special_tokens=False
        )[0]

        parsed_answer = current_app.config['PROCESSOR'].post_process_generation(
            generated_text, task="<OCR>", image_size=(image.width, image.height)
        )
        extracted_text = parsed_answer['<OCR>']

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT nom FROM tag")
            rows = cur.fetchall()
            cur.close

            condidate_labels = [row[0] for row in rows]

        except Exception as db_error:
            return render_template('note.html', error=f"Database error: {str(db_error)}", user_name = session.get('user_name'))    
        
        tag_results = zero_shot_classifier(extracted_text, condidate_labels)
        suggested_tags = tag_results['labels'][:3]
        
        return render_template(
            'Note.html', 
            image_url=file_name, 
            extracted_text=extracted_text, 
            suggested_tags=suggested_tags,
            user_name = session.get('user_name')
        )

        """except Exception as e:
            return render_template('note.html', error=f"Error extracting text: {str(e)}")"""     
    
    return render_template('Note.html',user_name = session.get('user_name'))

@notepage_bp.route('/extract/<image_name>', methods=['GET', 'POST'])
def ExtractText(image_name):
    
    # Retrieve model, processor, and device from Flask's app context
    model = current_app.config['MODEL']
    processor = current_app.config['PROCESSOR']
    device = current_app.config['DEVICE']
    torch_dtype = current_app.config['TORCH_DTYPE']

    try:
        
        # Image path
        img_path = os.path.join('app', 'Note', 'static', 'temp', image_name)
        prompt = "<OCR>"

        # Open and process the image
       
        image = Image.open(img_path)
        image = image.convert("RGB") 
        inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)

        # Generate OCR results
        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            do_sample=False,
            num_beams=3,
        )
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

        # Post-process OCR results
        parsed_answer = processor.post_process_generation(
            generated_text, task="<OCR>", image_size=(image.width, image.height)
        )

        return render_template('Note.html', extracted_text=parsed_answer['<OCR>'],image_url= image_name,user_name = session.get('user_name'))

    except Exception as e:
        return f"Error processing image: {str(e)}", 500

@notepage_bp.route('/save_note', methods=['POST'])
def save_note():
    print("save_note")
    # Récupérer les données du formulaire
    extracted_text = request.form.get('extracted_text')  # Texte extrait
    image_name = request.form.get('image_name')
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Date courante
    nom_txt = request.form.get('title')
    tags_input = request.form.getlist('tags[]')
    id_user = session.get('user_id') # pour le test
    print(extracted_text)
    print(image_name)
    print("nom txt")
    print(nom_txt)
    print(tags_input)

    # Vérifier si le texte extrait est présent
    if not extracted_text:
        return render_template('Note.html', error="Extracted text is missing",user_name = session.get('user_name'))
    if not nom_txt:
        return render_template('Note.html', error='Title is missing',user_name = session.get('user_name'))
    
    try:
    
        # Insérer les données dans la base de données
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO note (nom_txt,texte, image, date_creation, id_user) VALUES (%s, %s, %s, %s, %s)",
            (nom_txt, extracted_text, image_name, current_date, id_user)
        )
        mysql.connection.commit()
        note_id = cur.lastrowid

        if tags_input:
            for tag in tags_input:
                tag = tag.strip()  # Nettoyer le tag des espaces

                # Si le tag est vide, retournez une erreur
                if not tag:
                    return render_template('Note.html', error="Tag name cannot be empty.")

                # Vérifier si le tag existe déjà dans la base de données
                cur.execute("SELECT id_tag FROM tag WHERE nom = %s", (tag,))
                mysql.connection.commit()
                tag_row = cur.fetchone()

                if tag_row:
                    # Si le tag existe, on récupère son id
                    tag_id = tag_row[0]
                else:
                    # Si le tag n'existe pas, on l'insère et récupère son id
                    cur.execute("INSERT INTO tag (nom) VALUES (%s)", (tag,))
                    mysql.connection.commit()
                    tag_id = cur.lastrowid

                # Associer le tag à la note
                cur.execute("INSERT INTO note_tag (id_note, id_tag) VALUES (%s, %s)", (note_id, tag_id))
                mysql.connection.commit()

            # Commencer la transaction
            #mysql.connection.commit()
            cur.close()


        # Retourner un message de succès
        return render_template('Note.html', success="Note saved successfully!",user_name = session.get('user_name'))

    except Exception as e:
        return render_template('Note.html', error=f"Database error: {str(e)}")

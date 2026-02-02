# /app/$HomePage/routes.py
from . import homepage_bp  # Import the Blueprint object
from flask import redirect, request, current_app, url_for

import os
import requests
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM 


 # Import the Blueprint object


#importing packages

from flask import render_template


def delete_files_in_folder(folder_path, file_pattern='*'):
    # List all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

@homepage_bp.route('/')
def render_home():
    return render_template('home.html')

@homepage_bp.route('upload', methods=['GET', 'POST'])
def UploadImage():
    if request.method == 'POST':
        print("this is the request files ")
        print(request.files)
        if 'image' not in request.files:
            return render_template('home.html', error='No file part')
        file = request.files['image'] 
        if file.filename == '':
            return render_template('home.html', error=file.filename) 
        
    # Save the file to a temporary location 
        output_dir = os.path.join('app', 'Home', 'static', 'temp')
        file_name = file.filename
        file_path = os.path.join(output_dir, file.filename)
        delete_files_in_folder(output_dir)
        file.save(file_path) # Process the image using your custom preprocessing function 
        return render_template('Home.html', image_url= file_name)
    return render_template('Home.html')


@homepage_bp.route('extract/<image_name>', methods=['GET', 'POST'])
def ExtractText(image_name):
    # Retrieve model, processor, and device from Flask's app context
    model = current_app.config['MODEL']
    processor = current_app.config['PROCESSOR']
    device = current_app.config['DEVICE']
    torch_dtype = current_app.config['TORCH_DTYPE']

    try:
        # Image path
        img_path = os.path.join('app', 'Home', 'static', 'temp', image_name)
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

        return render_template('Home.html', extracted_text=parsed_answer['<OCR>'],image_url= image_name,popup=True)

    except Exception as e:
        return f"Error processing image: {str(e)}", 500

@homepage_bp.route('extract/Login/', methods=['GET', 'POST'])
def Render_Home():
    return redirect(url_for('Login.Login'))
        



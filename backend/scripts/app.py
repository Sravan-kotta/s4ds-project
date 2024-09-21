from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import pymupdf
import os
import io
import time
from google.cloud import vision
import google.generativeai as genai

app = Flask(__name__)
CORS(app)
users = {
    "admin": "password",
    "user": "passcode"
}
@app.route('/login', methods=['GET','POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    if users[username] == password:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
    


@app.route('/upload', methods=['GET','POST'])
# Folder containing the PDF files
def taker():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Save the file
    v = secure_filename(file.filename)
    app.config['UPLOAD_FOLDER'] = "C:/Users/srava/Desktop/s4ds-project/backend/data/raw"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], v)
    file.save(filepath)
    processed = pdf_to_img(v,filepath)
    #init_api_keys()
    os.environ['GOOGLE_API_KEY2'] = 'AIzaSyBnc0piIW-Kwb4AdpUB2PBEKjNvY1vm3_A'

# Step 2: Retrieve the API key from the environment variable
    GOOGLE_API_KEY2 = os.getenv('GOOGLE_API_KEY2')

# Step 3: Configure the API key for your service
    genai.configure(api_key=GOOGLE_API_KEY2)
    model2 = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

    process_all_folders('./data/processed', './data/results',model2)
    prompt = input("Extract the handwritten text from the following imags: ")
    x = generate_response(prompt)
    return jsonify({'result': processed,
                    'text': x}), 200

# Base folder to save the images
def pdf_to_img(name,path):
    app.config['UPLOAD_FOLDER2'] = "C:/Users/srava/Desktop/s4ds-project/backend/data/processed"
    doc = pymupdf.open(path)
    # Create a specific folder for this PDF's images
    pdf_output_folder = os.path.join(app.config['UPLOAD_FOLDER2'], name[:-4])
    os.makedirs(pdf_output_folder, exist_ok=True)

    # Convert each page to an image and save
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        pix = page.get_pixmap()
        image_path = os.path.join(
            pdf_output_folder, f'page_{page_number + 1}.png')
        pix.save(image_path)
    doc.close()

    print("Conversion completed.")
    return pdf_output_folder



def init_api_keys():
    try:
        #os.environ["GOOGLE_CLOUD_PROJECT"] = "text-extraction-423214"
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./text-extraction-423214-fecf2dc6bb42"
        os.environ['GOOGLE_CLOUD_API_KEY'] = ''
        #credential_path = r'C:\Users\srava\Downloads\buoyant-nectar-436323-a8-9de786931b9e.json'
        #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
        api_key = os.environ.get("GOOGLE_CLOUD_API_KEY")
        if not api_key:
            raise Exception("GOOGLE_CLOUD_API_KEY is not set")
        genai.configure(api_key=api_key)
    except Exception as exception:
        print("Error in initializing API keys:", exception)
        raise


def extract_handwritten_text(image_path: str, output_file_path: str):
    """Extracts handwritten text from an image and saves it to a text file."""
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(f'API returned error: {response.error.message}')

    extracted_text = response.full_text_annotation.text

    with open(output_file_path, 'a', encoding='utf-8') as text_file:
        text_file.write(extracted_text)

def extract_test(image_path: str, output_file_path: str, model):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    response = model.generate_content(["Provide the text as it is from the images as well as remove all the scribbled words in it.", content])
    extracted_text = response.text
    with open(output_file_path, 'a') as text_file:
        text_file.write(extracted_text)
def process_all_folders(base_folder: str, result_folder: str,model):
    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)
        result_file_path = os.path.join(result_folder, f'{folder}.txt')

        os.makedirs(result_folder, exist_ok=True)

        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(folder_path, file)
                    extract_test(image_path, result_file_path,model)
            print(f"Processed all images in {folder}.")


def generate_response(prompt: str):
    generation_config = {
        "temperature": 0.1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest", generation_config=generation_config)
    prompt_parts = [prompt]

    try:
        response = model.generate_content(prompt_parts)
        print(response.text)
    except Exception as exception:
        print("Error generating response:", exception)

if __name__ == '__main__':
    app.run(debug = True)
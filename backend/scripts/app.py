from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import pymupdf
import PIL.Image
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

# Step 2: Retrieve the API key from the environment variable
    GOOGLE_API_KEY2 = os.getenv('GOOGLE_API_KEY2')

# Step 3: Configure the API key for your service
    genai.configure(api_key=GOOGLE_API_KEY2)
    model2 = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    x = process_folder(processed, "C:/Users/srava/Desktop/s4ds-project/backend/data/results", model)
    for file in os.listdir(processed):
        path = os.path.join(processed, file)
        extract_text(path, x, model)
        time.sleep(10)
    f = io.open(x, mode="r", encoding="utf-8")
    text_c = f.read()
    return jsonify({'result': x,
                    'transcript': text_c}), 200

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




def extract_text(image_path: str, output_file_path: str, model):
    content = PIL.Image.open(image_path)
    response = model.generate_content(["Provide the text as it is from the images as well as remove all the scribbled words in it.", content])
    extracted_text = response.text
    app.config['create1'] = output_file_path
    with open(app.config['create1'], 'a', encoding="utf-8") as text_file:
        text_file.write(extracted_text)
def process_folder(folder: str, result_folder: str,model):
    folder_base = os.path.basename(folder)
    app.config['upload_folder3'] = result_folder
    b = secure_filename(folder_base)
    result_file_path = os.path.join(app.config['upload_folder3'], b+'.txt')
    return result_file_path




if __name__ == '__main__':
    app.run(debug = True)

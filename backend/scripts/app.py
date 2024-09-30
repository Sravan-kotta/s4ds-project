from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import pymupdf
import PIL.Image
import os
import io
import time
import re 
import google.generativeai as genai
import json
from logging import FileHandler,WARNING
app = Flask(__name__)
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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
    x = process_folder(processed, "C:/Users/srava/Desktop/s4ds-project/backend/data/results", model)
    for file in os.listdir(processed):
        path = os.path.join(processed, file)
        try:
            extract_text(path, x, model)
            time.sleep(10)
        except Exception as error:
            print (error)
            pass
    session['transcript_path'] = x 
    y = session.get('transcript_path')
    print(y)
    f = io.open(x, mode="r", encoding="utf-8")
    text_c = f.read()
    print(text_c)
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


@app.route('/evaluation', methods=['GET', 'POST'])
def evaluate():
        data = request.get_json()
    
        file_path = data.get('file_path')
        print(file_path)
        # Instead of getting form data, read the transcript directly from the processed file
        try:
            # Define the path to the file where the transcript is saved
            #result_file_path = r"C:\Users\srava\Desktop\s4ds-project\backend\data\results\AI_sem_7_2022_2023.txt"
            #result_file_path2 = session.get('transcript_path')
            result_file_path = file_path
            print(result_file_path)
            # Ensure the file exists and then read the content
            if not os.path.exists(result_file_path):
                return jsonify({'message': 'Transcript file not found.'}), 400

            # Read the transcript from the file
            with open(result_file_path, 'r') as file:
                student_response_text = file.read()

            # Proceed with the evaluation using the student's response
            question_paper_path = "C:/Users/srava/Desktop/s4ds-project/backend/data/etrx_qp (1).txt"
            
            if not os.path.exists(question_paper_path):
                return jsonify({'message': 'Question paper not found'}), 400

            # Evaluate the student's responses using the LLM
            result = evaluate_answers(student_response_text, question_paper_path)
            print(result)
            return jsonify({'evaluation_result': result}), 200

        except Exception as e:
            return jsonify({'message': f'Error processing evaluation: {e}'}), 500


def evaluate_answers(student_responses, question_paper_path):
    # Read the question paper from the file
    with open(question_paper_path, 'r') as file:
        question_paper = file.read()
    
    os.environ['GOOGLE_API_KEY2'] = 'AIzaSyBnc0piIW-Kwb4AdpUB2PBEKjNvY1vm3_A'

# Step 2: Retrieve the API key from the environment variable
    GOOGLE_API_KEY2 = os.getenv('GOOGLE_API_KEY2')

# Step 3: Configure the API key for your service
    genai.configure(api_key=GOOGLE_API_KEY2)

    # Construct the evaluation prompt
    prompt = f"""
    You are an evaluator assigned to grade a student's response based on the provided question paper.
    
    The following are the student's responses:

    {student_responses}

    Here is the question paper:

    {question_paper}

    You need to evaluate the student's answers and assign marks out of 10 for each answer. Provide feedback and give a total score out of 30.
    respond in a specific format, this is an example: "**Q1a:** <feedback>  **Award 2/5 marks**"
    """

    # Initialize the LLM model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate content using the model
    try:
        response = model.generate_content(prompt)
        print(f"LLM Response: {response.text}")
    except Exception as e:
        print(f"Error during model generation: {e}")
        return "Error in LLM evaluation."

    # Extract the evaluation result from the response
    evaluation_result = response.text.strip()
    pattern = r"\*\*(Q\d+[a-z]*):\*\*\s*(.*?)\s*\*\*Award\s*(\d+)/(\d+)\s*marks\*\*"
    
    # Use re.findall to find all matches in the text
    matches = re.findall(pattern, evaluation_result, re.DOTALL)
    pattern_total = rf"Total Score: (\d+)/(\d+)"

    match_total = re.findall(pattern_total, evaluation_result, re.DOTALL)
    if matches:
        # Create a list to store dictionaries for each match
        result_json = []
        
        # Loop through each match and create a dictionary
        for match in matches:
            question = match[0]
            comment = match[1].strip()
            marks_awarded = int(match[2])
            total_marks = int(match[3])
            
            # Append each match as a dictionary to the result list
            result_json.append({
                "question": question,
                "comment": comment,
                "marks_awarded": marks_awarded,
                "total_marks": total_marks
            })
        
        # Convert the list of dictionaries to a JSON format and return
        json.dumps(result_json, indent=4),match_total
    print(result_json)
    return evaluation_result

if __name__ == '__main__':
    app.run(debug = True)

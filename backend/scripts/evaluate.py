
from IPython.display import display, Markdown
from IPython.display import Image
import io
import google.generativeai as genai
import pandas as pd
import os
import PIL.Image

def init_model():
# Step 1: Set the environment variable for your API key
    os.environ['GOOGLE_API_KEY2'] = 'AIzaSyBnc0piIW-Kwb4AdpUB2PBEKjNvY1vm3_A'

    # Step 2: Retrieve the API key from the environment variable
    GOOGLE_API_KEY2 = os.getenv('GOOGLE_API_KEY2')

    # Step 3: Configure the API key for your service
    genai.configure(api_key=GOOGLE_API_KEY2)
    

#transcript = ''
#text = open(transcript, 'r')
#chat = model.start_chat(history=[])
init_model()
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
model2 = genai.GenerativeModel('models/gemini-1.5-pro-latest')
#response = chat.send_message(["the provided pdf contains a questionaire on ai, you will be provided answers to these questions from multiple students which you have to evaluate"])
#chat.send_message(["evaluate this sheet as per the question paper given above considering that each question is not dependent on each other and evaluate accordingly as per the given also take a note that Q1)is compulsory and Q2),Q3) are anyone type questions incase if both the parts of Q2 and Q3 are solved please check them both individually and evaluate carefully and given marks outoff 10 and consider that Q2and Q3 are of 10 marks for any one Question "])

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


def extract_text(image_path: str, output_file_path: str, model):
    content = PIL.Image.open(image_path)
    response = model.generate_content(["Provide the text as it is from the images as well as remove all the scribbled words in it.", content])
    extracted_text = response.text
    with open(output_file_path, 'a') as text_file:
        text_file.write(extracted_text)
def process_all_folders(folder: str, result_folder: str):
    folder_base = os.path.basename(folder)
    result_file_path = os.path.join(result_folder, f'{folder_base}.txt')
    return result_file_path

x = process_all_folders('backend/data/processed/white_box_merged', 'backend/data/results')
for file in os.listdir('backend/data/processed/white_box_merged'):
    path = os.path.join('backend/data/processed/white_box_merged', file)
    extract_text(path, x, model)




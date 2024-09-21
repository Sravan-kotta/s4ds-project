from flask import Flask, request, jsonify
from flask_cors import CORS
from IPython.display import display, Markdown
from IPython.display import Image

import google.generativeai as genai
import pandas as pd
import os

# Step 1: Set the environment variable for your API key
os.environ['GOOGLE_API_KEY2'] = 'AIzaSyBnc0piIW-Kwb4AdpUB2PBEKjNvY1vm3_A'

# Step 2: Retrieve the API key from the environment variable
GOOGLE_API_KEY2 = os.getenv('GOOGLE_API_KEY2')

# Step 3: Configure the API key for your service
genai.configure(api_key=GOOGLE_API_KEY2)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
model2 = genai.GenerativeModel('models/gemini-1.5-pro-latest')

transcript = ''
text = open(transcript, 'r')
chat = model.start_chat(history=[])

chat.send_message(["the provided pdf contains a questionaire on {subject}, you will be provided answers to these questions from multiple students which you have to evaluate",text])
chat.send_message(["evaluate this sheet as per the question paper given above considering that each question is not dependent on each other and evaluate accordingly as per the given also take a note that Q1)is compulsory and Q2),Q3) are anyone type questions incase if both the parts of Q2 and Q3 are solved please check them both individually and evaluate carefully and given marks outoff 10 and consider that Q2and Q3 are of 10 marks for any one Question "])

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


if __name__ == "__main__":
    with open(output_file_path, 'a', encoding='utf-8') as text_file:
        x = text_file.write(extracted_text)
    init_api_keys()
    process_all_folders('./data/processed', './data/results')
    prompt1 = input("the provided pdf contains a questionaire on {subject}, you will be provided answers to these questions from multiple students which you have to evaluate")
    prompt2 = input(x)
    prompt3 = input('After each question, the scale on which the answer is to be evaluated is provided, for example: "Exaplin features of CBC 5" the 5 indicated the answer is to be marked on a scale of 0 to 5')
    prompt4 = input("these are the answers. Everytime you encounter a section with studentdetails, note that the answers of a student have ended and new sheet starts")
    prompt = [prompt1,prompt2,prompt3,prompt4]
    generate_response(prompt)
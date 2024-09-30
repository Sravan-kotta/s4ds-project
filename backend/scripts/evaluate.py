
from IPython.display import display, Markdown
from IPython.display import Image
import io
import google.generativeai as genai
import pandas as pd
import os
import PIL.Image
import re

def evaluate():
    if request.method == 'GET':
        return jsonify({'message': 'Evaluation API is working. Use POST to submit data.'}), 200

    if request.method == 'POST':
        # Instead of getting form data, read the transcript directly from the processed file
        try:
            # Define the path to the file where the transcript is saved
            result_file_path = r"C:\Aryan(ps)\s4ds-project-main\backend\data\results\AI_sem_7_2022_2023.txt"

            # Ensure the file exists and then read the content
            if not os.path.exists(result_file_path):
                return jsonify({'message': 'Transcript file not found.'}), 400

            # Read the transcript from the file
            with open(result_file_path, 'r') as file:
                student_response_text = file.read()

            # Proceed with the evaluation using the student's response
            question_paper_path = r"C:/Aryan(ps)/s4ds-project-main/backend/data/etrx_qp(1).txt"
            
            if not os.path.exists(question_paper_path):
                return jsonify({'message': 'Question paper not found'}), 400

            # Evaluate the student's responses using the LLM
            result = evaluate_answers(student_response_text, question_paper_path)

            return jsonify({'evaluation_result': result}), 200

        except Exception as e:
            return jsonify({'message': f'Error processing evaluation: {e}'}), 500


def evaluate_answers(student_responses, question_paper_path):
    # Read the question paper from the file
    with open(question_paper_path, 'r') as file:
        question_paper = file.read()

    # Construct the evaluation prompt
    prompt = f"""
    You are an evaluator assigned to grade a student's response based on the provided question paper.
    
    The following are the student's responses:

    {student_responses}

    Here is the question paper:

    {question_paper}

    You need to evaluate the student's answers and assign marks out of 10 for each answer. Provide feedback and give a total score out of 30.
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

    return evaluation_result




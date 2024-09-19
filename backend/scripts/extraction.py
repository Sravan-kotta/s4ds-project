import os
import io
from google.cloud import vision
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS


def init_api_keys():
    try:
        os.environ["GOOGLE_CLOUD_PROJECT"] = "text-extraction-423214"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./text-extraction-423214-fecf2dc6bb42"
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


def process_all_folders(base_folder: str, result_folder: str):
    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)
        result_file_path = os.path.join(result_folder, f'{folder}.txt')

        os.makedirs(result_folder, exist_ok=True)

        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(folder_path, file)
                    extract_handwritten_text(image_path, result_file_path)
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


if __name__ == "__main__":
    init_api_keys()
    process_all_folders('./data/processed', './data/results')
    prompt = input("Extract the handwritten text from the following imags: ")
    generate_response(prompt)

from flask import Flask, request, jsonify
from flask_cors import CORS





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
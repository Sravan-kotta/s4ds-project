import os
import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['GET','POST'])
# Folder containing the PDF files
def taker():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Save the file
    filepath = os.path.join('backend/data/raw', file.filename)
    file.save(filepath)
    processed = pdf_to_img(file)
    return jsonify({'saved in': processed}), 200

# Base folder to save the images
def pdf_to_img(raw_file):
    output_base_folder = './data/processed'
    doc = raw_file

    # Create a specific folder for this PDF's images
    pdf_output_folder = os.path.join(output_base_folder, raw_file.filename[:-4])
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

if __name__ == '__main__':
    app.run(debug = True)
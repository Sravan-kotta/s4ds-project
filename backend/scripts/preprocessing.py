import os
from flask import Flask, request, jsonify
from flask_cors import CORS 


def remove_initial_content(content, marker):
    """Remove all content up to and including the specified marker."""
    try:
        end_index = content.index(marker) + len(marker)
        return content[end_index:]  # Return content after the marker
    except ValueError:
        # Marker not found, return original content
        return content

directory_path = './data/results'

# Text that marks the start and end of the unwanted section
start_marker = "INSTRUCTIONS\nसूचना\nDO NOT WRITE NUMBER ANY WHERE EXCEPT AT THE PLACE PROVIDED FOR"
end_marker = "४. होलो क्राफ्ट स्टीकर विहित जागेवरच लावावी."

# Marker for the initial content removal
initial_content_marker = "Write the answer book in blue or black ink/ball pen only and use of pencils in case of diagrams & sketches."

# Process each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove the initial content up to the specified line
        content = remove_initial_content(content, initial_content_marker)

        # Attempt to remove the unwanted text up to 4 times
        for _ in range(4):
            try:
                start_index = content.index(start_marker)
                end_index = content.index(end_marker) + len(end_marker)
                # Remove the unwanted text
                content = content[:start_index] + content[end_index:]
            except ValueError:
                # Break the loop if no more markers are found
                break

        # Overwrite the file with the cleaned content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Processed and updated {filename}")

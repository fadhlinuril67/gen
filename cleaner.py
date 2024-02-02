import os
import re

def clean_html_from_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Preprocess lines to remove those containing ANSI escape sequences
            cleaned_lines = []
            ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
            for line in lines:
                if not ansi_escape.search(line):
                    cleaned_lines.append(line)
                elif 'OK' in line:
                    # This checks for 'OK' specifically in lines with ANSI codes
                    # If you still want to remove lines with 'OK', regardless of ANSI codes
                    continue

            file_content = ''.join(cleaned_lines)
            start_index = file_content.find('<')
            end_index = file_content.rfind('>')
            if start_index != -1 and end_index != -1 and end_index > start_index:
                html_content = file_content[start_index:end_index+1]
            else:
                print(f"No valid HTML content boundaries found in {filename}.")
                continue

            # Create a new filename for the cleaned file
            new_filename = os.path.splitext(filename)[0] + '-cleaned.txt'
            new_file_path = os.path.join(folder_path, new_filename)

            with open(new_file_path, 'w', encoding='utf-8') as new_file:
                new_file.write(html_content)
            print(f"Content between the first '<' and last '>' written to {new_filename}.")

folder_path = './'
clean_html_from_files(folder_path)

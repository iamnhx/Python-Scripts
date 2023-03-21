import os
import subprocess

def get_book_title(isbn):
    command = f"isbn_meta {isbn} openl"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    output_lines = result.stdout.decode("utf-8").split("\n")
    for line in output_lines:
        if "Title:" in line:
            return line.split(":")[1].strip()
    return None

# Define the list of extensions to rename
file_extensions = [".azw3", ".epub", ".mobi", ".pdf"]

source_dir = "/Users/wolong/Documents/_Incoming"
for file_name in os.listdir(source_dir):
    file_path = os.path.join(source_dir, file_name)
    isbn = file_name[:13] if len(file_name[:13]) == 13 else file_name[:10]
    if isbn.isdigit() and (len(isbn) == 10 or len(isbn) == 13) and any(file_name.endswith(ext) for ext in file_extensions):
        book_title = get_book_title(isbn)
        if book_title:
            new_file_name = f"{book_title}{os.path.splitext(file_name)[-1]}"
            os.rename(file_path, os.path.join(source_dir, new_file_name))

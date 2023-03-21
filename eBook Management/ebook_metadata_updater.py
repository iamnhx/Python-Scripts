import os
import isbnlib
import subprocess

def process_file(file_path, isbn):
    # Use isbnlib to retrieve the book metadata
    book_metadata = isbnlib.meta(isbn)

    # Use isbnlib to retrieve the book description
    book_description = isbnlib.desc(isbn)

    # Use ebook-meta to update the metadata
    cmd = ['/Applications/calibre.app/Contents/MacOS/ebook-meta', file_path]
    for key, value in book_metadata.items():
        if value:
            if key == 'ISBN-13':
                cmd.extend(['--isbn', str(value)])
            elif key == 'Year':
                cmd.extend(['--date', str(value)])
            elif key == 'Authors':
                authors = ', '.join(value)
                cmd.extend(['--authors', authors])
            else:
                cmd.extend(['--'+key.lower(), str(value)])
    cmd.extend(['--comments', book_description])

    with open('ebook-meta-output.txt', 'w') as output_file:
        subprocess.run(cmd, stdout=output_file, stderr=output_file)

    with open('ebook-meta-output.txt', 'r') as output_file:
        output_content = output_file.read()
        if 'Syntax Error' in output_content:
            os.remove('ebook-meta-output.txt')
            return False

    os.remove('ebook-meta-output.txt')
    return True

def main():
    file_extensions = ('.epub', '.pdf')
    current_directory = os.getcwd()
    files_with_errors = []

    for root_dir, _, filenames in os.walk(current_directory):
        for filename in filenames:
            if filename.endswith(file_extensions):
                file_path = os.path.join(root_dir, filename)
                isbn = os.path.splitext(filename)[0]

                if not process_file(file_path, isbn):
                    files_with_errors.append(file_path)
                else:
                    cmd = ['/Applications/calibre.app/Contents/MacOS/ebook-meta', file_path]
                    result = subprocess.run(cmd, capture_output=True)
                    print('Metadata for file:', file_path)
                    print(result.stdout.decode('utf-8'))

    if files_with_errors:
        print('The following files could not be processed:')
        for error_file_path in files_with_errors:
            print(error_file_path)
    else:
        print('All files have been processed successfully.')

if __name__ == '__main__':
    main()

import os
import re
import isbnlib
import subprocess
from isbnlib.dev._exceptions import ISBNNotConsistentError

class ISBNInconsistencyError(Exception):
    def __init__(self, file_path, suggested_isbn):
        self.file_path = file_path
        self.suggested_isbn = suggested_isbn
        filename = os.path.basename(file_path)
        super().__init__(f"ISBN inconsistency for file: {filename}. Suggested ISBN: {suggested_isbn}")

class InvalidISBNError(Exception):
    pass

def process_file(file_path, isbn):
    file_name = os.path.basename(file_path)
    try:
        # Use isbnlib to retrieve the book metadata
        book_metadata = isbnlib.meta(isbn)
    except ISBNNotConsistentError as e:
        suggested_isbn_match = re.search(r"'(\d{13}|\d{10})'", str(e))
        if suggested_isbn_match:
            suggested_isbn = suggested_isbn_match.group(1)
            if suggested_isbn:
                suggested_isbn = isbnlib.to_isbn13(suggested_isbn)
        else:
            suggested_isbn = ''
        if suggested_isbn:
            try:
                book_metadata = isbnlib.meta(suggested_isbn)
                if book_metadata.get('ISBN-13') != isbn:
                    raise ISBNInconsistencyError(file_path, suggested_isbn)
            except isbnlib.NotValidISBNError:
                raise ISBNInconsistencyError(file_path, suggested_isbn)
        else:
            raise ISBNInconsistencyError(file_path, suggested_isbn)
    except InvalidISBNError as e:
        print(f"\033[91m{str(e)}\n\033[0m")
        return False

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

def main():
    file_extensions = ('.epub', '.pdf')
    current_directory = os.getcwd()
    files_with_invalid_isbn = []
    files_with_isbn_inconsistency = []
    processed_files = set()

    # Check if the processed files text file exists
    processed_files_path = os.path.join(current_directory, 'Processed Files.txt')
    if os.path.exists(processed_files_path):
        with open(processed_files_path) as f:
            for line in f:
                processed_files.add(line.strip())

    isbn_pattern = r'\b\d{13}\b'

    for root_dir, _, filenames in os.walk(current_directory):
        for filename in filenames:
            if filename in processed_files:
                continue
            if filename.endswith(file_extensions):
                file_path = os.path.join(root_dir, filename)
                isbn_match = re.search(isbn_pattern, filename)
                if isbn_match:
                    isbn = isbn_match.group(0)
                else:
                    print(f"\033[91mNo ISBN found in filename '{filename}'\n\033[0m")
                    files_with_invalid_isbn.append(file_path)
                    continue

                try:
                    result = process_file(file_path, isbn)
                except InvalidISBNError as e:
                    print(f"\033[91m{str(e)}\n\033[0m")
                    files_with_invalid_isbn.append(file_path)
                    continue
                except ISBNInconsistencyError as e:
                    print(f"\033[91m{str(e)}\n\033[0m")
                    files_with_isbn_inconsistency.append((e.file_path, e.suggested_isbn))
                    continue

                cmd = ['/Applications/calibre.app/Contents/MacOS/ebook-meta', file_path]
                result = subprocess.run(cmd, capture_output=True)
                print('Filename            :', os.path.basename(file_path))
                print(result.stdout.decode('utf-8'))

                # Add processed file name to the set and write it to the file
                processed_files.add(filename)
                with open(processed_files_path, 'a') as f:
                    f.write(f"{filename}\n")

    if len(files_with_invalid_isbn) > 0:
        plural = "s" if len(files_with_invalid_isbn) > 1 else ""
        print(f"\n{len(files_with_invalid_isbn)} file{plural} had an invalid ISBN:")
        for file_path in files_with_invalid_isbn:
            print(f"\033[91m{os.path.basename(file_path)}\033[0m")

    if len(files_with_isbn_inconsistency) > 0:
        plural = "s" if len(files_with_isbn_inconsistency) > 1 else ""
        print(f"\n{len(files_with_isbn_inconsistency)} file{plural} had an ISBN inconsistency:")
        for file_path, suggested_isbn in files_with_isbn_inconsistency:
            print(f"\033[91m{os.path.basename(file_path)}\033[0m, Suggested ISBN:\033[92m {suggested_isbn}\033[0m")

if __name__ == '__main__':
    main()
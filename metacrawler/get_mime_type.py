import os
import magic

def get_mime_type(file_path):
    """
    Determine the MIME type of a file using the python-magic library.
    
    :param file_path: Path to the file to check.
    :return: A string representing the MIME type or 'NA' if the type cannot be determined.
    """
    try:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)
        return mime_type
    except Exception as e:
        if DEBUG:
            print(f"Error determining MIME type for {file_path}: {e}")
        return 'NA'
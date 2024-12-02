"""
Module: get_mime_type

Description:
------------
This module provides a function to determine the MIME type of a file using the python-magic library.

Functions:
----------
get_mime_type(file_path: str) -> str
    Determine the MIME type of a file using the python-magic library.
"""

import os
import magic

def get_mime_type(file_path):
    """
    Function: get_mime_type
    
    Description:
    ------------
    Determine the MIME type of a file using the python-magic library.
    
    This function takes a file path as input and returns the MIME type of the file. 
    If the MIME type cannot be determined, it returns 'NA'. In case of an error, 
    it optionally prints an error message if the DEBUG flag is set to True.
    
    Parameters:
    -----------
    file_path : str
        Path to the file to check.
    
    Returns:
    --------
    str
        A string representing the MIME type or 'NA' if the type cannot be determined.
    """
    try:
        # Create a Magic object with MIME type detection enabled
        mime = magic.Magic(mime=True)
        
        # Use the Magic object to get the MIME type of the file
        mime_type = mime.from_file(file_path)
        
        return mime_type
    except Exception as e:
        # If DEBUG is set to True, print the error message
        if DEBUG:
            print(f"Error determining MIME type for {file_path}: {e}")
        
        # Return 'NA' if an error occurs
        return 'NA'
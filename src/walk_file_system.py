"""
Module: walk_file_system

Description:
------------
This module provides functionality to traverse a file system starting from a specified root directory and add files and directories to a graph database. It includes rate limiting for calls to a language model during testing.

Functions:
----------
- walk_file_system(root_dir: str, fs_graph: FileSystemGraph) -> None:
    Walks through the file system starting from root_dir and adds files and directories to the graph database.
"""

import os
import time  # Import time module
from file_system_graph import FileSystemGraph
from get_mime_type import get_mime_type
from meta_analyse import meta_analyse
from clean_up_file_system import clean_up_file_system
from azure_doc_converter import azure_doc_converter  # Import the Azure document converter function

DEBUG = os.getenv('TEST', 'False').lower() in ('true', '1', 't')  # Read DEBUG from environment variable

def walk_file_system(root_dir: str, fs_graph: FileSystemGraph):
    """
    Function: walk_file_system
    
    Description:
    ------------
    Walks through the file system starting from root_dir and adds files and directories to the graph database.
    
    Parameters:
    ------------
    root_dir : str
        The root directory from which to start the file system traversal.
    fs_graph : FileSystemGraph
        An instance of FileSystemGraph to which the files and directories will be added.
    
    Returns:
    --------
    None
    """
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        print(f"Error: The specified root directory does not exist: {root_dir}")
        return
    if not os.listdir(root_dir):
        print(f"Warning: The specified root directory is empty: {root_dir}")
        return

    current_walk_time = time.time()

    for root, dirs, files in os.walk(root_dir):
        dir_id = hash(root)
        
        # Process directory
        if root == root_dir:
            parent_dir_id = None  # No parent for the root directory
        else:
            parent_dir_id = hash(os.path.dirname(root))

        # Create or update the directory node
        dir_result = fs_graph.create_or_update_directory_node(
            dir_id=dir_id,
            parent_dir_id=parent_dir_id,
            dirname=os.path.basename(root),
            lastchecked=current_walk_time
        )
        print(f"Directory node created/updated: {dir_result}")  # Debug: Log result of directory node creation

        # Link directory to its parent (if it's not the root directory)
        if parent_dir_id is not None:
            fs_graph.link_directory_to_directory(dir_id, parent_dir_id)
            print(f"Linked directory {dir_id} to parent {parent_dir_id}")  # Debug: Log linking of directories

        # Iterate over files and create file nodes
        for file in files:
            file_path = os.path.join(root, file)
            file_id = hash(file_path)
            file_stats = os.stat(file_path)
            last_modified_time = file_stats.st_mtime

            # Initialize num_tokens and summary with default values
            num_tokens = 0
            summary = ""
            embedded_summary = []
            hashtags = []

            # Check if the file has been modified since the last time it was processed
            existing_file_node = fs_graph.get_file_node(file_id=file_id)
            if existing_file_node and existing_file_node['lastmodified'] == last_modified_time:
                # File hasn't changed, just update lastchecked
                fs_graph.update_file_node(file_id, {'lastchecked': current_walk_time})
                continue

            # Debug: Log file being processed
            if DEBUG:
                print(f"Processing file: {file_path}")

            # Only get MIME type for new files
            mime_type = get_mime_type(file_path) if not existing_file_node else existing_file_node['mime_type']

            if mime_type.startswith('text'):
                num_tokens, summary, embedded_summary, hashtags = meta_analyse(file_path=file_path)
            elif mime_type in [
                'application/pdf',
                'image/jpeg', 'image/png', 'image/bmp', 'image/tiff', 'image/heif',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'text/html'
            ]:
                converted_text = azure_doc_converter(file_path)
                num_tokens, summary, embedded_summary, hashtags = meta_analyse(converted_text=converted_text)
            else:
                num_tokens, summary, embedded_summary, hashtags = 0, "", [], []

            file_result = fs_graph.create_file_node(
                file_id=hash(file_path),
                dir_id=hash(root),
                filename=file,
                filetype=os.path.splitext(file)[1],
                filesize=file_stats.st_size,
                fileowner=file_stats.st_uid,
                hashtags=hashtags,
                lastmodified=last_modified_time,
                lastchecked=current_walk_time,
                creationdate=file_stats.st_ctime,
                mime_type=mime_type,
                num_tokens=num_tokens,
                summary=summary,
                embedded_summary=embedded_summary 
            )
            
            if DEBUG:
                print(f"File node created/updated: {file_result}")  # Debug: Log result of file node creation

            # After creating the file node
            if hashtags:
                for hashtag in hashtags:
                    fs_graph.create_hashtag_node(hashtag)
                    fs_graph.link_file_to_hashtag(file_id, hashtag)

            # Link file to its directory
            fs_graph.link_file_to_directory(file_id=file_id, dir_id=dir_id)

    # After walking, remove nodes that weren't checked in this walk
    clean_up_file_system(current_walk_time, fs_graph)

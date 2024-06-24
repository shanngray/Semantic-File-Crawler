import os
import time  # Import time module
from file_system_graph import FileSystemGraph
from get_mime_type import get_mime_type
from meta_analyse import meta_analyse

#DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')  # Read DEBUG from environment variable
DEBUG = True

def walk_file_system(root_dir: str, fs_graph: FileSystemGraph):
    """
    Walks through the file system starting from root_dir and adds files and directories to the graph database.
    """
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        print(f"Error: The specified root directory does not exist: {root_dir}")
        return
    if not os.listdir(root_dir):
        print(f"Warning: The specified root directory is empty: {root_dir}")
        return

    # Adding in rate limit for calls to LLM ***NOT REQUIRED FOR PRODUCTION USE***
    analyse_count = 0  # Initialize counter for meta_analyse calls
    start_time = time.time()  # Record the start time

    for root, dirs, files in os.walk(root_dir):
        parent_dir_id = hash(root)  # Unique identifier for the directory
        if root == root_dir:
            parent_dir_id = None  # No parent for the root directory
        else:
            parent_dir_id = hash(os.path.dirname(root))  # Parent directory ID

        # Debug: Log directory being processed
        print(f"Processing directory: {root}, Parent ID: {parent_dir_id}")

        # Create or update the directory node
        dir_result = fs_graph.create_directory_node(dir_id=hash(root), parent_dir_id=parent_dir_id, dirname=os.path.basename(root))
        print(f"Directory node created/updated: {dir_result}")  # Debug: Log result of directory node creation

        # Iterate over files and create file nodes
        for file in files:
            file_path = os.path.join(root, file)
            file_stats = os.stat(file_path)
            last_modified_time = file_stats.st_mtime

            # Initialize num_tokens and summary with default values
            num_tokens = 0
            summary = ""

            # Check if the file has been modified since the last time it was processed
            """
            existing_file_node = fs_graph.get_file_node(file_id=hash(file_path))
            if existing_file_node and existing_file_node['lastmodified'] == last_modified_time:
                if DEBUG:
                    print(f"Skipping unchanged file: {file_path}")
                continue  # Skip unchanged files
            """

            # Debug: Log file being processed
            if DEBUG:
                print(f"Processing file: {file_path}")

            mime_type = get_mime_type(file_path)  # Get MIME type

            # INCLUDES CODE TO RATE LIMIT LLM IN TESTING ENV
            if mime_type.startswith('text'):
                if analyse_count >= 10:
                    elapsed_time = time.time() - start_time
                    if elapsed_time < 60:
                        time.sleep(60 - elapsed_time)  # Sleep to ensure rate limit is not exceeded
                    analyse_count = 0  # Reset counter
                    start_time = time.time()  # Reset start time

                num_tokens, summary = meta_analyse(file_path)
                analyse_count += 1  # Increment counter

            file_result = fs_graph.create_file_node(
                file_id=hash(file_path),
                dir_id=hash(root),
                filename=file,
                filetype=os.path.splitext(file)[1],
                filesize=file_stats.st_size,
                fileowner=file_stats.st_uid,
                lastmodified=last_modified_time,
                creationdate=file_stats.st_ctime,
                walked=True,
                analysed=False,
                embedded=False,
                mime_type=mime_type,  # Add MIME type
                num_tokens=num_tokens,
                summary=summary
            )
            
            if DEBUG:
                print(f"File node created/updated: {file_result}")  # Debug: Log result of file node creation

            # Link file to its directory
            fs_graph.link_file_to_directory(file_id=hash(file_path), dir_id=hash(root))

        # If there is a parent directory, link the current directory to its parent
        if parent_dir_id is not None:
            fs_graph.link_directory_to_directory(dir_id=hash(root), parent_dir_id=parent_dir_id)

import mockfs
import os
import random
import time

def create_mock_filesystem():
    mfs = mockfs.MockFS()

    # File content generators
    def text_content():
        return f"This is a sample text file content. Random number: {random.randint(1, 1000)}"

    def binary_content():
        return bytes([random.randint(0, 255) for _ in range(100)])

    # File types
    file_types = [
        ('.txt', text_content),
        ('.docx', binary_content),
        ('.pdf', binary_content),
        ('.jpg', binary_content),
        ('.py', text_content),
        ('.json', text_content),
        ('.csv', text_content),
        ('.html', text_content),
        ('.xml', text_content),
        ('.md', text_content)
    ]

    # Create directory structure
    directory_structure = {
        '/root': {
            'documents': {
                'personal': {},
                'work': {
                    'projects': {
                        'project_a': {},
                        'project_b': {}
                    },
                    'reports': {}
                }
            },
            'images': {
                'vacation': {},
                'family': {}
            },
            'code': {
                'python': {},
                'javascript': {}
            },
            'misc': {}
        }
    }

    # Function to recursively create directories and files
    def create_files_and_dirs(structure, path=''):
        for name, content in structure.items():
            full_path = os.path.join(path, name)
            if isinstance(content, dict):
                mfs.makedirs(full_path)
                create_files_and_dirs(content, full_path)
            else:
                mfs.add_entries({full_path: content})

    # Create the basic structure
    create_files_and_dirs(directory_structure)

    # Add random files to each directory
    try:
        for root, dirs, files in mfs.walk('/root'):
            for _ in range(random.randint(1, 5)):  # Add 1-5 files per directory
                file_type, content_generator = random.choice(file_types)
                file_name = f"file_{random.randint(1000, 9999)}{file_type}"
                file_path = os.path.join(root, file_name)
                mfs.add_entries({file_path: content_generator()})
    except RuntimeError as e:
        if "generator raised StopIteration" in str(e):
            # This is the expected end of the walk, so we can safely ignore this error
            pass
        else:
            # If it's a different RuntimeError, re-raise it
            raise

    return mfs

def test_mock_filesystem():
    mfs = create_mock_filesystem()
    mockfs.replace_builtins(mfs._entries)  # Pass the entries dictionary instead of the MockFS instance

    try:
        # Your file system walking code here
        for root, dirs, files in os.walk('/root'):
            print(f"Directory: {root}")
            print(f"Subdirectories: {dirs}")
            print(f"Files: {files}")
            print("---")

        # Count total directories and files
        total_dirs = sum(len(dirs) for _, dirs, _ in os.walk('/root'))
        total_files = sum(len(files) for _, _, files in os.walk('/root'))
        print(f"Total directories: {total_dirs}")
        print(f"Total files: {total_files}")

    except RuntimeError as e:
        if "generator raised StopIteration" in str(e):
            pass  # Ignore RuntimeError caused by StopIteration
        else:
            raise  # Re-raise if it's a different RuntimeError

    finally:
        mockfs.restore_builtins()

def load_mock_fs():
    mfs = create_mock_filesystem()
    mockfs.replace_builtins(mfs._entries)  # Pass the entries dictionary instead of the MockFS instance

def close_mock_fs():
    mockfs.restore_builtins()
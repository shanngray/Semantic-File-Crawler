"""
Module: main

Description:
------------
This module initializes the file system graph, starts the file system traversal, and optionally
performs debug operations such as printing the number of nodes in the graph. It serves as the entry
point for the MetaCrawler application.

Attributes:
------------
DEBUG : bool
    A flag indicating whether debug mode is enabled, determined by the 'TEST' environment variable.
"""

import os
from file_system_graph import FileSystemGraph
from walk_file_system import walk_file_system
from dotenv import load_dotenv
from mock_filesystem import create_mock_filesystem, load_mock_fs, close_mock_fs

load_dotenv(".env")
DEBUG = os.getenv('TEST', 'False').lower() in ('true', '1', 't')  # Read TEST from environment variable

def main():
    """
    Function: main
    
    Description:
    ------------
    The main function initializes the file system graph, starts the file system traversal, and optionally
    performs debug operations such as printing the number of nodes in the graph.
    
    Parameters:
    ------------
    None
    
    Returns:
    ------------
    None
    """
    try:
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "abcd1234"
        fs_graph = FileSystemGraph(uri, username, password)

        # Set the root directory to start the crawl
        root_dir='/Users/shanngray/AI_Projects/MetaCrawler/tests/Test_Drive'

        if DEBUG:
            print(f"Connecting to database at {uri} with username {username}")
            print(f"Starting file system walk at: {root_dir}")

        # Start crawling the filesystem
        walk_file_system(root_dir, fs_graph)

        if DEBUG:
            try:
                query_result = fs_graph._execute_query("MATCH (n) RETURN COUNT(n) AS node_count")
                if query_result:
                    node_count = query_result[0]['node_count']  # Access the node count from the first record
                    print(f"Number of nodes in the graph: {node_count}")
                else:
                    print("No nodes found in the graph.")
            except Exception as e:
                print(f"Error during database query: {e}")

        # Close the connection to the database
        fs_graph.close()

        if DEBUG:
            print("Database connection closed")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    """
    Entity Type: Script Execution
    
    Description:
    ------------
    Entry point for the script. Calls the main function to start the process.
    
    Attributes/Parameters:
    ----------------------
    None
    
    Methods/Returns:
    ----------------
    None
    """
    main()

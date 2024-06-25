"""
Module: wipe_database

Description:
------------
This script wipes the entire database by deleting all nodes and relationships.
"""

from file_system_graph import FileSystemGraph

def main():
    """
    Function: main
    
    Description:
    ------------
    Connects to the database and wipes all nodes and relationships.
    
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

        fs_graph.wipe_database()
        print("Database wiped successfully.")

        fs_graph.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

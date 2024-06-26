"""
Module: fix_directory_relationships

Description:
------------
This module provides functionality to fix and verify directory relationships in the file system graph.
It is designed to be run as a one-time operation to ensure all directory relationships are correctly established.

Functions:
----------
- create_missing_directory_relationships(fs_graph: FileSystemGraph) -> int
- verify_directory_relationships(fs_graph: FileSystemGraph) -> list
- main(uri: str, username: str, password: str)
"""

from file_system_graph import FileSystemGraph

def create_missing_directory_relationships(fs_graph: FileSystemGraph) -> int:
    """
    Creates missing relationships between directories based on their parent_dir_id.

    Parameters:
    -----------
    fs_graph : FileSystemGraph
        An instance of FileSystemGraph to perform operations on the graph.

    Returns:
    --------
    int
        The number of relationships created.
    """
    query = """
    MATCH (child:Directory)
    WHERE child.parent_dir_id IS NOT NULL
    MATCH (parent:Directory {dir_id: child.parent_dir_id})
    WHERE NOT (parent)-[:CONTAINS]->(child)
    WITH parent, child
    MERGE (parent)-[:CONTAINS]->(child)
    RETURN count(*) as created_relationships
    """
    result = fs_graph._execute_query(query)
    created_relationships = result[0]['created_relationships'] if result else 0
    print(f"Created {created_relationships} missing directory relationships.")
    return created_relationships

def verify_directory_relationships(fs_graph: FileSystemGraph) -> list:
    """
    Verifies that all directories (except the root) have a parent relationship.

    Parameters:
    -----------
    fs_graph : FileSystemGraph
        An instance of FileSystemGraph to perform operations on the graph.

    Returns:
    --------
    list
        A list of directory IDs that are missing a parent relationship.
    """
    query = """
    MATCH (d:Directory)
    WHERE d.parent_dir_id IS NOT NULL
    AND NOT (d)<-[:CONTAINS]-()
    RETURN d.dir_id AS missing_parent
    """
    result = fs_graph._execute_query(query)
    missing_parents = [record['missing_parent'] for record in result]
    print(f"Found {len(missing_parents)} directories missing parent relationships.")
    return missing_parents

def main(uri: str, username: str, password: str):
    """
    Main function to fix and verify directory relationships.

    Parameters:
    -----------
    uri : str
        The URI of the Neo4j database.
    username : str
        The username for the Neo4j database.
    password : str
        The password for the Neo4j database.
    """
    fs_graph = FileSystemGraph(uri, username, password)

    try:
        print("Starting directory relationship fix...")
        created = create_missing_directory_relationships(fs_graph)
        print(f"Created {created} missing directory relationships.")

        print("\nVerifying directory relationships...")
        missing_parents = verify_directory_relationships(fs_graph)
        if missing_parents:
            print(f"Warning: Found {len(missing_parents)} directories without parent relationships.")
            print("Directory IDs missing parents:", missing_parents)
        else:
            print("All directories have parent relationships.")

    finally:
        fs_graph.close()

if __name__ == "__main__":
    # You can modify these values or use environment variables
    DB_URI = "bolt://localhost:7687"
    DB_USERNAME = "neo4j"
    DB_PASSWORD = "abcd1234"
    
    main(DB_URI, DB_USERNAME, DB_PASSWORD)
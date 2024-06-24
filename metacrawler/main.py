import os
from file_system_graph import FileSystemGraph
from walk_file_system import walk_file_system

#DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')  # Read DEBUG from environment variable
DEBUG = True
def main():
    try:
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "abcd1234"
        fs_graph = FileSystemGraph(uri, username, password)

        if DEBUG:
            print(f"Connecting to database at {uri} with username {username}")

        root_dir = "/Users/shanngray/AI_Projects/MetaCrawler"  # Starting point for file system traversal
        print(f"Starting file system walk at: {root_dir}")  # Debug: Confirm the directory path

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

        fs_graph.close()

        if DEBUG:
            print("Database connection closed")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


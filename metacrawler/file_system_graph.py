from neo4j import GraphDatabase
import os
import magic

class FileSystemGraph:
    """
    A class to represent a file system graph using Neo4j.

    Attributes:
    ----------
    driver : neo4j.GraphDatabase.driver
        The Neo4j driver instance.
    session : neo4j.Session
        The Neo4j session instance.

    Methods:
    -------
    close():
        Closes the Neo4j session and driver.
    _execute_query(query, **kwargs):
        Executes a Cypher query with the provided parameters.
    create_file_node(file_id, dir_id, filename, filetype, filesize, fileowner, lastmodified, creationdate, walked, analysed, embedded, mime_type, num_tokens, summary, lastchecked):
        Creates or updates a file node in the graph.
    create_or_update_directory_node(dir_id, parent_dir_id, dirname, lastchecked):
        Creates or updates a directory node in the graph.
    create_drive_node(drive_id, label):
        Creates or updates a drive node in the graph.
    link_directory_to_drive(dir_id, drive_id):
        Creates a relationship between a directory and a drive.
    link_file_to_directory(file_id, dir_id):
        Creates a relationship between a file and a directory.
    link_directory_to_directory(dir_id, parent_dir_id):
        Creates a relationship between a directory and its parent directory.
    get_file_node(file_id):
        Retrieves a file node from the graph.
    wipe_database():
        Wipes the entire database by deleting all nodes and relationships.
    """

    def __init__(self, uri, user, password):
        """
        Initializes the FileSystemGraph with a Neo4j driver and session.

        Parameters:
        ----------
        uri : str
            The URI of the Neo4j database.
        user : str
            The username for the Neo4j database.
        password : str
            The password for the Neo4j database.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.session = self.driver.session()

    def close(self):
        """
        Closes the Neo4j session and driver.
        """
        self.session.close()
        self.driver.close()

    def _execute_query(self, query, **kwargs):
        """
        Executes a Cypher query with the provided parameters.

        Parameters:
        ----------
        query : str
            The Cypher query to be executed.
        **kwargs : dict
            The parameters for the Cypher query.

        Returns:
        -------
        list
            The result of the query execution.
        """
        try:
            with self.driver.session() as session:
                result = session.write_transaction(lambda tx: list(tx.run(query, **kwargs)))
                return result
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def create_file_node(self, file_id, dir_id, filename, filetype, filesize, fileowner, lastmodified, creationdate, walked, analysed, embedded, mime_type, num_tokens, summary, lastchecked):
        """
        Creates or updates a file node in the graph.

        Parameters:
        ----------
        file_id : str
            The unique identifier for the file.
        dir_id : str
            The identifier of the directory containing the file.
        filename : str
            The name of the file.
        filetype : str
            The type of the file.
        filesize : int
            The size of the file in bytes.
        fileowner : str
            The owner of the file.
        lastmodified : str
            The last modified date of the file.
        creationdate : str
            The creation date of the file.
        walked : bool
            Whether the file has been walked.
        analysed : bool
            Whether the file has been analysed.
        embedded : bool
            Whether the file is embedded.
        mime_type : str
            The MIME type of the file.
        num_tokens : int
            The number of tokens in the file.
        summary : str
            The summary of the file.
        lastchecked : str
            The date when the file was last checked.

        Returns:
        -------
        list
            The result of the query execution.
        """
        query = (
            "MERGE (f:File {file_id: $file_id}) "
            "ON CREATE SET f.dir_id = $dir_id, f.filename = $filename, f.filetype = $filetype, "
            "f.filesize = $filesize, f.fileowner = $fileowner, f.lastmodified = $lastmodified, "
            "f.creationdate = $creationdate, f.walked = $walked, f.analysed = $analysed, f.embedded = $embedded, "
            "f.mime_type = $mime_type, f.num_tokens = $num_tokens, f.summary = $summary, f.lastchecked = $lastchecked "
            "ON MATCH SET f.dir_id = $dir_id, f.filename = $filename, f.filetype = $filetype, "
            "f.filesize = $filesize, f.fileowner = $fileowner, f.lastmodified = $lastmodified, "
            "f.creationdate = $creationdate, f.walked = $walked, f.analysed = $analysed, f.embedded = $embedded, "
            "f.mime_type = $mime_type, f.num_tokens = $num_tokens, f.summary = $summary, f.lastchecked = $lastchecked "
            "RETURN f"
        )
        return self._execute_query(query, file_id=file_id, dir_id=dir_id, filename=filename, filetype=filetype,
                                   filesize=filesize, fileowner=fileowner, lastmodified=lastmodified,
                                   creationdate=creationdate, walked=walked, analysed=analysed, embedded=embedded,
                                   mime_type=mime_type, num_tokens=num_tokens, summary=summary, lastchecked=lastchecked)

    def create_or_update_directory_node(self, dir_id, parent_dir_id, dirname, lastchecked):
        """
        Creates or updates a directory node in the graph.

        Parameters:
        ----------
        dir_id : str
            The unique identifier for the directory.
        parent_dir_id : str
            The identifier of the parent directory.
        dirname : str
            The name of the directory.
        lastchecked : str
            The date when the directory was last checked.

        Returns:
        -------
        list
            The result of the query execution.
        """
        query = (
            "MERGE (d:Directory {dir_id: $dir_id}) "
            "ON CREATE SET d.parent_dir_id = $parent_dir_id, d.dirname = $dirname, d.lastchecked = $lastchecked "
            "ON MATCH SET d.parent_dir_id = $parent_dir_id, d.dirname = $dirname, d.lastchecked = $lastchecked "
            "RETURN d"
        )
        return self._execute_query(query, dir_id=dir_id, parent_dir_id=parent_dir_id, dirname=dirname, lastchecked=lastchecked)

    def create_drive_node(self, drive_id, label):
        """
        Creates or updates a drive node in the graph.

        Parameters:
        ----------
        drive_id : str
            The unique identifier for the drive.
        label : str
            The label of the drive.

        Returns:
        -------
        list
            The result of the query execution.
        """
        query = (
            "MERGE (d:Drive {drive_id: $drive_id}) "
            "ON CREATE SET d.label = $label "
            "RETURN d"
        )
        return self._execute_query(query, drive_id=drive_id, label=label)

    def link_directory_to_drive(self, dir_id, drive_id):
        """
        Creates a relationship between a directory and a drive.

        Parameters:
        ----------
        dir_id : str
            The identifier of the directory.
        drive_id : str
            The identifier of the drive.
        """
        query = (
            "MATCH (d:Drive {drive_id: $drive_id}), (dir:Directory {dir_id: $dir_id}) "
            "MERGE (d)-[:CONTAINS]->(dir)"
        )
        self._execute_query(query, dir_id=dir_id, drive_id=drive_id)

    def link_file_to_directory(self, file_id, dir_id):
        """
        Creates a relationship between a file and a directory.

        Parameters:
        ----------
        file_id : str
            The identifier of the file.
        dir_id : str
            The identifier of the directory.
        """
        query = (
            "MATCH (dir:Directory {dir_id: $dir_id}), (f:File {file_id: $file_id}) "
            "MERGE (dir)-[:CONTAINS]->(f)"
        )
        self._execute_query(query, file_id=file_id, dir_id=dir_id)

    def link_directory_to_directory(self, dir_id, parent_dir_id):
        """
        Creates a relationship between a directory and its parent directory.

        Parameters:
        ----------
        dir_id : str
            The identifier of the directory.
        parent_dir_id : str
            The identifier of the parent directory.
        """
        query = (
            "MATCH (child:Directory {dir_id: $dir_id}), (parent:Directory {dir_id: $parent_dir_id}) "
            "MERGE (parent)-[:CONTAINS]->(child)"
        )
        self._execute_query(query, dir_id=dir_id, parent_dir_id=parent_dir_id)

    def get_file_node(self, file_id):
        """
        Retrieves a file node from the graph.

        Parameters:
        ----------
        file_id : str
            The identifier of the file.

        Returns:
        -------
        dict
            The file node as a dictionary, or None if not found.
        """
        query = (
            "MATCH (f:File {file_id: $file_id}) "
            "RETURN f"
        )
        result = self._execute_query(query, file_id=file_id)
        if result:
            return dict(result[0]['f'])
        return None

    def remove_file(self, file_id):
        """
        Removes a file node and its relationships from the graph.

        Parameters:
        ----------
        file_id : str
            The identifier of the file to be removed.
        """
        query = (
            "MATCH (f:File {file_id: $file_id}) "
            "DETACH DELETE f"
        )
        self._execute_query(query, file_id=file_id)

    def remove_directory(self, dir_id):
        """
        Removes a directory node and all its contents (subdirectories and files) from the graph.

        Parameters:
        ----------
        dir_id : str
            The identifier of the directory to be removed.
        """
        query = (
            "MATCH (d:Directory {dir_id: $dir_id}) "
            "OPTIONAL MATCH (d)-[:CONTAINS*]->(subdir:Directory) "
            "OPTIONAL MATCH (d)-[:CONTAINS*]->(file:File) "
            "DETACH DELETE d, subdir, file"
        )
        self._execute_query(query, dir_id=dir_id)

    def wipe_database(self):
        """
        Wipes the entire database by deleting all nodes and relationships.

        Returns:
        --------
        None
        """
        query = "MATCH (n) DETACH DELETE n"
        self._execute_query(query)
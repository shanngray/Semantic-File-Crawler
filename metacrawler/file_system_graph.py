from neo4j import GraphDatabase
import os
import magic

class FileSystemGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.session = self.driver.session()

    def close(self):
        self.session.close()
        self.driver.close()

    def _execute_query(self, query, **kwargs):
        try:
            with self.driver.session() as session:
                # Use a write transaction to execute the query and fetch results within the transaction scope
                result = session.write_transaction(lambda tx: list(tx.run(query, **kwargs)))
                return result  # Return the fully fetched list of records
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def create_file_node(self, file_id, dir_id, filename, filetype, filesize, fileowner, lastmodified, creationdate, walked, analysed, embedded, mime_type, num_tokens, summary):
        query = (
            "MERGE (f:File {file_id: $file_id}) "
            "ON CREATE SET f.dir_id = $dir_id, f.filename = $filename, f.filetype = $filetype, "
            "f.filesize = $filesize, f.fileowner = $fileowner, f.lastmodified = $lastmodified, "
            "f.creationdate = $creationdate, f.walked = $walked, f.analysed = $analysed, f.embedded = $embedded, f.mime_type = $mime_type, "
            "f.num_tokens = $num_tokens, f.summary = $summary "
            "RETURN f"
        )
        return self._execute_query(query, file_id=file_id, dir_id=dir_id, filename=filename, filetype=filetype, filesize=filesize, fileowner=fileowner, lastmodified=lastmodified, creationdate=creationdate, walked=walked, analysed=analysed, embedded=embedded, mime_type=mime_type, num_tokens=num_tokens, summary=summary)

    def create_directory_node(self, dir_id, parent_dir_id, dirname):
        query = (
            "MERGE (d:Directory {dir_id: $dir_id}) "
            "ON CREATE SET d.parent_dir_id = $parent_dir_id, d.dirname = $dirname "
            "RETURN d"
        )
        return self._execute_query(query, dir_id=dir_id, parent_dir_id=parent_dir_id, dirname=dirname)

    def create_drive_node(self, drive_id, label):
        query = (
            "MERGE (d:Drive {drive_id: $drive_id}) "
            "ON CREATE SET d.label = $label "
            "RETURN d"
        )
        return self._execute_query(query, drive_id=drive_id, label=label)

    def link_directory_to_drive(self, dir_id, drive_id):
        query = (
            "MATCH (d:Drive {drive_id: $drive_id}), (dir:Directory {dir_id: $dir_id}) "
            "MERGE (d)-[:CONTAINS]->(dir)"
        )
        self._execute_query(query, dir_id=dir_id, drive_id=drive_id)

    def link_file_to_directory(self, file_id, dir_id):
        query = (
            "MATCH (dir:Directory {dir_id: $dir_id}), (f:File {file_id: $file_id}) "
            "MERGE (dir)-[:CONTAINS]->(f)"
        )
        self._execute_query(query, file_id=file_id, dir_id=dir_id)

    def link_directory_to_directory(self, dir_id, parent_dir_id):
        query = (
            "MATCH (child:Directory {dir_id: $dir_id}), (parent:Directory {dir_id: $parent_dir_id}) "
            "MERGE (parent)-[:CONTAINS]->(child)"
        )
        self._execute_query(query, dir_id=dir_id, parent_dir_id=parent_dir_id)

"""
This module provides functionality for cleaning up the file system graph by removing
outdated files and directories that were not present in the most recent walk.

It contains a single function, clean_up_file_system, which performs the cleanup operation
on a given FileSystemGraph instance.
"""

from file_system_graph import FileSystemGraph

def clean_up_file_system(current_walk_time, fs_graph):
    """
    Function: clean_up_file_system
    
    Description:
    ------------
    Removes files and directories from the graph that weren't present in the current walk,
    and cleans up orphaned hashtag nodes.
    
    Parameters:
    -----------
    current_walk_time : float
        The timestamp of the current walk.
    fs_graph : FileSystemGraph
        An instance of FileSystemGraph to perform operations on the graph.
    
    Returns:
    --------
    None
    """
    # Query to find files that weren't checked in the current walk
    file_query = (
        "MATCH (f:File) "
        "WHERE f.lastchecked < $current_walk_time "
        "RETURN f.file_id AS file_id"
    )
    
    # Query to find directories that weren't checked in the current walk
    dir_query = (
        "MATCH (d:Directory) "
        "WHERE d.lastchecked < $current_walk_time "
        "RETURN d.dir_id AS dir_id"
    )
    
    # Execute queries on directories first so that child files are removed.
    outdated_dirs = fs_graph._execute_query(dir_query, current_walk_time=current_walk_time)
    
    # Remove outdated directories
    for record in outdated_dirs:
        fs_graph.remove_directory(record['dir_id'])

    # Execute query on files after directories have already been removed
    outdated_files = fs_graph._execute_query(file_query, current_walk_time=current_walk_time)
    
    # Remove outdated files
    for record in outdated_files:
        fs_graph.remove_file(record['file_id'])
    
    # Clean up orphaned hashtag nodes
    orphaned_hashtags = fs_graph.cleanup_orphaned_hashtags()
    
    print(f"Cleanup complete. Removed {len(outdated_files)} files, {len(outdated_dirs)} directories, and {len(orphaned_hashtags)} orphaned hashtags.")

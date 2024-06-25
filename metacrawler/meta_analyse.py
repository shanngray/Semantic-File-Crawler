"""
Module: meta_analyse

Description:
------------
This module provides functionality to analys the content of a file by reading its contents, tokenizing the text, and summarizing it using a language model.

Functions:
----------
- meta_analyse(file_path: str) -> tuple:
    Analyzes the content of a file, tokenizes the text, and summarizes it.
"""

import tiktoken
import mimetypes
from summarise_agent import summarise_agent
from hashtag_agent import hashtag_agent

def meta_analyse(file_path):
    """
    Function: meta_analyse
    
    Description:
    ------------
    Analyzes the content of a file by reading its contents, tokenizing the text, and summarizing it using a language model.
    
    Parameters:
    ------------
    file_path : str
        The path to the file that needs to be analyzed.
    
    Returns:
    --------
    tuple
        A tuple containing the number of tokens in the file and the summary of the file content.
    """
    try:
        # Read the file contents
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
    except UnicodeDecodeError:
        raise ValueError("The file is not encoded in UTF-8")

    # Tokenize the text using tiktoken's BPE tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")
    
    tokens = tokenizer.encode(file_contents)
    num_tokens = len(tokens)

    # Send tokens to a small LLM
    if num_tokens < 50000:
        summary = summarise_agent()
        embedded_summary = embed(summary)
        hashtags = hashtag_agent()
    else:
        # Send tokens to a large LLM
        print("TOO MANY TOKENS!")
        summary = "DOC WAS TOO LONG!!"
    
    return num_tokens, summary, embedded_summary, hashtags
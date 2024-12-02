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
from embed import embed

def meta_analyse(*, file_path: str = None, converted_text: str = None):
    """
    Function: meta_analyse
    
    Description:
    ------------
    Analyzes the content of a file or converted text by tokenizing and summarizing it using a language model.
    
    Parameters:
    ------------
    file_path : str, optional
        The path to the file that needs to be analyzed.
    converted_text : str, optional
        The pre-converted text content to be analyzed.
    
    Returns:
    --------
    tuple
        A tuple containing the number of tokens, summary, embedded summary, and hashtags.
    """
    if file_path is None and converted_text is None:
        raise ValueError("Either file_path or converted_text must be provided")
    
    if file_path is not None and converted_text is not None:
        raise ValueError("Only one of file_path or converted_text should be provided")

    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            raise ValueError("The file is not encoded in UTF-8")
    else:
        content = converted_text

    # Tokenize the text using tiktoken's BPE tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")
    
    tokens = tokenizer.encode(content)
    num_tokens = len(tokens)

    # Send tokens to a small LLM
    if num_tokens < 50000:
        summary = summarise_agent(content)
        embedded_summary = embed(summary)
        hashtags = hashtag_agent(content)
    else:
        # Send tokens to a large LLM
        print("TOO MANY TOKENS!")
        summary = "DOC WAS TOO LONG!!"
    
    return num_tokens, summary, embedded_summary, hashtags
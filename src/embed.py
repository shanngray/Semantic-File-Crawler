"""
Module: embed

Description:
------------
This module provides functionality to generate embeddings for a given text using the OpenAIEmbeddings model.

Functions:
----------
embed(text: str) -> list:
    Generates embeddings for the input text using the OpenAIEmbeddings model.
"""

from langchain_openai import OpenAIEmbeddings

def embed(text: str):
    """
    Function: embed
    
    Description:
    ------------
    Generates embeddings for the input text using the OpenAIEmbeddings model.
    
    Parameters:
    ------------
    text : str
        The input text to be embedded.
    
    Returns:
    --------
    list
        A list of embeddings representing the input text.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return embeddings.embed_query(text)
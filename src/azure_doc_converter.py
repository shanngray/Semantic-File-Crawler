"""
Module: azure_doc_converter

Description:
------------
This module provides functionality to convert documents using Azure AI Document Intelligence.
It utilizes the AzureAIDocumentIntelligenceLoader from langchain_community to process and extract
information from various document types.

Methods:
--------
azure_doc_converter(file_path: str) -> str
"""

import os
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from dotenv import load_dotenv

load_dotenv()

def azure_doc_converter(file_path):
    """
    Function: azure_doc_converter

    Description:
    ------------
    Converts a document at the given file path using Azure AI Document Intelligence
    and extracts the page content as a string.

    Parameters:
    -----------
    file_path : str
        The path to the document file to be converted.

    Returns:
    --------
    str
        The extracted page content as a string.
    """
    
    endpoint = "https://shandocint.cognitiveservices.azure.com/"
    key = os.getenv("AZURE_DOC_KEY")
    loader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=endpoint,
        api_key=key,
        file_path=file_path,
        api_model="prebuilt-layout",
        mode="single"
    )

    documents = loader.load()
    
    # Extract the page_content from the first document
    if documents and len(documents) > 0:
        return documents[0].page_content
    else:
        return ""  # Return an empty string if no content is found

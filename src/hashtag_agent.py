"""
Module: tags_agent

Description:
------------
This module defines an agent that processes and creates hashtags for documents using a language model.

Attributes/Parameters:
----------------------
N/A

Methods/Returns:
----------------
summarise_agent: function
    Processes a document and tags it.
    
    Parameters:
    -----------
    N/A
    
    Returns:
    --------
    hashtags: A list of hashtags for the document.
"""

from langchain_core.output_parsers import StrOutputParser
#from langchain_cohere import ChatCohere
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from extract_hashtags import extract_hashtags

def hashtag_agent(file_contents):
    """
    Function: hash_agent
    
    Description:
    ------------
    Processes a document and creates hashtags it using a language model.
    
    Parameters:
    -----------
    N/A
    
    Returns:
    --------
    hashtags: A list of hashtags for the document.
    """
    
    # Define the system prompt that sets the context for the feedback generation.
    system_prompt = (
        "# ROLE:\n"
        "You are an expert at social media and finding the best hashtags to describe a document.\n\n"
        "# TASK:\n"
        "Review the document and provide a list of hashtags.\n\n"
        "# NOTES: \n"
        " - Don't make anything up\n."
        " - Make sure the hashtags are meaningful and categorise the document in a useful manner.\n"
        " - Please only reply with the hashtags and don't add any extra commentary."
    )
    
    # Initialize the language model with specific parameters for controlled generation.
    llm = ChatOpenAI(model="gpt-4o",temperature=0.2)
    #llm = ChatCohere(model_name="command-r-plus", temperature=0.4)
    
    # Create a prompt template that includes the system prompt and placeholders for dynamic content.
    query_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "Document to be summarised: {working_doc}.")
            #MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # Define the output parser to handle the model's text output.
    output_parser = StrOutputParser()
 
    # Chain the components to process the input and generate feedback.
    hashtag_chain = query_prompt | llm | output_parser

    raw_hashtags = hashtag_chain.invoke({"working_doc": file_contents})

    # Extract hashtags from the raw string
    hashtags = extract_hashtags(raw_hashtags)
    # If no hashtags were found, return an empty list
    if not hashtags:
        return []

    return hashtags

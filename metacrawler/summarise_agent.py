"""
Module: summarise_agent

Description:
------------
This module defines an agent that processes and summarises documents using a language model.

Attributes/Parameters:
----------------------
N/A

Methods/Returns:
----------------
summarise_agent: function
    Processes a document and summarises it.
    
    Parameters:
    -----------
    N/A
    
    Returns:
    --------
    summary: A brief summary of the document.
"""

from langchain_core.output_parsers import StrOutputParser
#from langchain_cohere import ChatCohere
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def summarise_agent(file_contents):
    """
    Function: summarise_agent
    
    Description:
    ------------
    Processes a document and summarises it using a language model.
    
    Parameters:
    -----------
    N/A
    
    Returns:
    --------
    summary: A brief summary of the document.
    """
    
    # Define the system prompt that sets the context for the feedback generation.
    system_prompt = (
        "# ROLE:\n"
        "You are an expert at summarisation. Being succinct is an artform.\n\n"
        "# TASK:\n"
        "Review the document and provide a succinct summary.\n\n"
        "# NOTES: \n"
        " - Don't make anything up\n."
        " - Make sure your response is clear, concise and analytical.\n"
        " - Please only reply with the summary and don't add any extra commentary."
    )
    
    # Initialize the language model with specific parameters for controlled generation.
    llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
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
    summary_chain = query_prompt | llm | output_parser

    summary = summary_chain.invoke({"working_doc": file_contents})

    return summary

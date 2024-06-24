import tiktoken
import mimetypes
from summarise_agent import summarise_agent

def meta_analyse(file_path):

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

    # Placeholder for sending tokens to an LLM
    if num_tokens < 50000:
        summarise_chain = summarise_agent()
        summary = summarise_chain.invoke({"working_doc": file_contents})
        # Send tokens to a small LLM
        pass  # Replace with actual code to send tokens to a small LLM
    else:
        # Send tokens to a large LLM
        print("TOO MANY TOKENS!")
        summary = "DOC WAS TOO LONG!!"
        pass  # Replace with actual code to send tokens to a large LLM

    return num_tokens, summary
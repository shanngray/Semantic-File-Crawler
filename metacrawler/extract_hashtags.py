def extract_hashtags(raw_hashtags):
    """
    Extracts hashtags from a string and returns them as a list.

    Parameters:
    -----------
    raw_hashtags : str
        A string containing hashtags and possibly other text.

    Returns:
    --------
    list
    A list of hashtags as strings, without the '#' symbol.
    """
    # Split the string into words
    words = raw_hashtags.split()
        
    # Filter for words starting with '#' and remove the '#'
    hashtags = [word[1:] for word in words if word.startswith('#')]
        
    return hashtags

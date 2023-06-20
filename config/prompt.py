"""Prompt configuration"""
import dotenv
import sys

def get_prompt(): 
    """Get the prompt that will be used for generating the text from the .env file"""

    keys = ["PROMPT"]
    values = [dotenv.get_key(dotenv.find_dotenv(), key) for key in keys]

    # Check that all values were found
    if None in values:
        missing_keys = [key for key, value in zip(
            keys, values) if value is None]
        print(
            f"Error: the following environment variables are missing: {', '.join(missing_keys)}")
        sys.exit(1)
    
    prompt = values[0]
    return prompt
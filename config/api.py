"""This module contains the functions that will be used to get the API URL from the .env file"""
import dotenv
import sys


def get_api_url():
    """Get the API URL that will be used for scrapping from the .env file"""
    keys = ["API_URL"]
    values = [dotenv.get_key(dotenv.find_dotenv(), key) for key in keys]

    # Check that all values were found
    if None in values:
        missing_keys = [key for key, value in zip(
            keys, values) if value is None]
        print(
            f"Error: the following environment variables are missing: {', '.join(missing_keys)}")
        sys.exit(1)
    api_url = values[0]
    return api_url

def get_open_api_key():
    """Get OPEN API KEY from the .env file"""
    keys = ["OPEN_API_KEY"]
    values = [dotenv.get_key(dotenv.find_dotenv(), key) for key in keys]

    # Check that all values were found
    if None in values:
        missing_keys = [key for key, value in zip(
            keys, values) if value is None]
        print(
            f"Error: the following environment variables are missing: {', '.join(missing_keys)}")
        sys.exit(1)
    open_api_key = values[0]
    return open_api_key
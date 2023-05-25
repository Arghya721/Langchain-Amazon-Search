"""Amazon data cleaner module"""
import json
from marshmallow import ValidationError
from schema.amazon_db import AmazonSchema


def clean_product_title(product_title):
    """Clean the product title"""
    cleaned_title = product_title.strip()

    # also remove unicode characters
    cleaned_title = cleaned_title.encode('ascii', 'ignore').decode()

    return cleaned_title


def clean_text_data(text_data):
    """Clean the text data"""

    # check if text_data is a list
    if not isinstance(text_data, list):
        return None

    cleaned_text_data = [x.strip() for x in text_data if x.strip()]

    # remove \n from the list
    cleaned_text_data = [x.replace('\n', '') for x in cleaned_text_data]

    # remove <br> from the list
    cleaned_text_data = [x.replace('<br>', '') for x in cleaned_text_data]

    # also remove unicode characters
    cleaned_text_data = [x.encode('ascii', 'ignore').decode()
                         for x in cleaned_text_data]

    # make cleaned_text_data string
    cleaned_text_data = json.dumps(cleaned_text_data)

    return cleaned_text_data


def clean_product_details(product_details):
    """Clean the product details"""
    cleaned_product_details = {}

    # check if product details is dict
    if not isinstance(product_details, dict):
        return None

    for key, value in product_details.items():
        # remove \n from key and value
        cleaned_key = " ".join(key.split()).replace("\u200f", "").replace("\u200e", "").replace(":", "").strip()
        cleaned_value = " ".join(value.split()).replace("\u200f", "").replace("\u200e", "").replace(":", "")
        cleaned_value = cleaned_value.replace(cleaned_key, "").strip()  # Remove cleaned_key from cleaned_value
        cleaned_product_details[cleaned_key] = cleaned_value

    # make cleaned_product_details string
    cleaned_product_details = json.dumps(cleaned_product_details)

    return cleaned_product_details


def amazon_data_formater(raw_amazon_data):
    """Format raw Amazon data to match the schema"""

    formated_amazon_data_list = []

    for item in raw_amazon_data:
        try:

            # check if textData is in the item
            if 'textData' in item:
                item['textData'] = clean_text_data(item['textData'])

            # check if productTitle is in the item
            if 'productTitle' in item:
                item['productTitle'] = clean_product_title(
                    item['productTitle'])

            # check if productDescription is in the item
            if 'productDescription' in item:
                item['productDescription'] = clean_product_details(
                    item['productDescription'])

            # check if productDetails is in the item
            if 'productDetails' in item:
                item['productDetails'] = clean_product_details(
                    item['productDetails'])

            # check if technicalDetails is in the item
            if 'technicalDetails' in item:
                item['technicalDetails'] = clean_product_details(
                    item['technicalDetails'])

            # check if additionalDetails is in the item
            if 'additionalDetails' in item:
                item['additionalDetails'] = clean_product_details(
                    item['additionalDetails'])

            formated_amazon_data_list.append(AmazonSchema().load(item))
        except ValidationError as error:
            print(error.messages)

    return formated_amazon_data_list

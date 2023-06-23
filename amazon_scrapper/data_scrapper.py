"""This module contains the functions to scrap the data from the response"""
from bs4 import BeautifulSoup

def check_if_data_exists(response):
    """Check if the data exists in the response"""
    soup = BeautifulSoup(response.content, 'html.parser')
    no_results = soup.find_all('div', class_='s-asin')

    # check if the string contains this string "Try checking your spelling or use more general terms"
    if len(no_results) == 0:
        return True
    else:
        return False


def scrap_search_page_data(response, api_url, sort_by):
    """Scrap the search page data from the response"""

    # declare a list to store the data
    search_page_data = []

    # parse the response
    soup = BeautifulSoup(response.content, 'html.parser')

    # get useful chunk from the soup
    page_data_htmls = soup.find_all('div', class_='s-asin')

    for page_data_html in page_data_htmls:

        asin = page_data_html.get('data-asin')
        sponsored = page_data_html.find('span', class_='a-color-secondary')

        if sponsored is None:
            sponsored = False
        elif sponsored.text == "Sponsored":
            sponsored = True
        else:
            sponsored = False

        product_title = page_data_html.find(
            'span', class_='a-size-base-plus a-color-base a-text-normal')
        if product_title is None:
            product_title = page_data_html.find(
                'span', class_='a-size-medium a-color-base a-text-normal')
            if product_title is None:
                product_title = "Not found"
            else:
                product_title = product_title.text
        else:
            product_title = product_title.text
        product_price = page_data_html.find('span', class_='a-price-whole')
        if product_price is None:
            continue
        else:
            product_price = product_price.text
        

        # get image url
        image_url = page_data_html.find('img', class_='s-image').get('src')

        product_link =  api_url + "dp/" + asin

        product_details = {
            'asin': asin,
            'sponsored': sponsored,
            'productTitle': product_title,
            'productPrice': product_price,
            'productLink': product_link,
            'image_url': image_url
        }

        search_page_data.append(product_details)
    
    # sort the search page data
    search_page_data = sort_search_page_data(search_page_data, sort_by)

    return search_page_data


def sort_json_by_price(json_response, ascending=True):
    """Sort the json response by price"""
    sorted_json = sorted(json_response, key=lambda x: int(x["productPrice"].replace(",", "")), reverse=not ascending)
    return sorted_json

def sort_search_page_data(search_page_data, sort_by):
    """Sort the search page data"""
    sorted_search_page_data = search_page_data
    if sort_by == "asc":
        sorted_search_page_data = sort_json_by_price(search_page_data, ascending=True)
    elif sort_by == "desc":
        sorted_search_page_data = sort_json_by_price(search_page_data, ascending=False)
    
    return sorted_search_page_data



def scrap_page_data(response, product, api_url):
    """Scrap the page data from the response"""

    # parse the response
    soup = BeautifulSoup(response.content, 'html.parser')

    # get useful chunk from the soup
    page_data_html = soup.find('div', id='dp')

    if page_data_html is None:
        return product

    # get the product title
    product_title = None

    try:
        product_title = page_data_html.find('span', id='productTitle').text or None
    except AttributeError:
        print("No product title found")

    # get productStore url
    product_store_url = None
    try:
        product_store_url = page_data_html.find(
            'a', id='bylineInfo').get('href') or None
    except AttributeError:
        print("No product store url found")

    # if product_store_url is not none add amazon.in
    if product_store_url is not None:
        product_store_url = api_url + product_store_url

    # Extract all the text data from the HTML block
    text_data = None
    try:
        text_data = page_data_html.find(
            'div', id='feature-bullets').find_all(text=True)
    except AttributeError:
        print("No text data found")

    # get the product description
    product_description = None
    try:
        product_description = page_data_html.find(
            'div', id='productDescription').text or None
    except AttributeError:
        print("No product description found")

    # Find the HTML block that contains the product details
    product_details = None
    try:
        product_details = page_data_html.find(
            'div', id='detailBulletsWrapper_feature_div')
    except AttributeError:
        print("No product details found")

    # Extract all the product details from the HTML block
    product_details_dict = {}
    try:
        for product_detail in product_details.find_all('li'):
            product_details_dict[product_detail.find('span', class_='a-text-bold').text] = product_detail.text
    except AttributeError:
        print("No product details found")

    # extract technical details
    technical_details = page_data_html.find(
        'div', id='productDetails_techSpec_section_1')

    # Extract all the technical details from the HTML block
    technical_details_dict = {}

    try : 
        for technical_detail in technical_details.find_all('tr'):
            technical_details_dict[technical_detail.find(
                'th', class_='a-color-secondary a-size-base prodDetSectionEntry').text] = technical_detail.find('td', class_='a-size-base prodDetAttrValue').text
    except AttributeError:
        print("No technical details found")

    # extract additional details
    additional_details = page_data_html.find(
        'div', id='productDetails_db_sections')

    # Extract all the additional details from the HTML block
    additional_details_dict = {}
    try:
        for additional_detail in additional_details.find_all('tr'):
            additional_details_dict[additional_detail.find(
                'th', class_='a-color-secondary a-size-base prodDetSectionEntry').text] = additional_detail.find('td', class_='a-size-base prodDetAttrValue').text
    except AttributeError:
        print("No additional details found")

    # add all data into product
    product['textData'] = text_data
    product['productTitle'] = product_title
    product['productStoreUrl'] = product_store_url
    product['productDescription'] = product_description
    product['productDetails'] = product_details_dict
    product['technicalDetails'] = technical_details_dict
    product['additionalDetails'] = additional_details_dict

    return product

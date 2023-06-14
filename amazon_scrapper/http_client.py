"""This module contains the http client for the amazon scrapper. This module is responsible for making the requests to the API. After getting the response from the API, it passes the response to the data_scrapper module to scrap the data from the response."""
from concurrent.futures import ThreadPoolExecutor
import requests
import config.api as config
from amazon_scrapper.data_scrapper import scrap_search_page_data


def get_search_page_data(api_url):
    """Get the search page data from the API"""

    # declare headers for the requests
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }


    response = requests.get(api_url, headers=headers, timeout=5)

    search_page_data = []

    # check if the request is successfull
    if response.status_code == 200:
        # scrap the data
        search_page_data = search_page_data + \
            scrap_search_page_data(response, config.get_api_url())

    return search_page_data


# def get_page_data(search_page_data) -> dict:
#     """Get the page data from the URL"""

#     # declare headers for the requests
#     headers = {
#         'authority': 'www.amazon.com',
#         'pragma': 'no-cache',
#         'cache-control': 'no-cache',
#         'dnt': '1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'sec-fetch-site': 'none',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-dest': 'document',
#         'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     }

#     page_data = []

#     for product in search_page_data:

#         # make query params
#         request_url = product['productLink']

#         # make the request
#         response = requests.get(request_url, headers=headers)

#         # check if the request is successfull
#         if response.status_code == 200:
#             # scrap the data
#             page_data.append(scrap_page_data(response, product))

#     return page_data


# faster version of get_page_data using threadPool
def get_page_data(search_page_data, api_url) -> dict:
    """Get the page data from the URL"""

    def process_product(product):
        # declare headers for the requests
        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        # make query params
        request_url = product['productLink']

        # make the request
        response = requests.get(request_url, headers=headers, timeout=15)

        # check if the request is successful
        if response.status_code == 200:
            # scrap the data
            page_data.append(scrap_page_data(response, product, api_url))

    page_data = []

    # Create a ThreadPoolExecutor with max_workers set to the number of products
    with ThreadPoolExecutor(max_workers=64) as executor:
        # Submit each product processing to the executor
        futures = [executor.submit(process_product, product)
                   for product in search_page_data]

        # Wait for all futures to complete
        for future in futures:
            future.result()

    return page_data

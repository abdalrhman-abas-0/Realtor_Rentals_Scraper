"""
this module contains functions for initiating and running the crawler.

it uses the scrapers_m module to request the website api and return 
the json response which contain the desired data.

Functions:
    initiate_crawler() -> tuple[configure_headers, back_end_API, str]
        Returns the headers, crawler and page content for scraping.
    run_crawler(initiate_classes:function, headers:configure_headers, crawler_: back_end_API,
        request:str, property_id: int, page_url:str="",page_source:str="") -> json:
            Returns the json response from the crawler for a given request.
"""

from inputs_m.inputs import WEBSITE
from scrapers_m.abstract_classes import back_end_API, configure_headers
from scrapers_m.c_handler import headers_configuring, back_end_API_
from scrapers_m.headers import change_headers_
import json

def initiate_crawler() -> tuple[configure_headers, back_end_API, str]:
    """ Returns the headers, crawler, and page content for scraping.

    it instantiates the headers_configuring, back_end_API_ and change_headers_
    classes and returns those instances along with the first-page source code.
    
    Returns:
        tuple[configure_headers, back_end_API, str]: A tuple of
            an instance of headers_configuring class, an instance of
            back_end_API_ class, a string of the page source.
    """
    page_content, search_page_api_headers, result_api_headers, requests_data_dict = change_headers_(WEBSITE).get_headers()
    headers = headers_configuring(requests_data_dict, search_page_api_headers, result_api_headers)
    crawler_ = back_end_API_(120)
    return headers, crawler_, page_content

def run_crawler(initiate_classes:initiate_crawler, headers:configure_headers, crawler_: back_end_API, request:str, property_id: int, page_url:str="",page_source:str="") -> json:
    """Returns the json response from the crawler for a given request.

    i uses the instances passed into it to request the website api using
    the request, property_id and page_url to make the write request and
    return the json response of it.
    
    it will re-make requests automatically if the response is empty "None".
    
    Note:
        if a request failed the back_end_API.back_end method will sleep 
        for sleep_sec seconds "a class argument" and remake the request
        and if the request failed for the second time it will return 
        None.
    
    Args:
        initiate_classes (function): A function that returns the headers,
            crawler and page content.
        headers (configure_headers): An instance of headers_configuring class.
        crawler_ (back_end_API): An instance of back_end_API_ class.
        request (str): the request type ("pages" or "results").
        property_id (int): the property id or search page number to be scraped.
        page_url(str, optional): A string of the page url, (default is "").
        page_source(str, optional): A string of the page source, (default is "").

    Returns:
        json: A dictionary of the json response from the crawler.
    """
    if page_source == "":
        while True:
            if request == "pages":
                url, get_data, request_headers = headers.primary_adjust_headers(request,property_id)
            else:
                url, get_data, request_headers = headers.secondary_adjust_headers(request,property_id, page_url)
            
            json_response = crawler_.back_end(url, request_headers, get_data)
            if json_response != None:
                break
            else:
                headers, crawler_, page_content = initiate_classes()
    else:
        json_response = crawler_.parse_first_page(page_source)
  
    return json_response

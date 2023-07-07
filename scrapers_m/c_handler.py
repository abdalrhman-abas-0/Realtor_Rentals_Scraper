"""website crawler.

This module requests the website api and extract the json objects
which contains the needed data.

this module is responsible for configuring all the headers and 
request body for each request made.
    
it requests the website api to get the response which 
contains the data to be scraped.

it also extracts the json object form the first page 
source code to later extract the need info from it.

This script requires that `httpx_html, re, winsound` be installed within the Python
environment you are running this script in.

the classes in this module inherit form the abstract classes found in
scrapers_m.abstract_classes module.

This file can also be imported as a module and contains the following

classes:
    headers_configuring(configure_headers) :
        configure the headers and bodies for each request made.
    back_end_API_(back_end_API):
        requests sender to and first page parser. 
"""
from httpx_html import HTMLSession, HTML
from time import sleep
import winsound
import json
import re
from inputs_m.inputs import LISTING_PER_PAGE
from scrapers_m.abstract_classes import configure_headers,back_end_API

class headers_configuring(configure_headers) :
    """configure the headers and bodies for each request made.
    
    this class inherits the abstract class configure_headers found in 
    scrapers_m.abstract_classes module.
     
    uses the stored request_body elements, search_page_api_headers and 
    result_api_headers to create the appropriate headers and request body
    for each request depending on the method used and it's inputs. 
    
    Attributes:
        request_body (dict): dict of multiple request bodies.
        search_page_api_headers (dict): the headers for the search page request.
        result_api_headers (dict): the headers for a result page request.
        
    Methods:
        primary_adjust_headers(request:str, page:int) -> tuple[str,str,dict]
            Adjusts the headers for the primary stage requests.
        secondary_adjust_headers(request:str, property_id:int, web_page:str) -> tuple[str, str, dict]
            Adjusts the headers for the secondary stage requests.
        
    """
    
    def __init__(self,request_body:dict, search_page_api_headers:dict, result_api_headers:dict):
        self.request_body = request_body
        self.search_page_api_headers = search_page_api_headers
        self.result_api_headers = result_api_headers 

    def primary_adjust_headers(self, request:str, page:int) -> tuple[str,str,dict]:
        """
        Adjusts the headers for the primary stage requests.

        ues the request parameter to pull out the appropriate headers to use 
        from the request_body dict and modifies the headers and the request body
        according to the page parameter.
        
        Args:
            request (str): The request.
            page (int): The page number.

        Returns:
            url (str): the API url of the request to be made.
            get_data (str): the body of the post request to be made.
            request_headers (dict): the headers of the post request to be made.
        """
        request_headers = self.search_page_api_headers.copy()
        url = request_headers["url"]
        del request_headers["url"]
        
        get_data = self.request_body.copy()
        get_data = get_data[request]
        get_data = re.sub(r'pg-\d+',f'pg-{page}',re.sub(r'"offset":\d+', f'"offset":{((page-1)*LISTING_PER_PAGE)}', get_data))
        
        return url, get_data, request_headers 
    
    def secondary_adjust_headers(self, request:str, property_id:int, web_page:str) -> tuple[str, str, dict]: 
        """
        Adjusts the headers for the secondary stage requests.

        ues the request parameter to pull out the appropriate headers to use 
        from the request_body dict and modifies the headers and the request body
        according to the page parameter.
        
        Args:
            request (str): The request.
            property_id (int): The property ID.
            web_page (str): The web page.

        Returns:
            url (str): the API url of the request to be made.
            get_data (str): the body of the post request to be made.
            request_headers (dict): the headers of the post request to be made.
        """  
        request_headers = self.result_api_headers.copy()
        url = request_headers["url"]
        del request_headers["url"]
        request_headers["referer"] = web_page
        
        get_data = self.request_body.copy()
        get_data = get_data[f"{request}"]
        
        if request == "schools":
            get_data = re.sub(r'"property_id":"\d+"', f'"property_id":"{property_id}"', get_data)
        else:
            get_data = re.sub(r'"propertyId":"\d+"', f'"propertyId":"{property_id}"', get_data)
            
        return url, get_data, request_headers 
    
    
class back_end_API_(back_end_API):
    """requests sender to and first page parser. 

    it inherits form the abstract class back_end_API found
    in scrapers_m.abstract_classes module.
    
    contacts the website api got get the needed json response.
    it also extracts json object form the source of the first
    page.
    
    Args:
        back_end_API (class): an abstract class.
    
    Attributes:
        session (HTMLSession): stores the html session used to connect to
            scraped website's api.
        sleep_sec(int): the sleep duration between the failed responses.
    
    Methods:
        back_end(url:str, request_headers:dict, request_body:str) -> json
            requests sender.
        parse_first_page(page_content:str) -> json
            first page parser.
    
    Properties:
        sound_alarm
            creates sound "used to alarm problems".
    """
    
    def __init__(self, sleep_sec:int):
        self.sleep_sec = sleep_sec
        self.session = HTMLSession()
             
    def back_end(self, url:str, request_headers:dict, request_body:str) -> json:
        """requests sender.
        
        Sends a POST request to the given URL with the given headers and body.
        if the response is not valid it will sleep self.sleep_sec seconds 
        and remake the request.

        Args:
            url (str): The URL to send the request to.
            request_headers (dict): The headers to include in the request.
            request_body (str): The body of the request.

        Returns:
            response (json): The response from the server.
        """     
        response = None 
        slept = False     
        while slept == False:  
            try:
                r = self.session.post(url, headers= request_headers, data = request_body)
                response = r.html
                response = json.loads(str(response.html))
                break
            except:
                if response != None and slept == True:
                    self.sound_alarm
                else:
                    slept = True
                    sleep(self.sleep_sec)
        return response 
     
    def parse_first_page(self,page_content:str) -> json:
        """first page parser.
        
        Parses the first search page and extract it's json contents.

        uses the request_html library to parse the page_content
        and extract the json object which contains the results.
        
        Args:
            page_content (str): The HTML content of the page.

        Returns:
            response (dict): The parsed json data from the page.
        """
        parsedHtml = HTML(html= page_content)
        response = json.loads(parsedHtml.find("#__NEXT_DATA__")[0].text)
        return response
    
    @property
    def sound_alarm (self) -> None:
        """creates sound "used to alarm problems".
        """ 
        winsound.Beep(90, 100)
        winsound.Beep(1200, 100)
        winsound.Beep(1200, 100)
        winsound.Beep(1000, 300)
        winsound.Beep(900, 250)
        winsound.Beep(800, 200)    


            

        
                
        
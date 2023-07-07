"""
This module contains abstract classes for configuring headers,
making requests and parsing the first page of a website.

Classes:
    configure_headers: 
        An abstract base class for adjusting the headers and bodies for each request.
    back_end_API: 
        An abstract base class for making requests and parsing the first page of a website.
    change_headers:
        An abstract base class for updating and getting the headers, requests body(s) and urls.
    scrapers:
        this class parses the request responses and extract the need data.
"""
from abc import ABC, abstractmethod

class configure_headers(ABC):
    """configure the headers and bodies for each request made.
    
    Methods:
        primary_adjust_headers()
            Adjusts the headers for the primary stage requests.
        secondary_adjust_headers()
            Adjusts the headers for the secondary stage requests.
    """
    @abstractmethod
    def primary_adjust_headers(self):
        """used to adjusts the headers for the primary stage requests."""
        pass
    @abstractmethod
    def primary_adjust_headers(self):
        """used to adjusts the headers for the secondary stage requests."""
        pass  
       
class back_end_API(ABC):
    """used to make requests and parse the first page.
    
    Methods:
    back_end()
        requests sender.
    parse_first_page()
        first page parser.
    """
    @abstractmethod
    def back_end(self):
        """used to send requests to the website api."""
        pass
    @abstractmethod
    def parse_first_page(self):
        """used to parse the first page."""
        pass

    
class change_headers(ABC):
    """updates/gets the request headers and body(s)
    
    Methods:
        get_headers()
            used to extract the headers, requests body(s) and urls.  
    """
    @abstractmethod
    def get_headers(self):
        """used to extract the headers, requests body(s) and urls."""
        pass
        
class scrapers(ABC):
    """this class parses the request responses and extract the need
    data.
    
    Methods:
        primary():
            take the search results page responses and extract the primary data.
        secondary():
            take the result page responses and extract the secondary data.
    """
    @abstractmethod
    def primary():
            """take the search results page responses and extract the primary data."""
        
    @abstractmethod
    def secondary():
        """take the result page responses and extract the secondary data."""
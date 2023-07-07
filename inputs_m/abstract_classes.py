"""This module contains abstract classes for defining scraping
    variables and handling available pages.

Classes:
    i_handlers:
        An abstract base class for defining the essential variables for scraping.
    available_pages:
        An abstract base class for handling the available pages for scraping.
"""
from abc import ABC, abstractmethod

class i_handlers(ABC):
    """defines the essential variables for scraping.
    
    Methods:
        search_info()
            gets the search subject and location.
        record()
            reads the TXT_TRACKER file and updates the scraper attributes.
        def construct_file_name()
            creates the tracker file
    """
    @abstractmethod
    def search_info (self): 
        """gets the search subject and location."""
        pass
    @abstractmethod
    def record(self):
        """reads the TXT_TRACKER file and updates the scraper attributes."""
        pass 
    @abstractmethod       
    def construct_file_name(self):
        """creates the tracker file"""
        pass
    
class available_pages(ABC):
    """handle the available pages for scraping.
    
    Methods:
        def get_pages()
            gets the number of pages available for scraping from the page_source.
        pages_to_scrape()
            determines the number of pages to be scraped.
    """
    @abstractmethod    
    def get_pages(self):
        """gets the number of pages available for scraping from the page_source.""" 
        pass  
    @abstractmethod    
    def pages_to_scrape(self):
        """determines the number of pages to be scraped."""    
        pass
    
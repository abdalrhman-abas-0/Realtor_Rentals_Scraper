"""
This module contains a function for initiating the inputs module to 
get the key inputs necessary for scraping.

Functions:
    r_inputs(page_content: str) -> tuple[str, str, list, int, int, int, str, str, str]
        Returns the search subject, location, pages to scrape, counters, file names and date time.
"""
from inputs_m.i_handler import i_handlers_, available_pages_
from inputs_m.inputs import TXT_TRACKER

def r_inputs (page_content: str) -> tuple[str, str, list, int, int, int, str, str, str]:
    """ initiates the inputs_m module to get the key inputs necessary for scraping.

    it looks for the TXT_TRACKER file to extract the scraping record to continue 
    the previous scraping process and if a new scraping project is in hand it 
    re-configure the user inputs and create a new TXT_TRACKER file 
    to record and track the scraping process.
 
    Args:
        page_content (str): the source code for the first search result page.
        
    Returns:
        tuple[str, str, list, int, int, int, str, str, str]: a tuple of the 
            subject of which the search is being conducted,
            the location of which the search is being conducted,
            the original url of the first page,
            a soup object of the first page, 
            list of the pages that will be scraped after checking the pages
            available for a certain search on the website,
            the pages scraped count, 
            the results scraped count, 
            the number of the last saved file (primary/secondary),
            the URL of the last scraped result page, 
            the name of the .txt file which records the scraping process, 
            the beginning time of the scraping process.
    """    
    handlers_c =  i_handlers_()
    available_pages_to_scrape = available_pages_()
    handlers_c.search_info() 
    
    if TXT_TRACKER.lower() == "no":
        results_scraped, save_index, s_listing, txt_tracker, date_time = handlers_c.construct_file_name()     
    else: 
        results_scraped, save_index, s_listing, txt_tracker, date_time = handlers_c.record()
        
    page_counter = handlers_c.page_counter
    search_subject = handlers_c.search_subject
    search_location = handlers_c.search_location
    pages_available = handlers_c.pages_available
      
    available_pages_to_scrape.get_pages(txt_tracker, pages_available , page_content)  
    pages_to_scrape = available_pages_to_scrape.pages_to_scrape(page_counter)
 
    return search_subject, search_location, pages_to_scrape ,page_counter, results_scraped, save_index, s_listing, txt_tracker, date_time

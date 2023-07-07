"""
this file contains the inputs necessary for a scraping project.

Attributes:
    URL (str): the url of the first page to scrape.
    SITE_NAME (str): the name of the website being scraped.  
    WEBSITE (str): the url of the main page of the website.
    SITE_WITH_DOMAINE (str): the name of the website with it's domaine   
    PAGES_TO_SCRAPE (int): no. of pages desired to be scraped. 
    KEY_COLUMN (str): the name of the column which is unique for each result.   
    RESULT_PER_PAGE (int): determines the number of the results saved in a file.   
    TXT_TRACKER (str): the name of the .txt file that contains the record of unsuccessful scrapes, 
        enter"no" if new scraping process is desired.  
    NO_OF_RESULTS_PER_FILE (int): the no. of results per page to be saved in one file.
    RESULT_PAGE_COLUMN (str): the name of the column that will store the URLs for the secondary stage.
    LISTING_PER_PAGE (int): the number of results in a search page. 

"""

URL ="https://www.realtor.com/apartments/Austin_TX/type-single-family-home"
"""str: the url of the first page to scrape."""

SITE_NAME = 'Realtor'
"""str: the name of the website being scraped."""

SITE_WITH_DOMAINE = 'realtor.com'
"""str: the name of the website with it's domaine"""

PAGES_TO_SCRAPE = 2
"""int: no. of pages desired to be scraped."""

KEY_COLUMN = "property id"
"""str: the name of the column which is unique for each result."""  

TXT_TRACKER = "no"
"""str: the name of the .txt file that contains the record of unsuccessful scrapes, 
    enter"no" if new scraping process is desired."""

NO_OF_RESULTS_PER_FILE = 42
"""int: the no. of results per page to be saved in one file."""

RESULT_PAGE_COLUMN = "listing page"
"""str: the name of the column that will store the URLs for the secondary stage."""

LISTING_PER_PAGE = 42
"""int: the number of results in a search page."""


WEBSITE = URL[:len(URL)-len("/type-single-family-home")]
"""str: the url of the main page of the website."""

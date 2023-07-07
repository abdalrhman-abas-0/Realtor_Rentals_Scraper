""" this sub-package contains all the modules required to 
    initiate or continue a current or previous scraping process.
    
Modules:

    inputs.py
        this file contains the inputs necessary for a scraping project.
        Attributes:
            URL (str): the url of the first page to scrape.
            SITE_NAME (str): the name of the website being scraped.  
            WEBSITE (str): the url of the main page of the website.
            SITE_WITH_DOMAINE (str): the name of the website with it's domaine   
            PAGES_TO_SCRAPE (int): no. of pages desired to be scraped. 
            KEY_COLUMN (str): the name of the column which is unique for each result.   
            RESULT_PER_PAGE (int): determines the number of the results saved in a file.   
            TXT_TRACKER (str): the name of the .txt file that contains the record 
                of unsuccessful scrapes, enter"no" if new scraping process is desired.  
            NO_OF_RESULTS_PER_FILE (int): the no. of results per page to be saved in one file.
            RESULT_PAGE_COLUMN (str): the name of the column that will store the URLs 
                for the secondary stage.
            LISTING_PER_PAGE (int): the number of results in a search page.
            
    abstract_classes.py
        this module contains abstract classes for defining scraping
        variables and handling available pages.
        classes:
            i_handlers:
                An abstract base class for defining the essential variables for scraping.
            available_pages:
                An abstract base class for handling the available pages for scraping.
            
    i_handler.py
        this module is responsible for configuring all the variables
        needed to initiate the scraping process.
        classes:
            class i_handlers_(i_handlers): 
                defines the essential variables for scraping.
            available_pages_(available_pages):
                A class to handle the available pages for scraping.
        Raises:
            FileNotFoundError: If the TXT_TRACKER file is not found in the Outputs files folder.
"""


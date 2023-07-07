"""this sub-package contains all the modules which are
responsible for crawling and parsing the website being
scraped.

Modules:

    abstract_classes.py
        this module contains abstract classes for configuring headers,
        making requests and parsing the first page of a website.
        classes:
            configure_headers: 
                An abstract base class for adjusting the headers and bodies for each request.
            back_end_API: 
                An abstract base class for making requests and parsing the first page of a website.
            change_headers:
                An abstract base class for updating and getting the headers, requests body(s) and urls.
            scrapers:
                this class parses the request responses and extract the need data.
        
    headers.py
        this module navigates the website to be scraped and
        catches the post requests to get the request headers,
        body(s) needed for crawling the website.
        classes:
            change_headers_ (change_headers)
                updates/gets the request headers and body(s).
                this class inherit form the abstract class
                change_headers found in 
                scrapers_m.abstract_classes module.
    
    c_handler.py
        this module requests the website api and extract the json objects
        which contains the needed data.
        classes:
            headers_configuring(configure_headers):
                configure the headers and bodies for each request made.
            back_end_API_(back_end_API):
                requests sender to and first page parser.
    
    scraper.py
        this module contains the scraper/parser methods.
        classes:
            class scrapers_(scrapers):
                contain the scrapers methods which extract the data form the json response.  
"""


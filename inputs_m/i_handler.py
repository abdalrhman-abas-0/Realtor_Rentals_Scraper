"""this module is responsible for configuring all the variables
needed to initiate the scraping process.
    
this module uses it's classes to configure the variables needed
to start the scraping process according to the txt tracker file
found in the "Outputs files" folder when continuing an uncompleted
scraping process.

if a new scraping process is in hand then it will create a new
txt tracker file for the curring scraping process using the 
subject, location and time and date of the search.

it also sets the number of pages to be scraped according
to the number of pages available for the search on the 
site being scraped.

This script requires that `httpx_html, re` be installed within the Python
environment you are running this script in.

the classes in this module inherit form the abstract classes found in
inputs_m.abstract_classes module.

This file can also be imported as a module and contains the following

classes:
    class i_handlers_(i_handlers): 
        defines the essential variables for scraping.
    available_pages_(available_pages):
        A class to handle the available pages for scraping.

Raises:
    FileNotFoundError: If the TXT_TRACKER file is not found in the Outputs files folder.
"""
import datetime
from httpx_html import HTML
import os
import re
from inputs_m.inputs import SITE_WITH_DOMAINE, PAGES_TO_SCRAPE, URL, TXT_TRACKER, NO_OF_RESULTS_PER_FILE
from inputs_m.abstract_classes import i_handlers, available_pages

class i_handlers_(i_handlers): 
    """ defines the essential variables for scraping.
    
    it in uses inputs_m.abstract_classes.i_handlers class
    as a parent class. 
    
    this class defines the essential variable for the scraping process
    according to the txt tracker file and if it's not created yet
    (new scraping process is in hand) it will return the default values
    for some of these variables which are stored in it's class attributes
    or defined by it's methods.
    
    Attributes:
        page_counter (int): the number of the scraped pages.
        results_scraped (int): the number of the scraped results "if any".
        p_save_index (int): the number of the last saved "primary" json file.
        s_save_index (int): the number of the last saved "secondary" json file. 
        save_index (int): the number of the last saved json file.
        pages_available (int): the number of result pages available for a search.
        s_listing (str): the url of the last saved result.
        
    Methods:
        search_info() -> None
            gets the search subject and location.
        record() -> tuple[int, int, str, str, str]
            Reads the TXT_TRACKER file and updates the scraper attributes.
        def construct_file_name() -> tuple[int, int, str, str, str]
            creates the tracker file.
            
    Raises:
            FileNotFoundError: If the TXT_TRACKER file is not found in the Outputs files folder.    
    """
    
    page_counter = 0
    results_scraped = 0
    p_save_index = 0
    s_save_index = 0
    save_index = 0
    pages_available = 0
    s_listing = ""
    
    def search_info (self) -> None:
        """gets the search subject and location.
        
        This method extracts the search_subject and search_location from the URL
        and set them as a class attributes.
        """
        url = URL.replace("-", "_")
        search_subject = re.search(r"(?<=www.realtor.com/)\w+(?=/)", url)[0]
        search_location = re.sub(r"\d+", r"", url[url.index(search_subject)+ len(search_subject)+1:]).strip("_").replace("/", "-")
        
        self.search_subject = search_subject
        """search_subject (str): the subject of the scraping process."""
        self.search_location = search_location
        """search_location (str): the location of the subject scraping process."""
    
    def record(self) -> tuple[int, int, str, str, str]:
        """Reads the TXT_TRACKER file and updates the scraper attributes.

        This method reads the TXT_TRACKER file from the Outputs files folder
        and extracts information such as pages available, save index, listing,
        page counter, and date time. It then updates the corresponding attributes
        of the scraper object.

        Returns:
            self.results_scraped (int): the number of the scraped results.
            self.save_index (int): the number of the last saved json file.
            self.s_listing (str): the url of the last scraped listing.
            txt_tracker (str): the name of the txt_tracker file.
            date_time (str): the creation date of the txt_tracker file.

        Raises:
            FileNotFoundError: If the TXT_TRACKER file is not found in the Outputs files folder.
        """
        txt_tracker = TXT_TRACKER.strip(" ").lower()   
        try:
            # changing the directory to the to the finished scraped files folder   
            os.chdir('Outputs files')
            file = open(txt_tracker , 'r')
            for line in file:
                if "pages available." in line:
                    self.pages_available = int(re.search(r"\d+", line)[0])
                    
                if 'secondary' in line:
                    self.s_save_index = int(re.search(r"\d+", line)[0])
                    continue
                
                if 'primary' in line:
                    self.p_save_index = int(re.search(r"\d+", line)[0])
                    continue
                
                if "page number " in line:
                    try:
                        page_counter = int(line.strip("\n").replace("page number ",""))
                    except:
                        pass
                
                if SITE_WITH_DOMAINE in line and URL not in line:
                    self.s_listing = line.strip('\n')
                    
            self.results_scraped = self.p_save_index * NO_OF_RESULTS_PER_FILE 

            file.close()
            
            self.page_counter = page_counter
                
            date_time = re.search(r'\d{4}\-\d{2}\-\d{2}\s\d{2}\.\d{2}\.\d{2}',txt_tracker)[0]
            
            if self.s_save_index > 0:
                save_index = self.s_save_index
            else:
                save_index = self.p_save_index
                
            self.save_index = save_index + 1
            
        except FileNotFoundError :
            print(f'FileNotFoundError: TXT_TRACKER[{txt_tracker}], No such file or in "Outputs files" folder!')
            os._exit(0)
            
        finally:
            # return back to the original directory
            os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
            
        return self.results_scraped, self.save_index, self.s_listing, txt_tracker, date_time 
                
    def construct_file_name(self) -> tuple[int, int, str, str, str]:
        """creates the tracker file.
        
        constructs the tracker file name based on the search subject, 
        location and current date and time and return the default 
        values for some class attributes.

        it will also create an txt tracker file in the "Outputs files" folder
        which will be later used to track the scraping process.
        
        Returns:
            self.results_scraped (int): the number of the scraped results.
            self.save_index (int): the number of the last saved json file.
            self.s_listing (str): the url of the last scraped listing.
            txt_tracker (str): the name of the txt_tracker file.
            date_time (str): the creation date of the txt_tracker file.
        """
        # Get the current date and time as a string, without the microseconds
        date_time = str(datetime.datetime.now())[:str(datetime.datetime.now()).index('.')].replace(':', '.')
        # Format the file name with the tracker details
        txt_tracker = f'tracker {self.search_subject} in {self.search_location} at {date_time}.txt'
        # Create a new text file in the Outputs files folder and close it
        file = open("Outputs files/" + txt_tracker, 'w')
        file.close()
                
        return self.results_scraped, self.save_index, self.s_listing, txt_tracker, date_time
 
    
class available_pages_(available_pages):
    """A class to handle the available pages for scraping.
    
    it in uses inputs_m.abstract_classes.available_pages class
    as a parent class.  
     
    this class uses it's methods to get the number of available pages
    for a specific search and defines the number of pages to be scraped
    accordingly.
    
    Attributes:
        building_upon_previous (bool): A flag to indicate if the scraping 
            is continuing from a previous process.
        pages_available (int): The number of pages available for scraping. 
    
    Methods:
        def get_pages(txt_tracker: str, pages_available:int = 0, page_source:str="") -> None 
            Gets the number of pages available for scraping from the page_source.
        pages_to_scrape(page_counter:int) -> list
            determines the number of pages to be scraped.
    """
    
    def __init__(self):
        self.building_upon_previous = False
        self.pages_available = 0
           
    def get_pages(self, txt_tracker: str, pages_available:int = 0, page_source:str="") -> None: 
        """Gets the number of pages available for scraping from the page_source.

        used to extract the number of available pages for a search and assign it to 
        the pages_available class attribute, it uses the first page's source code 
        which is passed as an str and if it's not passed it the pages_available equals 1.
        
        Args:
            txt_tracker (str): The file name of the tracker.
            pages_available (int, optional): The number of pages available from a previous process
                if any, (default is 0)
            page_source (str, optional): The HTML source of the first page, 
                (Defaults is None).
        """
        if pages_available == 0:           
            if page_source == "":
                # If there is no pagination element, assume there is only one page
                self.pages_available = 1
            else:
                # Parse the HTML and find the last page number from the pagination element
                parsedHtml = HTML(html= page_source)
                self.pages_available = int(parsedHtml.find('div[aria-label="pagination"]>a')[-2].text)
                
            # Write the number of pages available to the tracker file
            result_pages = f'{self.pages_available} pages available.'
            with open("Outputs files/" + txt_tracker,'a') as f:
                f.write(f'{self.pages_available} pages available.') 
            
        else:
            # If there are pages available from a previous process, use that number and set the flag to True
            self.building_upon_previous = True
            self.pages_available = pages_available 
            result_pages = f"carrying out a previous scraping process, {pages_available} pages available."

        print(result_pages)
            
    def pages_to_scrape(self,page_counter:int) -> list:
        """determines the number of pages to be scraped
        
        creates a list of length self.pages_available, which 
        can be all the pages available for the search or just
        the number of pages defined by the user.

        Args:
            page_counter (int): The current page number in the scraping process.

        Returns:
            pages_to_scrape (list): A list of page numbers to scrape.
        """
        # If the user input is greater than the available pages, use the latter
        if PAGES_TO_SCRAPE > self.pages_available:
            pages_to_scrape = self.pages_available
        else:
            # Otherwise, use the user input
            pages_to_scrape = PAGES_TO_SCRAPE
        # Increment the number of pages to scrape by one to account for indexing
        pages_to_scrape += 1  
        # Create a list of page numbers to scrape starting from the current page counter
        pages_to_scrape = list(range(1,pages_to_scrape))[page_counter:]
        return pages_to_scrape
    
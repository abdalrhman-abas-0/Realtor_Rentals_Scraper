# **Realtor_Rentals_Scraper**

* This project is a scraper template that can perform a seamless successful scraping process even if it faced a temporary blockage from the site or in case of a power outage and it saves the outputs as JSON files.
* it's intended to work as a template suitable to be modified to work with many scraping libraries and across many sites.
* it can use many scraping libraries like BeautifulSoup, HTTPS, Selenium, and more.

# Project Structure:

* This scraper consists mainly of 3 sub-packages and 3 modules plus the run file and the Outputs files folder:

```python
Realtor_Rentals_Scraper:
│   __init__.py
│   f_crawlers.py
|   f_inputs.py
│   f_scraper.py
|   LICENSE.txt
│   README.md
│   requirements.txt
│   run.py
│
├───inputs_m
│       __init__.py
|       abstract_classes.py
│       inputs.py
│       i_handler.py
│
├───Outputs files
├───outputs_m
│       __init__.py
|       abstract_classes.py
│       o_handler.py
│
└───scrapers_m
        __init__.py
        abstract_classes.py
        headers.py
        scraper.py
        s_handler.py
```

> the "Outputs files" folder is where the out .json files and the .txt tracker file will be saved.

> the txt_tracker file is used to track and record the scraping process, it's created at the beginning of the scraping process at the "Outputs files" directory and automatically deleted when the scraping process is concluded successfully.

# Project Logic:

## The f_ modules:

- f_inputs.py:
  * initiates the inputs_m module to get the key inputs necessary for scraping.
  * it looks for the TXT_TRACKER file to extract the scraping record to continue
    the previous scraping process and if a new scraping project is in hand it
    re-configure the user inputs and create a new TXT_TRACKER file
    to record and track the scraping process.
- f_crawlers.py:
  * This module contains functions for initiating and running the crawler.
  * it uses the scrapers_m module to request the website api and return
    the JSON response which contains the desired data.
- f_scraper.py:
  * This module defines the stage from which the program will start running.
  * it contains a function that reads a text file and determines the stage
    of the scraping process based on the txt_tracker file contents.
  * it uses the os module to change the working directory and handle file paths.

## Scraping Process Stages (run.py):

### 0. pre scraping stage:

in this stage, the inputs are evaluated, and modified to suit the program and the amount of results available for a certain scraping project, then it checks if it will continue an old scrape if yes it looks for the record of the old scrape in the .txt file which is already been input by the user in the input file if not the program creates a new .txt file to record the current scraping process.

### **1. primary stage**:

the program scrapes the results from the primary pagination pages available for a search and saves them page by page in .json file.

### 2. Saving the Primary files:

in this stage the program builds a pandas DataFrame for each primary file and saves it as one main .json file then it deletes the primary .json files for each page.

### **3. secondary stage**:

this stage extracts the URLs for each result from the primary DataFrame built in the previous stage and scrapes the results one by one or as asynchronous chunks and saves the results as .json files.

### 4. Saving the Secondary files:

as stage no. 2 This stage also builds a DataFrame from these files and saves it as one .json file then it deletes all the secondary files.

### 5. Joining the DataFrames:

In this stage, the primary and secondary stages are joined and saved into one file and the .txt file, primary & secondary files are deleted.

> This stage from which the program will begin running from in case of continuing an uncompleted scraping is determined by f_scraper module after looking to the last step taken by the scraper in the .txt file which is saved in the scrapers_m sub-module and automatically erased after completion.

## Inputs module:

| Variable               | Functionality                                                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| URL                    | str: the url of the first page to scrape.                                                                                       |
| SITE_NAME              | str: the name of the website being scraped.                                                                                     |
| SITE_WITH_DOMAINE      | str: the name of the website with it's domaine.                                                                                 |
| PAGES_TO_SCRAPE        | int: no. of pages desired to be scraped.                                                                                        |
| KEY_COLUMN             | str: the name of the column which is unique for each result.
| TXT_TRACKER            | str: the name of the .txt file that contains the record of unsuccessful scrapes, enter "no" if new scraping process is desired. |
| NO_OF_RESULTS_PER_FILE | int: the no. of results per page to be saved in one file.                                                                       |
| RESULT_PAGE_COLUMN     | str: the name of the column that will store the URLs for the secondary stage.                                                   |
| LISTING_PER_PAGE       | int: the number of results in a search page.                                                                                    |

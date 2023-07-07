"""A module that runs a web scraping project to collect data from a real estate website.

This module uses the f_inputs, f_scrapers, f_crawlers, scrapers_m and outputs_m modules 
to handle the inputs, outputs and scraping tasks. It also uses the os, time and tqdm
modules to manage the file system, sleep intervals and progress bars. 
It takes the user inputs for the search subject, location, 
pages to scrape and text file name, and then initiates the crawler and scraper functions
to extract data from the website. It saves the data in text files and data frames, 
and combines the primary and secondary data frames into one final data frame.

Functions:
    main() -> None:
        The main function that runs the web scraping project.
"""

import os 
from time import sleep
from tqdm import tqdm

from f_inputs import r_inputs
from f_scraper import stage_tracker
from f_crawlers import run_crawler, initiate_crawler

from scrapers_m.scraper import scrapers_
from outputs_m.o_handler import outputs, save_data_frames_
 
from inputs_m.inputs import RESULT_PAGE_COLUMN, NO_OF_RESULTS_PER_FILE, URL, KEY_COLUMN

def main() -> None:
    """The main function that runs the web scraping project.

    This function takes no arguments and returns nothing. 
    It calls the r_inputs function to get the user inputs, 
    and then calls the stage_tracker function to determine 
    the stage of the scraping process. 
    
    Depending on the stage, it calls different functions 
    from the f_crawlers, scrapers_m and outputs_m modules 
    to crawl, scrape and save the data. 
    
    It also uses tqdm to display progress bars for each stage. 
    
    Finally, it combines the primary and secondary data frames into 
    one final data frame and prints a message indicating the 
    number of results scraped.
    
    """
    os.system('cls')
    headers = None
    
    headers, crawler_, page_content= initiate_crawler()
    
    # extracts the txt_tracker file name (saved or newly created)
    search_subject, search_location, pages_to_scrape, page_counter, results_scraped, save_index, s_listing, txt_tracker, date_time = r_inputs(page_content)
    scrape = scrapers_()
    data = outputs() 
    save = save_data_frames_(txt_tracker,search_subject, search_location,save_index)

    # initiate the stage tracker function to continue an old scraping project
    stage = stage_tracker(txt_tracker)
        
    if stage == 1 :
        site = URL   
        if len(pages_to_scrape) > 0 or page_counter == 1:
            with tqdm(total=(len(pages_to_scrape)),unit ="search page", desc ="primary scraper") as pbar:
                for page in pages_to_scrape :
                    
                    if page == 1:
                        site = URL
                        response = run_crawler(initiate_crawler, headers, crawler_, "pages", page, site, page_content)
                    else:
                        site = URL+f"/pg-{page}"
                        response = run_crawler(initiate_crawler, headers, crawler_, "pages", page, site)
                        
                    scrape.primary(response, data.results_list)
                    
                    save.lists_to_files(data.results_list, f"page number {page}", 'primary')
                    data.reset_outputs('primary')
        
                    pbar.update(1)
        
        stage += 1
        
    if stage >= 2: 
        # building the primary df to use it to scrape the secondary df
        primary_df, df_index = save.build_df('primary', RESULT_PAGE_COLUMN,s_listing)
        print(f"{len(primary_df)} primary results already scraped.")
        
        if stage == 2:
            # reset the outputs handler attributes
            data.reset_outputs()
            save.reset_save_index()
            stage += 1
                
    if stage == 3:
        
        if headers == None:
            headers, crawler_, page_content = initiate_crawler()
            
        scraping_df = primary_df[df_index:]
        listings_list = list(scraping_df[RESULT_PAGE_COLUMN])
        id_list = list(scraping_df[KEY_COLUMN])
        results_tracker = len(scraping_df)# a variable as an index can't be used to track the scraping in case of duplicated urls
        
        with tqdm(total=len(scraping_df),unit ="listing", desc ="secondary scraper") as pbar:
            for listing, id in zip(listings_list, id_list) : 
                    
                sleep(0.7)
                fire_back_end = run_crawler(initiate_crawler, headers, crawler_, "fire", id, listing)
                fire_json = scrape.secondary(fire_back_end, "fire")
                
                sleep(0.7)
                flood_back_end = run_crawler(initiate_crawler, headers, crawler_, "flood", id, listing)
                flood_json = scrape.secondary(flood_back_end, "flood")
                
                sleep(0.7)
                schools_back_end= run_crawler(initiate_crawler, headers, crawler_, "schools", id, listing)
                schools_json = scrape.secondary(schools_back_end, "schools")
                
                back_end_info = {
                    "property id":id,
                    "fire factor score":fire_json,
                    "flood factor score":flood_json,
                    "schools":schools_json
                    }
                    
                # adding the values of the back_end_info to the main listing dict
                data.results_list.append(back_end_info)  
                results_tracker -= 1  
                 
                pbar.update(1)

                if (len(data.results_list) % NO_OF_RESULTS_PER_FILE) == 0 :
                    save.lists_to_files(data.results_list, listing, 'secondary')
                    data.reset_outputs('secondary')

                if listings_list[-1] is listing and len(data.results_list) > 0:
                    save.lists_to_files(data.results_list, listing, 'secondary')
                    data.reset_outputs('secondary')

                sleep(4)

        stage += 1
    else:
        print(f'{results_scraped} secondary files are already scraped.')
        stage += 1
    
    if stage >= 4:    
        #building the primary df to use it to scrape the secondary df
        secondary_df, df_index = save.build_df('secondary', RESULT_PAGE_COLUMN, s_listing)
        print(f"{len(secondary_df)} results scraped successfully.")
        # combine the primary and secondary dataframes 
        combined = save.combine_df(primary_df, secondary_df, date_time)
        print(f'done, scraped {combined} results.')
        
    else:
        save.lists_to_files(listing, 'secondary')
        data.reset_outputs('secondary')
        print(f'error scraped {listings_list.index(listing)} of {len(listings_list)} results only.')
   
if __name__ == '__main__':
    main()          


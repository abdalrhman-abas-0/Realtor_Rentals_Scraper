"""outputs saver.

this module contains the class which manages the scraping output files. 

this module uses it's classes to store the scraped data as a list then
it constructs a dataframes from this list and save it in one or more
.json files according to the scraping process stage.

at the end of each stage it constructs a single dataframe and save 
it in one .json file

finally at the end of the scraping process it joins the .json files
constructed at the end of each scraping stage (primary, secondary) 
to save it as one .json file.

it also records the saved .json files in a txt tracker file which
can be later used to continue an incomplete scraping process,
the tracker file is created in the "Outputs files" folder and it's 
deleted ate the end of the scraping process.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

the save_data_frames class inherits form the abstract class 
save_data_frames found in outputs_m.abstract_classes module.

classes:
    outputs()
        this class contains all the methods that manages the 
        scraping outputs.
    class save_data_frames_()
        saves the scraped results in a file formate "json".
        inherits form outputs_m.abstract_classes.save_data_frames
        class.
"""
import os
import pandas as pd
from inputs_m.inputs import KEY_COLUMN
from outputs_m.abstract_classes import save_data_frames

class outputs():
    """ tracks and stores the scraped results.
    
    this class contains all the methods which stores and 
    tracks the scraped results.
        
    Attributes:
        results_scraped (int): no. of the scraped results,
            (default is 0).
        results_list (list): empty as default,it is a container 
            for the scraping outputs, (default is []).
        bot_name (str): the scraper stage name 'EX: primary',
            (default is "").
    Methods:
        reset_outputs (bot_name:str = "") -> None
            empty the outputs list & zero out the results_scraped.
        count_results () -> None
            tracks the scraped results count.
    """    
    results_scraped = 0
    results_list = []
    bot_name = ""
        
    def reset_outputs (self, bot_name:str = "") -> None:
        """ empty the outputs list & zero out the results_scraped.
            
        it will empty the results_list, assign the bot_name to
        self.bot_name and zero out the self.results_scraped 
        if the bot_name is an empty string.
            
        Args:
            bot_name (str, optional): the scraper stage name 'EX: primary', 
                (default is []).
        """        
        self.bot_name = bot_name
        self.results_list = []
        
        if self.bot_name == "":
            self.results_scraped = 0
            
    def count_results (self) -> None:
        """tracks the scraped results count.
        
        adds the length of the self.results_list to the self.results scraped
        attribute.
        """
        self.results_scraped += len(self.results_list) 
            
            
class save_data_frames_(save_data_frames):
    """saves the scraped results in a file formate EX:json, csv.

    this class uses it's methods to construct dataframes from 
    the scraped results list passed into it's methods (lists_to_files)
    then save it as .json files according to the scraping stage 
    (primary, secondary) and writes the saved files in the 
    txt tracker file which is saved in the "Outputs files" folder.
    
    it's also concatenates the individually saved .jon files at the end
    of each scraping stage (EX:primary)stage into one file.
    
    at the end of the scraping process it combines the single file
    saved at the end of the primary and secondary stages and
    save it in one file.
    
    any file saved it's recorded in the txt tracker file in the 
    "Outputs files" folder which can be used to continue an uncompleted
    scraping process, the txt tracker file is deleted at the 
    end of the scraping process.
    
    Attributes:
        txt_tracker (str): the name of the .txt file which contains a record 
            of the scraping process.
        search_subject(str): the subject of the search.
        search_location(str): the location of the search.
        save_index (int, optional): the number of the saved files,
            (default is 0).
    
    Methods:
        lists_to_files(results_list:list ,site:str , bot_name: str) -> None
            this method saves the contents of the results_list in .json files.
        reset_save_index() -> None
            zero out the save index.
        def build_df (bot_name: str, result_page_column: str, s_listing:str="") -> tuple[pd.core.frame.DataFrame, int]
            joins multiple dataframes which are constructed for multiple .json files.
        def combine_df (primary_df: pd.DataFrame, secondary_df: pd.DataFrame, date_time:str) -> int
            combines the primary and secondary dataframes to get the final .json file. 
    """  

    def __init__(self, txt_tracker: str, search_subject: str, search_location: str, save_index= 0):        
        assert save_index >= 0 , 'save index is less than 0 !!'
        self.save_index = save_index
        self.txt_tracker = txt_tracker
        self.search_subject = search_subject
        self.search_location = search_location
        
    def reset_save_index(self) -> None:
        """zero out the save index."""
        self.save_index = 0      
           
    def lists_to_files(self, results_list:list ,site:str , bot_name: str) -> None:
        """ this method saves the contents of the results_list in .json files.
        
        this method construct dataframes from the scraped results list 
        passed then save it as .json files according to the scraping stage
        "bot_name"(EX: primary, secondary), and writes the saved files 
        in the txt tracker file which is saved in the "Outputs files" folder.
        
        it will save the .json files in '"Outputs files" folder' file 
        and writes the saved files in the txt tracker file which
        is saved in the "Outputs files" folder.
            
        Args:
            results_list (list): list of dicts of each scraped result.
            site (str): the URL of the last page scraped successfully.
            bot_name (str): the scraping stage name 'EX: primary/secondary'.
        """        
              
        # changing the directory to the to the finished scraped files folder   
        os.chdir('Outputs files')    
        
        df = pd.DataFrame(results_list)
        
        df.to_json(f"realtor  {self.search_subject} in {self.search_location} {self.save_index} {bot_name}.json", orient = None)
        
        try:
            file = open((self.txt_tracker),'a') 
        except:
            file = open((self.txt_tracker),'w') 
                  
        file.write('\n')
        file.write (f"realtor  {self.search_subject} in {self.search_location} {self.save_index} {bot_name}.json") 
        file.write('\n')
        file.write(F'{site}')   
        file.close() 
        
        self.save_index +=  1
        
        # navigating back to the original directory
        os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))


        

    def build_df (self, bot_name: str, result_page_column: str, s_listing:str="") -> tuple[pd.core.frame.DataFrame, int]:
        """ joins multiple dataframes which are constructed for multiple .json files.
        
        it searches the txt tracker file for the scraped .json files for 
        a scraping stage 'EX: primary' and concatenate it into one DataFrame
        and saves it as a .json file then it returns the pandas DataFrame 
        and the number of the last concatenated sub-.json file.
         
        it writes the saved files in the txt tracker file which 
        is saved in the "Outputs files" folder. 

        it deletes the individual .json file of each stage after 
        saving their contents in one .json file.
        
        Args:
            bot_name (str): the scraping stage name 'EX: primary/secondary'.
            result_page_column (str): the column which contains the url for
                each result page.
            s_listing (str, optional): the url of the last scraped result,
                (default is "").

        Returns:
            df (pandas.DataFrame): data frame of the concatenated main file.
            df_index (int): the number of the last page scraped successfully.
        """        
        df_index = 0 

        # concatenating all the Secondary dataframes to one data frame
        # changing the directory to the to the finished scraped files folder   
        os.chdir('Outputs files')
        
        file = open(self.txt_tracker,'r')
        
        if bot_name.upper() in file.read():
            # constructing a dataframe out of the maine files if it's jason is already saved
            # the file must be closed and reopened in order to execute any code under the if condition
            file.close()
            file = open(self.txt_tracker,'r')    
            for line in file :
                if bot_name.upper() in line:
                    main_json = line.strip('\n')
                    df = pd.read_json(main_json)

        else:
            # the file must be closed and reopened in order to execute any code under the if condition
            file.close() 
            file = open(self.txt_tracker,'r')     
            for line in file: 
                J_file = line.strip('\n')
                if f'{bot_name}.json' in line:
                    if  f' 0 {bot_name}.json' in line:
                        df0 = pd.read_json(J_file)
                        continue
                    try: 
                        df = pd.concat([df0, pd.read_json(J_file)], axis=0, ignore_index= True)
                        df0 = df 
                    except:
                        pass
                    df = df0
            df = df0
          
        if KEY_COLUMN in df.columns:  
            df.drop_duplicates(subset= [KEY_COLUMN], inplace= True)

        # saving the main file and appending it's name in the txt file in upper case
        df.to_json(f"realtor {bot_name.upper()} {self.search_subject} in {self.search_location}.json", orient = None)
        file = open(self.txt_tracker,'a')            
        file.write('\n')
        file.write (f"realtor {bot_name.upper()} {self.search_subject} in {self.search_location}.json")  
        file.close() 
    
        # deleting all the concatenated {bot_name} data frames
        file = open(self.txt_tracker,'r')
        for line in file:
            if f'{bot_name}' in line:
                try:
                    os.remove(line.strip('\n'))
                except:
                    pass
        file.close()
        
        # navigating back to the original directory
        os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
        
        if s_listing and bot_name == 'primary': # incase of resuming an old project
            df_index = int(df[result_page_column][df[result_page_column] == s_listing].index[0]) + 1
               
        return df, df_index 

        
    def combine_df (self, primary_df: pd.DataFrame, secondary_df: pd.DataFrame, date_time:str) -> int:
        """combines the primary and secondary dataframes to get the final .json file. 
        
        it uses the txt tracker file to read the scraped .json files and
        an the end it deletes it from the "Outputs files" folder.
        
        it deletes the .json file constructed at the end of each stage 
        after saving their contents in one .json file.
         
        Args:
            primary_df (pd.DataFrame): the results DataFrame of the primary stage.
            secondary_df (pd.DataFrame): the results DataFrame of the secondary stage.
            date_time (str): the date of the beginning of the scraping process.

        Returns:
            df_length(int): the length of the merged DataFrame.
        """         
        os.chdir('Outputs files') 
                
        file = open(self.txt_tracker,'r')
           
        df_combined = pd.merge(primary_df,secondary_df, on=[KEY_COLUMN, KEY_COLUMN])   
        df_combined.to_json(f"Realtor {self.search_subject} in {self.search_location} at {date_time}.json", orient = None)
        
        # deleting all the concatenated {bot_name} data frames
        # EX: primary .json files saved
        file = open(self.txt_tracker,'r')
        for line in file:
            try:
                os.remove(line.strip('\n'))
            except:
                pass
        file.close()
        
        # deleting the txt_tracker file it self after saving the final output file
        os.remove(self.txt_tracker)
        
        os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
        df_length = len(df_combined)
        return df_length  
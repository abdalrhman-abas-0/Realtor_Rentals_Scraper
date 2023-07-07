"""
This module contains an abstract class for saving the scraped results in 
different file formats.

Classes:
    save_data_frames:
        An abstract base class for saving the scraped results in a 
        file formate like "json, csv, etc".
"""
from abc import ABC, abstractclassmethod

class save_data_frames(ABC):
    """saves the scraped results in a file formate like "json, csv, etc".
    
    Methods:
        lists_to_files()
            saves the contents of the results_list in files.
        reset_save_index()
            zero out the save index.
        def build_df ()
            joins multiple dataframes which are constructed for multiple files.
        def combine_df ()
            combines the primary and secondary dataframes to get the final file. 
    """ 
    @abstractclassmethod
    def lists_to_files(self):
        """saves the contents of the results_list in files."""
        pass
    @abstractclassmethod
    def reset_save_index(self):
        """zero out the save index used to name the save files."""
        pass
    @abstractclassmethod
    def build_df (self):
        """joins multiple dataframes which are constructed for multiple files."""
        pass
    @abstractclassmethod    
    def combine_df (self):
        """combines the primary and secondary dataframes to get the final file."""
        pass
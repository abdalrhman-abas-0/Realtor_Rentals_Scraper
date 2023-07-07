"""this sub-package contains all the modules which are concerned 
    with handling and saving the scraped data.
    
Module:
    o_handler.py
        This module contains an abstract class for saving the scraped results in 
        different file formats.
        classes:
            outputs()
                this class contains all the methods that manages the 
                scraping outputs.
            class save_data_frames_()
                saves the scraped results in a file formate "json".
                inherits form outputs_m.abstract_classes.save_data_frames
                class.
    
    abstract_classes.py
        This module contains an abstract class for saving the scraped results in 
        different file formats.
        classes:
            save_data_frames:
                An abstract base class for saving the scraped results in a 
                file formate like "json, csv, etc".
    
"""


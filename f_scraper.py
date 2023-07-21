"""this module defines the stage from which the program will start running.

it contains a function that reads a text file and determines the stage
of the scraping process based on the txt_tracker file contents.
it uses the os module to change the working directory and handle file paths.

Functions:
    stage_tracker(txt_tracker: str) -> 
        defined the stage from which the program will start running.
"""

import os

def stage_tracker(txt_tracker: str) -> int:
    """ defined the stage from which the program will start running.
    
    it defines the stage from which the program will run after looking to the 
    recorded steps in the txt_tracker file name and will start the scraping 
    process accordingly.
        
    Args:
        txt_tracker (str): a return of the r_inputs function in the f_inputs module.
            it's defaults to "no" if a new scraping project is initiated.
            
    Returns:
        int: defines the stage from which the program will start running.
    """    
    os.chdir('Outputs files')
    stage = 0

    try: 
        file = open(txt_tracker,'r').read()
        stage = 0
        
        if 'SECONDARY' in file:
            stage = 4
        
        elif 'secondary' in file:
            stage = 3
        
        elif 'PRIMARY' in file:
            stage = 2
            
        # 'primary' in file content or the txt_tracker file is 
        # empty just been created for a the new scraping
        # process in hand.   
        else:
            stage = 1  

    except:
        print(f'{txt_tracker} is not located in "Outputs files"!!')
            
    os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
    
    return stage

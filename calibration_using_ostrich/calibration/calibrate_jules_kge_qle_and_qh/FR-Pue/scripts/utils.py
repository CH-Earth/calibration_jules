import os
import glob
from pathlib import Path


# Function to extract a given setting from the control file
def read_from_control( file, setting ):
    
    # Open 'control_active.txt' and ...
    with open(file) as contents:
        for line in contents:
            
            # ... find the line with the requested setting
            if setting in line and not line.startswith('#'):
                break
    
    # Extract the setting's value
    substring = line.split('|',1)[1]      # Remove the setting's name (split into 2 based on '|', keep only 2nd part)
    substring = substring.split('#',1)[0] # Remove comments, does nothing if no '#' is found
    substring = substring.strip()         # Remove leading and trailing whitespace, tabs, newlines
       
    # Return this value    
    return substring


def check_create_folder(userpath):
    # Ensure userpath is a valid path object
    try:
        path = Path(userpath)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            #print(f"Directory created at: {path}")
        else:
            #print(f"Directory already exists: {path}")
            pass
        return path
    except (PermissionError, OSError) as e:
        #print(f"Error creating directory: {e}")
        return None
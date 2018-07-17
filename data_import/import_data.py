# -*- coding: utf-8 -*-
"""
Import generated data
"""

import json
from pathlib import Path

def get_json_files_in_directory(directory):
    """
    Returns all the json files in the directory
    """
    path = Path(directory)
    json_files = [json_file for json_file in path.iterdir() if json_file.suffix == ".json"]
    
    return json_files

def from_json_string(string):
    """
    Returns an experiment's data from the given json string
    """
    return json.loads(string)
    
    
def from_json_file(path):
    """
    Returns the experiment data from the json file at the given path
    """
    with open(path) as file:
        data = json.load(file)
    return data
    

def from_directory(directory, add_directory_to_image_path=True):
    """
    Returns a list of all experiment data in the given directory
    """
    data = []
    for file in get_json_files_in_directory(directory):
        data.append(from_json_string(file.read_text()))
        
        if add_directory_to_image_path:
            # Add the filepath
            for i in range(len(data[-1]['imageFiles'])):
                data[-1]['imageFiles'][i] = "{}{}".format(directory, data[-1]['imageFiles'][i])
            
        
    return data
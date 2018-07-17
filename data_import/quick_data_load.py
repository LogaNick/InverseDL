# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 11:21:16 2018

@author: codej
"""

from import_data import from_directory
from convert_data import convert_data_to_tensors

def get_examples_labels_from_directory(directory="data/experiment_0/",
                                       quantize=True,
                                       one_hot=True):
    data = from_directory(directory)
    
    examples = convert_data_to_tensors(data)
    labels = convert_data_to_tensors(data, [], ["translation"], quantize=quantize,
                                     one_hot=one_hot)
    
    return examples, labels
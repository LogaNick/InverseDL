# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 11:21:16 2018

@author: codej
"""

from import_data import from_directory
from convert_data import convert_data_to_tensors

data = from_directory("data/experiment_0/")

examples = convert_data_to_tensors(data)
labels = convert_data_to_tensors(data, [], ["translation"])
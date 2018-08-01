# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 11:21:16 2018

@author: codej
"""
from data_import.import_data import from_directory
from data_import.convert_data import convert_data_to_tensors, write_tfrecord

def get_examples_labels_from_directory(directory="data_import/data/experiment_0/",
                                       quantize=True,
                                       one_hot=True):
    data = from_directory(directory)
    
    examples = convert_data_to_tensors(data)
    labels = convert_data_to_tensors(data, [], ["translation"], quantize=quantize,
                                     one_hot=one_hot)
    
    return examples, labels

def create_tfrecord(directory="data_import/data/experiment_0/",
                    output_filename="train.tfrecords",
                    quantize=True,
                    one_hot=True,
                    record_bound_divisions=[4],
                    object_records=["translation"],
                    combine_labels=True):
    
    data = from_directory(directory)
    write_tfrecord(data, output_filename,  object_records=object_records,
                                           quantize=quantize, 
                                           one_hot=one_hot,
                                           record_bound_divisions=record_bound_divisions)
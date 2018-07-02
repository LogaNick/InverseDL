# -*- coding: utf-8 -*-
"""
Converts json files to usable data for our models
"""
import tensorflow as tf
import sys
sys.path.append('..')

# Maybe look into using queues?


def decode_image(image_filename):
    """
    Creates the tensorflow representation of the image
    
    See this: https://stackoverflow.com/questions/34340489/tensorflow-read-images-with-labels
    ^ Includes using queues
    """
    file_contents = tf.read_file(image_filename)
    return tf.image.decode_image(file_contents)

def convert_to_tf_variable(vector, name=None, dtype=tf.float32):
    tf.variable(dtype=dtype, )

def convert_data_to_tensors(data, fields=["imageFiles$0"], conversion_functions=[decode_image]):
    """
    Converts a list of data (as imported by import_data) to a list of
    tensor lists (for each field in fields)
    
    Each field in fields is split on $. The parts are then used to as keys
    or indices to the dicts/lists in the data object
    """
    
    # If conversion_functions isn't full, extend with Nones
    conversion_functions.extend([None] * (len(fields) - len(conversion_functions)))
    
    converted_data = []
    
    all_split_fields = []
    for field in fields:
        # Split the fields
        all_split_fields.append(field.split("$"))
    
    for datum in data:
        converted_datum = []
        
        current_datum_property = datum
        
        for split_fields, conversion_function in zip(all_split_fields, conversion_functions):
            for split_field in split_fields:
                key_index = None
                # Going to try to store an int for indexes, otherwise it's a key (string)
                try:
                    key_index = int(split_field)
                except ValueError:
                    key_index = split_field
                
                current_datum_property = current_datum_property[key_index]
                
            converted = current_datum_property[key_index]
            
            if conversion_function is not None:
                converted = conversion_function(converted)
            else:
                """"""
            
            converted_datum.append()
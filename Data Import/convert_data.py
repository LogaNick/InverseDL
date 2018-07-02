# -*- coding: utf-8 -*-
"""
Converts json files to usable data for our models
"""
import tensorflow as tf
import numpy as np

# Maybe look into using queues?


def decode_image(image_filename):
    """
    Creates the tensorflow representation of the image
    
    See this: https://stackoverflow.com/questions/34340489/tensorflow-read-images-with-labels
    ^ Includes using queues
    """
    file_contents = tf.read_file(image_filename)
    return tf.image.decode_image(file_contents)

def decode_object_record(record_name, record_data):
    """
    Creates the tensorflow representation of the given record_name
    
    record_name is a string representing the name of the record (in the json file)
    record_data is the dictionary that was retrieved from the json file
    """
    if record_name is "name":
        # This is a string (and not a dictionary)
        return record_data
    elif record_name is "translation" or record_name is "eulerAngles" or \
        record_name is "scale":
        # Translation, eulerAngles, and scale are all 3-dimensional vectors
        return [record_data['x'], record_data['y'], record_data['z']]
    elif record_name is "quaternion":
        # A quaternion is 4 dimensional
        return [record_data['x'], record_data['y'], record_data['z'], record_data['w']]
    elif record_name is "translationMatrix" or record_name is "rotationMatrix" or \
        record_name is "scaleMatrix" or record_name is "transformationMatrix":
        # A 4x4 matrix (this may need to be transposed)
        return np.matrix("""
                         {} {} {} {};
                         {} {} {} {};
                         {} {} {} {};
                         {} {} {} {}""".format(
                         record_data['e00'], record_data['e01'], record_data['e02'], record_data['e03'],
                         record_data['e10'], record_data['e11'], record_data['e12'], record_data['e13'],
                         record_data['e20'], record_data['e21'], record_data['e22'], record_data['e23'],
                         record_data['e30'], record_data['e31'], record_data['e32'], record_data['e33']))
        
        
def convert_to_tf_variable(vector, name=None, dtype=tf.float32):
    tf.variable(dtype=dtype, )

def convert_data_to_tensors(data, image_indices=[0], object_records=[]):
    """
    Converts a list of data (as imported by import_data) to a list of
    tensor lists (for each field in fields)

    """
    converted_data = []
    
    for datum in data:
        converted_datum = []
    
        for image_index in image_indices:
            converted_datum.append(decode_image(image_filename=datum['imageFiles'][image_index]))
        
        # Add in all the object records with the given name (may want to only specify certain indices in the future)
        for object_record in datum['objectRecords']:
            for object_record_key in object_records:
                converted_datum.append(decode_object_record(object_record, object_record[object_record_key]))
                
        converted_data.append(converted_datum)
        
    return converted_data
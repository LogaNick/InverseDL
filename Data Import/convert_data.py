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
    
    See https://www.tensorflow.org/programmers_guide/datasets "Reading input data"
    for issues with this for large datasets
    """
    return tf.convert_to_tensor(get_convertable_object_record(record_name, record_data))
    
def get_convertable_object_record(record_name, record_data):
    """
    Takes record_data[record_name] and makes it convertable to a tensor
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
        
    print("Could not return {} from {}".format(record_name, record_data))
    
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
        
        # Add in all the object records with the given name 
        # TODO: (may want to only specify certain indices in the future)
        for object_record in datum['objectRecords']:
            for object_record_key in object_records:
                # Get the record as a tensorflow readable value, then convert
                # it to a tensor
                converted_datum.append(decode_object_record(object_record_key, object_record[object_record_key]))
                
        converted_data.append(converted_datum)
        
    return converted_data

def write_tfrecord(examples, labels, output_filename="train.tfrecords"):
    """
    Writes a tensorflow record to outpu_filename using the examples and labels
    
    See https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/how_tos/reading_data/convert_to_records.py
    and http://machinelearninguru.com/deep_learning/tensorflow/basics/tfrecord/tfrecord.html
    and https://medium.com/mostly-ai/tensorflow-records-what-they-are-and-how-to-use-them-c46bc4bbb564
    """
    with tf.python_io.TFRecordWriter(output_filename) as writer:
        for example, label in zip(examples, labels):
            # Create a feature dictionary
            feature = {"example" : example, "label" : label}
            
            tf_example = tf.train.Example(features=tf.train.Features(feature=feature))
            
            writer.write(tf_example.SerializeToString())
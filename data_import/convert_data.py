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

def get_image_bytes(image_filename):
    x = None
    with open(image_filename, 'rb') as f:
        x = f.read()
    
    return x

def decode_object_record(record_name, 
                         record_data, 
                         quantize=True,
                         record_bounds=None,
                         record_bound_divisions=4,
                         one_hot=True,
                         convert_to_tensor=True):
    """
    Creates the tensorflow representation of the given record_name
    
    record_name is a string representing the name of the record (in the json file)
    record_data is the dictionary that was retrieved from the json file
    
    See https://www.tensorflow.org/programmers_guide/datasets "Reading input data"
    for issues with this for large datasets
    """
    converted_object_record = get_convertable_object_record(record_name, record_data)
    
    if quantize:
        if record_bounds is None:
            record_bounds, order = get_record_bounds(record_name, record_bound_divisions)
        converted_object_record = quantize_data(converted_object_record, record_bounds, order)
        
        if one_hot:
            converted_object_record = make_one_hot(converted_object_record, record_bound_divisions)
        else:
            # Make the scalar a list for tensorflow
            converted_object_record = [converted_object_record]
        
    if convert_to_tensor:
        converted_object_record = tf.convert_to_tensor(converted_object_record)
    
    return converted_object_record

def make_one_hot(data, classes):
    """
    Takes the given data (which should be an int between 0 and classes - 1),
    and makes it a one-hot vector
    """
    one_hot = [*[0] * classes]
    if data < classes and data >= 0:
        one_hot[data] = 1
        
    return one_hot

def quantize_data(data, record_bounds, order=None):
    """
    Divides the data. Goes through each point in record_bounds. If each dimension
    of data is smaller than the first point, it's in class 0, if not checks the
    next point (if it's smaller in each dimension than that, then class 1), and
    so on. Will default to class -1 if it's outside the bounds specified
    """
    
    if order is not None:
        # Re-arrange the dimensions of the data
        data = np.array(data)[order]
    
    for i in range(len(record_bounds)):
        boundary_point = record_bounds[i]
        out_of_bounds = False
        for j in range(len(boundary_point)):
            if np.around(data[j], 4) > boundary_point[j]:
                out_of_bounds = True
                break
        
        if out_of_bounds:
            continue
        
        return i
    
    
    print("Could not place {} into bounds {}".format(data, record_bounds))
    
    return i

def get_rotation_order(rotation_axis):
    order = [0, 1, 2] # rotX
    if rotation_axis is "rotY":
        order = [1, 0, 2] # Second and third order doesn't matter?
    elif rotation_axis is "rotZ":
        order = [2, 0, 1] # Again, not sure if second and third order matter
    
    return order

def get_record_bounds(record_name, divisions=4, rotation_axis="rotY"):
    """
    Returns the bounds that will be used to separate the record_name into
    quantized parts. Also returns the order of the dimensions the bound array
    represents (ie: a bounds of [0, 5] with an order [1, 0] means y is
    sampled first, then x). An order of None means there is no change in the
    order of the dimensions (dimension 0 is dimension 0, 1 is 1, etc)
    """
    order = None
    if record_name is "translation":
        min_bounds = [-5, -5]
        max_bounds = [5, 5]
    elif record_name is "eulerAngles":
        min_bounds = [0]
        max_bounds = [360]
        order = get_rotation_order(rotation_axis)
    else:
        pass
    
    bounds_length = len(min_bounds)
    
    num_increments_per_dimension = int(pow(divisions, 1 / bounds_length))
    increment_value = (np.array(max_bounds) - np.array(min_bounds)) / num_increments_per_dimension
    
    # This is the furthest point "left" in each dimension. Anything that is less than this in each dimension is in class 0
    start_bounds = min_bounds + increment_value
    
    bounds = []
    
    # I think of this like a bit array, except the number of digits per bit
    # is determined by num_increments_per_dimension. So 2 increments per dimension
    # is binary, 3 is trinary, etc...
    current_increment_index = [*[0] * len(min_bounds)]
    
    for i in range(divisions):
        bound = start_bounds.copy()
        for j in range(len(current_increment_index)):
            bound[j] = bound[j] + current_increment_index[j] * increment_value[j]
        
        bounds.append(bound)
        
        # Increment the current_increment_index, do rollovers
        for k in range(len(current_increment_index)):
            current_increment_index[k] = current_increment_index[k] + 1
            if current_increment_index[k] >= num_increments_per_dimension:
                current_increment_index[k] = 0
            else:
                break
        
    return bounds, order

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

def get_raw_images(data, image_indices=[0]):
    converted_data = []
    
    for datum in data:
        converted_datum = []
    
        for image_index in image_indices:
            # Decode image
            image = get_image_bytes(datum['imageFiles'][image_index])
            
            converted_datum.append(image)
        
        converted_data.append(converted_datum)
    
    return converted_data

def get_examples(data, object_records=["translation"], quantize=True, 
                 one_hot=True, convert_to_tensor=False, record_bound_divisions=[4]):
    """
    Cutting up convert_data_to_tensors, this will gather the examples without
    any images
    """
    converted_data = []
    
    for datum in data:
        converted_datum = []
        # Add in all the object records with the given name 
        # TODO: (may want to only specify certain indices in the future)
        for object_record in datum['objectRecords']:
            idx = 0 # For determining which divisions to look at
            for object_record_key in object_records:
                # Get the record as a tensorflow readable value, then convert
                # it to a tensor
                converted_datum.append(decode_object_record(object_record_key, object_record[object_record_key],
                                                            quantize=quantize, 
                                                            one_hot=one_hot,
                                                            convert_to_tensor=convert_to_tensor,
                                                            record_bound_divisions=record_bound_divisions[idx]))
                
                idx = idx + 1
                
        converted_data.append(converted_datum)
        
    return converted_data

def convert_data_to_tensors(data, image_indices=[0], object_records=[],
                            quantize=True, one_hot=True, image_size=[32, 32, 3]):
    """
    Converts a list of data (as imported by import_data) to a list of
    tensor lists (for each field in fields)

    """
    converted_data = []
    
    for datum in data:
        converted_datum = []
    
        for image_index in image_indices:
            # Decode image
            image = decode_image(image_filename=datum['imageFiles'][image_index])
            # Reshape image so we have its size defined
            image.set_shape(image_size)#tf.image.resize_image_with_crop_or_pad(image, image_size[0], image_size[1])
            
            converted_datum.append(image)
        
        # Add in all the object records with the given name 
        # TODO: (may want to only specify certain indices in the future)
        for object_record in datum['objectRecords']:
            for object_record_key in object_records:
                # Get the record as a tensorflow readable value, then convert
                # it to a tensor
                converted_datum.append(decode_object_record(object_record_key, object_record[object_record_key],
                                                            quantize=quantize, 
                                                            one_hot=one_hot))
                
        converted_data.append(converted_datum)
        
    return converted_data

def multiply_list_with_previous_sublist(list_of_numbers):
    """
    Returns [1, l_0 , l_1 * l_0, ...]
    """
    multiplied_list = []
    for idx in range(len(list_of_numbers)):
        multiplied = 1
        for j in range(idx):
            multiplied = multiplied * list_of_numbers[j]
        multiplied_list.append(multiplied)
    
    return multiplied_list
        

def get_combined_labels(labels, record_bound_divisions):
    combined_labels = []
    # Get a nice representation of each of the values we have to multiply each
    # dimension by to add together for a combined label
    multiplied_list = multiply_list_with_previous_sublist(record_bound_divisions)
    
    for label in labels:
        label = np.squeeze(label)
       
        # Sometimes squeeze will make us a scalar, so this is a quick hack
        # to make us a list again
        try:
            len(label)
        except:
            label = [label]
        
        new_label = 0
        for idx in range(len(record_bound_divisions)):
            new_label = new_label + multiplied_list[idx] * label[idx]
        combined_labels.append(new_label)
        
    return combined_labels

def write_tfrecord(data, output_filename="train.tfrecords", 
                   object_records=["translation"], quantize=True, 
                   one_hot=True, convert_to_tensor=False, record_bound_divisions=[4],
                   combine_labels=True):
    """
    Writes a tensorflow record to output_filename using the examples and labels
    
    See https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/how_tos/reading_data/convert_to_records.py
    and http://machinelearninguru.com/deep_learning/tensorflow/basics/tfrecord/tfrecord.html
    and https://medium.com/mostly-ai/tensorflow-records-what-they-are-and-how-to-use-them-c46bc4bbb564
    """
    examples = get_raw_images(data)
    labels = get_examples(data, object_records, quantize, one_hot, record_bound_divisions=record_bound_divisions)
    
    if combine_labels:
        labels = get_combined_labels(labels, record_bound_divisions)
    
    with tf.python_io.TFRecordWriter(output_filename) as writer:
        for example, label in zip(examples, labels):
            # Create a feature dictionary
            feature = {
                        "example" : tf.train.Feature(bytes_list=tf.train.BytesList(value=example)),
                        "label" :  tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
                       }
            
            tf_example = tf.train.Example(features=tf.train.Features(feature=feature))
            
            writer.write(tf_example.SerializeToString())

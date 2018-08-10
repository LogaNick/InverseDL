# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 14:51:45 2018

@author: codej
"""

import tensorflow as tf

i = 0
l = []

cache_poses = True
poses = []

for example in tf.python_io.tf_record_iterator("test.tfrecords"):
    i = i + 1
    result = tf.train.Example.FromString(example)
    l.append(result.features.feature['label'].int64_list.value[0])
    
    if cache_poses:
        poses.append(result.features.feature['pose'].float_list.value)

print(i)

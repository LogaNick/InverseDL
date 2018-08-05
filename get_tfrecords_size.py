# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 14:51:45 2018

@author: codej
"""

import tensorflow as tf

i = 0
l = []

for example in tf.python_io.tf_record_iterator("train.tfrecords"):
    i = i + 1
    result = tf.train.Example.FromString(example)
    l.append(result.features.feature['label'].int64_list.value[0])

print(i)

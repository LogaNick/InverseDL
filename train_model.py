# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 14:11:10 2018

@author: codej
"""

from data_import.quick_data_load import get_examples_labels_from_directory
import Models.MatrixCapsulesEMTensorflow as capsule
import Models.MatrixCapsulesEMTensorflow.config
import Models.MatrixCapsulesEMTensorflow.train as train

#examples, labels = get_examples_labels_from_directory("data_import/data/experiment_0/")

train.main([None, "rotation_8"])
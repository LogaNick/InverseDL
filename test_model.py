# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 14:11:10 2018

@author: codej
"""

import Models.MatrixCapsulesEMTensorflow as capsule
import Models.MatrixCapsulesEMTensorflow.config
import Models.MatrixCapsulesEMTensorflow.test_2 as test

#examples, labels = get_examples_labels_from_directory("data_import/data/experiment_0/")

test.main([None, "animals_pose"])

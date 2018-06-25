# -*- coding: utf-8 -*-
"""
Converts json files to usable data for our models
"""

import tensorflow as tf


def decode_image(directory, image_filename):
    """
    Creates the tensorflow representation of the image
    """
    return tf.image.decode_image("{}/{}".format(directory, image_filename))
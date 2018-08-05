import tensorflow as tf 
import scipy.misc
import os
import argparse
import cv2

from Models.MatrixCapsulesEMTensorflow.config import cfg

# Specify the TEST_LOGDIR first
TEST_LOGDIR = os.path.join('test_logdir', 'caps', 'smallNORB', 'test_log')

EXPORT_DIR = './export_dir'
# Original images directory and Reconstructed images directory
original_dir = os.path.join(EXPORT_DIR, 'original')
reconstructed_dir = os.path.join(EXPORT_DIR, 'reconstructed')



def save_from_ckpt_to_imgs():
    assert(os.path.isdir(TEST_LOGDIR))

    # Declare a image decoder so that we can decode binary format images later
    image_str = tf.placeholder(tf.string)
    im_tf = tf.image.decode_image(image_str)

    # Create output image directory
    if not os.path.exists(EXPORT_DIR):
        # Create directories if not exist
        if not os.path.exists(original_dir):
            os.makedirs(original_dir)
        if not os.path.exists(reconstructed_dir):
            os.makedirs(reconstructed_dir)

    # Get all the event files' paths
    event_file_paths = [os.path.join(TEST_LOGDIR, filename) for filename in os.listdir(TEST_LOGDIR) if os.path.isfile(os.path.join(TEST_LOGDIR, filename))]

    # Image counters
    original_img_counter = 0
    reconstructed_img_counter = 0

    # Iterate every event file and export the images
    for event_file_path in event_file_paths:
        for e in tf.train.summary_iterator(event_file_path):
            for v in e.summary.value:
                # print(v)
                with tf.Session() as sess:
                    for i in range(cfg.max_outputs):
                        if v.tag == os.path.join('decoder/original_image/image', str(i)):
                            # im = im_tf.eval({image_str: v.image.encoded_image_string})
                            im = sess.run(im_tf, {image_str: v.image.encoded_image_string})
                            output_path = os.path.join(original_dir, 'ori_{}.jpg'.format(str(original_img_counter)))
                            print("Saving '{}'".format(output_path))
                            cv2.imwrite(output_path, im)
                            
                            original_img_counter = original_img_counter + 1

                        if v.tag == os.path.join('decoder/reconstructed_image/image', str(i)):
                            im = sess.run(im_tf, {image_str: v.image.encoded_image_string})
                            output_path = os.path.join(reconstructed_dir, 'rec_{}.jpg'.format(str(reconstructed_img_counter)))
                            print("Saving '{}'".format(output_path))
                            cv2.imwrite(output_path, im)

                            reconstructed_img_counter = reconstructed_img_counter + 1
if __name__ == '__main__':
    save_from_ckpt_to_imgs()
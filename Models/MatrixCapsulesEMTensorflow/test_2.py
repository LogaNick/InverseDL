"""
License: Apache-2.0
Author: Suofei Zhang | Hang Yu | Xu
E-mail: zhangsuofei at njupt.edu.cn | hangyu5 at illinois.edu | xu.chen at dal.ca
"""

import tensorflow as tf 
from Models.MatrixCapsulesEMTensorflow.config import cfg, get_coord_add, get_dataset_size_train, get_dataset_size_test, get_num_classes, get_create_inputs
import time
import os
import Models.MatrixCapsulesEMTensorflow.capsnet_em as net
import tensorflow.contrib.slim as slim

import logging 
import daiquiri

daiquiri.setup(level=logging.DEBUG)
logger = daiquiri.getLogger(__name__)

def main(args):
    """ Get dataset hyperparameters. """
    assert len(args) == 2 and isinstance(args[1], str) 
    dataset_name = args[1]

    coord_add = get_coord_add(dataset_name)
    dataset_size_train = get_dataset_size_train(dataset_name)
    dataset_size_test = get_dataset_size_test(dataset_name)
    num_classes = get_num_classes(dataset_name)
    create_inputs = get_create_inputs(
        dataset_name, is_train=False, epochs=cfg.epoch)

    """ Set reproduciable random seed """
    tf.set_random_seed(1234)

    with tf.Graph().as_default():
        num_batches_per_epoch_train = int(dataset_size_train / cfg.batch_size)
        num_batches_test = int(dataset_size_test / cfg.batch_size)

        batch_x, batch_labels = create_inputs()
        batch_x = slim.batch_norm(batch_x, center=False, is_training=False, trainable=False)
        
        output, _ = net.build_arch(batch_x, coord_add,
                                   is_train=False,
                                   num_classes=num_classes)
        batch_acc = net.test_accuracy(output, batch_labels)
        saver = tf.train.Saver()

        step = 0

        summaries = []
        summaries.append(tf.summary.scalar('accuracy', batch_acc))
        summary_op = tf.summary.merge(summaries)

        with tf.Session(config=tf.ConfigProto(
                allow_soft_placement=True,
                log_device_placement=False)) as sess:
            sess.run(tf.local_variables_initializer())
            sess.run(tf.global_variables_initializer())

            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)
            
            if not os.path.exists(cfg.test_logdir + '/caps/{}/'.format(dataset_name)):
                os.path.exists(cfg.test_logdir + '/caps/{}/'.format(dataset_name))
            summary_writer = tf.summary.FileWriter(
                cfg.test_logdir + '/caps/{}'.format(dataset_name), graph=sess.graph)

            files = os.listdir(cfg.logdir + '/caps/{}/'.format(dataset_name))
            for epoch in range(1, cfg.epoch):
                ckpt_re = ".ckpt-%d" % (num_batches_per_epoch_train * epoch)
                for __file in files:
                    if __file.endswith(ckpt_re + ".index"):
                        ckpt = os.path.join(cfg.logdir + '/caps/{}/'.format(dataset_name), __file[:-6])
                
                saver.restore(sess, ckpt)

                accuracy_sum = 0
                for i in range(num_batches_test):
                    batch_acc_v, summary_str = sess.run([batch_acc, summary_op])
                    print('%d batches are tested.' % step)
                    summary_writer.add_summary(summary_str, step)

                    accuracy_sum += batch_acc_v

                    step += 1
                
                ave_acc = accuracy_sum / num_batches_test
                print('the average accuracy is %f' % ave_acc)

            coord.join(threads)

if __name__ == "__main__":
    tf.app.run()

    
import tensorflow as tf
import tensorflow.contrib.slim as slim
from Models.MatrixCapsulesEMTensorflow.config import cfg
import numpy as np

def cross_ent_loss(logits, y):
    loss = tf.losses.sparse_softmax_cross_entropy(labels=y, logits=logits)
    loss = tf.reduce_mean(loss)

    return loss

def test_accuracy(logits, labels):
    logits_idx = tf.to_int32(tf.argmax(logits, axis=1))
    logits_idx = tf.reshape(logits_idx, shape=(cfg.batch_size,))
    correct_preds = tf.equal(tf.to_int32(labels), logits_idx)
    accuracy = tf.reduce_sum(tf.cast(correct_preds, tf.float32)) / cfg.batch_size

    return accuracy

def build_arch(input, is_train: bool, num_classes: int):
    """A simple linear MLP with no hidden layer.
    
       returns: logits for output classes
    """
    bias_initializer = tf.truncated_normal_initializer(
        mean=0.0, stddev=0.01)
    tf.logging.info('MLP input shape: {}'.format(input.get_shape()))

    with slim.arg_scope([slim.fully_connected], trainable=is_train, biases_initializer=bias_initializer):
        with tf.variable_scope('MLP') as scope:
            output = slim.fully_connected(input, num_outputs=num_classes, scope=scope, activation_fn=None)

            tf.logging.info('output shape: {}'.format(output.get_shape()))
    return output
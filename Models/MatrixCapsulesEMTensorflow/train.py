"""
License: Apache-2.0
Author: Suofei Zhang | Hang Yu
E-mail: zhangsuofei at njupt.edu.cn | hangyu5 at illinois.edu
"""

import tensorflow as tf
import tensorflow.contrib.slim as slim
from Models.MatrixCapsulesEMTensorflow.config import cfg, get_coord_add, get_dataset_size_train, get_dataset_size_test, get_num_classes, get_create_inputs
import time
import numpy as np
import sys
import os
import Models.MatrixCapsulesEMTensorflow.capsnet_em as net

import logging
import daiquiri

daiquiri.setup(level=logging.DEBUG)
logger = daiquiri.getLogger(__name__)


def main(args):
    """Get dataset hyperparameters."""
    assert len(args) == 2 and isinstance(args[1], str)
    dataset_name = args[1]
    logger.info('Using dataset: {}'.format(dataset_name))

    """Set reproduciable random seed"""
    # Note that this only acts at the graph level.
    # This does not seed at the operation level.
    tf.set_random_seed(1234)

    coord_add = get_coord_add(dataset_name)
    if cfg.is_train:
        dataset_size = get_dataset_size_train(dataset_name)
    else:
        dataset_size = get_dataset_size_test(dataset_name)
    num_classes = get_num_classes(dataset_name)
    create_inputs = get_create_inputs(dataset_name, is_train=cfg.is_train, epochs=cfg.epoch)

    with tf.Graph().as_default(), tf.device('/cpu:0'):
        """Get global_step."""
        global_step = tf.get_variable(
            'global_step', [], initializer=tf.constant_initializer(0), trainable=False)

        """Get batches per epoch."""
        num_batches_per_epoch = int(dataset_size / cfg.batch_size)

        """Use exponential decay leanring rate?"""
        lrn_rate = tf.maximum(tf.train.exponential_decay(
            1e-3, global_step, num_batches_per_epoch, 0.8), 1e-5)
        tf.summary.scalar('learning_rate', lrn_rate)
        opt = tf.train.AdamOptimizer()  # lrn_rate

        """Get batch from data queue."""
        batch_x, batch_labels, pose_label = create_inputs()

        # TODO: GET pose_label FROM batch_labels. Should be shape [batch size, 16]
        #pass

        # batch_y = tf.one_hot(batch_labels, depth=10, axis=1, dtype=tf.float32)

        """Define the dataflow graph."""
        m_op = tf.placeholder(dtype=tf.float32, shape=())
        with tf.device('/gpu:0'):
            with slim.arg_scope([slim.variable], device='/cpu:0'):
                batch_squash = tf.divide(batch_x, 255.)
                batch_x = slim.batch_norm(batch_x, center=False, is_training=cfg.is_train, trainable=cfg.is_train)
                output, pose_out = net.build_arch(batch_x, coord_add, is_train=cfg.is_train,
                                                  num_classes=num_classes)
                # loss = net.cross_ent_loss(output, batch_labels)
                tf.logging.debug(pose_out.get_shape())
                
                # Display the changes in margin over time
                tf.summary.scalar('margin', m_op)

                loss, spread_loss, pose_loss, _ = net.spread_loss(
                    output, pose_out, batch_squash, batch_labels, pose_label, m_op)
                acc = net.test_accuracy(output, batch_labels)
                threshold_acc_20 = net.threshold_accuracy(pose_out, pose_label, threshold=20)
                threshold_acc_10 = net.threshold_accuracy(pose_out, pose_label, threshold=10)
                threshold_acc_5 = net.threshold_accuracy(pose_out, pose_label, threshold=5)
                threshold_acc_2 = net.threshold_accuracy(pose_out, pose_label, threshold=2)
                threshold_acc_1 = net.threshold_accuracy(pose_out, pose_label, threshold=1)
                threshold_acc_half = net.threshold_accuracy(pose_out, pose_label, threshold=0.5)
                threshold_acc_tenth = net.threshold_accuracy(pose_out, pose_label, threshold=0.1)
                threshold_acc_hundredth = net.threshold_accuracy(pose_out, pose_label, threshold=0.001)
                
                tf.summary.scalar('spread_loss', spread_loss)
                tf.summary.scalar('pose_loss', pose_loss)
                tf.summary.scalar('all_loss', loss)
                tf.summary.scalar('train_acc', acc)
                tf.summary.scalar('threshold_acc_20', threshold_acc_20)
                tf.summary.scalar('threshold_acc_10', threshold_acc_10)
                tf.summary.scalar('threshold_acc_5', threshold_acc_5)
                tf.summary.scalar('threshold_acc_2', threshold_acc_2)
                tf.summary.scalar('threshold_acc_1', threshold_acc_1)
                tf.summary.scalar('threshold_acc_half', threshold_acc_half)
                tf.summary.scalar('threshold_acc_tenth', threshold_acc_tenth)
                tf.summary.scalar('threshold_acc_hundredth', threshold_acc_hundredth)

            """Compute gradient."""
            grad = opt.compute_gradients(loss)
            # See: https://stackoverflow.com/questions/40701712/how-to-check-nan-in-gradients-in-tensorflow-when-updating
            grad_check = [tf.check_numerics(g, message='Gradient NaN Found!')
                          for g, _ in grad if g is not None] + [tf.check_numerics(loss, message='Loss NaN Found')]

        """Apply graident."""
        with tf.control_dependencies(grad_check):
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies(update_ops):
                train_op = opt.apply_gradients(grad, global_step=global_step)

        """Set Session settings."""
        sess = tf.Session(config=tf.ConfigProto(
            allow_soft_placement=True, log_device_placement=False))
        sess.run(tf.local_variables_initializer())
        sess.run(tf.global_variables_initializer())

        """Set Saver."""
        var_to_save = [v for v in tf.global_variables(
        ) if 'Adam' not in v.name]  # Don't save redundant Adam beta/gamma
        saver = tf.train.Saver(var_list=var_to_save, max_to_keep=cfg.epoch)

        """Display parameters"""
        total_p = np.sum([np.prod(v.get_shape().as_list()) for v in var_to_save]).astype(np.int32)
        train_p = np.sum([np.prod(v.get_shape().as_list())
                          for v in tf.trainable_variables()]).astype(np.int32)
        logger.info('Total Parameters: {}'.format(total_p))
        logger.info('Trainable Parameters: {}'.format(train_p))

        # read snapshot
        if not cfg.is_train:
            latest = tf.train.latest_checkpoint(os.path.join(cfg.logdir, dataset_name))
            saver.restore(sess, latest)
        """Set summary op."""
        summary_op = tf.summary.merge_all()

        """Start coord & queue."""
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        """Set summary writer"""
        if cfg.is_train:
            logdir_ = cfg.logdir,
            naming = 'train'
        else:
            logdir_ = cfg.test_logdir
            naming = 'test'
        
        if not os.path.exists(logdir_ + '/caps/{}/{}_log/'.format(dataset_name, naming)):
            os.makedirs(logdir_ + '/caps/{}/{}_log/'.format(dataset_name, naming))
        summary_writer = tf.summary.FileWriter(
            logdir_ + '/caps/{}/{}_log/'.format(dataset_name, naming), graph=sess.graph)  # graph = sess.graph, huge!

        """Main loop."""
        m_min = 0.2
        m_max = 0.9
        m = m_min
        for step in range(cfg.epoch * num_batches_per_epoch + 1):
            tic = time.time()
            """"TF queue would pop batch until no file"""
            try:
                _, loss_value, summary_str = sess.run(
                    [train_op, loss, summary_op], feed_dict={m_op: m})
                logger.info('%d iteration finishs in ' % step + '%f second' %
                            (time.time() - tic) + ' loss=%f' % loss_value)
            except KeyboardInterrupt:
                sess.close()
                sys.exit()
            except tf.errors.InvalidArgumentError:
                logger.warning('%d iteration contains NaN gradients. Discard.' % step)
                continue
            else:
                """Write to summary."""
                if step % 5 == 0:
                    summary_writer.add_summary(summary_str, step)

                """Epoch wise linear annealling."""
                if (step % num_batches_per_epoch) == 0:
                    if step > 0:
                        m += (m_max - m_min) / (cfg.epoch * cfg.m_schedule)
                        if m > m_max:
                            m = m_max

                    """Save model periodically"""
                    ckpt_path = os.path.join(
                        logdir_ + '/caps/{}/'.format(dataset_name), 'model-{:.4f}.ckpt'.format(loss_value))
                    saver.save(sess, ckpt_path, global_step=step)


if __name__ == "__main__":
    tf.app.run()

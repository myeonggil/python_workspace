import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image
import math
import operator
import os

def google_learning(image_path):
    num_features = 6209
    num_filters = 6
    # accuracy 95%
    tf.reset_default_graph()
    sess = tf.InteractiveSession() # 변수 초기화

    train_x = np.load('./learning/train_x.npy')
    train_y = np.load('./learning/train_y.npy')
    y_train_one_hot = tf.squeeze(tf.one_hot(train_y, 6), axis=1)

    X = tf.placeholder(tf.float32, [None, 64, 64, 3])  # 32x32 이미지 제공 input
    Y = tf.placeholder(tf.float32, [None, 6])  # 1 ~ 5로
    keep_prob = tf.placeholder(tf.float32)

    W1 = tf.Variable(tf.random_normal([3, 3, 3, 64], stddev=0.01))
    L1 = tf.nn.conv2d(X, W1, strides=[1, 1, 1, 1], padding='SAME')
    L1 = tf.nn.relu(L1)
    L1 = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    # L1 = tf.nn.dropout(L1, keep_prob=keep_prob)

    W2 = tf.Variable(tf.random_normal([3, 3, 64, 128], stddev=0.01))
    L2 = tf.nn.conv2d(L1, W2, strides=[1, 1, 1, 1], padding='SAME')
    L2 = tf.nn.relu(L2)
    L2 = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    # L2 = tf.nn.dropout(L2, keep_prob=keep_prob)

    W3 = tf.Variable(tf.random_normal([3, 3, 128, 128], stddev=0.01))
    L3 = tf.nn.conv2d(L2, W3, strides=[1, 1, 1, 1], padding='SAME')
    L3 = tf.nn.relu(L3)
    L3 = tf.nn.max_pool(L3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    # L3 = tf.nn.dropout(L3, keep_prob=keep_prob)
    L3 = tf.reshape(L3, [-1, 128 * 8 * 8])

    W4 = tf.get_variable("W4", shape=[128 * 8 * 8, 625], initializer=tf.contrib.layers.xavier_initializer())
    b4 = tf.Variable(tf.random_normal([625]))
    L4 = tf.nn.relu(tf.matmul(L3, W4) + b4)
    L4 = tf.nn.dropout(L4, keep_prob=keep_prob)

    W5 = tf.get_variable("W5", shape=[625, 6], initializer=tf.contrib.layers.xavier_initializer())
    b5 = tf.Variable(tf.random_normal([6]))
    hypothesis = tf.matmul(L4, W5) + b5

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()

    saver.restore(sess, './learning/image_matching.ckpt')
    image = Image.open(image_path)
    size = (64, 64)
    try:
        re_image = image.resize(size)
        pix = np.array(re_image).reshape(1, 64, 64, 3)
    except:
        return 'error', 'error'

    print('Prediction:', sess.run(tf.argmax(hypothesis, 1), feed_dict={X: pix, keep_prob: 1.0}))
    x = sess.run(hypothesis, feed_dict={X: pix, keep_prob: 1.0})
    result = sess.run(tf.argmax(hypothesis, 1), feed_dict={X: pix, keep_prob: 1.0})[0]

    # return result
    return result, x[0][result]

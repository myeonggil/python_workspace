import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image
import math
import operator
import os

def learning(image_path):
    num_features = 6209
    num_filters = 6
    # accuracy 95%
    tf.reset_default_graph()
    sess = tf.InteractiveSession() # 변수 초기화

    train_x = np.load('./learning/train_x.npy')
    train_y = np.load('./learning/train_y.npy')
    print(train_y.shape)
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

    """X = tf.placeholder(tf.float32, [None, 32, 32, 3])  # 32x32 이미지 제공 input

    with tf.name_scope('layer1') as scope:
        W1 = tf.get_variable('W1', [5, 5, 3, 32],
                             initializer=tf.contrib.layers.xavier_initializer())
        # W1 = tf.Variable(tf.random_normal([3, 3, 3, 32], stddev=0.01))
        L1 = tf.nn.conv2d(X, W1, strides=[1, 1, 1, 1], padding='SAME')
        b1 = tf.Variable(tf.random_normal([32]))
        L1 = tf.nn.relu(tf.add(L1, b1))
        L1 = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # L1 = tf.nn.dropout(L1, keep_prob=keep_prob)

        w1_hist = tf.summary.histogram('weights1', W1)
        b1_hist = tf.summary.histogram('biases1', b1)
        layer1 = tf.summary.histogram('layer1', L1)

    with tf.name_scope('layer2') as scope:
        W2 = tf.get_variable('W2', [5, 5, 32, 64],
                             initializer=tf.contrib.layers.xavier_initializer())
        # W2 = tf.Variable(tf.random_normal([3, 3, 32, 64], stddev=0.01))
        L2 = tf.nn.conv2d(L1, W2, strides=[1, 1, 1, 1], padding='SAME')
        b2 = tf.Variable(tf.random_normal([64]))
        L2 = tf.nn.relu(tf.add(L2, b2))
        L2 = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # L2 = tf.nn.dropout(L2, keep_prob=keep_prob)

        w2_hist = tf.summary.histogram('weights2', W2)
        b2_hist = tf.summary.histogram('biases2', b2)
        layer2 = tf.summary.histogram('layer2', L2)

    with tf.name_scope('layer3') as scope:
        W3 = tf.get_variable('W3', [5, 5, 64, 128],
                             initializer=tf.contrib.layers.xavier_initializer())
        # W3 = tf.Variable(tf.random_normal([3, 3, 32, 64], stddev=0.01))
        L3 = tf.nn.conv2d(L2, W3, strides=[1, 1, 1, 1], padding='SAME')
        b3 = tf.Variable(tf.random_normal([128]))
        L3 = tf.nn.relu(tf.add(L3, b3))
        L3 = tf.nn.max_pool(L3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # L3 = tf.nn.dropout(L3, keep_prob=keep_prob)

        w3_hist = tf.summary.histogram('weights3', W3)
        b3_hist = tf.summary.histogram('biases3', b3)
        layer3 = tf.summary.histogram('layer3', L3)

    with tf.name_scope('layer4') as scope:
        W4 = tf.get_variable('W4', [5, 5, 128, 128],
                             initializer=tf.contrib.layers.xavier_initializer())
        # W4 = tf.Variable(tf.random_normal([3, 3, 128, 128], stddev=0.01))
        L4 = tf.nn.conv2d(L3, W4, strides=[1, 1, 1, 1], padding='SAME')
        b4 = tf.Variable(tf.random_normal([128]))
        L4 = tf.nn.relu(tf.add(L4, b4))
        # L4 = tf.nn.max_pool(L4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # L4 = tf.nn.dropout(L4, keep_prob=keep_prob)

        w4_hist = tf.summary.histogram('weights4', W4)
        b4_hist = tf.summary.histogram('biases4', b4)
        layer4 = tf.summary.histogram('layer4', L4)

    with tf.name_scope('layer5') as scope:
        W5 = tf.get_variable('W5', [5, 5, 128, 256],
                             initializer=tf.contrib.layers.xavier_initializer())
        # W3 = tf.Variable(tf.random_normal([3, 3, 128, 128], stddev=0.01))
        L5 = tf.nn.conv2d(L4, W5, strides=[1, 1, 1, 1], padding='SAME')  # strides
        b5 = tf.Variable(tf.random_normal([256]))
        L5 = tf.nn.relu(tf.add(L5, b5))
        L6 = tf.reshape(L5, [-1, 8 * 8 * 64])

        W6 = tf.get_variable('W6', [8 * 8 * 64, 6],
                             initializer=tf.contrib.layers.xavier_initializer())
        b6 = tf.Variable(tf.random_normal([6]))

        hypothesis = tf.matmul(L6, W6) + b6

        w5_hist = tf.summary.histogram('weights5', W5)
        b5_hist = tf.summary.histogram('biases5', b5)
        hypothesis_hist = tf.summary.histogram('hypothesis', hypothesis)"""


    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()

    saver.restore(sess, './learning/image_matching.ckpt')
    image = Image.open(image_path)
    size = (64, 64)
    try:
        re_image = image.resize(size)
        print(np.array(re_image).shape)
        pix = np.array(re_image).reshape(1, 64, 64, 3)
        print(pix.shape)
    except:
        return 'error'

    print('Prediction:', sess.run(tf.argmax(hypothesis, 1), feed_dict={X: pix, keep_prob: 1.0}))
    x = sess.run(hypothesis, feed_dict={X: pix, keep_prob: 1.0})
    result = sess.run(tf.argmax(hypothesis, 1), feed_dict={X: pix, keep_prob: 1.0})[0]
    sub = {}

    jeans = np.load('./learning/jeans_result.npy')
    outer = np.load('./learning/outer_result.npy')
    shirts = np.load('./learning/shirts_result.npy')
    top = np.load('./learning/top_result.npy')
    sweathers = np.load('./learning/sweathers_result.npy')
    slacks = np.load('./learning/slacks_result.npy')

    result1_len = len(jeans)
    result2_len = result1_len + len(outer)
    result3_len = result2_len + len(shirts)
    result4_len = result3_len + len(slacks)
    result5_len = result4_len + len(sweathers)
    result6_len = result5_len + len(top)

    file = ''
    index = 0
    image_list = 0

    if result == 0:
        file = 'jeans'
        start = 0
        end = result1_len
        image_list = os.listdir('./Images/use_images/train/jeans')
        for i in range(0, len(jeans)):
            sub[i] = math.fabs(jeans[index][0] - x[0][result])
            index += 1

    if result == 1:
        file = 'outer'
        start = result1_len
        end = result2_len
        image_list = os.listdir('./Images/use_images/train/outer')
        for i in range(0, len(outer)):
            sub[i] = math.fabs(outer[index][0] - x[0][result])
            index += 1

    if result == 2:
        file = 'shirts'
        start = result2_len
        end = result3_len
        image_list = os.listdir('./Images/use_images/train/shirts')
        for i in range(0, len(shirts)):
            sub[i] = math.fabs(shirts[index][0] - x[0][result])
            index += 1

    if result == 3:
        file = 'slacks'
        start = result3_len
        end = result4_len
        image_list = os.listdir('./Images/use_images/train/slacks')
        for i in range(0, len(slacks)):
            sub[i] = math.fabs(top[index][0] - x[0][result])
            index += 1

    if result == 4:
        file = 'sweathers'
        start = result4_len
        end = result5_len
        image_list = os.listdir('./Images/use_images/train/sweathers')
        for i in range(0, len(sweathers)):
            sub[i] = math.fabs(sweathers[index][0] - x[0][result])
            index += 1

    if result == 5:
        file = 'top'
        start = result5_len
        end = result6_len
        image_list = os.listdir('./Images/use_images/train/top')
        for i in range(0, len(top)):
            sub[i] = math.fabs(top[index][0] - x[0][result])
            index += 1

    index = 0
    """for i in range(start, end):
        temp_train_x = train_x[i].reshape(1, 64, 64, 3)
        y = sess.run(hypothesis, feed_dict={X: temp_train_x, keep_prob: 1.0})
        sub[index] = math.fabs(y[0][result] - x[0][result])
        index += 1"""

    sorted_sub = sorted(sub.items(), key=operator.itemgetter(1))
    directory = 1
    info = []

    for i in range(0, 16):
        info.append('./Images/use_images/train/' + file + '/%s' % (image_list[sorted_sub[i][0]]))
        # info = Image.open('../Images/use_images/train/' + file + '/%s' % (image_list[sorted_sub[i][0]]))
        """arr = np.array(info).tolist()
        plt.imshow(arr)
        plt.show()"""

    print(sorted_sub)
    print(info)
    # return result
    return result, x[0][result], info

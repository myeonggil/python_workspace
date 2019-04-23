import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image
import math
import operator
import os

num_features = 6209
num_filters = 32
# accuracy 95%
sess = tf.InteractiveSession() # 변수 초기화

train_x = np.load('./train_x.npy')
train_y = np.load('./train_y.npy')
print(train_y.shape)
y_train_one_hot = tf.squeeze(tf.one_hot(train_y, 6), axis=1)

X = tf.placeholder(tf.float32, [None, 64, 64, 3])   # 32x32 이미지 제공 input
keep_prob = tf.placeholder(tf.float32)

X = tf.placeholder(tf.float32, [None, 64, 64, 3])   # 32x32 이미지 제공 input

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

W4 = tf.get_variable("W4", shape=[128 * 8 * 8, 625],
                     initializer=tf.contrib.layers.xavier_initializer())
b4 = tf.Variable(tf.random_normal([625]))
L4 = tf.nn.relu(tf.matmul(L3, W4) + b4)
L4 = tf.nn.dropout(L4, keep_prob=keep_prob)

W5 = tf.get_variable("W5", shape=[625, 6], initializer=tf.contrib.layers.xavier_initializer())
b5 = tf.Variable(tf.random_normal([6]))
hypothesis = tf.matmul(L4, W5) + b5

sess = tf.Session()
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()

saver.restore(sess, './image_matching.ckpt')

count = []
dir_len = os.listdir('../Images/define_images')
sub = {}

"""for i in range(0, len(dir_len)):
    file_len = os.listdir('../Images/define_images/%d' % (i + 1))
    count.append(len(file_len))
    sub['sub%d' % (i + 1)] = np.zeros(count[i])"""

image_list = []
max_list = []

index = 0
count = [990, 1313, 1060, 1083, 632, 1131]


sub1 = np.zeros((990, 1), dtype='float')
sub2 = np.zeros((1313, 1), dtype='float')
sub3 = np.zeros((1060, 1), dtype='float')
sub4 = np.zeros((1083, 1), dtype='float')
sub5 = np.zeros((632, 1), dtype='float')
sub6 = np.zeros((1131, 1), dtype='float')

for i in range(0, 6):
    print(i)
    for j in range(0, count[i]):
        temp_train_x = train_x[index].reshape(1, 64, 64, 3)
        y = sess.run(hypothesis, feed_dict={X: temp_train_x, keep_prob: 1.0})[0][i]
        if i == 0:
            sub1[j: j + 1] = y
        elif i == 1:
            sub2[j: j + 1] = y
        elif i == 2:
            sub3[j: j + 1] = y
        elif i == 3:
            sub4[j: j + 1] = y
        elif i == 4:
            sub5[j: j + 1] = y
        elif i == 5:
            sub6[j: j + 1] = y
        index += 1


"""for i in range(0, count1):
    temp_train_x = train_x[i].reshape(1, 64, 64, 3)
    y = sess.run(hypothesis, feed_dict={X: temp_train_x})[0][0]
    sub1[index: index + 1] = y
    index += 1

index = 0
count2_2 = count1 + count2
print(count2_2)
for i in range(count1, count2_2):
    temp_train_x = train_x[i].reshape(1, 64, 64, 3)
    y = sess.run(hypothesis, feed_dict={X: temp_train_x})[0][1]
    sub2[index: index + 1] = y
    index += 1

index = 0
count3_3 = count2_2 + count3
print(count3_3)
for i in range(count2_2, count3_3):
    temp_train_x = train_x[i].reshape(1, 64, 64, 3)
    y = sess.run(hypothesis, feed_dict={X: temp_train_x})[0][2]
    sub3[index: index + 1] = y
    index += 1

index = 0
count4_4 = count3_3 + count4
print(count4_4)
for i in range(count3_3, count4_4):
    temp_train_x = train_x[i].reshape(1, 64, 64, 3)
    y = sess.run(hypothesis, feed_dict={X: temp_train_x})[0][3]
    sub4[index: index + 1] = y
    index += 1

index = 0
count5_5 = count4_4 + count5
print(count5_5)
for i in range(count4_4, count5_5):
    temp_train_x = train_x[i].reshape(1, 64, 64, 3)
    y = sess.run(hypothesis, feed_dict={X: temp_train_x})[0][4]
    sub5[index: index + 1] = y
    index += 1

index = 0
count6_6 = count4_4 + count5
print(count5_5)
for i in range(count4_4, count5_5):
    temp_train_x = train_x[i].reshape(1, 64, 64, 3)
    y = sess.run(hypothesis, feed_dict={X: temp_train_x})[0][4]
    sub5[index: index + 1] = y
    index += 1"""

np.save('jeans_result', sub1)
np.save('outer_result', sub2)
np.save('shirts_result', sub3)
np.save('slacks_result', sub4)
np.save('sweathers_result', sub5)
np.save('top_result', sub6)

"""for i in range(0, len(train_y)):
    if y_train_one_hot.eval()[i][result] == 1.:
        temp_train_x = train_x[i].reshape(1, 64, 64, 3)
        y = sess.run(hypothesis, feed_dict={X: temp_train_x})
        sub[i] = math.fabs(y[0][result] - x[0][result])"""
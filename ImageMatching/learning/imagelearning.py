import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread
from tensorflow.python.keras._impl.keras.datasets.cifar10 import load_data
from PIL import Image
import os

"""
y_train의 기본 구조는 50000 x 1행렬이다.
one_hot encoding으로 한개의 열을 10개의 열로 변환 시키고 행으로 구분한다. 총 10개 종류의 이미지가 있기 때문에
마지막으로 크기가 axis=1인 차원은 제거한 형태로 변환한다.
"""

num_features = 6209

def image_load():
    num_features = 6209
    # num_features = 2894
    image_index = 1
    directory = 1

    result_x = np.zeros((num_features, 64, 64, 3), dtype='uint8')
    result_y = np.zeros((num_features, 1), dtype='uint8')
    index_sum = 0
    index = 0

    file_list = {1: 'jeans', 2: 'outer', 3: 'shirts', 4: 'slacks', 5: 'sweathers', 6: 'top'}

    for key, value in file_list.items():
        path = '../Images/define_images/train/'
        path += value
        imgs = os.listdir(path)
        print(key, value)

        for img in imgs:
            img_open = Image.open('../Images/define_images/train/%s/%s' % (value, img))
            train_y = []

            try:
                train_x = np.array(img_open).reshape(1, 64, 64, 3)
                result_x[index: index + 1, :, :, :] = train_x
                train_y.append(key - 1)
                result_y[index_sum: index_sum + 1] = np.array(train_y)
                index += 1
                index_sum += 1
            except:
                print('error directory = %s index = %s' % (path, img))


    return (result_x, result_y)

(train_x, train_y) = image_load()

"""np.save('train_x', train_x)
np.save('train_y', train_y)

# (test_x, test_y) = image_load()

# np.save('test_x', test_x)
# np.save('test_y', test_y)"""

# 5개의 convolution layer와 1개의 fully connected layer로 구성
sess = tf.InteractiveSession() # 변수 초기화

def learning(x_train, y_train_one_hot2, total_batch):
    for i in range(total_batch):
        batch_xs, batch_ys = next_batch(64, x_train, y_train_one_hot2)
        feed_dict = {X: batch_xs, Y: batch_ys}
        cost_val, _ = sess.run([cost, optimizer], feed_dict=feed_dict)
        if i % 100 == 0:
            print('Cost: ', cost_val)

def next_batch(num, data, labels):
    idx = np.arange(0, len(data))
    np.random.shuffle(idx)
    idx = idx[:num]
    data_shuffle = [data[i] for i in idx]
    labels_shuffle = [labels[i] for i in idx]

    return np.asarray(data_shuffle), np.asarray(labels_shuffle)

train_x = np.load('train_x.npy')
train_y = np.load('train_y.npy')
# test_x = np.load('test_x.npy')
# test_y = np.load('test_y.npy')
print(train_x.shape)
print(train_y.shape)
# print(test_x.shape)
# print(test_y.shape)


y_train_one_hot = tf.squeeze(tf.one_hot(train_y, 6), axis=1)
# y_test_one_hot = tf.squeeze(tf.one_hot(test_y, 6), axis=1)

X = tf.placeholder(tf.float32, [None, 64, 64, 3])   # 64x64 이미지 제공 input
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

W4 = tf.get_variable("W4", shape=[128 * 8 * 8, 625],
                     initializer=tf.contrib.layers.xavier_initializer())
b4 = tf.Variable(tf.random_normal([625]))
L4 = tf.nn.relu(tf.matmul(L3, W4) + b4)
L4 = tf.nn.dropout(L4, keep_prob=keep_prob)

W5 = tf.get_variable("W5", shape=[625, 6], initializer=tf.contrib.layers.xavier_initializer())
b5 = tf.Variable(tf.random_normal([6]))
hypothesis = tf.matmul(L4, W5) + b5

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypothesis, labels=Y))
optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)
#   AdamOptimizer 이 방식은 별로인듯하다.
#   RMSPropOptimizer 이 방식도 별로인듯하다.
#   GradientDescentOptimizer 총 3가지 방식을 사용하면서 비교 할 예정

correct_predict = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_predict, tf.float32))  # cast float32형태로 변환

train_epoch = 15
batch_size = 100

summary = tf.summary.merge_all()
sess = tf.Session()
sess.run(tf.global_variables_initializer())
#   eval()함수는 초기화 후에 사용할 수 있다... 이유는??

# writer = tf.summary.FileWriter('./result_logs')
# writer.add_graph(sess.graph)

global_steps = 1

for epoch in range(train_epoch):    # train 횟수
    avg_cost = 0
    total_batch = int(num_features / batch_size)

    for i in range(0, total_batch):
        batch_xs, batch_ys = next_batch(128, train_x, y_train_one_hot.eval())
        feed_dict = {X: batch_xs, Y: batch_ys}
        cost_val, _ = sess.run([cost, optimizer], feed_dict={X: batch_xs, Y: batch_ys, keep_prob: 0.7})
        avg_cost += cost_val
        # writer.add_summary(s, global_step=global_steps)
        # global_steps += 1

    print('avg_cost:', avg_cost / total_batch)
    test_xs, test_ys = next_batch(512, train_x, y_train_one_hot.eval())
    correct_predict = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_predict, tf.float32))  # cast float32형태로 변환
    print('Accuracy: ', sess.run(accuracy, feed_dict={X: test_xs, Y: test_ys, keep_prob: 1.0}))

test_xs, test_ys = next_batch(2048, train_x, y_train_one_hot.eval())
correct_predict = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_predict, tf.float32))  # cast float32형태로 변환
print('Accuracy: ', sess.run(accuracy, feed_dict={X: test_xs, Y: test_ys, keep_prob: 1.0}))

saver = tf.train.Saver()
saver.save(sess, './image_matching.ckpt')
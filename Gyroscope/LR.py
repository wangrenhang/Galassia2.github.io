# Use linear regression to calculate the best calibration matrix
import tensorflow as tf
import numpy as np
from numpy.linalg import inv
import csv

X = []
Y = []
# rawcsv = open("MPU6050_filtered.csv", 'r')
rawcsv = open("MPU3300_filtered.csv", 'r')
csvDict = csv.DictReader(rawcsv)
# Training data collection
for line in csvDict:
    Y.extend([float(line['X']), float(line['Y']), float(line['Z'])])

    if line["Axis"] == 'X':
        X.extend([float(line["Angular velocity"]), 0.0, 0.0, 1])
    elif line["Axis"] == 'Y':
        X.extend([0.0, float(line["Angular velocity"]), 0.0, 1])
    elif line["Axis"] == 'Z':
        X.extend([0.0, 0.0, float(line["Angular velocity"]), 1])
    else:
        continue

dataset_size = len(X)//4
X = np.reshape(X, (dataset_size, 4))
Y = np.reshape(Y, (dataset_size, 3))
rawcsv.close()
print("Dataset size is : %d" % dataset_size)

# Output X's data to check
# file = open(r"Y.txt", 'w')
# for i in X:
#     file.write(str(i))
#     file.write('\r\n')
# file.close()

# Training parameters
batch_size = 1500
w = tf.Variable(tf.random_normal([4, 3], stddev=1, seed=1))
x = tf.placeholder(tf.float32, shape=(None, 4), name = "input")
y_ = tf.placeholder(tf.float32, shape=(None, 3), name = "output")

# Forward propagation
y = tf.matmul(x, w)
# Backward propagation
global_step = tf.Variable(0, trainable=False)
learning_rate = tf.train.exponential_decay(0.8, global_step, dataset_size/batch_size, 0.99)
cross_entropy = tf.reduce_mean(tf.abs(y-y_))
train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy, global_step = global_step)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    STEPS = 50000
    for i in range(STEPS):
        start = (i * batch_size) % dataset_size
        end = min(start+batch_size, dataset_size)

        sess.run(train_step, feed_dict={x: X[start:end], y_: Y[start:end]})

        if i % 10000 == 0:
            entropy = sess.run(cross_entropy, feed_dict={x: X, y_: Y})
            print(entropy)

    # Get bias and scale matrix respectively
    w = sess.run(w)
    bias = w[3]
    bias = np.reshape(bias, (1, 3))
    w = w[:-1]
    w = np.reshape(w, (3, 3))
    w = inv(w)
    print(w, '\n', bias)






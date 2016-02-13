import glob
import time

import numpy as np
import pylab as plt

from fastish_pca import fastish_PCA
from scipy.ndimage import imread
from sklearn.kernel_ridge import KernelRidge

TRAINING_FACES_FILEPATH = 'training.csv'
NEUTRAL_FACES_BLOB = 'faces_dataset/*a*'
HAPPY_FACES_BLOB = 'faces_dataset/*b*'                                     
BOTTLENECK = 300
IMG_SHAPE = (96, 96)

print "Loading faces (training) ..."
start = time.time()
training_faces = np.loadtxt(TRAINING_FACES_FILEPATH) / 255
start = time.time() - start
print "Done in %.2fs" % start

print "Calculating PCA approx. ..."
start = time.time()
U, s, V = fastish_PCA(training_faces, BOTTLENECK, 2)
start = time.time() - start
print "Done in %.2fs" % start

print "Found eigenvalues"
print s

print "Loading faces (neutral) ..."

start = time.time()
neutral = []
for filename in sorted(glob.glob(NEUTRAL_FACES_BLOB)):
  neutral.append(np.dot(V.T, imread(filename, flatten=True).flatten()))
neutral = np.array(neutral)
start = time.time() - start
print "Done in %.2fs" % start

print "Loading faces (happy) ..."
start = time.time()
happy = []
for filename in sorted(glob.glob(HAPPY_FACES_BLOB)):
  happy.append(imread(filename, flatten=True).flatten())
happy = np.array(happy)
start = time.time() - start
print "Done in %.2fs" % start

print "Performing Ridge Regression ..."
start = time.time()
ridge = KernelRidge(alpha=.5, kernel='rbf').fit(neutral, happy)
start = time.time() - start
print "Done in %.2fs" % start

plt.imshow(1 - ridge.predict(V.T.dot(imread("test.jpg", flatten=True).flatten()).reshape((1, -1))).reshape(IMG_SHAPE), cmap='Greys')
plt.show()

f = plt.figure()
k = 3
for i, filename in enumerate(glob.glob(NEUTRAL_FACES_BLOB)):
  if i >= k:
    break
  filename2 = filename[:-8] + 'b' + filename[-7:] 

  img = imread(filename, flatten=True)
  img2 = imread(filename2, flatten=True)

  representation = V.T.dot(img.flatten())

  reconstruction = V.dot(representation).reshape(IMG_SHAPE)
  prediction = ridge.predict(representation.reshape((1, -1))).reshape(IMG_SHAPE)
  
  f.add_subplot(k, 4, 4*i + 1)
  plt.imshow(1 - img, cmap='Greys')

  f.add_subplot(k, 4, 4*i + 2)
  plt.imshow(1 - reconstruction, cmap='Greys')
  
  f.add_subplot(k, 4, 4*i + 3)
  plt.imshow(1 - img2, cmap='Greys')

  f.add_subplot(k, 4, 4*i + 4)
  plt.imshow(1 - prediction, cmap='Greys')
plt.show()

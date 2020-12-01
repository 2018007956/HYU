# https://github.com/mattnedrich/MeanShift_py
import cv2
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import MeanShift
from sklearn.datasets import make_blobs

path = 'C:\\Users\\LG\\Desktop\\1.jpg'
img = cv2.imread(path,cv2.IMREAD_COLOR)

lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
X, _ = make_blobs(n_samples = 100, centers = lab, cluster_std = 1.5)

ms = MeanShift()
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

print(cluster_centers)
n_clusters_ = len(np.unique(labels))
print("Number of estimated clusters:", n_clusters_)

colors = 10*['r','g','b','c','k','y','m']
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(len(X)):
    ax.scatter(X[i][0], X[i][1], X[i][2], c=colors[labels[i]], marker='o')

ax.scatter(cluster_centers[:,0],cluster_centers[:,1],cluster_centers[:,2],
            marker="x",color='k', s=150, linewidths = 5, zorder=10)

plt.show()
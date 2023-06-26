import pandas as pd
import sys
import math
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import random
def load_dataset():
    global df, num_of_cluster, epsilon, min_pts, data_dict

    # Parameters
    num_of_cluster = int(argv[2])
    epsilon = float(argv[3])   # Radius
    min_pts = int(argv[4])   # Density threshold

    # File read & make dataset to dictionary
    df = pd.read_csv(argv[1], sep="\t", names=["index", "x", "y"])
    data_dict = {}
    for d in df.values.tolist():
        data_dict[int(d[0])] = (d[1], d[2])

def is_in_distance(x1, y1, x2, y2, eps):
    # Euclidean distance
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dist <= eps

def dbscan():
    global clusters
    clusters = []
    visited_idx = []
    cluster_idx = 0
    while data_dict.keys():
        # criteria = random.choice(list(data_dict.keys()))
        criteria = list(data_dict.keys())[0] # 의미적으로는 random
        queue = deque([criteria])  # core candidate's index
        clusters.append([])
        while queue:
            core_candidate = queue.popleft()
            # Skip processed points
            if not core_candidate in visited_idx:
                clusters[cluster_idx].append(core_candidate)
                visited_idx.append(core_candidate)

                # Find neighbors of core_candidate
                neighbors = []
                x1, y1 = data_dict[core_candidate]
                for idx in data_dict.keys():
                    x2, y2 = data_dict[idx]
                    # Check min_pts
                    if is_in_distance(x1, y1, x2, y2, epsilon):
                        neighbors.append(idx)

                # if it is the core point, Expand queue
                if len(neighbors) >= min_pts:  
                    for idx in neighbors:
                        queue.append(idx)
                        
        # Remove labeled data
        for d in clusters[cluster_idx]:
            del data_dict[d]
        cluster_idx += 1

def write():
    clusters.sort(key=lambda x: len(x), reverse=True)
    for i in range(num_of_cluster):
        output = pd.DataFrame(data= np.array(clusters[i]))
        output.to_csv(str(argv[1])[0:-4]+'_cluster_'+str(i)+'.txt', header=None, index=None)
        # print('cluster_'+str(i)+': ',output.shape)
        
def show_plot():
    load_dataset()
    colors = ['r','g','b','y','m','c','pink','orange']
    title = argv[1].split('/')[-1][:-4]+'_clustering_result'
    plt.title(title)
    for i in range(num_of_cluster):
        for index in clusters[i]:
            x,y = data_dict[index]
            plt.scatter(x,y, color=colors[i], s=2)
            del data_dict[index]
    # Outliers
    # print('outliers:',len(data_dict))
    for x,y in data_dict.values():
        plt.scatter(x,y, color='gray', s=2)
    plt.savefig('./result_img/'+title+'.png') 

    

if __name__ == '__main__':
    argv = sys.argv
    load_dataset()
    dbscan()
    write()
    # show_plot()
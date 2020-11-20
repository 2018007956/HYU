import re
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
import sys

def hierarchical_clustering(data, linkage, no_of_clusters):
    # initial similarity matrix
    color = ['r', 'g', 'b', 'y', 'c', 'm', 'k', 'w']
    initial_distances = pairwise_distances(data, metric='cosine')
    initial_similarity = 1 - initial_distances

    # making all the diagonal elements infinity
    np.fill_diagonal(initial_similarity, -sys.maxsize)
    clusters, spans = find_clusters(initial_similarity, linkage)

    # plotting the clusters & write txt (clusters, span)
    iteration_number = initial_similarity.shape[0] - no_of_clusters
    clusters_to_plot = clusters[iteration_number]
    arr = np.unique(clusters_to_plot)
    span = []
    N = len(spans)-1 # similarity index
    for i in range(N-2,N):
        span.append(spans[i])

    indices_to_plot = []
    fig = plt.figure()
    fig.suptitle(linkage+' link clustering')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    for x in np.nditer(arr):
        indices_to_plot.append(np.where(clusters_to_plot == x))

    c = []
    data = data.tolist()
    tuple_data=[]
    for n in range(len(data)):
        tuple_data.append(tuple(data[n]))

    for m in range(len(indices_to_plot)):     # indices_to_plot에 해당되는 인덱스의 데이터끼리 묶기
        ap = []
        for n in range(len(indices_to_plot[m][0])):
            idx = indices_to_plot[m][0][n]    # dtype이 있으므로 [0]위치가 index들어있는 위치임
            ap.append(tuple_data[idx])
        c.append(ap)

    p = 0
    data = np.array(data)
    for i in range(0, len(indices_to_plot)):
        for j in np.nditer(indices_to_plot[i]):
            ax.scatter(data[j, 0], data[j, 1], c=color[p])
        p = p + 1

    # plt.show()
    return c, span


def find_clusters(input, linkage):
    clusters = {}
    row_index = -1
    col_index = -1
    array = []
    spans = []

    for n in range(input.shape[0]):
        array.append(n)

    clusters[0] = array.copy()

    for k in range(1, input.shape[0]):
        max_val = -sys.maxsize
        for i in range(0, input.shape[0]):
            for j in range(0, input.shape[1]):
                if (input[i][j] >= max_val):
                    max_val = input[i][j]
                    row_index = i
                    col_index = j

        spans.append(max_val)

        # Single Linkage
        if linkage == "single":
            for i in range(0, input.shape[0]):
                if i != col_index and i != row_index:
                    temp = max(input[col_index][i], input[row_index][i])
                    input[col_index][i] = temp
                    input[i][col_index] = temp
        # Complete Linkage
        elif linkage == "complete":
            for i in range(0, input.shape[0]):
                if i != col_index and i != row_index:
                    temp = min(input[col_index][i], input[row_index][i])
                    input[col_index][i] = temp
                    input[i][col_index] = temp
        # Average Linkage
        elif linkage == "average":
            for i in range(0, input.shape[0]):
                if i != col_index and i != row_index:
                    temp = (input[col_index][i] + input[row_index][i]) / 2
                    input[col_index][i] = temp
                    input[i][col_index] = temp

        for i in range(0, input.shape[0]):
            input[row_index][i] = -sys.maxsize
            input[i][row_index] = -sys.maxsize

        minimum = min(row_index, col_index)
        maximum = max(row_index, col_index)
        for n in range(len(array)):
            if (array[n] == maximum):
                array[n] = minimum
        clusters[k] = array.copy()

    return clusters, spans

## main
with open("C:\\Users\\LG\\Desktop\\assignment~20\\CoordinatePlane_1.txt","r") as file:
    k, n = map(int, file.readline().split())
    count = 0
    data = []
    for line in file:
        for i in line.split():
            temp = re.split(',',i)
            data.append((int(temp[0]),int(temp[1])))
            count+=1

data = np.reshape(data,(-1,2))

fig = plt.figure()
fig.suptitle('Scatter Plot for clusters')
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.scatter(data[:,0],data[:,1])
# plt.show()


single_clusters, single_span=hierarchical_clustering(data,"single",3)
complete_clusters, complete_span = hierarchical_clustering(data,"complete",3)
avg_clusters, avg_span = hierarchical_clustering(data,"average",3)

## write
with open('C:\\Users\\LG\\Desktop\\assignment~20\\CoordinatePlane_{}_output.txt'.format(k),'w') as f:
    f.write(str(k)+'\n---\nsingle\n')
    f.write('clusters: '+str(single_clusters)[1:-1]+'\n')
    f.write('span: '+str(single_span).strip('[]')+'\n')

    f.write('---\ncomplete\n')
    f.write('clusters: '+str(complete_clusters)[1:-1]+'\n')
    f.write('span: '+str(complete_span).strip('[]')+'\n')

    f.write('---\naverage\n')
    f.write('clusters: ' + str(avg_clusters)[1:-1] + '\n')
    f.write('span: ' + str(avg_span).strip('[]') + '\n')



# https://github.com/fjean/pymeanshift
import cv2
import pymeanshift as pms
import matplotlib.pyplot as plt
import pandas
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import itertools
from PIL import Image
imgPath = 'C:\\Users\\LG\\Desktop\\3.jpg'
img = cv2.imread(imgPath)
img = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)

(segmented_image, labels_image, number_regions) = pms.segment(img, spatial_radius=20, range_radius=20 , min_density=300)

### Show graph ###
plt.figure()
x = img[:,:,0].flatten()
y = img[:,:,1].flatten()

seg = segmented_image[:,:,0:2]
# 리스트를 tuple로 변환하고 중복 제거
make = list(itertools.chain.from_iterable(seg))
mode = list(map(tuple, make))
mode = list(set(mode))
mode = np.array(mode)
# print(mode)
# print(mode[:,0])

xseg = segmented_image[:,:,0].flatten()

xx = mode[:,0]
yy = mode[:,1]

indice = [0] # 색이 바뀌는 지점 index
count=0
temp=xseg[0]
for i in xseg:
    if temp==i:
        count+=1
    else:
        indice.append(count)
        count+=1
    temp = i

xseg=np.array(xseg)
color = ['r', 'g', 'b', 'y', 'c', 'm', 'k','orange','darkgoldenrod','lawngreen','deeppink','pink','maroon','skyblue','slateblue','brown','gold','tomato','aqua','navy','steelblue']

# unique 순번에 따라 색 순번 매김
j = 0
unique = np.unique(xx) # 이부분 필요없는데 그냥 색 순서 바껴서 함
unique = list(unique)
for j in range(len(indice)-1):
    num = unique.index(xseg[indice[j]])
    # while num > 6:
    #     num-=7
    plt.scatter(x[indice[j]:indice[j+1]],y[indice[j]:indice[j+1]],s=1, c=color[num])
    # print('index:',indice[j],indice[j+1])
    # print('value:',xseg[indice[j]:indice[j+1]])
    # print('========')
num = unique.index(xseg[indice[j+1]])
plt.scatter(x[indice[j+1]:],y[indice[j+1]:],s=1, c=color[num])
plt.scatter(mode[:,0],mode[:,1],marker='o',s=10,c='black')
plt.title('mean_shift clustering')
plt.show()


segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_LAB2RGB)
cv2.imshow('segmented',segmented_image)
cv2.waitKey()
print('number of clusters:',number_regions)
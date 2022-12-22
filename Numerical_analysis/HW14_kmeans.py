import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas
import itertools

imgPath = 'C:\\Users\\LG\\Desktop\\1.jpg'
img = cv2.imread(imgPath)
img = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)


Z = img.reshape((-1,3))
# convert to np.float32
Z = np.float32(Z)
# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 6
ret,label,center=cv2.kmeans(Z,K,None,criteria,100,cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]

res2 = res.reshape((img.shape))

### Show graph ###
plt.figure()
x = img[:,:,0].flatten()
y = img[:,:,1].flatten()

seg = res2[:,:,0:2]
# 리스트를 tuple로 변환하고 중복 제거
make = list(itertools.chain.from_iterable(seg))
mean = list(map(tuple, make))
mean = list(set(mean))
mean = np.array(mean)

xseg = res2[:,:,0].flatten()

xx = mean[:,0]
yy = mean[:,1]

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

j = 0
unique = np.unique(xx)
unique = list(unique)
print(len(indice)-1)
for j in range(len(indice)-1):
    num = unique.index(xseg[indice[j]])
    # while num > 6:
    #     num-=7
    plt.scatter(x[indice[j]:indice[j+1]],y[indice[j]:indice[j+1]],s=1, c=color[num])
    a+=1

num = unique.index(xseg[indice[j+1]])
plt.scatter(x[indice[j+1]:],y[indice[j+1]:],s=1, c=color[num])
plt.scatter(mean[:,0],mean[:,1],marker='o',s=10,c='black')
plt.title('k-means clustering')
plt.show()


res2 = cv2.cvtColor(res2, cv2.COLOR_LAB2RGB)
cv2.imshow('res2',res2)
cv2.waitKey(0)
cv2.destroyAllWindows()
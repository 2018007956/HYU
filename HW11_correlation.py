import cv2
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

path = 'C:\\Users\\LG\\Desktop\\colorimage\\3.jpg'
img = cv2.imread(path,cv2.IMREAD_COLOR)

b,g,r = cv2.split(img)

# 가로, 세로 픽셀을 0으로 채우고, 채널을 빨강, 초록, 파랑으로
# zeros = np.zeros(img.shape[:2], dtype = "uint8")
# cv2.imshow('Red',cv2.merge([zeros, zeros, r]))
# cv2.waitKey()
# cv2.imshow('Green',cv2.merge([zeros, g, zeros]))
# cv2.waitKey()
# cv2.imshow('Blue',cv2.merge([b, zeros, zeros]))
# cv2.waitKey()

# print(r)
# 연관성 그래프로 표현해보기

# plt.scatter(g,c='g')
# plt.show()

b = b.flatten()
g = g.flatten()
r = r.flatten()

# RGB correlation coefficients
df = pd.DataFrame({'g':g, 'r':r})
df2 = pd.DataFrame({'g':g, 'b':b})
df3 = pd.DataFrame({'r':r, 'b':b})

corr = df.corr(method = 'pearson')
corr2 = df2.corr(method = 'pearson')
corr3 = df3.corr(method = 'pearson')


# print(corr)
# print()
# print(corr2)
# print()
# print(corr3)
# print()

# YUV correlation coefficients
img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

y,u,v = cv2.split(img_yuv)

# cv2.imshow('Y',y)
# cv2.waitKey()
# cv2.imshow('U',u)
# cv2.waitKey()
# cv2.imshow('V',v)
# cv2.waitKey()

y = y.flatten()
u = u.flatten()
v = v.flatten()

df = pd.DataFrame({'y':y, 'u':u})
df2 = pd.DataFrame({'y':y, 'v':v})
df3 = pd.DataFrame({'u':u, 'v':v})
corr = df.corr(method = 'pearson')
corr2 = df2.corr(method = 'pearson')
corr3 = df3.corr(method = 'pearson')
# print(corr)
# print()
# print(corr2)
# print()
# print(corr3)

# dff = pd.DataFrame({'g':g,'y':y})
# corrr = dff.corr(method = 'pearson')
# print(corrr)


# img = [cv2.imread(i,cv2.IMREAD_COLOR) for i in glob.glob(path)]
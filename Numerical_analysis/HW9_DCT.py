import cv2
import numpy as np

def select(orig):
    s = orig.shape
    orig = orig.flatten()
    absorig = np.abs(orig)
    # 절댓값이 최대인 값 16개 찾기 -> 16개 추출 후 새로 생성
    select_orig = np.zeros(orig.shape)
    for _ in range(16):
        m=absorig.argmax()
        select_orig[m]=orig[m]
        absorig[m]=0

    select_orig = select_orig.reshape(s)
    return select_orig

def blocking(orig,x,y):
    return orig[16*x : 16*(x+1),16*y : 16*(y+1)]

img = cv2.imread("C:\\Users\\LG\\Desktop\\5.jpg").astype('float32')
r,g,b=cv2.split(img)

A=[r,g,b]
B=[]
for i in range(3):
    c = []
    for y in range(b.shape[1] // 16):
        r = []
        for x in range(b.shape[0] // 16):
            block = blocking(A[i], x, y)
            bdct = cv2.dct(block)
            select_dct=select(bdct)
            # print(bdct)
            # print('----------------')
            # print(select_dct)
            # print('----------------')
            idct = cv2.idct(select_dct).astype('int')
            # print(idct)
            # print('==============')
            if len(r)==0:
                r=idct
            else:
                r=np.vstack([r,idct])
        if len(c)==0:
            c=r
        else:
            c=np.hstack([c,r])
    B.append(c) # r,g,b
im = cv2.merge((B[0],B[1],B[2]))
#print(im)
print(img-im)
cv2.imwrite("C:\\Users\\LG\\Desktop\\55.png",im)



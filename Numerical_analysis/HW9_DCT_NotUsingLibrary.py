# open library 안쓰고 DCT/IDCT 해보기
import cv2
import numpy as np
import time
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

def C(u):
    if u==0:
        return 1/np.sqrt(2)
    else:
        return 1

def DCT(S):
    F = np.zeros((16,16))
    for v in range(16):
        for u in range(16):
            sum=0
            for y in range(16):
                for x in range(16):
                    sum += S[y][x] * np.cos((2*y+1) * v * np.pi / 32) * np.cos((2*x+1) * u * np.pi / 32)
            F[v][u] =  1/8 * C(v) * C(u) * sum
    return F


def IDCT(F):
    S = np.zeros((16,16))
    for y in range(16):
        for x in range(16):
            sum=0
            for v in range(16):
                for u in range(16):
                    sum += C(u) * C(v) * F[v][u] * np.cos((2*y+1) * v * np.pi / 32) * np.cos((2*x+1) * u * np.pi / 32)
            S[y][x] = 1/8 * sum
    return S.astype(np.int)



img = cv2.imread("C:\\Users\\LG\\Desktop\\1.jpg").astype('float32')
r,g,b=cv2.split(img)

A=[r,g,b]
B=[]
start = time.time()
for i in range(3):
    c = []
    for y in range(b.shape[1] // 16):
        r = []
        for x in range(b.shape[0] // 16):
            bdct = DCT(blocking(A[i], x, y))
            select_dct=select(bdct)
            idct=IDCT(select_dct)
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
print(img-im)
print('time:',time.time()-start)
cv2.imwrite("C:\\Users\\LG\\Desktop\\11.png",im)
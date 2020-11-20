import cv2
import glob
import numpy as np
from matplotlib import pyplot as plt
import random
import os

path = 'C:\\Users\\LG\\Desktop\\pattern\\*.jpg'
images = [cv2.imread(i,cv2.IMREAD_GRAYSCALE) for i in glob.glob(path)]

name = [os.path.basename(i) for i in glob.glob(path)]

img_num = 0
criteria_mask = []
cmaxarg= [[0 for col in range(5)] for row in range(20)] # 4열 20행
cvalue= [[0 for col in range(5)] for row in range(20)]
cmagnitude=[]
save=[]
min_threshold=[]
max_threshold=[]
for img in images:

    h, w = img.shape
    dft = cv2.dft(np.float32(img[h//2-32:h//2+32, w//2-32:w//2+32]),flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

    save.append(magnitude[33:50,33:50].flatten())

    plt.subplot(121), plt.imshow(img[h // 2 - 32:h // 2 + 32, w // 2 - 32:w // 2 + 32], cmap='gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(magnitude, cmap='gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.show()

    img_num+=1

path = 'C:\\Users\\LG\\Desktop\\pattern\\*.jpg'
images = [cv2.imread(i,cv2.IMREAD_GRAYSCALE) for i in glob.glob(path)]

img_num = 0
hit_num = 0
for testimg in images:
    print('<',name[img_num],'>')

    h,w = testimg.shape
    result = []
    # 이미지 하나당 5번씩
    for n in range(5):
        # 랜덤한 64x64 block 추출
        x = random.randrange(h-64) # 1부터 가로 사이즈 -64 사이의 난수 생성
        y = random.randrange(w-64)
        print('{}:{}, {}:{}'.format(x,x+63,y,y+63))
        mask = testimg[x:x+64,y:y+64]

        dft2 = cv2.dft(np.float32(mask), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft2[0, 0] = 0
        dft_shift2 = np.fft.fftshift(dft2)

        magnitude2 = 20 * np.log(cv2.magnitude(dft_shift2[:, :, 0], dft_shift2[:, :, 1]))
        # plt.subplot(121), plt.imshow(mask, cmap='gray')
        # plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(magnitude2, cmap='gray')
        # plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        # plt.show()

        # ## <pattern recognition>
        # print(magnitude2[32,32]) # DC 성분 위치
        a=magnitude2[33:50,33:50].flatten()

        b=[]
        for i in range(20):
            b.append(np.mean(np.abs(save[i]-a))) # 비교

        idx = np.argmin(b)
        result.append(name[idx])

    print(result)

    # 적중률 계산
    if len(result)!=0:
        for n in range(5):
            if result[n] == name[img_num]:
                hit_num += 1

    img_num += 1

print('100번의 횟수 중 패턴을 잘 인식한 횟수:',hit_num)

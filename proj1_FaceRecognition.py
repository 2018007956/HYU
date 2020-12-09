import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np

def createDataMatrix(images):
    print('creating data matrix',end=' ... ')
    '''
    Allocate space for all images in one data matrix
        The size of the data matrix is
        ( w * h * 3, numImages )

        where,

        w = width of an image in the dataset
        h = height of an image in the dataset
        3 is for the 3 color channels
    '''
    numImages = len(images)
    sz = images[0].shape
    data = np.zeros((numImages, sz[0] * sz[1]), dtype=np.float32)
    for i in range(numImages):
        image = images[i].flatten()
        data[i,:] = image
    print('DONE')
    return data


path = 'C:\\Users\\LG\\Desktop\\grayfaces\\*.jpg'
img = [cv2.imread(file,cv2.IMREAD_GRAYSCALE) for file in glob.glob(path)]   # 흑백사진이지만, 흑백으로 읽어와야 RGB값 3개가 안나온다
img = np.array(img)
mean = img.mean(axis=0).astype("int")#face image들의 mean vector(0~255에 해당하는벡터)를 구해서
A = img - mean # 각 face img에 mean vector를 빼면 ak라는 벡터가 만들어짐
A = createDataMatrix(A)
matA =A.T @ A # covariance matrix
U, s, V = np.linalg.svd(matA, full_matrices=True)

S = np.zeros(matA.shape)
for i in range(len(s)):
    S[i][i] = s[i]
appA = U @ S @ V

'''appA-> 1024차원의 0~255의 int값들을 제곱하고(A.T@A) 더하니까
평균적으로 intensity가 100이라 하더라도 100^2이고, 여기에 1024가 되니까 (mean벡터를 빼도) 
백만 천만단위로 나온다'''

# test face recognition
standard = img[5]
standard2 = img[1] # 차이값이 큰 두 이미지를 fixed해서 영향없는 벡터 0으로 만들어줌
test_Face = standard - mean
test_Face2 = standard2 - mean
test_Face = test_Face.flatten()
test_Face2 = test_Face2.flatten()

testFace = img[3]
testFace2 = img[4] # test할 두 이미지 선택
testFaceMS = testFace - mean
testFaceMS2 = testFace2 - mean
testFaceMS = testFaceMS.flatten()
testFaceMS2 = testFaceMS2.flatten()
mean = mean.flatten()
r_list = [25, 50, 100, 200, 400, 800, 1600]
for r in r_list:
    # find the coeffiecients
    makingzero = (U[:,:r].T @ test_Face).astype("int")
    makingzero2 = (U[:,:r].T @ test_Face2).astype("int")

    coefficients = (U[:, :r].T @ testFaceMS).astype("int")
    coefficients2 = (U[:, :r].T @ testFaceMS2).astype("int")
    # print('1 :',coefficients)
    # print('2 :',coefficients2)
    # print('1-2 :',coefficients - coefficients2)

    zero=[]
    for i in range(len(coefficients)):
        if abs(coefficients[i] - coefficients2[i])<20:
            zero.append(i)

    for i in range(len(zero)):
        z = zero.pop()
        coefficients[z]=0
        coefficients2[z]=0
    # print(coefficients-coefficients2)
    # print('rank :',r)
    distance = 0
    for i in range(len(coefficients)):
        distance += coefficients[i]**2
    # print('image 1) distance :',distance)
    distance2 = 0
    for i in range(len(coefficients2)):
        distance2 += coefficients2[i]**2
    # print('image 2) distance :',distance2)
    # print('distance difference :',abs(distance-distance2))


    # generate face image using eigenfaces
    reconFace = mean + U[:,:r]  @ coefficients
    img = plt.imshow(np.resize(reconFace, (32, 32)))
    img.set_cmap('gray')
    plt.title('r = ' + str(r))
    plt.axis('off')
    plt.show()

    reconFace2 = mean + U[:, :r] @ coefficients2
    img = plt.imshow(np.resize(reconFace2, (32, 32)))
    img.set_cmap('gray')
    plt.title('r = ' + str(r))
    plt.axis('off')
    plt.show()

if abs(distance-distance2)<600000:
    print('두 사람은 같은 사람입니다.')
else:
    print('두 사람은 다른 사람입니다.')



import os
import glob
import cv2 # OpenCV, 이미지 처리 라이브러리
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
eye_casecade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_eye.xml')

path = 'C:\\Users\\LG\\Desktop\\nnn\\*.jpg'
img = [cv2.imread(file) for file in glob.glob(path)]
name = [os.path.basename(file) for file in glob.glob(path)]
gray_img=[]
face=[]
cropped_img=[]
resize_img=[]
eyes=[]
for i in range(len(img)):
    gray_img.append(cv2.cvtColor(img[i], cv2.COLOR_BGR2GRAY))
    face.append(face_cascade.detectMultiScale(gray_img[i],scaleFactor=1.1, minNeighbors=1, minSize=(50, 50)))
    if len(face[i])==1: # 얼굴이 1개로 인식된것만 수행
        for (x,y,w,h) in face[i]:
            cropped_img.append(gray_img[i][y:y+h, x:x+w])
            resize_img.append(cv2.resize(cropped_img[i],(32,32)))
            cv2.imwrite("C:\\Users\\LG\\Desktop\\new2\\%s"%(name[i]),resize_img[i])
    else:
        cropped_img.append(None)
        resize_img.append(None)
        eyes.append(None)

'''
img=cv2.imread(file)을 하면 이미지들이 row vecter형태로 들어가고 2차원벡터가 된다. 10개 이미지의 img를 직접 표현해보면
[img1벡터값]  [img1벡터값]    ...     [img1벡터값]
[img10벡터값] [img10벡터값]   ...     [img10벡터값]
[img2벡터값]  [img2벡터값]    ...     [img2벡터값]
.
.
.
[img9벡터값]  [img9벡터값]    ...     [img9벡터값]
'''

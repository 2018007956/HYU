import numpy as np
import os
import glob
import cv2 # OpenCV, 이미지 처리 라이브러리
# 이미지 크기 변경
from PIL import Image

path = 'C:\\Users\\LG\\Desktop\\fabric_pattern\\10.jpg'
# for i in os.listdir(path):
img = Image.open(path)
resize_img=img.resize((200,200))
resize_img.save("C:\\Users\\LG\\Desktop\\fabric_pattern\\10.jpg")

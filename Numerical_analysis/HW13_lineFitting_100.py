# HW13_lineFitting.py 파일을 100번 반복하고 그래프 표현
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# y = 2x-1
Points = [[-5,-11.0], [-4,-9], [-3,-7], [-2,-5], [-1,-3], [0,0], [1,1], [2,3], [3,5], [4,7], [5,9], [6,11]]

print_E=[]
print_X=[]
print_d=[]
better=0
worse=0
plt.figure()
for q in range(100):
    Points = np.array(Points)
    '''### Line fitting using whole 12 samples ###'''
    P = Points.copy()  # list P : noise가 섞인 좌표값
    for i in range(len(Points)):
        n = random.gauss(0, 2)
        P[i][1] = P[i][1] + n

    # line fitting
    P = np.array(P)
    line_fitter = LinearRegression()
    line_fitter.fit(P[:, 0].reshape(-1, 1), P[:, 1])

    ## Calculate the error
    diff_E = sum(np.abs(Points[:, 1] - line_fitter.predict(P[:, 0].reshape(-1, 1))))
    print_d.append(diff_E)

    '''### Line fitting using RANSAC ###'''
    E = []
    LeastSquare=[]
    graph_num = 0
    for j in range(3):
        # 1. Randomly select 6 samples from 12 points
        Points = list(Points)
        sixList = random.sample(Points, 6) # sample을 6개 뽑고
        sixList = np.array(sixList)
        sampleList = np.zeros(sixList.shape) # noise 섞기
        for i in range(len(sixList)):
            n = random.gauss(0, 2)
            sampleList[i][0] = sixList[i][0]
            sampleList[i][1] = sixList[i][1] + n
        sampleList = np.array(sampleList)
        sample_x = sampleList[:,0]
        sample_y = sampleList[:,1]

        # 2. Find the fitted line using 6 samples and least square
        line_fitter.fit(sample_x.reshape(-1,1),sample_y)

        # 3. Calculate the error
        sixList = np.array(sixList)
        diff = sum(np.abs(sixList[:,1] - line_fitter.predict(sample_x.reshape(-1,1)))) # 파란그래프 - 빨간그래프

        # 4. Compare the current error with previous error
        # 처음엔 무조건 넣어주고, 이후 값들은 리스트의 최소값보다 작을때만 저장
        if len(E) == 0:
            E.append(diff)
        else:
            if np.min(E) > diff:
                # del E[0] # 이전 값 지워도 되는데 그냥 쌓음
                E.append(diff)
                graph_num = j

    print_E.append(E[-1])
    print_X.append(q)
    if diff_E > E[-1]:
        better+=1
    else:
        worse+=1

plt.scatter(print_X, print_d, color='blue')
plt.plot(print_X, print_d, color='blue')
plt.scatter(print_X, print_E, color='orange')
plt.plot(print_X, print_E, color='orange')
plt.show()

print('100번 중 RANSAC을 사용했을 때 더 좋은 결과 나온 횟수 :',better)
print('100번 중 RANSAC을 사용했을 때 더 안 좋은 결과 나온 횟수 :',worse)
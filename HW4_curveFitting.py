import numpy as np
import numpy.linalg as linalg
import random
import matplotlib.pyplot as plt

# sample data list
data = [[-2.9, 35.4],
    [-2.1, 19.7],
    [-0.9, 5.7],
    [1.1, 2.1],
    [0.1, 1.2],
    [1.9, 8.7],
    [3.1, 25.7],
    [4.0, 41.5]]

# 리스트에서 랜덤으로 6개의 값을 추출하고 행렬로 만든다
sampleList = random.sample(data, 6)
matrix = np.array(sampleList)
print('Randomly select 6 points:')
print(sampleList)

# Matrix A 만들기
# data matrix의 1열 추출
a = matrix[:, 0]
# 2 열 추출 (벡터b)
b = matrix[:, 1]

A1 = np.array((a)*(a))
A2 = np.array(a)
A3 = np.ones((6,1))

A = np.column_stack([A1,A2,A3])
print('matrix A:')
print(A)

# pseudoinverse of A :(A.T * A)^(-1) * A.T
# x = pseudoinverse of A * b
p = linalg.pinv(A)
x = np.dot(np.array(p),b)
print('x:',x) # x = [a b c]

# matlab으로 y=ax^2+bx+c 그래프 그리기
a = np.linspace(-5, 5)
b= x[0]*(a**2) + x[1]*a + x[2]
plt.ylim(0,50)
plt.plot(a,b,'r')

# sample data 좌표 표시
plt.scatter(matrix[:,0],matrix[:,1])

#plt.show()


# error 구하기
def f(a):
    return x[0]*(a**2) + x[1]*a + x[2]

b = matrix[:, 1]
g = list()
for i in matrix[:, 0]:
    g.append(f(i))
print('b:',b)
print('g:',g)
g = np.array(g)

# error
error = (b-g)**2
print('error: ',end='')
e = 0
for i in range(6):
    e += error[i]
print(e)
import random
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(12,5))
ax1 = fig.add_subplot(1,2,1, projection='3d')
ax2 = fig.add_subplot(1,2,2)
color = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta'] # y: yellow, c: cyan청록, m:magenta자홍색

mean=[]
save=[]
max_dist=[]
for i in range(5):
    # 정한 범위에서 6개 랜덤 추출(중복 허용)
    r = [random.choice(range(1,10)) for j in range(6)]
    coor = [random.choice(range(1,50)) for j in range(3)] # 가우시안 분포를 하기위해 중심잡아주는 좌표 생성
    print('X:({},{}) Y:({},{}) Z:({},{})'.format(r[0],r[1],r[2],r[3],r[4],r[5]))
    X = [coor[0]+random.gauss(r[0], r[1]) for j in range(300)]
    Y = [coor[1]+random.gauss(r[2], r[3]) for j in range(300)]
    Z = [coor[2]+random.gauss(r[4], r[5]) for j in range(300)]
    ax1.scatter(X, Y, Z, c=color[i])
    ax2.scatter(X, Y, c=color[i])
    save.append([coor,r])

    # mean vector
    mean = list(mean)
    mean.append([np.mean(X),np.mean(Y),np.mean(Z)])
    print('mean: {:.2f}, {:.2f}, {:.2f}'.format(mean[-1][0],mean[-1][1],mean[-1][2]))
    print()
    mean = np.array(mean)
    dist = []
    for j in range(300):
        dist.append(np.abs(mean[i,0] - X[j]) + np.abs(mean[i,1] - Y[j]) + np.abs(mean[i,2] - Z[j]))
    max_dist.append(np.max(dist))


ax1.scatter(mean[:,0],mean[:,1],mean[:,2], c='black',s=30)
ax2.scatter(mean[:,0],mean[:,1], c='k',s=30)
# plt.show()


# ## Testing with new vectors
print('===',save)
print('mean:',mean)
print('max dist:',max_dist)
mean = np.array(mean)
# 각 클러스터마다 100개씩 뽑아서 잘 assign되는지 확인
for i in range(5):
    X = [mean[i][0]+random.gauss(save[i][1][0], save[i][1][1]) for j in range(100)]
    Y = [mean[i][1]+random.gauss(save[i][1][2], save[i][1][3]) for j in range(100)]
    Z = [mean[i][2]+random.gauss(save[i][1][4], save[i][1][5]) for j in range(100)]
    # 각 mean들과 비교
    right = 0
    wrong = 0
    out_bound = 0
    point =[]
    for j in range(100):
        dist = np.abs(mean[:,0] - X[j]) + np.abs(mean[:,1] - Y[j]) + np.abs(mean[:,2] - Z[j])
        m = np.argmin(dist) # 클러스터링
        point.append(m)
        # 해당 클러스터로 인식되고, 적당한 범위 안에 존재하는지 (뒤 조건은 인식률을 올려주기 위함)- 비교
        # 모든 클러스터에 out bound인지 확인
        if dist[m] > np.max(max_dist) - np.max(max_dist) //3:
            out_bound +=1
        # 최소거리인 클러스터에서 out bound인지 확인
        else:
            if m == i and dist[m] < max_dist[i] - max_dist[i] // 3:
                right += 1
            elif m == i and dist[m] > max_dist[i] - max_dist[i] // 3:
                out_bound += 1
            elif m != i and dist[m] < max_dist[m] - max_dist[m] // 3:
                wrong += 1
            elif m != i and dist[m] > max_dist[m] - max_dist[m] // 3:
                out_bound += 1
    print('{}:{}) right: {} wrong: {} out_bound: {}'.format(i,color[i],right,wrong,out_bound))
    print(point)
    print('mixed cluster: ',np.unique(point))
    print()


# 클러스터에 속하지 않는 새로운 샘플데이터 100개를 뽑아서 클러스터링 해봄
save = np.array(save)
coor = save[:,0]

x = [x[0] for x in coor]
y = [y[0] for y in coor]
z = [z[0] for z in coor]

rand = random.randint(50,55)
while rand in x: # x에 없는 숫자일때까지 계속 랜덤 숫자 생성
    rand = random.randint(50,55)
newX = rand

rand = random.randint(50,55)
while rand in y: # x에 없는 숫자일때까지 계속 랜덤 숫자 생성
    rand = random.randint(50,55)
newY = rand

rand = random.randint(50,55)
while rand in z: # x에 없는 숫자일때까지 계속 랜덤 숫자 생성
    rand = random.randint(50,55)
newZ = rand

r = [random.choice(range(1,10)) for j in range(6)]
X = [newX+random.gauss(r[0], r[1]) for j in range(100)]
Y = [newY+random.gauss(r[2], r[3]) for j in range(100)]
Z = [newZ+random.gauss(r[4], r[5]) for j in range(100)]
print('X:({},{}) Y:({},{}) Z:({},{})'.format(r[0],r[1],r[2],r[3],r[4],r[5]))
ax1.scatter(X, Y, Z, c=color[-1])
ax1.scatter(newX, newY, newZ, c='black',s=30)
ax2.scatter(X, Y, c=color[-1])
ax2.scatter(newX, newY, c='black',s=30)
print('mean: {:.2f}, {:.2f}, {:.2f}'.format(np.mean(X), np.mean(Y), np.mean(Z)))
plt.show()

# 각 mean들과 비교
right = 0
wrong = 0
out_bound = 0
point =[]
for j in range(100):
    dist = np.abs(mean[:, 0] - X[j]) + np.abs(mean[:, 1] - Y[j]) + np.abs(mean[:, 2] - Z[j])
    m = np.argmin(dist) # 클러스터링
    point.append(m)

    if dist[m] > max_dist[m] - max_dist[m] // 3:
        out_bound += 1
    else:
        wrong += 1
print('new samples:magenta) wrong:',wrong, 'out_bound:',out_bound)
print(point)
print('mixed cluster: ',np.unique(point))
print()


import random
import matplotlib.pyplot as plt
import numpy as np

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# color = ['r', 'g', 'b', 'y', 'c'] # y: yellow, c: cyan청록
# mean=[]
# save=[]
# maximum_distance=[]
# for i in range(5):
#     # 정한 범위에서 6개 랜덤 추출(중복 허용)
#     r = [random.choice(range(1,10)) for j in range(6)]
#     coor = [random.choice(range(1,50)) for j in range(3)] # 가우시안 분포를 하기위해 중심잡아주는 좌표 생성
#     print('X:({},{}) Y:({},{}) Z:({},{})'.format(r[0],r[1],r[2],r[3],r[4],r[5]))
#     X = [coor[0]+random.gauss(r[0], r[1]) for j in range(300)]
#     Y = [coor[1]+random.gauss(r[2], r[3]) for j in range(300)]
#     Z = [coor[2]+random.gauss(r[4], r[5]) for j in range(300)]
#     ax.scatter(X, Y, Z, c=color[i])
#     save.append([coor,r])
#
#     # mean vector
#     mean = list(mean)
#     mean.append([np.mean(X),np.mean(Y),np.mean(Z)])
#     print('mean:',mean[-1])
#     print()
#
#     mean = np.array(mean)
#     for j in range(300):
#         dist = np.abs(mean[:,0] - X[j])
#     maximum_distance.append(np.max(dist))
#
#
# ax.scatter(mean[:,0],mean[:,1],mean[:,2], c='black',s=30)
# plt.show()

# (compare)
save = [[[22, 38, 11], [3, 3, 3, 6, 9, 2]], [[6, 11, 33], [2, 1, 2, 2, 7, 9]], [[18, 43, 4], [7, 5, 8, 9, 1, 8]], [[46, 44, 13], [6, 9, 3, 6, 6, 3]], [[11, 49, 24], [8, 9, 4, 9, 3, 5]]]
maximum_distance = [3.6862028054906446, 17.057821686984454, 11.965401504221711, 49.80867382394615, 46.532879242442334]
mean = [[25.01889853, 41.14155782, 20.12254908],[ 7.88239543, 12.88988418, 39.97680487],[25.09468381, 50.63206204,  5.4408023 ],[51.41488036, 47.02662234, 19.15842535],[19.51486642, 52.47354175, 26.78940188]]

## Testing with new vectors
mean =list(mean)
print('===',save)
print('max dist:',maximum_distance)
print('mean:',mean)
print('### Testing ###')
mean = np.array(mean)
# 각 클러스터마다 100개씩 뽑아서 잘 assign되는지 확인
for i in range(5):
    X = [save[i][0][0]+random.gauss(save[i][1][0], save[i][1][1]) for j in range(100)]
    Y = [save[i][0][1]+random.gauss(save[i][1][2], save[i][1][3]) for j in range(100)]
    Z = [save[i][0][2]+random.gauss(save[i][1][4], save[i][1][5]) for j in range(100)]

    # 각 mean들과 비교
    right = 0
    wrong = 0
    out_bound = 0
    point =[]
    for j in range(100):
        dist = np.abs(mean[:,0] - X[j])
        m = np.argmin(dist) # 클러스터링
        point.append(m)
        # 해당 클러스터로 인식되고, 적당한 범위 안에 존재하는지 (뒤 조건은 인식률을 올려주기 위함)- 비교
        if m==i:
            # m==i 만 했을때 보다 wrong 비율낮음
            if dist[m] < maximum_distance[i]-maximum_distance[i]//2:
                right += 1
            else:
                out_bound+=1
        else:
            wrong+=1
    print(i,') right:',right, 'wrong:',wrong, 'out_bound:',out_bound)
    print(point)
    print('mixed cluster: ',np.unique(point))
    print()


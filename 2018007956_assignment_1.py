def bestPath(visited,i,j):
    visited.pop()
     # 목적지 다음 마지막 값부터 5로 바꿈
    length = 1 # 최단 경로 개수
    time =1 # 탐색 노드 개수
    while len(visited) > 0:
        n = visited[-1]  # 리스트의 마지막값 (가지고있는 좌표중 goal가 가장 가까움)
        # goal부터 끝까지 거슬러 올라가며 best path 판별
        if n == [i - 1, j] or n == [i, j - 1] or n == [i + 1, j] or n == [i, j + 1]:
            # 아래 세줄은 목적지를 5가아닌 4로 그대로 표현해주기 위함
            if maze[i][j] == 4:
                [i,j] = visited.pop()
                length-=1
                time-=1
                continue
            maze[i][j] = 5
            [i, j] = visited.pop()
            length+=1
            time+=1
        else:
            visited.pop()
            time+=1
    return length,time

def bfs(maze,k,m,n,key,goal):
    visited = []
    queue = [[0, 1]]  # 시작 노드 추가/ 방문이 필요한 노드들에 대한 정보 (Fringe : 노드가 나오긴 했지만 아직 펼쳐지지 않은 노드들)

    while queue:
        [i, j] = queue.pop(0)
        visited.append([i, j])

        if [i,j]==goal:
            # 최적 경로 표현
            length,time=bestPath(visited, i, j)
            # 파일 출력
            file = open('C:\\Users\\LG\\Desktop\\Artificial_Intelligence_assignment_1\\Maze_%d_BFS_output.txt'%(k),'w')
            for a in maze:
                for b in a:
                    file.write(str(b))
                file.write('\n')
            file.write('---\n')
            file.write('length='+str(length)+'\n') # distance[i][j]=length 같음 distance굳이 쓸 필요X
            file.write("time="+str(time))
            file.close()
            break


        # 상하좌우 탐색
        # 아래 노드 탐색
        # 방문한 적이 없고 방문한 노드의 인접노드라 리스트에 들어간적 없는 노드-> 완전 new node
        if i < m - 1 and maze[i + 1][j] != 1 and [i + 1, j] not in visited and [i + 1, j] not in queue:
            queue.append([i + 1, j])
        # 오른쪽 노드 탐색
        if j < n - 1 and maze[i][j + 1] != 1 and [i, j + 1] not in visited and [i, j + 1] not in queue:
            queue.append([i, j + 1])
        # 왼쪽 노드 탐색
        if j > 0 and maze[i][j - 1] != 1 and [i, j - 1] not in visited and [i, j - 1] not in queue:
            queue.append([i, j - 1])
        # 위 노드 탐색
        if i > 0 and maze[i - 1][j] != 1 and [i - 1, j] not in visited and [i - 1, j] not in queue:
            queue.append([i - 1, j])



# =======================================================================================
# Iterative deepening search

never =[]
#루프에 빠진 경우(고립된경우)
def stuck(i,j,length,time, data):
    maze[i][j] = 2
    length -= 1
    # pop 후에는 다른 방향으로 가야함 -> never list 사용
    # 전 상태가 왼,오로 이동하던 것이었다면
    if [i,j-1] == data[-1] or [i,j+1] == data[-1]:
        while len(data)>1 and data[-1][0] == data[-2][0]: # 스택에 최소2개는 있어야 비교가능
            n=data.pop()
            never.append(n)
            maze[n[0]][n[1]] = 2
            length-=1
            # 왼,오로 pop하던도중 위아래로 탐색가능한 노드가 존재한다면
            # 즉 pop된 노드 주위에 탐색할 경로가 있으면 never에 안들어가고 탐색해줌
            if maze[n[0]+1][n[1]]!=1 and [n[0]+1,n[1]] not in data and [n[0]+1,n[1]] not in never:
                data.append([n[0]+1,n[1]])
                length+=1
                time+=1
            elif maze[n[0]-1][n[1]]!=1 and [n[0]-1,n[1]] not in data and [n[0]-1,n[1]] not in never:
                data.append([n[0]-1,n[1]])
                length += 1
                time += 1
            if data[-1][0] == data[-2][0]:
                never.append([i, j])
                return length,time
        else:
            never.append([i,j])

    # 전 상태가 위아래로 이동하던 것이었다면
    if [i-1,j] == data[-1] or [i+1,j] == data[-1]:
        while len(data)>1 and data[-1][1] == data[-2][1]:
            n=data.pop()
            never.append(n)
            maze[n[0]][n[1]]=2
            length -= 1
            if maze[n[0]][n[1]+1] != 1 and [n[0], n[1]+1] not in data and [n[0], n[1]+1] not in never:
                data.append([n[0], n[1]+1])
                length += 1
                time += 1
            elif maze[n[0]][n[1]-1] != 1 and [n[0], n[1]-1] not in data and [n[0], n[1]-1] not in never:
                data.append([n[0], n[1]-1])
                length += 1
                time += 1
            if data[-1][1] == data[-2][1]:
                never.append([i,j])
                return length,time
        else:
            never.append([i,j])
    return length,time


def ids_Clockwise(i,j,length,time, stack, limit):
    # 시계 방향으로 탐색 12시->3시->6시->9시
    # 위 노드 탐색 (1이 아닌 2 또는 6 또는 4일때만 탐색)
    prestack = stack.copy()
    while i > 0 and maze[i - 1][j] != 1 and [i - 1, j] not in stack and [i - 1, j] not in never:
        stack.append([i - 1, j])
        maze[i][j] = 5
        length+=1
        time+=1
        i-=1
    # 오른쪽 노드 탐색
    while j <= limit and j<n-1 and maze[i][j+1] != 1 and [i, j + 1] not in stack and [i, j + 1] not in never:
        stack.append([i, j + 1])
        maze[i][j] = 5
        length += 1
        time += 1
        j+=1
    # 아래 노드 탐색
    while i <= limit and i<m-1 and maze[i + 1][j] != 1 and [i + 1, j] not in stack and [i + 1, j] not in never:
        stack.append([i + 1, j])
        maze[i][j] = 5
        length += 1
        time += 1
        if [i, j] == [0, 1]:
            maze[i][j]=3
        i+=1
    # 왼쪽 노드 탐색
    while j > 0 and maze[i][j - 1] != 1 and [i, j - 1] not in stack and [i, j - 1] not in never:
        stack.append([i, j - 1])
        maze[i][j] = 5
        length += 1
        time += 1
        j-=1

    # stack에 append된게 없으면 고립된 상태이므로 방향이 같지 않을때까지 값을 pop한다 - pop된 좌표는 never에 넣는다
    if len(prestack)==len(stack):
        length,time=stuck(i,j,length,time, stack)
    return length,time


def ids(maze,k,m,n,key,goal):
    stack = [[0, 1]]

    limit = 0
    length, time=0,0
    while True:
        [i,j]=stack.pop()

        # 인접한 노드가 4라면 탐색 종료
        if [i,j]==goal:
            file = open('C:\\Users\\LG\\Desktop\\Artificial_Intelligence_assignment_1\\Maze_%d_IDS_output.txt' % (k), 'w')
            for a in maze:
                for b in a:
                    file.write(str(b))
                file.write('\n')
            file.write('---\n')
            file.write('length=' + str(length) + '\n')  # distance[i][j]=length 같음 distance굳이 쓸 필요X
            file.write("time=" + str(time))
            file.close()
            break
        else:
            limit+=1
            length,time=ids_Clockwise(i, j,length,time, stack, limit)



# =======================================================================================
# Greedy best first search
class MinHeap(object):
    def __init__(self):
        self.queue = [None]

    def insert(self, n):
        # 맨 마지막에 삽입할 원소를 임시로 추가
        self.queue.append(n)
        last_index = len(self.queue) - 1
        # 루트로 올때까지 부모를 타고 올라가면서 크기 비교
        while 0 < last_index:
            parent_index = self.parent(last_index)
            if 0< parent_index and self.queue[parent_index] > self.queue[last_index]:
                self.swap(last_index, parent_index)
                last_index = parent_index
            else:
                break

    def delete(self):
        last_index = len(self.queue) - 1
        if last_index < 0:
            return
        self.swap(1, last_index) # 마지막 원소와 루트를 바꿔주고 (큰게위로올라오고 제일 작은 값은 밑으로 내려감)
        minv = self.queue.pop() # 마지막 원소를 제거한다 (제일 작은 값 삭제)
        self.minHeapify(1)  # root에서부터 heapify를 시작한다
        return minv

    # 임시 root값부터 자식들과 값을 비교해나가며 재정렬하는 함수
    def minHeapify(self, i):
        left_index = self.leftchild(i)
        right_index = self.rightchild(i)
        min_index = i  # 일단 가장 작은 것을 자신으로 놓고, 더 작은 값의 index를 넣어준다
        if left_index <= len(self.queue) - 1 and self.queue[left_index] < self.queue[min_index]:
            min_index = left_index
        if right_index <= len(self.queue) - 1 and self.queue[right_index] < self.queue[min_index]:
            min_index = right_index
        # 만약 자신이 가장 작은 것이 아니면 heapify
        if min_index != i:
            self.swap(i, min_index) # 자식들 중 가장 작은 것과 바꿔주고
            self.minHeapify(min_index) # recursive call을 하여 내려가서 다시 진행

    def swap(self, i, parent_index):
        if parent_index>0:
            self.queue[i], self.queue[parent_index] = self.queue[parent_index], self.queue[i]

    def parent(self, index):
        return index // 2

    def leftchild(self, index):
        return index * 2

    def rightchild(self, index):
        return index * 2 + 1


# Estimate of (optimal) cost from n to goal
# 네방향으로 이동하니까 distance의 추정값을 manhattan distance로 함
# 벽이 없다고 가정한 목적지까지의 거리를 계산
def h(n, goal):
    return abs(goal[0]-n[0]) + abs(goal[1]-n[1])

def gbfs(maze,k,m,n,key,goal):
    visited = [[0,1]]
    dic = {}
    length, time =1,1
    i,j=0,1 # 초기 시작 위치
    while True:
        stuck_num = 0
        # 방문한 적이 없고 방문한 노드의 인접노드라 리스트에 들어간적 없는 노드-> 완전 new node
        # 네 방향을 다 탐색하고, manhattan distance가 가장 작은 값을 먼저 탐색
        #print('현재위치:', [i,j])
        predic = dic.copy()
        if i < m - 1 and maze[i + 1][j] != 1 and [i + 1, j] not in visited and [i + 1, j] not in never:
            dic[i + 1, j] = h([i + 1, j], goal)
        if j < n - 1 and maze[i][j + 1] != 1 and [i, j + 1] not in visited and [i, j + 1] not in never:
            dic[i, j + 1]= h([i, j + 1], goal)
        if j > 0 and maze[i][j - 1] != 1 and [i, j - 1] not in visited and [i, j - 1] not in never:
            dic[i, j - 1]=h([i, j - 1], goal)
        if i > 0 and maze[i - 1][j] != 1 and [i - 1, j] not in visited and [i - 1, j] not in never:
            dic[(i - 1, j)]=h([i - 1, j], goal)

        mh = MinHeap()
        keydic = {}
        for key, value in dic.items():
            if list(key) not in visited:
                keydic[key] = value
                mh.insert(value)

                # stuck인 경우
                if len(predic) == len(dic):
                    stuck_num += 1
                    if len(mh.queue) > 0:
                        if stuck_num != 0:
                            for _ in range(len(mh.queue) - 1):
                                time += 1
                                tmp = mh.delete()
                                x = invkeydic.get(tmp)
                                never.append(x)
                                if x in keydic:
                                    if keydic[x] == tmp:
                                        mh.insert(tmp)
                                        never.pop()

        if len(mh.queue) == 1:  # pop할 값이 없고 none만 있는 경우
            kk = keydic.popitem()  # pop이아니라 그냥 가져만와야하므로
            keydic[kk[0]] = kk[1]  # 다시넣음
            mh.insert(dic.get(kk[0]))

        minv = mh.delete()  # 가장 작은 값 추출

        invkeydic = {v: k for k, v in keydic.items()}
        #print('```', invkeydic)
        [i, j] = invkeydic.get(minv)
        visited.append([i, j])
        #print('```', [i, j])
        length += 1
        time += 1
        #print('------',length)

        visited.append([i, j])  # 다음으로 방문할 노드 리스트에 넣음

        if [i, j] == goal:
            maze[i][j] = 4
            bestPath(visited, i, j)
            file = open('C:\\Users\\LG\\Desktop\\Artificial_Intelligence_assignment_1\\Maze_%d_GBFS_output.txt' % (k), 'w')
            for a in maze:
                for b in a:
                    file.write(str(b))
                file.write('\n')
            file.write('---\n')
            file.write('length=' + str(length) + '\n')  # distance[i][j]=length 같음 distance굳이 쓸 필요X
            file.write("time=" + str(time))
            file.close()
            break

    # 최적 경로 표현


# =======================================================================================
# A* algorithm
def a_star(maze,k,m,n,key,goal):
    visited = [[0, 1]]
    dic = {}
    length, time = 1, 1
    distance = [[0 for columns in range(n)] for rows in range(m)]  # 해당 지점까지의 거리를 담는 리스트
    distance[0][0] = 1
    i, j = 0, 1  # 초기 시작 위치
    while True:
        stuck_num = 0
        #print('현재위치:', [i, j])
        predic = dic.copy()
        if i < m - 1 and maze[i + 1][j] != 1 and [i + 1, j] not in visited and [i + 1, j] not in never:
            distance[i + 1][j] = distance[i][j] + 1
            # f = g + h
            # f = start노드부터 현재노드까지의 distance(정확한 값) + 현재노드부터 goal노드까지의 distance의 추정값(정확한 값X)
            dic[i + 1, j] = distance[i + 1][j]+ h([i + 1, j], goal)
        if j < n - 1 and maze[i][j + 1] != 1 and [i, j + 1] not in visited and [i, j + 1] not in never:
            distance[i][j + 1] = distance[i][j] + 1
            dic[i, j + 1] = distance[i][j + 1] +h([i, j + 1], goal)
        if j > 0 and maze[i][j - 1] != 1 and [i, j - 1] not in visited and [i, j - 1] not in never:
            distance[i][j - 1] = distance[i][j] + 1
            dic[i, j - 1] = distance[i][j - 1] +h([i, j - 1], goal)
        if i > 0 and maze[i - 1][j] != 1 and [i - 1, j] not in visited and [i - 1, j] not in never:
            distance[i - 1][j] = distance[i][j] + 1
            dic[(i - 1, j)] = distance[i - 1][j] + h([i - 1, j], goal)

        mh = MinHeap()
        keydic = {}
        for key, value in dic.items():
            if list(key) not in visited:
                keydic[key] = value
                mh.insert(value)
                if len(predic) == len(dic):
                    stuck_num += 1
                    if len(mh.queue) > 0:
                        if stuck_num != 0:
                            for _ in range(len(mh.queue) - 1):
                                time += 1
                                tmp = mh.delete()
                                x = invkeydic.get(tmp)
                                never.append(x)
                                if x in keydic:
                                    if keydic[x] == tmp:
                                        mh.insert(tmp)
                                        never.pop()

        if len(mh.queue) == 1:
            kk = keydic.popitem()
            keydic[kk[0]] = kk[1]
            mh.insert(dic.get(kk[0]))

        minv = mh.delete()

        invkeydic = {v: k for k, v in keydic.items()}
        #print('```', invkeydic)
        [i, j] = invkeydic.get(minv)
        visited.append([i, j])
        #print('```', [i, j])
        length += 1
        time += 1
        visited.append([i, j])
        #print('------',length)

        if [i, j] == goal:
            maze[i][j] = 4
            bestPath(visited, i, j)
            file = open('C:\\Users\\LG\\Desktop\\Artificial_Intelligence_assignment_1\\Maze_%d_A_star_output.txt' % (k), 'w')
            for a in maze:
                for b in a:
                    file.write(str(b))
                file.write('\n')
            file.write('---\n')
            file.write('length=' + str(length) + '\n')  # distance[i][j]=length 같음 distance굳이 쓸 필요X
            file.write("time=" + str(time))
            file.close()
            break


# =======================================================================================
with open("C:\\Users\\LG\\Desktop\\Artificial_Intelligence_assignment_1\\Maze_1.txt","r") as file:
    k,m,n = map(int, file.readline().split())
    maze = []
    for line in file:
        for i in line.split():
            maze.append(list(map(int,i)))

# 전체 노드 탐색해서 끝점 4와 키 6의 위치파악
goal = []
key = []
for i in range(len(maze)):
    for j in range(len(maze[0])):
        if maze[i][j] == 4:
            goal = [i, j]
        if maze[i][j] == 6:
            key.append([i,j])



#bfs(maze,k,m,n,key,goal)
#ids(maze,k,m,n,key,goal)
gbfs(maze,k,m,n,key,goal)
#a_star(maze,k,m,n,key,goal)


# for i in maze:
#     for j in i:
#         print(j,end=' ')
#     print()


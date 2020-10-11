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
    # 전상태가 왼,오로 이동하던 것이었다면
    if [i,j-1] == data[-1] or [i,j+1] == data[-1]:
        #print('왼 또는 오로 이동하던중 막힘')
        while len(data)>1 and data[-1][0] == data[-2][0]: # 스택에 최소2개는 있어야 비교가능
            # 직전에 위 또는 아래로 움직임
            #print('1)2로 바꿈:',data[-1])
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
        #print('위 또는 아래로 이동하던중 막힘')
        while len(data)>1 and data[-1][1] == data[-2][1]:
            #print('2)2로 바꿈:', data[-1])
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
        #never.append([i,j])
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

    #a_sub_b = [x for x in stack if x not in prestack]
    # stack에 append된게 없으면 고립된 상태이므로 방향이 같지 않을때까지 값을 pop한다 - pop된 좌표는 never에 넣는다
    if len(prestack)==len(stack):
        length,time=stuck(i,j,length,time, stack)
    return length,time

def ids(maze,k,m,n,key,goal):
    #visited = []
    stack = [[0, 1]]

    limit = 0
    length, time=0,0
    while True:
        [i,j]=stack.pop()
        #visited.append([i, j])

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
            # print([i, j])
            # print('never:', never)
            # #print('limit:',limit)
            # print('-----')



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
        #self.queue.pop()
        #print('queue: ',self.queue)
        minv = self.queue.pop() # 마지막 원소를 제거한다 (제일 작은 값 삭제)
        #print('minv: ',minv)
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

    def printHeap(self):
        print(self.queue)


# Estimate of (optimal) cost from n to goal
# 네방향으로 이동하니까 distance의 추정값을 manhattan distance로 함
# 벽이 없다고 가정한 목적지까지의 거리를 계산
def h(n, goal):
    return abs(goal[0]-n[0]) + abs(goal[1]-n[1])

def gbfs(maze,k,m,n,key,goal):
    visited = [[0,1]]
    #minheap = [[0, 1]]  # 시작 노드 추가/ 방문이 필요한 노드들에 대한 정보 (Fringe : 노드가 나오긴 했지만 아직 펼쳐지지 않은 노드들)
    distance = [[0 for columns in range(n)] for rows in range(m)]  # 해당 지점까지의 거리를 담는 리스트
    # m = len(maze) : # of rows, n = len(maze[0]) : # of columns
    distance[0][0] = 1

    dic = {}
    #mh = MinHeap()

    i,j=0,1 # 초기 시작 위치
    while True:
        stuck_num = 0
        # 방문한 적이 없고 방문한 노드의 인접노드라 리스트에 들어간적 없는 노드-> 완전 new node
        # 네 방향을 다 탐색하고, manhattan distance가 가장 작은 값을 먼저 탐색
        print('현재위치:', [i,j])
        print('never:',never)
        predic = dic.copy()
        if i < m - 1 and maze[i + 1][j] != 1 and [i + 1, j] not in visited and [i + 1, j] not in never:
            dic[i + 1, j] = h([i + 1, j], goal)
            #mh.insert(dic[i + 1, j])
            distance[i + 1][j] = distance[i][j] + 1
        if j < n - 1 and maze[i][j + 1] != 1 and [i, j + 1] not in visited and [i, j + 1] not in never:
            dic[i, j + 1]= h([i, j + 1], goal)
            #mh.insert(dic[i, j + 1])
            distance[i][j + 1] = distance[i][j] + 1
        if j > 0 and maze[i][j - 1] != 1 and [i, j - 1] not in visited and [i, j - 1] not in never:
            dic[i, j - 1]=h([i, j - 1], goal)
            #mh.insert(dic[i, j - 1])
            distance[i][j - 1] = distance[i][j] + 1
        if i > 0 and maze[i - 1][j] != 1 and [i - 1, j] not in visited and [i - 1, j] not in never:
            dic[(i - 1, j)]=h([i - 1, j], goal)
            #mh.insert(dic[i - 1, j])
            distance[i - 1][j] = distance[i][j] + 1


        # dic값을 조정해도, minv을 구하는 minheap mh는 수정이 안된다는 문제점
        mh = MinHeap()
        print('dic:',dic.items())
        reverse_dic = {v: k for k, v in dic.items()} #->>같은 키값은 없애버림 하지만 reverse_dic은 최소인 값을 갖는 노드를 추출하는 용도이므로
                                                    # 같은 값을 가지는 이전 노드는 없어져도 됨.////

        num=0
        keylist=[]
        for key, value in dic.items():
            if list(key) not in visited:# and list(key) not in never:
                # 현재위치의 인접노드만 min tree에 넣어서 작은값 뽑아냄 -> 고립됐을때 나갈 방법이 없음
               # if list(key) ==[i+1,j] or list(key)==[i-1,j] or list(key)==[i,j+1] or list(key)==[i,j-1]:
                print(key, value)
                keylist.append(key)
                mh.insert(value)

                # # stuck인 상황은 인접노드만 mh에 넣음
                if len(predic) == len(dic):
                    #print('stuck!!!!!!!!!!!!!!')
                    stuck_num+=1
                    # 만약 인접노드가 존재하면 mh에 인접노드만 남긴다
                    # 인접노드의 순번은 num-1
                    num+=1
                    if len(mh.queue)>0:
                        #print('stucknum:',stuck_num)
                        if stuck_num!=0:
                            #for _ in range(stuck_num-1):
                            for _ in range(len(mh.queue)-1):
                                tmp = mh.delete()
                                # 근처노드면 다시 넣음
                                x = reverse_dic.get(tmp)
                                #print('x:',x)
                                #print('i,j:',[i,j])
                                #print('keylist:',keylist)
                                if keylist[stuck_num-1]==x:
                                    #if x[0]==i or x[1]==j:
                                    if abs(x[0]-i)+abs(x[1]-j)<10:
                                        #print('inininin')
                                        mh.insert(tmp)
                            #print('====')
                            # else:
                        #     if len(mh.queue)>2:
                        #         print('heyyyyyyyyyy')
                        #         mh.delete()

                            # 만약 tmp의 값에 해당하는 좌표가 인접노드라면 다시 넣어주고 끝냄 -> 최소값을 가지는 것은 인접노드가 된다
                        #print(reverse_dic)
                        #n = reverse_dic.get(tmp)
                        #print('n:',n)
                            # if n = (i+1,j) or n=(i-1,j) or n=(i,j-1) or n=(i,j+1):
                            #     mh.insert()
                            #     break


        # stuck이 되면 min값을 빼는데, mh에 인접노드가 있으면 글로 가야됨!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # if len(predic) == len(dic):
        #     print('stuck!!!!!!!!!!!!!!')

        print('min값 빼기 전 mh:',mh.queue)
        minv = mh.delete() # 가장 작은 값 추출
        # value를 이용해 key를 찾기 위해 {key,value}를 뒤집어{value:key}로 저장하고 찾는다
        #reverse_mh = {v:k for k,v in dic.items()}
        #print('mh:',mh.queue)
        print('minv:', minv)

        # 쓰인 값은 dic에서 지워버림
        dic = {k:v for k,v in dic.items() if k not in visited}
        reverse_dic = {v: k for k, v in dic.items()}
        [i, j] = reverse_dic.get(minv)  # 가장 작은 distance를 가지는 좌표 반환-
        print('방문한좌표는바로빼버리는dic:',dic)
        print('visited i,j:',[i,j])

        print('stucknum:',stuck_num)
        # # 방문했던 i,j가 추출된다면, 루프에 빠진 것이므로 mh.delete를 한번해준다
        #if [i, j] in visited:
        #     print('이미있다!!!!!!!!!!!!!!!!!!!!!1')
        #     mh.delete()
        #     minv = mh.delete()
        #     print('다시뺌minv:',minv)
        #     print('mh:',mh.queue)
        #     [i, j] = reverse_dic.get(minv)

        print('visited:',visited)
        visited.append([i, j]) # 다음으로 방문할 노드 리스트에 넣음




        print('-----')
        # 4라면 탐색 종료
        if [i,j]==goal:
            file = open('C:\\Users\\LG\\Desktop\\Artificial_Intelligence_assignment_1\\Maze_%d_GBFS_output.txt' % (k), 'w')
            for a in maze:
                for b in a:
                    print(b,end=' ')
                print()
                #     file.write(str(b))
                # file.write('\n')
            # file.write('---\n')
            # file.write('length=' + str(length) + '\n')  # distance[i][j]=length 같음 distance굳이 쓸 필요X
            # file.write("time=" + str(time))
            # file.close()
            break

    # 최적 경로 표현
    bestPath(visited,i,j)

# =======================================================================================
# A* algorithm
def a_star(maze,m,n,key,goal):
    distance = [[0 for columns in range(n)] for rows in range(m)]
    distance[0][0] = 1

    visited = []
    dic = {}
    mh = MinHeap()
    i, j = 0, 1  # 초기 시작 위치
    while True:
        # 방문한 적이 없고 방문한 노드의 인접노드라 리스트에 들어간적 없는 노드-> 완전 new node
        # 네 방향을 다 탐색하고, manhattan distance가 가장 작은 값을 먼저 탐색
        # print('visited:',visited)
        # print('minheap:',mh.queue)
        if i < m - 1 and maze[i + 1][j] != 1 and [i + 1, j] not in visited:  # and [i + 1, j] not in minheap:
            distance[i + 1][j] = distance[i][j] + 1
            # f = g + h
            # f = start노드부터 현재노드까지의 distance(정확한 값) + 현재노드부터 goal노드까지의 distance의 추정값(정확한 값X)
            dic[i + 1, j] = distance[i + 1][j] + h([i + 1, j], goal)
            mh.insert(dic[i + 1, j])
        # distance[i + 1][j] = distance[i][j] + 1
        if j < n - 1 and maze[i][j + 1] != 1 and [i, j + 1] not in visited:  # and [i, j + 1] not in minheap:
            distance[i][j + 1] = distance[i][j] + 1
            dic[i, j + 1] = distance[i][j + 1] + h([i, j + 1], goal)
            mh.insert(dic[i, j + 1])
            # distance[i][j + 1] = distance[i][j] + 1
        if j > 0 and maze[i][j - 1] != 1 and [i, j - 1] not in visited:  # and [i, j - 1] not in minheap:
            distance[i][j - 1] = distance[i][j] + 1
            dic[i, j - 1] = distance[i][j - 1] + h([i, j - 1], goal)
            mh.insert(dic[i, j - 1])
        # distance[i][j - 1] = distance[i][j] + 1
        if i > 0 and maze[i - 1][j] != 1 and [i - 1, j] not in visited:  # and [i - 1, j] not in minheap:
            distance[i - 1][j] = distance[i][j] + 1
            dic[(i - 1, j)] = distance[i - 1][j] + h([i - 1, j], goal)
            mh.insert(dic[i - 1, j])
            # distance[i - 1][j] = distance[i][j] + 1
        print(dic)
        print('mh: ',mh.queue)
        minv = mh.delete()  # 가장 작은 값 추출
        print('min:',minv)
        # value를 이용해 key를 찾기 위해 {key,value}를 뒤집어{value:key}로 저장하고 찾는다
        reverse_mh = {v: k for k, v in dic.items()}
        print('re: ',reverse_mh)
        [i, j] = reverse_mh.get(minv)  # 가장 작은 distance를 가지는 좌표 반환
        print([i,j])
        visited.append([i, j])  # 다음으로 방문할 노드 리스트에 넣음
        maze[i][j] = 5  ###### 고립된 부분까지 5로 변경됨. visited한 곳이니까######

        print('-----')
        # 4라면 탐색 종료
        if [i, j] == goal:
            return


# =======================================================================================
with open("C:\\Users\\LG\\Desktop\\Artificial_Intelligence_assignment_1\\Maze_4.txt","r") as file:
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


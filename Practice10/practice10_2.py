import queue
#设计邻接矩阵
class Graph():
    #初始化基本结构
    def __init__(self, n):
        self.vNum = n  
        self.gType = 0
        self.vexs = [0] * self.vNum ##建立一个全为0的顶点矩阵
        self.arcs = [[0] * self.vNum for _ in range(self.vNum)] #建立一个全为0的邻接矩阵
    #添加顶点
    def addVex(self, v, i):
        self.vexs[i] = v
    #添加边，并设置权
    def addArcs(self, v1, v2, cost):
        self.arcs[v1][v2] = cost
        self.arcs[v2][v1] = cost
    #深度优先搜索算法
    def dfs_matrix(self, i, visited=None):
        if visited is None: 
            visited = [False] * self.vNum #设置访问矩阵，记录顶点是否已被访问
        print('Vertex:', self.vexs[i]) #输出当前访问的顶点
        visited[i] = True #修改此顶点访问情况为True
        for j in range(self.vNum):
            if self.arcs[i][j] != 0 and not visited[j]: #判断该顶点是否是上一个顶点的邻接顶点，以及该顶点是否未被访问
                #若是，则对该顶点迭代此函数
                self.dfs_matrix(j, visited)
    #广度优先搜索算法
    def bfs_matrix(self,k):
        visited = [False] * self.vNum #设置访问矩阵，记录顶点是否已被访问
        q = queue.Queue()  # 初始化辅助队列
        print('Vertex:', self.vexs[k]) #输出当前访问的顶点
        visited[k] = True #修改此顶点访问情况为True
        q.put(k) #将该顶点加入队列
        while not q.empty():
            i = q.get() #从队列中取出一个顶点
            for j in range(self.vNum):
                if self.arcs[i][j] != 0 and not visited[j]: #判断该顶点是否是上一个顶点的邻接顶点，以及该顶点是否未被访问
                    print('Vertex:', self.vexs[j]) #若是，则输出该顶点
                    visited[j] = True #修改此顶点访问情况为True
                    q.put(j) #将该顶点加入队列

#代码测试
#创建一个图
g = Graph(5)
#往图中添加顶点
g.addVex('A', 0)
g.addVex('B', 1)
g.addVex('C', 2)
g.addVex('D', 3)
g.addVex('E', 4)
#往图中添加边及权
g.addArcs(0, 1, 60)
g.addArcs(0, 2, 80)
g.addArcs(0, 3, 30)
g.addArcs(1, 2, 40)
g.addArcs(1, 3, 75)
g.addArcs(2, 4, 35)
g.addArcs(3, 4, 45)
print('邻接矩阵为：')
print(g.arcs)
print('深度优先搜索：')
g.dfs_matrix(0)
print('广度优先搜索：')
g.bfs_matrix(0)
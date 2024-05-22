class vexNode():
    def __init__(self, v1=-1):
        self.id = v1
        self.adjList = None  # 初始化顶点节点的邻接边列表为None

class adjNode():
    def __init__(self, dest=-1, weight=0):
        self.id = dest
        self.weight = weight  # 存储边的权重
        self.next = None  # 初始化邻接边节点的下一个节点为None

class Graph():
    #初始化基本结构
    def __init__(self, n):
        self.vNum = n
        self.vertices = [None] * self.vNum  # 使用列表存储顶点节点
    #添加顶点
    def addVex(self, v, i):
        self.vertices[i] = vexNode(v)  # 在索引位置i处存储一个顶点节点对象
    # 添加边并设置权重
    def addArcs(self, v1, v2, weight): 
        newNode = adjNode(v2, weight)  # 创建一个新的邻接边节点，指向v2，带有权重值
        newNode.next = self.vertices[v1].adjList  # 将新节点连接到顶点v1的邻接边列表的头部
        self.vertices[v1].adjList = newNode  # 更新顶点v1的邻接边列表为新节点
        newNode = adjNode(v1, weight)  # 创建另一个新的邻接边节点，指向v1，带有权重值
        newNode.next = self.vertices[v2].adjList  # 将新节点连接到顶点v2的邻接边列表的头部
        self.vertices[v2].adjList = newNode  # 更新顶点v2的邻接边列表为新节点
    #输出图
    def printGraph(self):
        for i in range(self.vNum):
            print("Vertex", self.vertices[i].id, ":", end=" ")  # 打印顶点的id值，用于表示顶点
            temp = self.vertices[i].adjList  # 获取当前顶点的邻接边列表的头部
            while temp:
                print(" ->", self.vertices[temp.id].id, "(Weight:", temp.weight, ")", end="")  # 打印邻接顶点的id和边的权重
                temp = temp.next  # 移动到下一个邻接边节点
            print("")  # 换行，准备打印下一个顶点的信息

#测试代码
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
#输出图
g.printGraph()
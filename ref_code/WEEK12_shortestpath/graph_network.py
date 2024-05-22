'''

(1)分别设计邻接矩阵和邻接表,实现图的创建和存储
(2)用邻接矩阵或邻接表实现图的DFS和BFS算法 deepFirstSearch breadthFirstSearch
(3)针对不同的图的存储方式,分析BFS算法的时间复杂度。

'''



# 邻接表

class AdjNode:
    '''邻接 节点'''
    def __init__(self, adjnodeid, weight=-1) -> None:
        self.weight = weight # 到node的损耗 权重 图的权重为1 
        self.adjnodeid = adjnodeid # 邻接顶点的id
        self.next = None 

class GraphNode:
    ''' 图顶点 '''
    def __init__(self, nodeid, data) -> None:
        self.nodeid = nodeid # 顶点id
        self.data = data # 顶点值
        self.adjnodenum = 0 
        self.adjlist = None # 存储AdjNode
    def addAdjNode(self, adjnode, weight) -> bool:
        '''添加邻接点'''
        '''
        邻接点id    nodeid 
        权重        weight    
        '''
        if self.isAdjNode(adjnode.adjnodeid) is True: # 当已经有此节点时 返回false
            return False
        
        newadjnode = AdjNode(adjnode.adjnodeid, weight)
        if self.adjlist is None: # 当没有邻接点时
            self.adjlist = newadjnode # 
            self.adjnodenum += 1
        else:
            pn = self.adjlist
            while pn is not None:
                pn2 = pn
                pn = pn.next
            pn2.next = newadjnode
            self.adjnodenum += 1
        return True
    
    def traverseAllAdjNode(self):
        '''遍历顶点邻接的所有点 返回邻接点id的数组'''
        traverseresult = []
        pn = self.adjlist
        while pn is not None:
            traverseresult.append(pn.adjnodeid)
            pn = pn.next
        return traverseresult
    
    def isAdjNode(self, adjnodeid) -> bool:
        '''查找邻接点'''
        pn = self.adjlist
        while pn is not None:
            if pn.adjnodeid == adjnodeid:
                return True 
            pn = pn.next
        return False


class Graph:
    def __init__(self) -> None:
        self.nodenum = 0 # 顶点个数
        self.node = [] # 顶点
        self.adjmatrix = []

    def insertNode(self, node):
        self.nodenum += 1
        self.node.append(node)

    def indexOfNode(self, nodeid):
        for i in self.node:
            if i.nodeid == nodeid:
                return i # 返回GraphNode
        return None

 

    def buildAdjMatrixByAdjList(self) -> bool:
        '''构建邻接矩阵'''
        if self.nodenum == 0:
            return None
        adjmatrix = []
        for i in range(self.nodenum):
            adjmatrix.append([])
        for i in range(self.nodenum):
            for j in range(self.nodenum):
                if i == j:
                    adjmatrix[i].append(0) # i == j 权重设置为0 
                else:
                    adjmatrix[i].append(float("inf")) # 初始化矩阵
        for item in self.node:
            pnadj = item.adjlist
            while pnadj is not None:
                adjmatrix[item.nodeid][pnadj.adjnodeid] = pnadj.weight
                pnadj = pnadj.next
        self.adjmatrix = adjmatrix
        return True
        
        

    def BFS(self, nodestart):
        '''广度优先 Breadth First Search'''
        queue = [nodestart] # queue存放 当前节点邻接的所有GraphNodes
        bsfresult = [] # 存放遍历的结果
        
        while len(queue) != 0: 
            queue2 = [] # 下一层的顶点集合
            for item in queue: # 遍历队列中的顶点
                if item not in bsfresult: # item为GraphNode
                    bsfresult.append(item) 
                adjnodeid = item.traverseAllAdjNode()
                for i in adjnodeid:
                    adjnode = self.indexOfNode(i) # GraphNode
                    if adjnode not in queue2:
                        queue2.append(adjnode)
            queue = queue2
            if len(bsfresult) == self.nodenum:
                break
        return bsfresult
                

    def DFS_iteration(self, node, dfsresult):
        '''深度优先 Depth First Search'''
        '''
        node 顶点
        dfsresult深度优先遍历结果
        '''
        if len(dfsresult) != self.nodenum: # 当遍历结果中的元素等于图的顶点数时 返回搜索结果 
            if node not in dfsresult: # 当遍历结果中没有这个节点  
                dfsresult.append(node) # 添加节点到dfsresult中

            adjpn = node.adjlist # 查找该节点的邻接表

            while adjpn is not None: # 对邻接表中的所有点进行查找
                newnode = self.indexOfNode(adjpn.adjnodeid) # 查找邻接表中邻接点对应的GraphNode
                if newnode in dfsresult: # 这个node 已经被搜索 则跳到下一个顶点搜索
                    adjpn = adjpn.next
                    continue
                self.DFS_iteration(newnode, dfsresult) # 如果没有被搜索，迭代
                adjpn = adjpn.next
        return dfsresult # 当所有点都被访问过，返回dfsresult


    def DFS(self, startnode):
        dfsresult = []
        dfsresult = self.DFS_iteration(startnode, dfsresult)
        return dfsresult



# test
def main():
    '''-----------------------------------------------------构造图/网络-----------------------------------------------------'''
    newgraph = Graph()
    newgraphnode0 = GraphNode(0, 'A')
    newgraphnode1 = GraphNode(1, 'B')
    newgraphnode2 = GraphNode(2, 'C')
    newgraphnode3 = GraphNode(3, 'D')
    newgraphnode4 = GraphNode(4, 'E')


    
    # 与点A邻接的点 构建邻接表
    newadjnode1 = AdjNode(1, 60) # a-b 60
    newadjnode2 = AdjNode(0, 60) # b-a 60
    newgraphnode0.addAdjNode(newadjnode1, 60)
    newgraphnode1.addAdjNode(newadjnode2, 60)
    del newadjnode1, newadjnode2

    newadjnode1 = AdjNode(2, 80) # a-c 80
    newadjnode2 = AdjNode(0, 80) # c-a 80
    newgraphnode0.addAdjNode(newadjnode1, 80)
    newgraphnode2.addAdjNode(newadjnode2, 80)
    del newadjnode1, newadjnode2

    newadjnode1 = AdjNode(3, 30) # a-d 30
    newadjnode2 = AdjNode(0, 30) # d-a 30
    newgraphnode0.addAdjNode(newadjnode1, 30)
    newgraphnode3.addAdjNode(newadjnode2, 30)
    del newadjnode1, newadjnode2

    # 与点B邻接的点构建邻接表
    newadjnode1 = AdjNode(2, 40) # b-c 40
    newadjnode2 = AdjNode(1, 40) # c-b 40
    newgraphnode1.addAdjNode(newadjnode1, 40)
    newgraphnode2.addAdjNode(newadjnode2, 40)
    del newadjnode1, newadjnode2

    newadjnode1 = AdjNode(3, 75) # b-c 75
    newadjnode2 = AdjNode(1, 75) # c-b 75
    newgraphnode1.addAdjNode(newadjnode1, 75)
    newgraphnode3.addAdjNode(newadjnode2, 75)
    del newadjnode1, newadjnode2





    # 与点C邻接的点构建邻接表
    newadjnode1 = AdjNode(4, 35) # c-e 35
    newadjnode2 = AdjNode(2, 35) # e-c 35
    newgraphnode2.addAdjNode(newadjnode1, 35)
    newgraphnode4.addAdjNode(newadjnode2, 35)
    del newadjnode1, newadjnode2


    # 与点D邻接的点构建邻接表
    newadjnode1 = AdjNode(4, 45) # d-e 45
    newadjnode2 = AdjNode(3 ,45) # e-d 45
    newgraphnode3.addAdjNode(newadjnode1, 45)
    newgraphnode4.addAdjNode(newadjnode2, 45)
    del newadjnode1, newadjnode2




    # 添加节点
    newgraph.insertNode(newgraphnode0)
    newgraph.insertNode(newgraphnode1)
    newgraph.insertNode(newgraphnode2)
    newgraph.insertNode(newgraphnode3)
    newgraph.insertNode(newgraphnode4)

    '''-----------------------------------------------------广度优先遍历-----------------------------------------------------'''
    print('''\n-----------------------------------------------------广度优先遍历-----------------------------------------------------''')
    bfsresult = newgraph.BFS(newgraphnode0) # A B C D E 
    print('从顶点A开始深度优先遍历，遍历结果为:',end='\t')
    for item in bfsresult:
        print(item.data, end='\t')

    bfsresult = newgraph.BFS(newgraphnode1) # B A C D E
    print('\n从顶点B开始深度优先遍历，遍历结果为:',end='\t')
    for item in bfsresult:
        print(item.data, end='\t')

    bfsresult = newgraph.BFS(newgraphnode2) # C A B E D 
    print('\n从顶点C开始深度优先遍历，遍历结果为:',end='\t')
    for item in bfsresult:
        print(item.data, end='\t')

    bfsresult = newgraph.BFS(newgraphnode3) # D A B E C
    print('\n从顶点D开始深度优先遍历，遍历结果为:',end='\t')
    for item in bfsresult:
        print(item.data, end='\t')

    bfsresult = newgraph.BFS(newgraphnode4) # E C D A B
    print('\n从顶点E开始深度优先遍历，遍历结果为:',end='\t')
    for item in bfsresult:
        print(item.data, end='\t')
    
    '''-----------------------------------------------------深优先遍历-----------------------------------------------------'''
    print('''\n-----------------------------------------------------深度度优先遍历-----------------------------------------------------''')
    dfsresult = newgraph.DFS(newgraphnode0) # A B C E D
    print('\n从顶点A开始广度优先遍历，遍历结果为:',end='\t')
    for item in dfsresult:
        print(item.data, end='\t')

    dfsresult = newgraph.DFS(newgraphnode1) # B A C E D
    print('\n从顶点B开始广度优先遍历，遍历结果为:',end='\t')
    for item in dfsresult:
        print(item.data, end='\t')

    dfsresult = newgraph.DFS(newgraphnode2) # C A B D E
    print('\n从顶点C开始广度优先遍历，遍历结果为:',end='\t')
    for item in dfsresult:
        print(item.data, end='\t')

    dfsresult = newgraph.DFS(newgraphnode3) # D A B C E
    print('\n从顶点D开始广度优先遍历，遍历结果为:',end='\t')
    for item in dfsresult:
        print(item.data, end='\t')

    dfsresult = newgraph.DFS(newgraphnode4) # E C A B D
    print('\n从顶点E开始广度优先遍历，遍历结果为:',end='\t')
    for item in dfsresult:
        print(item.data, end='\t')

    '''-----------------------------------------------------邻接矩阵-----------------------------------------------------'''
    print('''\n-----------------------------------------------------邻接矩阵-----------------------------------------------------''')
    newgraph.buildAdjMatrixByAdjList()
    for item in newgraph.adjmatrix:
        print(item)

if __name__ == "__main__":
    main()
    
        


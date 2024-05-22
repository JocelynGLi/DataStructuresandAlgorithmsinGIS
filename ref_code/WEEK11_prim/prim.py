'''
利用普利姆算法构造最小生成树
'''
from graph_network import Graph,  GraphNode, AdjNode
import copy
def getMinAdj(vect):
    minadj = float("inf")
    min_i = -1
    for i in range(len(vect)):
        if vect[i] != 0 and vect[i] < minadj: # 不是对角线上的点 或者 已经访问的点
            minadj = vect[i]
            min_i = i
    return minadj, min_i
            


def primMiniSpanTree(graph):
    '''基于prim算法的最小生成树'''
    # 找到权重最小的邻接边
    graphnode = [] # 存放已经访问的点
    adjmatrix = copy.copy(graph.adjmatrix) # 拷贝权重矩阵

    # 找到网络中最小的邻接边
    minweight = float('inf')
    for i in range(graph.nodenum):
        for j in range(graph.nodenum):
            weight = adjmatrix[i][j]
            if (weight != float("inf")) and (weight != 0):
                if weight < minweight:
                    minweight = weight
                    pnid1 = i
                    pnid2 = j
    adjmatrix[pnid1][pnid2] = 0
    adjmatrix[pnid2][pnid1] = 0 # 针对无向网 无向图
    graphnode.append(graph.node[pnid1])
    graphnode.append(graph.node[pnid2])

    while len(graphnode) != graph.nodenum:
        minweight = float("inf")

        for item in graphnode:
            minadj, min_i = getMinAdj(adjmatrix[item.nodeid])
            if minadj < minweight:
                minweight = minadj
                pnid = min_i
        for item in graphnode:
            adjmatrix[item.nodeid][pnid] = 0
            adjmatrix[pnid][item.nodeid] = 0
        graphnode.append(graph.node[pnid])
    return graphnode        

    


def main():
    # 构建网络
    newgraph = Graph()
    newnode0 = GraphNode(0, '1')
    newnode1 = GraphNode(1, '2') 
    newnode2 = GraphNode(2, '3')
    newnode3 = GraphNode(3, '4') 
    newnode4 = GraphNode(4, '5')
    newnode5 = GraphNode(5, '6') 

    newadjnode1 = AdjNode(1, 6)
    newadjnode2 = AdjNode(0, 6)
    newnode0.addAdjNode(newadjnode1, 6)
    newnode1.addAdjNode(newadjnode2, 6)
    del newadjnode1, newadjnode2
    newadjnode1 = AdjNode(2, 1)
    newadjnode2 = AdjNode(0, 1)
    newnode0.addAdjNode(newadjnode1, 1)
    newnode2.addAdjNode(newadjnode2, 1)
    del newadjnode1, newadjnode2
    newadjnode1 = AdjNode(3, 5)
    newadjnode2 = AdjNode(0, 5)
    newnode0.addAdjNode(newadjnode1, 5)
    newnode3.addAdjNode(newadjnode2, 5)
    del newadjnode1, newadjnode2

    newadjnode1 = AdjNode(2, 5)
    newadjnode2 = AdjNode(1, 5)
    newnode1.addAdjNode(newadjnode1, 5)
    newnode2.addAdjNode(newadjnode2, 5)
    del newadjnode1, newadjnode2
    newadjnode1 = AdjNode(4, 3)
    newadjnode2 = AdjNode(1, 3)
    newnode1.addAdjNode(newadjnode1, 3)
    newnode4.addAdjNode(newadjnode2, 3)
    del newadjnode1, newadjnode2

    newadjnode1 = AdjNode(3, 7)
    newadjnode2 = AdjNode(2, 7)
    newnode2.addAdjNode(newadjnode1, 7)
    newnode3.addAdjNode(newadjnode2, 7)
    del newadjnode1, newadjnode2
    newadjnode1 = AdjNode(4, 5)
    newadjnode2 = AdjNode(2, 5)
    newnode2.addAdjNode(newadjnode1, 5)
    newnode4.addAdjNode(newadjnode2, 5)
    del newadjnode1, newadjnode2
    newadjnode1 = AdjNode(5, 4)
    newadjnode2 = AdjNode(2, 4)
    newnode2.addAdjNode(newadjnode1, 4)
    newnode5.addAdjNode(newadjnode2, 4)
    del newadjnode1, newadjnode2

    newadjnode1 = AdjNode(5, 2)
    newadjnode2 = AdjNode(3, 2)
    newnode3.addAdjNode(newadjnode1, 2)
    newnode5.addAdjNode(newadjnode2, 2)
    del newadjnode1, newadjnode2

    newadjnode1 = AdjNode(5, 6)
    newadjnode2 = AdjNode(4, 6)
    newnode4.addAdjNode(newadjnode1, 6)
    newnode5.addAdjNode(newadjnode2, 6)
    del newadjnode1, newadjnode2


    newgraph.insertNode(newnode0)
    newgraph.insertNode(newnode1)
    newgraph.insertNode(newnode2)
    newgraph.insertNode(newnode3)
    newgraph.insertNode(newnode4)
    newgraph.insertNode(newnode5)
    newgraph.buildAdjMatrixByAdjList()



    primnintree = primMiniSpanTree(newgraph)
    print("最小生成树：", end="\t")
    for item in primnintree:
        print(item.data, end='\t')





if __name__ == "__main__":
    main()
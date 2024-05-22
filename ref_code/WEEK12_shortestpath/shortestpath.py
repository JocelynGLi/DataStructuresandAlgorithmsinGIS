'''设计算法，求图中示例道路路网数据中，任意两点间的最短路径'''

from graph_network import Graph, GraphNode, AdjNode
from shapefeature import loadjsonfile, Point, distance
import matplotlib.pyplot as plt
from KDT import KDTree
import copy
# 生成路网的相交点 存放在数组中
def getMin(lst):
    minnum = float("inf")
    minidx = None
    for i in range(len(lst)):
        if lst[i] < minnum and lst[i] != 0:
            minnum = lst[i]
            minidx = i
    return minnum, minidx

def dijkstraMinPath(graph, vertex1, vertex2):
    '''dijkstra算法计算最短路径'''
    idx1 = vertex1.nodeid
    idx2 = vertex2.nodeid
    graph.buildAdjMatrixByAdjList()
    
    minpathnode = [vertex1]
    # p1 到 点的 距离
    p1toohter = copy.copy(graph.adjmatrix[idx1])  # vertex1 到所有点的距离
    p1toohter2 = copy.copy(p1toohter)
    a = -1
    allnodespath = [[vertex1] for i in range(graph.nodenum)]
    while a != graph.nodenum - 1: # # 遍历所有的点
        a += 1

        mindist, minidx = getMin(p1toohter2) # 在没有被访问过的点中选出最小的点 
        if minidx is None: # 不与网络相连的点
            continue

        minnode = graph.indexOfNode(minidx)
        minpathnode.append(minnode) 

        minnode2other = copy.copy(graph.adjmatrix[minidx])
        # 添加点后对距离进行更新
        for i in range(len(allnodespath)):
            if mindist + minnode2other[i] <= p1toohter[i]:
                p1toohter[i] = mindist + minnode2other[i]
                p1toohter2[i] = mindist + minnode2other[i]
                allnodespath[i] = copy.copy(allnodespath[minidx])
                insertnewnode = graph.indexOfNode(i)
                if insertnewnode not in allnodespath:
                    allnodespath[i].append(graph.indexOfNode(i))

        p1toohter2[minidx] = float("inf")  # 用于标记 已经访问过的点

    v1tov2 = allnodespath[idx2]
    return v1tov2
def minPath(graph, point1, point2, adddist = 50):
  
    '''
    point1 = [x, y]
    point2 = [x, y]
    '''
    nodekdt = KDTree()
    # 将各个顶点创建KDT 然后进行最邻近搜索
    for item in graph.node:
        nodekdt.insertNode(item.nodeid, item.data.x, item.data.y) # 插入节点

    vertex1, mindistance1, distance1, inrangepoints1 = nodekdt.getNearestPoint(point1[0], point1[1], adddist)
    vertex2, mindistance2, distance2, inrangepoints2 = nodekdt.getNearestPoint(point2[0], point2[1], adddist)

    vertexgraph1 = graph.indexOfNode(vertex1.data)
    vertexgraph2 = graph.indexOfNode(vertex2.data) # 与point1 和 point2
    
    path = dijkstraMinPath(graph, vertexgraph1, vertexgraph2)
    return path, vertexgraph1, vertexgraph2
    
def main():
    # load data
    filename = "road-sample-utm-fixed.geojson"
    data = loadjsonfile(filename)
    features = data["features"]
    

    # 存储相交点
    roadnetwork = Graph() # 路网
    nodecoordset = [] # 标记是否添加此节点
    filename2 = r"intersection pointset.geojson" # 在QGIS生成相交点
    data2 = loadjsonfile(filename2)
    features2 = data2["features"]
    id = -1
    for item in features2:
        pointcoor = item["geometry"]["coordinates"]
        if [pointcoor[0], pointcoor[1]] not in nodecoordset:
            id += 1
            nodecoordset.append([pointcoor[0], pointcoor[1]])
            newpoint = Point(pointcoor[0], pointcoor[1])
            newgraphnode = GraphNode(id, newpoint)
            roadnetwork.insertNode(newgraphnode)

    # 构建路网的邻接表
    # 邻接节点的weight为两点的距离
    for item in features:
        polylinecoor = item["geometry"]["coordinates"][0] # [[x,y],[x2,y2],...,[xn, yn]] #点集
        for i in range(len(polylinecoor)):
            if [polylinecoor[i][0], polylinecoor[i][1]] in nodecoordset:
                idx = nodecoordset.index([polylinecoor[i][0], polylinecoor[i][1]])
                newgraphnode = roadnetwork.node[idx] # 如果是交叉点
            else:
                id += 1
                newpoint = Point(polylinecoor[i][0], polylinecoor[i][1])
                newgraphnode = GraphNode(id, newpoint)
                roadnetwork.insertNode(newgraphnode)
            if i == 0: # 第一个点
                pregraphnode = newgraphnode
                continue
            else:
                weight = distance(newgraphnode.data, pregraphnode.data)
                newadjnode1 = AdjNode(pregraphnode.nodeid, weight)
                newadjnode2 = AdjNode(newgraphnode.nodeid, weight)
                newgraphnode.addAdjNode(newadjnode1, weight)
                pregraphnode.addAdjNode(newadjnode2, weight)    
            pregraphnode = newgraphnode

    

    # 绘制相交点
    for item in roadnetwork.node:
        pn = item.adjlist
        while pn is not None:
            id = pn.adjnodeid
            node2 = roadnetwork.node[id]
            plt.plot([item.data.x, node2.data.x], [item.data.y, node2.data.y], color='b')
            pn = pn.next
    # for item in nodecoordset:
    #     plt.plot(item[0], item[1], marker='o', markersize=5, color='b')


# 通过kdt 任意点搜索 最邻接的顶点
    point1 = [ -1346.122084857910522, -15338.791312239467516]
    point2 = [ -2500.030693930719281, -22800.161494807514828]
    plt.plot(point1[0], point1[1], marker='*', markersize=5, color='g')
    plt.plot(point2[0], point2[1], marker='*', markersize=5, color='g')


    
    path, vertexgraph1, vertexgraph2 = minPath(roadnetwork, point1, point2)
    plt.plot([point1[0], vertexgraph1.data.x], [point1[1], vertexgraph1.data.y], color='g')
    plt.plot([point2[0], vertexgraph2.data.x], [point2[1], vertexgraph2.data.y], color='g')
    x = []
    y = []
    for item in path:
        x.append(item.data.x)
        y.append(item.data.y)
    plt.plot(x, y, markersize=3, color='r')
    plt.show()
    


if __name__ == "__main__":
    main()
'''
对图中点的集合，用Python语言设计k-d树数据结构

实现对这些坐标点数据的插入(insertNode)、删除(deleteNode)和查找(search)算法。

'''

'''以构造一个二维的kd树为例'''
import random
import matplotlib.pyplot as plt
from math import *
class KDNode:
    def __init__(self, data, x, y, lev) -> None:
        '''
        x, y 数据
        lev 节点的层数 root的层数为0
        '''
        self.data = data
        self.x = x
        self.y = y
        self.lev = lev
        self.left = None
        self.right = None
    def isInRange(self, *arg):
        if self.x >= arg[0] and self.x <= arg[2] and self.y >= arg[1] and self.y <= arg[3]:
            return True
        else:
            return False
      


class KDTree:
    def __init__(self, k=2) -> None:
        '''
        构造一个二维的kd树 k=2
        '''
        self.root = None
        self.k = k
    
    '''---------------------------------------------------------插入节点---------------------------------------------------------'''
    def insertNode(self, data, x, y):
        if self.root is None: # 空树
            newkdnode = KDNode(data, x, y, 0)
            self.root = newkdnode
        else:
            pn = self.root
            flag = 0 # 标记左右节点
            lev = 0 # 记录节点的层数
            while pn is not None:
                pn2 = pn
                if pn.lev % 2 == 0: # 偶数层 比较x的大小
                    if x <= pn.x:
                        pn = pn.left
                        flag = 1
                    elif x > pn.x:
                        pn = pn.right
                        flag = 2
                elif pn.lev % 2 == 1: # 奇数层 比较y的大小
                    if y <= pn.y:
                        pn = pn.left
                        flag = 1
                    elif y > pn.y:
                        pn = pn.right
                        flag = 2
                lev += 1
            newkdnode = KDNode(data, x, y, lev)
            if flag == 1:
                pn2.left = newkdnode
            else:
                pn2.right = newkdnode
    
    '''---------------------------------------------------------查询---------------------------------------------------------'''
    def indexOfNode(self, x, y, lev=-1):
        '''通过找节点的位置'''
        ''' 
        return pn, pn2, flag
        pn 当前节点
        pn2 pn的父节点
        flag = 1 pn2.left = pn 
        flag = 2 pn2.right =pn
        '''
        pn = self.root
        pn2 = pn
        flag = 0
        while pn is not None:
            if lev == -1:
                if x == pn.x and y == pn.y:
                    break
            else:
                if x == pn.x and y == pn.y and lev == pn.lev:
                    break
            pn2 = pn
            if pn.lev % 2 == 0: # 偶数层
                if x <= pn.x:
                    pn = pn.left
                    flag = 1
                elif x > pn.x:
                    pn = pn.right
                    flag = 2
            elif pn.lev % 2 == 1: # 奇数层
                if y <= pn.y:
                    pn = pn.left
                    flag = 1
                elif y > pn.y:
                    pn = pn.right
                    flag = 2
        if pn is None:
            return None
        return pn, pn2, flag
    '''---------------------------------------------------------删除节点---------------------------------------------------------'''
    def getMaxNode(self, pndelete, flag): # 找出父节点的子树中的最大值节点
        if flag == 1:
            bsfpn = self.BFS(pndelete.left)
        elif flag == 2:
            bsfpn = self.BFS(pndelete.left)
        max = float('-inf')
        if pndelete.lev % 2 == 0: # 找x的最大值
            for item in bsfpn:
                if item.x > max:
                    max = item.x
                    pnmax = item
        elif pndelete.lev % 2 == 1 : # 找y的最大值
            for item in bsfpn:
                if item.y > max:
                    max = item.y
                    pnmax = item
        pn, pn2, flag = self.indexOfNode(pnmax.x, pnmax.y)
        return pn
    def getMinNode(self, pndelete, flag): # 找出父节点的子树中的最小值节点
        if flag == 1:
            bsfpn = self.BFS(pndelete.left)
        elif flag == 2:
            bsfpn = self.BFS(pndelete.left)
        min = float('inf')
        if pndelete.lev % 2 == 0: # 找x的最大值
            for item in bsfpn:
                if item.x < min:
                    min = item.x
                    pnmin = item
        elif pndelete.lev % 2 == 1 : # 找y的最大值
            for item in bsfpn:
                if item.y < min:
                    min = item.y
                    pnmin = item
        pn, pn2, flag = self.indexOfNode(pnmin.x, pnmin.y)
        return pn
    def deleteNode(self, pn):
        '''删除节点'''
        if pn is None:
            return False
        if pn.left is None and pn.right is None: # 删除叶子节点
            pn, pn2, flag = self.indexOfNode(pn.x, pn.y, pn.lev)
            if flag == 1:
                pn2.left = None
            elif flag == 2:
                pn2.right = None
            return True
        elif pn.left is not None: # 如果pn的左子树有节点，则找x/y的最大值节点，并将该节点的值赋给pn， 然后递归 直到删除叶子节点
            flag = 1
            pndel = self.getMaxNode(pn, flag)
            pn.x = pndel.x
            pn.y = pndel.y
            pn.data = pndel.data
            self.deleteNode(pndel)
        elif pn.right is not None: # 找最小值
            flag = 2
            pndel = self.getMinNode(pn, flag)
            pn.x = pndel.x
            pn.y = pndel.y
            pn.data = pndel.data
            self.deleteNode(pndel)



         

    '''---------------------------------------------------------遍历---------------------------------------------------------'''
    # 广度优先遍历
    def BFS(self, pn):
        '''广度优先遍历'''
        queue = [pn]
        bsf = []
        while len(queue) != 0:
             queue2 = []
             for i in queue:
                 bsf.append(i)
                 if i.left is not None:
                     queue2.append(i.left)
                 if i.right is not None:
                     queue2.append(i.right)
                 queue = queue2
        return bsf
    def preordersearch(self, s, pn):
        '''深度优先遍历（先序）'''
        if pn is not None:
            s.append(pn)
            self.preordersearch(s, pn.left)
            self.preordersearch(s, pn.right)
        return s


    '''---------------------------------------------------------最临近搜索---------------------------------------------------------'''
    # 最邻近搜索
    def NearestNeighborSearch(self, pn, x, y, distance, inrangepoint):
        xmin = x - distance
        ymin = y - distance
        xmax = x + distance
        ymax = y + distance
        if pn is not None:
            if pn.lev % 2 == 0: # 偶数层 比较x
                if pn.isInRange(xmin, ymin, xmax, ymax):
                    inrangepoint.append(pn)
                    self.NearestNeighborSearch(pn.left, x, y, distance, inrangepoint)
                    self.NearestNeighborSearch(pn.right, x, y, distance, inrangepoint)
                if pn.isInRange(xmin, ymin, xmax, ymax) is not True:
                    if pn.x > xmin and pn.x < xmax:
                        self.NearestNeighborSearch(pn.left, x, y, distance, inrangepoint)
                        self.NearestNeighborSearch(pn.right, x, y, distance, inrangepoint)
                    elif pn.x <= xmin:
                        self.NearestNeighborSearch(pn.right, x, y, distance, inrangepoint)
                    elif pn.x >= xmax:
                        self.NearestNeighborSearch(pn.left, x, y, distance, inrangepoint)
            elif pn.lev % 2 == 1: # 奇数层 比较y
                if pn.isInRange(xmin, ymin, xmax, ymax):
                    inrangepoint.append(pn)
                    self.NearestNeighborSearch(pn.left, x, y, distance, inrangepoint)
                    self.NearestNeighborSearch(pn.right, x, y, distance, inrangepoint)
                if pn.isInRange(xmin, ymin, xmax, ymax) is not True:
                    if pn.y > ymin and pn.y < ymax:
                        self.NearestNeighborSearch(pn.left, x, y, distance, inrangepoint)
                        self.NearestNeighborSearch(pn.right, x, y, distance, inrangepoint)
                    elif pn.y <= ymin:
                        self.NearestNeighborSearch(pn.right, x, y, distance, inrangepoint)
                    elif pn.y >= ymax:
                        self.NearestNeighborSearch(pn.left, x, y, distance, inrangepoint)
        return inrangepoint
    def getNearestPoint(self, x, y, adddist, distance=0):
        if self.root is None:
            return False
        else:
            point = KDNode('', x, y, 0)
            inrangepoints = []
            inrangepoints = self.NearestNeighborSearch(self.root, x, y, distance, inrangepoints)
            
            if len(inrangepoints) == 0:
                distance += adddist
                return self.getNearestPoint(x, y, adddist, distance)
            # while len(inrangepoints) == 0:
            #     distance += adddist
            #     inrangepoints = self.NearestNeighborSearch(self.root, x, y, distance, inrangepoints)
            
                
            mindistance = float('inf')
            nearestpoint = None
            for item in inrangepoints:
                temp_dist = getDistance(item, point)
                if temp_dist < mindistance:
                    nearestpoint = item
                    mindistance = temp_dist
            return nearestpoint, mindistance, distance, inrangepoints


def getDistance(point1, point2):
    distance = sqrt(pow(point1.x - point2.x, 2)+ pow(point1.y - point2.y, 2))
    return distance
    
def drawPoints(data, colorpoint = 'b'):
    x = []
    y = []
    for item in data:
        x.append(item.x)
        y.append(item.y)
    plt.scatter(x, y, color = colorpoint)
    return
def drawRange(*arg):
    x = [arg[0], arg[2], arg[2], arg[0], arg[0]]
    y = [arg[1], arg[1], arg[3], arg[3], arg[1]]
    plt.plot(x, y, color = 'r')
    return 


if __name__ == "__main__":
    # 构建kd树
    newkdtree = KDTree()
    newkdtree.insertNode('A', 40, 60) # A
    newkdtree.insertNode('B', 10, 75) # B
    newkdtree.insertNode('C', 70, 20) # C
    newkdtree.insertNode('D', 25, 15) # D
    newkdtree.insertNode('E', 80, 70) # E
    newkdtree.insertNode('F', 20, 45) # F
    newkdtree.insertNode('G', 35, 45) # G
    newkdtree.insertNode('H', 60, 50) # H
    # 遍历
    bsf = newkdtree.BFS(newkdtree.root)
    bsfdata = []
    for i in bsf:
        bsfdata.append(i.data)
    print('广度优先遍历结果为{}'.format(bsfdata))
    s = []
    s = newkdtree.preordersearch(s, newkdtree.root)
    preorddata = []
    for i in s:
        preorddata.append(i.data)
    print("先序深度遍历的结果为{}".format(preorddata))
    # 查找节点
    pn, pn2, flag = newkdtree.indexOfNode(25, 15)
    print("(25,15)的值为：{}".format(pn.data))
    if newkdtree.indexOfNode(12, 49) is None:
        print("没有找到该节点(12, 49)")
    else:
        pn, pn2, flag = newkdtree.indexOfNode(12, 49)
        print(pn.data)
    # 删除节点
    pn, pn2, flag = newkdtree.indexOfNode(80, 70)
    newkdtree.deleteNode(pn)
    bsf = newkdtree.BFS(newkdtree.root)
    bsfdata = []
    for i in bsf:
        bsfdata.append(i.data)
    print('广度优先遍历结果为{}'.format(bsfdata))







    # test 最邻近搜索
    newkdtree = KDTree()
    newkdtree.insertNode('A', 40, 60) # A
    newkdtree.insertNode('B', 10, 75) # B
    newkdtree.insertNode('C', 70, 20) # C
    newkdtree.insertNode('D', 25, 15) # D
    newkdtree.insertNode('E', 80, 70) # E
    newkdtree.insertNode('F', 20, 45) # F
    newkdtree.insertNode('G', 35, 45) # G
    newkdtree.insertNode('H', 60, 50) # H
    plt.figure("1")
    for i in range(20):
        newkdtree.insertNode('', float(random.randint(10, 80)), float(random.randint(10, 80)))
    bsf = newkdtree.BFS(newkdtree.root)
    drawPoints(bsf)
    inrangepoints = []
    inrangepoints = newkdtree.NearestNeighborSearch(newkdtree.root, 30, 20, 20, inrangepoints)

    drawPoints(inrangepoints, 'r')
    drawRange(10, 0, 50, 40)
    
    plt.figure("2")
    drawPoints(bsf)
    nearestpoint, mindistance, distance, inrangepoints = newkdtree.getNearestPoint(30, 20, 10, 3)
    drawRange(30-distance, 20-distance, 30+distance, 20+distance)
    plt.plot(30, 20, marker = '*', markersize = 10, color = 'r')
    drawPoints(inrangepoints, 'r')
    plt.plot(nearestpoint.x, nearestpoint.y, marker = "+")

    plt.show()
    

    









        
        

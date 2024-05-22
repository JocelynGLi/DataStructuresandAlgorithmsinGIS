'''
根据图构建四叉树，并实现以下算法

1、用Python语言编写一个点四叉树索引程序，要求接受城市的名称和它们的地理位置(lon,lat)，然后将它们插入到四叉树中。

2、设计算法：计算到指定位置P(lon,lat)的距离为d的范围内（或与城市C的距离为d的范围内）的所有的城市名称。（选做）
'''
from math import *
import matplotlib.pyplot as plt
class City:
    def __init__(self, cityname, lon, lat):
        self.name = cityname
        self.longitude = lon
        self.latitude = lat

class QuadTreeNode:
    def __init__(self, city):
        self.city = city
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
class QuadTree:
    def __init__(self):
        self.root = None
    def insertNode(self, city):
        newqtnode = QuadTreeNode(city)
        if self.root is None:
            self.root = newqtnode
            return True
        else:
            pn = self.root
            pn2 = pn
            flag = 0
            while pn is not None:
                pn2 = pn
                if (city.longitude > pn.city.longitude) and (city.latitude >= pn.city.latitude):
                    pn = pn.nw
                    flag = 1
                elif (city.longitude <= pn.city.longitude) and (city.latitude > pn.city.latitude):
                    pn = pn.sw
                    flag = 2
                elif (city.longitude < pn.city.longitude) and (city.latitude <= pn.city.latitude):
                    pn = pn.se
                    flag = 3
                elif (city.longitude >= pn.city.longitude) and (city.latitude < pn.city.latitude):
                    pn = pn.ne
                    flag = 4
                else:
                    print("该节点已存在，插入失败")
                    return False
            if flag == 1:
                pn2.nw = newqtnode
            elif flag == 2:
                pn2.sw = newqtnode
            elif flag == 3:
                pn2.se = newqtnode
            elif flag == 4:
                pn2.ne = newqtnode
            return True
    def preOrderSearch(self, s, pn):
        '''深度优先遍历（先序）'''
        if pn is not None:
            s.append(pn)
            self.preOrderSearch(s, pn.nw)
            self.preOrderSearch(s, pn.ne)
            self.preOrderSearch(s, pn.sw)
            self.preOrderSearch(s, pn.se)
        return s    
    def BFS(self, pn):
        '''广度优先遍历'''
        queue = [pn]
        bsf = []
        while len(queue) != 0:
            queue2 = []
            for i in queue:
                bsf.append(i)
                if i.nw is not None:
                    queue2.append(i.nw)
                if i.ne is not None:
                    queue2.append(i.ne)
                if i.sw is not None:
                    queue2.append(i.sw)
                if i.se is not None:
                    queue2.append(i.se)

                queue = queue2
        return bsf
    def getDistance(self, city1, city2):
        distance = sqrt(pow(city1.longitude - city2.longitude, 2) + pow(city1.latitude - city2.latitude, 2)) # 欧式距离
        return distance
    def getCityByDistance(self, city, dist_threshold):
        nearcities = []
        allcity = self.BFS(self.root)
        for i in allcity:
            dist = self.getDistance(city, i.city)
            if  dist < dist_threshold:
                nearcities.append(i)
        return nearcities
    def drawCities(self):
        bsf = self.BFS(self.root)
        for i in bsf:
            plt.plot(i.city.longitude, i.city.latitude, marker = "+", color = 'b')
if __name__ == "__main__":
    city1 = City("Louisville", 38, 85)
    city2 = City("Chicago", 41, 87)
    city3 = City("Washington", 38, 77)
    city4 = City("Nashville", 36, 87)
    city5 = City("Atlanta", 34, 84)
    city6 = City("Pittsburgh", 40, 79)
    city7 = City("New York", 40, 74)
    city8 = City("Cleveland", 41, 81)
    city9 = City("Dayton", 39, 84)
    city10 = City("Montreal", 45, 73)
    newqtree = QuadTree()
    newqtree.insertNode(city1)
    newqtree.insertNode(city2)
    newqtree.insertNode(city3)
    newqtree.insertNode(city4)
    newqtree.insertNode(city5)
    newqtree.insertNode(city6)
    newqtree.insertNode(city7)
    newqtree.insertNode(city8)
    newqtree.insertNode(city9)
    newqtree.insertNode(city10)
    s = []
    s = newqtree.preOrderSearch(s, newqtree.root)



    print("先序深度优先遍历")
    for i in s:
        print(i.city.name)
    bsf = newqtree.BFS(newqtree.root)



    print("广度优先遍历")
    for i in bsf:
        print(i.city.name)


    print("查找附近的城市")
    plt.figure("查找附近的城市")
    ax = plt.subplot(111)
    newqtree.drawCities()
    
    newcity = City("", 39, 75)
    nearcities = newqtree.getCityByDistance(newcity, 10)

    for i in nearcities:
        print(i.city.name)
        plt.plot(i.city.longitude, i.city.latitude, marker = '+', color = 'r')
        ax.text(i.city.longitude, i.city.latitude, i.city.name)

    plt.plot(newcity.longitude, newcity.latitude, marker = 'o', color = 'r')

    plt.show()

        
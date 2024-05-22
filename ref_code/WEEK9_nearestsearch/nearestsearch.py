'''
实现最邻近搜索算法

在地理空间M中给定一个点集S和一个目标点q（q∈M），在S中找到距离最近的点（距离由欧式距离决定）。

注：可以使用K-d树、点的四叉树、区域四叉树、金字塔索引等数据结构
'''
from KDT import KDTree, drawRange
import json
import matplotlib.pyplot as plt
def loadJson(jsonfilename):
    with open(jsonfilename, 'r', encoding='utf-8') as jf:
        data = json.load(jf)
        return data
def getRestaurPoi(data):
    restaurpoi = KDTree()
    for i in data["features"]:
        lon = i["properties"]["lng"]
        lat = i["properties"]["lat"]
        name = i["properties"]["name"]
        restaurpoi.insertNode(name, lon, lat)
    return restaurpoi
def drawPOI(data):
    allpois = data.BFS(data.root)
    x = []
    y = []
    for item in allpois:
        x.append(item.x)
        y.append(item.y)
    plt.scatter(x, y)


        




if __name__ == "__main__":
    jsonfilename = r"restaur-poi.geojson"
    data= loadJson(jsonfilename)
    restaurpoi = getRestaurPoi(data)
    plt.figure("POI")
    ax = plt.subplot(121)
    drawPOI(restaurpoi)
    pointx = 121.45
    pointy = 31.035
    nearestpoint, mindistance, distance, inrangepoints = restaurpoi.getNearestPoint(pointx, pointy, 0.001)
    # 最邻近搜索，设置一个Point点，再和搜索范围 如果该搜索范围中没有找该点 则会扩大搜索范围继续查找
    drawRange(pointx-distance, pointy-distance, pointx+distance, pointy+distance)
    plt.plot(pointx, pointy, marker='*', color = 'r')
    plt.plot(nearestpoint.x, nearestpoint.y, marker='+', color = 'r')
    ax2 = plt.subplot(122)
    drawRange(pointx-distance, pointy-distance, pointx+distance, pointy+distance)
    plt.plot(pointx, pointy, marker='*', color = 'r')
    plt.plot(nearestpoint.x, nearestpoint.y, marker='+', color = 'r')
    plt.plot([nearestpoint.x, pointx], [nearestpoint.y, pointy], color = 'b')
    str = "{0:.5f}".format(mindistance)
    ax2.text((pointx+nearestpoint.x)/2, (pointy+nearestpoint.y)/2, str)

    plt.show()

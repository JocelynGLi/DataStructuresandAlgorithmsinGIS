import geopandas
import json
import numpy as np
from math import *
import matplotlib.pyplot as plt
'''
计算sh_dist_utm.geojson数据文件中各行政区的周长与面积，并与提供的数据对比验证。
'''

# read geojson file
def loadgeojsonfile(filename):
    '''读取geojson文件'''
    data = geopandas.read_file(filename)
    return data
def loadjsonfile(filename):
    '''读取json格式的数据'''
    '''utf-8编码'''
    with open(filename, 'r', encoding="utf-8") as jsfile:
        data = json.load(jsfile)
        return data
    


class Point:
    '''点'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
def distance(point1, point2):
    dist = sqrt(pow((point1.x - point2.x), 2) + pow((point1.y - point2.y),  2))
    return dist



class PolyLine:
    '''折线'''
    def __init__(self, pointset):
        '''pointset为numpy的array'''
        self.npoints = pointset.shape[0]
        self.point = []
        for i in range(self.npoints):
            newpoint = Point(pointset[i][0], pointset[i][1])
            self.point.append(newpoint)
    def getbbox(self):
        xmin = self.point[0].x
        xmax = self.point[0].x
        ymin = self.point[0].y
        ymax = self.point[0].y
        for item in self.point:
            if item.x < xmin:
                xmin = item.x
            if item.x > xmax:
                xmax =item.x
            if item.y < ymin:
                ymin = item.y
            if item.y > ymax:
                ymax = item.y
        return xmax, xmin, ymax, ymin
    def drawbox(self):
        xmax, xmin, ymax, ymin = self.getbbox()
        plt.plot([xmin, xmax, xmax, xmin, xmin], [ymin, ymin, ymax, ymax, ymin], 'r')

    def drawpolyline(self):
        x = []
        y = []
        for item in self.point:
            x.append(item.x)
            y.append(item.y)
        plt.plot(x, y, 'g')



class Polygon:
    '''多边形'''
    def __init__(self, pointset):
        self.npoints = pointset.shape[0] # 多边形的点的个数
        self.point = [] # 多边形的点集
        for i in range(self.npoints):
            newpoint = Point(pointset[i][0] , pointset[i][1])
            self.point.append(newpoint)    
    def getarea(self):
        '''计算多边形的面积'''
        area = 0
        for i in range(self.npoints - 1):
            area += 0.5 * (self.point[i+1].y + self.point[i].y) * (self.point[i+1].x - self.point[i].x)
        return area/1000000 # 单位：km2
    def getleng(self):
        '''计算多边形的周长'''
        leng = 0
        for i in range(self.npoints - 1):
            leng += distance(self.point[i], self.point[i+1])
        return leng/1000 # 单位：km
    def getbbox(self):
        '''获取多边形的最小外接矩形'''
        xmax = self.point[0].x
        xmin = self.point[0].x
        ymax = self.point[0].y
        ymin = self.point[0].y # 初始化
        for i in range(self.npoints - 1):        
            if self.point[i].x < xmin:
                xmin = self.point[i].x
            if self.point[i].x > xmax:
                xmax = self.point[i].x
            if self.point[i].y < ymin:
                ymin = self.point[i].y
            if self.point[i].y > ymax:
                ymax = self.point[i].y
        return xmax, xmin, ymax, ymin
    def drawpolygon(self, color='b'):
        pointx = []
        pointy = []
        for i in range(self.npoints):
            pointx.append(self.point[i].x)
            pointy.append(self.point[i].y)
        plt.plot(pointx, pointy, color)
    def drawbbox(self):
        xmax, xmin, ymax, ymin = self.getbbox()
        plt.plot([xmin, xmax, xmax, xmin, xmin], [ymin, ymin, ymax, ymax, ymin], 'r')

 

class MultiPolygon:
    '''多多边形'''
    def __init__(self, polygon): 
        self.nparts = len(polygon) # 多多边形的多边形个数
        self.multipolygon = polygon 
    def getarea(self):
        area = 0
        for item in self.multipolygon:
            area += item.getarea()
        return area
    def getleng(self):
        leng = 0
        for item in self.multipolygon:
            leng += item.getleng()
        return leng
    def drawmultipolygon(self):
        for item in self.multipolygon:
            item.drawpolygon()
    


## test
if __name__ == "__main__":
    filename = r"sh_dist_utm.geojson"
    filename = r"WEEK4 5\taxi_utm\sh_dist_utm.geojson"
    data = loadgeojsonfile(filename)
    data2 = loadjsonfile(filename)
    print("---------------Shape Area and Length of Districts from File(unit: square kilometers and kilometer)---------------")
    for i in range(9):
        print("{0}区\t面积：\t{1:.2f}\t周长：\t{2:.2f}".format(data["NAME"][i], data["Shape_Area"][i], data["Shape_Leng"][i]))
    print("--------------- Calculate the Shape Area and Length of Districts(unit: square kilometers and kilometer)---------------")
    for i in range(9): # 计算9个行政区的周长和面积
        feature_cor = data2["features"][i]['geometry']['coordinates']
        if len(feature_cor) == 1: # 要素只有一个多边形
            districtcor = np.array(feature_cor[0][0]) # 区多边形的坐标点集
            district_polygon = Polygon(districtcor)
            area = district_polygon.getarea()
            leng = district_polygon.getleng()
            print("{0}区\t面积：\t{1:.2f}\t周长：\t{2:.2f}".format(data2["features"][i]["properties"]["NAME"], area, leng))
            district_polygon.drawpolygon()
        elif len(feature_cor) > 1: #要素有多个多边形
            nparts = len(feature_cor)
            polygon = [] 
            for j in range(nparts):
                districtcor = np.array(feature_cor[j][0])
                district_polygon = Polygon(districtcor)
                polygon.append(district_polygon)
            district_polygon = MultiPolygon(polygon)
            area = district_polygon.getarea()
            leng = district_polygon.getleng()
            print("{0}区\t面积：\t{1:.2f}\t周长：\t{2:.2f}".format(data2["features"][i]["properties"]["NAME"], area, leng))
            district_polygon.drawmultipolygon()
    filename2 = r'WEEK4 5\taxi_utm\2taxi_traces_utm.geojson'
    data3 = loadjsonfile(filename2)
    line = data3["features"][0]['geometry']['coordinates']
    linecor = np.array(line)
    trace_polyline = PolyLine(linecor)
    trace_polyline.drawpolyline()
    plt.show()
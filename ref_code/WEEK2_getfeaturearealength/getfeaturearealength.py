import geopandas
import json
import numpy as np
from math import *
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

if __name__ == "__main__":
    filename = r"sh_dist_utm.geojson"
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

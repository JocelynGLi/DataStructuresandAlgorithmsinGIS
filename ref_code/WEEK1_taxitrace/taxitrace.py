import csv
import math
from math import *


''' 
有2辆出租车（A车和C车）的轨迹数据，csv格式，utf-8字符编码。包含的字段值有车牌号（分组用），行政区、定位时间，经度和纬度，瞬时速度和方向角。
    （1）计算各组瞬时车速的最大值，最小值、平均值和变异系数
    （2）求出A车和C车轨迹中，距离最近的两个点。
'''
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def readdata(filename):
    '''读取数据'''
    '''utf-8编码'''
    '''返回路径A和路径C路径的坐标'''
    with open(filename,'r',encoding="utf-8") as csvfile:
        csv_read = csv.DictReader(csvfile)
        routeA = []
        routeC = []
        for item in csv_read:
            if item["车牌号"] == "00028285631475467C53540B25F6853A":
                routeA.append(item)
            elif item["车牌号"] == "000BA4D4FF6B202DEE08318485CE6E4C":
                routeC.append(item)
    return routeA, routeC
def maxnum(data, key):
    '''获取最大值'''
    data_max = 0
    for item in data:
        temp = float(item[key])
        if temp > data_max:
            data_max = temp
    return data_max

def minnum(data, key):
    '''获取最小值'''
    data_min = 10000
    for item in data:
        temp  = float(item[key])
        if temp < data_min:
            data_min = temp
    return data_min



def averagenum(data, key):
    '''平均值'''
    '''data：数据集'''
    '''key：计算的参考属性'''
    total = 0 # 总和
    count = 0 # 计数
    for item in data:
        total += float(item[key])
        count += 1 
    data_average = total / count # 均值
    return data_average
    
def STDV(data, key):
    '''标准差'''
    total = 0 # 平方和
    count = 0 # 计数
    aver_data = averagenum(data, key)
    for item in data:
        total += pow((float(item[key]) - aver_data), 2)
        count += 1
    data_stdv= sqrt(total / count)
    return data_stdv


def COV(data, key):
    '''变异系数 = 标准差/平均值'''
    data_aver = averagenum(data, key) # 均值
    data_stdv = STDV(data, key) # 标准差
    data_cov = data_stdv / data_aver # 变异系数
    return data_cov

def getdistance(point1, point2):
    '''计算两点之间的间距'''
    '''将经纬度坐标作为(x, y)，采用欧式距离计算'''
    distance = 0
    distance = sqrt(pow((point1.x - point2.x), 2) + pow((point1.y - point2.y), 2))
    return distance
def getmindist(routeA, routeC):
    '''获取最短距离'''
    routeA_cor = []
    routeC_cor = []
    for item in routeA:
        point = Point(float(item['经度']), float(item['纬度']))
        routeA_cor.append(point)
    for item in routeC:
        point = Point(float(item['经度']), float(item['纬度']))
        routeC_cor.append(point)
    point_A = None # 最小距离的A点
    point_C = None # 最小距离的C点
    mindistance = 10000 # 最小距离
    for a in routeA_cor:
        for c in routeC_cor:
            temp_dis = getdistance(a, c)
            if temp_dis < mindistance:
                mindistance = temp_dis
                point_A = a
                point_C = c
    return point_A, point_C, mindistance


if __name__ == "__main__":
    filename = r"2辆车的轨迹数据.csv" #utf-8编码 csv
    routeA, routeC = readdata(filename)
    routeA_maxV = maxnum(routeA, '瞬时速度')
    routeC_maxV = maxnum(routeC, '瞬时速度')
    routeA_minV = minnum(routeA, '瞬时速度')
    routeC_minV = minnum(routeC, '瞬时速度')
    routeA_averV = averagenum(routeA, '瞬时速度')
    routeC_averV = averagenum(routeA, '瞬时速度')
    routeA_covV = COV(routeA, '瞬时速度')
    routeC_covV = COV(routeC, '瞬时速度')
    pointA, pointC, mindistance = getmindist(routeA, routeC)

    print("-------------统计A组瞬时车速-------------")
    print("最大值\t\t{0}".format(routeA_maxV))
    print("最小值\t\t{0}".format(routeA_minV))
    print("平均值\t\t{0}".format(routeA_averV))
    print("变异系数\t{0}".format(routeA_covV))
    print("-------------统计C组瞬时车速-------------")
    print("最大值\t\t{0}".format(routeC_maxV))
    print("最小值\t\t{0}".format(routeC_minV))
    print("平均值\t\t{0}".format(routeC_averV))
    print("变异系数\t{0}".format(routeC_covV))
    print("---------轨迹A和轨迹C两点最近距离---------")
    print("最近距离为\t{0}".format(mindistance))
    
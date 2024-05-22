'''
运用矢量叉积方法，上机实现下列算法

1、折线段（PolyLine）拐向的判断算法实现； # direction()

2、点在线上的算法实现； # isinline()点是否在线段上 isinpolyline()点是否在折线上

3、直线段相交算法实现； # islineintersect()直线段是否相交

4、基于扫描线算法：判断点在多边形内的算法实现； # ispointinpolygon()

5、基于练习4：计算网线车轨迹经过了上海市的哪些行政区。# pathindistrict() ispolylineinpolygon()

'''
import matplotlib.pyplot as plt
from shapefeature import Point, Polygon, MultiPolygon, PolyLine, loadjsonfile

import numpy as np

#
# 算法实现
# 
def direction(point1, point2, point3):
    '''判断折线段拐向'''
    '''point1 为线段起始点 point2 为中间点 point3为终点'''
    '''
    return 1 共线
    return 2 向左
    return 3 向右
    '''
    v1 = (point2.x - point1.x, point2.y - point1.y)
    v2 = (point3.x - point1.x, point3.y - point1.y)
    m = v1[0] * v2[1] - v1[1] * v2[0]
    if m ==0:
        return 1
    elif m > 0:
        return 2
    elif m < 0:
        return 3
    else:
        return False
    
    
def isinline(point1, point2, point3):
    '''点在线上'''
    '''
    point1 point2 为线段上的两个端点，point3 为判断是否在线上的点
    '''
    if direction(point1, point2, point3) == 1: # 三点共线
        '''判断在线内还是在延长线上'''
        if (point3.x > point2.x and point3.x >point1.x) or (point3.x < point1.x and point3.x < point1.x):
            return False # 在延长线上
        else:
            return True # 点在线内    
    else: # 三点不共线
        return False
def isinpolyline(point, polyline):
    '''点在折线上'''
    '''
    point 点
    '''
    n = polyline.npoints # 折线段的点的多少
    for i in range(n - 1):
        inline = isinline(polyline.point[i], polyline.point[i+1], point)
        if inline == True:
            return i
    return -1
def getmax(data):
    maxnum = data[0]
    for item in data:
        if item > maxnum:
            maxnum = item
    return maxnum
def getmin(data):
    minnum = data[0]
    for item in data:
        if item < minnum:
            minnum = item
    return minnum
def lineintersect(p1, p2, q1, q2):
    '''两个线段是否相交'''
    dire1 = direction(p1, p2, q1)
    dire2 = direction(p1, p2, q2)
    if dire1 == dire2 and dire1 != 1: # 点q1、q2在线段p1p2同侧 
        return None
    elif dire1 == dire2 and dire1 == 1: # 四点共线
        if (q1.x > getmax([p1.x, p2.x]) and q2.x > getmax([p1.x, p2.x])) or (q1.x < getmin([p1.x, p2.x]) and q2.x < getmin([p1.x, p2.x])): # 两线段的外接矩形不重合
            return None
        elif (getmax([p1.x, p2.x])== getmax([q1.x, q2.x])) and (getmin([p1.x, p2.x]) == getmin(q1.x, q2.x)):# 两线段重合 返回一条线段的两个点
            return [p1, p2] 
        else: # 两线段不重合 中间的点
            interval = [getmin([p1.x, p2.x, q1.x, q2.x]), getmax([p1.x, p2.x, q1.x, q2.x])]
            pointset = [] 
            if p1.x > interval[0] and p1.x < interval[1]:
                pointset.append(p1)
            if p2.x > interval[0] and p2.x < interval[1]:
                pointset.append(p2)
            if q1.x > interval[0] and q1.x < interval[1]:
                pointset.append(q1)
            if q2.x > interval[0] and q2.x < interval[1]:
                pointset.append(q2)
            if len(pointset) == 1:
                pointset.append(p1)
            return pointset
    else: # 点q1、q2在线段p1p2异侧
        xi= ( (p1.x * p2.y - p1.y * p2.x) * (q1.x - q2.x) - (p1.x - p2.x) * (q1.x * q2.y - q1.y * q2.x) ) / ( (p1.x - p2.x) * (q1.y - q2.y) - (p1.y - p2.y) * (q1.x - q2.x) ) 
        yi= ( (p1.x * p2.y - p1.y * p2.x) * (q1.y - q2.y) - (p1.y - p2.y) * (q1.x * q2.y - q1.y * q2.x) ) / ( (p1.x - p2.x) * (q1.y - q2.y) - (p1.y - p2.y) * (q1.x - q2.x) )
        interpoint = Point(xi, yi)
        if (interpoint.x > max([p1.x, p2.x])) or (interpoint.x < min([p1.x, p2.x])) or (interpoint.x > max([q1.x, q2.x])) or (interpoint.x < min([q1.x, q2.x])):
            return None
        else:
            return [interpoint]
        
def ispointinpolygon(point, polygon):
    '''基于扫描线算法：判断点在多边形内'''
    xmax, xmin, ymax, ymin = polygon.getbbox() # 获取多边形的外接矩形
    if (point.x > xmax) or (point.x < xmin) or (point.y > ymax) or (point.y < ymin): # 超过多边形边界
        return False
    else:
        rayline = [point, Point(xmax+1, point.y)] # 水平方向的射线
        n_intersect = 0 
        for i in range(polygon.npoints - 1):
            if (point.x == polygon.point[i].x) and (point.y == polygon.point[i].y):# 当点在多边形上时
                return True 
            else:# 当点不在多边形时
                intersectpoint1 = lineintersect(rayline[0], rayline[1], polygon.point[i], polygon.point[i+1]) # 求交点  
                if intersectpoint1 is not None: 
                    if len(intersectpoint1) == 2: # 当射线与线段共线时
                        n_intersect += 1 
                    elif (len(intersectpoint1) == 1) and (intersectpoint1[0].x == polygon.point[i].x): #当不共线但交点恰好是线段端点时
                        n_intersect = n_intersect
                    else:
                        n_intersect += 1

        if n_intersect%2 == 0: # 交点为偶数
            return False
        else:
            return True # 奇数
def islineinpolygon(polyline, polygon):
    '''判断折线段是否经过多边形'''
    inpolygonpoints = []
    for item in polyline.point:
        isinpolygon = ispointinpolygon(item, polygon)
        if isinpolygon is True:
            inpolygonpoints.append(item)
    return inpolygonpoints
    
def islineinmultipolygon(polyline, mulplygon):
    '''判断折线段是否经过多多边形'''
    ispass = []
    for item in mulplygon.multipolygon:
        inpolygonpoints = islineinpolygon(polyline, item)
        if len(inpolygonpoints) is not 0:
            ispass.append(1)
        else:
            ispass.append(0)
    return ispass


def drawintersectline(ax, p1, p2, q1, q2):
    interspn = lineintersect(p1, p2, q1, q2)
    plt.plot([p1.x, p2.x], [p1.y, p2.y], 'r')
    plt.plot([q1.x, q2.x], [q1.y, q2.y], 'r')
    if interspn is not None:
        for i in interspn:
            plt.plot(i.x, i.y,'o')
        plt.title("intersect")
    else:
        plt.title("do not intersect")

def drawline(line):
    x = []
    y = []
    for item in line:
        x.append(item.x)
        y.append(item.y)
    plt.plot(x, y, 'r')




if __name__ == "__main__":
    filename1 = r"taxi_utm\2taxi_pos_utm.geojson" # 出租车位置
    filename2 = r"taxi_utm\2taxi_traces_utm.geojson" # 出租车轨迹 polyline
    filename3 = r"taxi_utm\sh_dist_utm.geojson" # 上海市行政区

    taxipos_data = loadjsonfile(filename1)
    taxitrace_data = loadjsonfile(filename2)
    shdist_data = loadjsonfile(filename3)

    # '''------------------------------判断拐向------------------------------'''
    # plt.figure("判断拐向")
    line1 = taxitrace_data["features"][0]['geometry']['coordinates']
    linecor1 = np.array(line1)
    trace_polyline1 = PolyLine(linecor1)
    line2 = taxitrace_data["features"][1]['geometry']['coordinates']
    linecor2 = np.array(line2)
    trace_polyline2 = PolyLine(linecor2)
    # 在polyline中取三个点
    point = []
    for i in range(3):
        point.append(trace_polyline1.point[i])    
    dire = direction(point[0], point[1], point[2])
    ax = plt.subplot(1,1,1)
    plt.plot([point[0].x, point[1].x, point[2].x], [point[0].y, point[1].y, point[2].y], 'r',marker='o')
    pname = ['p1', 'p2', 'p3']
    for i in range(3):
        ax.text(point[i].x + 2, point[i].y + 2, pname[i])
    if dire == 1:
        plt.title("three-point congruence")
    elif dire == 2:
        plt.title("The line turns left.")
    else:
        plt.title("The line turns right.")
    '''------------------------------点在线上------------------------------'''
    # 点是否在线段上
    inline = isinline(point[0], point[1], point[2])
    plt.figure("判断点是否在线段上")
    if inline is False:
        print("[{0},{1}]不在线上".format(point[2].x, point[2].y))
    plt.plot([point[0].x, point[1].x], [point[0].y, point[1].y],'r')
    plt.plot(point[2].x, point[2].y, marker = 'o')
    plt.title("[{0:.2f},{1:.2f}]This point is not on the line.".format(point[2].x, point[2].y))
    # 点是否在折线上
    plt.figure("点是否在折线上")
    inline = isinpolyline(point[2], trace_polyline1)
    trace_polyline1.drawpolyline()
    plt.plot(point[2].x, point[2].y, marker = 'o')
    if inline == -1:
        plt.title("[{0:.2f},{1:.2f}]This point is not on the line.".format(point[2].x, point[2].y))
    else:
        plt.plot([trace_polyline1.point[i].x, trace_polyline1.point[i+1].x], [trace_polyline1.point[i].y, trace_polyline1.point[i+1].y],'r')
        plt.title("[{0:.2f},{1:.2f}]This point is on the line.".format(point[2].x, point[2].y))
    '''------------------------------线段相交------------------------------'''
    plt.figure("线段相交")
    ax = plt.subplot(2,2,1)
    p1 = Point(1, 1)
    p2 = Point(2, 2)
    q1 = Point(1, 2)
    q2 = Point(2, 1)
    drawintersectline(ax, p1, p2, q1, q2) # 相交
    ax = plt.subplot(2,2,2)
    p1 = Point(1, 1)
    p2 = Point(2, 2)
    q1 = Point(3, 4)
    q2 = Point(1, 5)
    drawintersectline(ax, p1, p2, q1, q2) # 不相交
    ax = plt.subplot(2,2,3)
    p1 = Point(1, 1)
    p2 = Point(2, 2)
    q1 = Point(3, 3)
    q2 = Point(4, 4)
    drawintersectline(ax, p1, p2, q1, q2) # 不相交
    ax = plt.subplot(2,2,4)
    p1 = Point(1, 1)
    p2 = Point(2, 1)
    q1 = Point(1, 1)
    q2 = Point(4, 1)
    drawintersectline(ax, p1, p2, q1, q2) # 相交
    '''------------------------------点是否在多边形内------------------------------'''
    plt.figure("判断点在多边形内")
    ax = plt.subplot(111)
    region = shdist_data["features"][0]['geometry']['coordinates']
    dist_polygon = Polygon(np.array(region[0][0]))
    dist_polygon.drawpolygon()
    p = Point(350080, 3438040)
    i = ispointinpolygon(p, dist_polygon)

    plt.plot(p.x, p.y, marker = 'o')
    ax.text(p.x, p.y, i)
    p2 = Point(347462.046155321528204,3448444.67926961928606)
    i = ispointinpolygon(p2, dist_polygon)
    plt.plot(p2.x, p2.y, marker = 'o')
    ax.text(p2.x, p2.y, i)

    p3 = Point(334130, 3446980)
    i = ispointinpolygon(p3, dist_polygon)
    ax.text(p3.x, p3.y, i)
    plt.plot(p3.x, p3.y, marker = 'o')
    '''------------------------------线是否在多边形内------------------------------'''
    plt.figure("线是否在多边形内")
    ax = plt.subplot(111)
    region = shdist_data["features"][6]['geometry']['coordinates']
    dist_polygon = Polygon(np.array(region[0][0]))
    dist_polygon.drawpolygon()
    trace_polyline1.drawpolyline()
    trace_polyline2.drawpolyline()
    inpolygonpoints1 = islineinpolygon(trace_polyline1, dist_polygon)
    inpolygonpoints2 = islineinpolygon(trace_polyline2, dist_polygon)
    if inpolygonpoints1 is not None:
        text = "this line passes through the polygon"
        ax.text(trace_polyline1.point[0].x, trace_polyline1.point[0].y, text)
        drawline(inpolygonpoints1)
    else: 
        text = "this line does not pass through the polygon"
        ax.text(trace_polyline1.point[0].x, trace_polyline1.point[0].y, text)

    if inpolygonpoints2 is not None:
        text = "this line passes through the polygon"
        ax.text(trace_polyline2.point[0].x, trace_polyline2.point[0].y, text)
        drawline(inpolygonpoints2)
    else: 
        text = "this line does not pass through the polygon"
        ax.text(trace_polyline2.point[0].x, trace_polyline2.point[0].y, text)
    '''------------------------------线经过哪些多多边形------------------------------'''
    plt.figure("轨迹经过的行政区，红色为经过，蓝色为未经过")
    polygon = []
    for i in range(9):# 9个行政区
        feature_cor = shdist_data["features"][i]['geometry']['coordinates']
        if len(feature_cor) == 1: # 要素只有一个多边形
            districtcor = np.array(feature_cor[0][0]) # 区多边形的坐标点集
            district_polygon = Polygon(districtcor)
            polygon.append(district_polygon)
        elif len(feature_cor) > 1: #要素有多个多边形
            nparts = len(feature_cor)
            for j in range(nparts):
                districtcor = np.array(feature_cor[j][0])
                district_polygon = Polygon(districtcor)
                polygon.append(district_polygon)
    district_multipolygon = MultiPolygon(polygon)
    district_multipolygon.drawmultipolygon()
    trace_polyline1.drawpolyline()
    trace_polyline2.drawpolyline()
    ispass = islineinmultipolygon(trace_polyline1, district_multipolygon)
    for i in range(len(ispass)):
        if ispass[i] == 1:# 经过
            district_multipolygon.multipolygon[i].drawpolygon('r')
    ispass = islineinmultipolygon(trace_polyline2, district_multipolygon)
    for i in range(len(ispass)):
        if ispass[i] == 1:# 经过
            district_multipolygon.multipolygon[i].drawpolygon('r')
    plt.show()    

     

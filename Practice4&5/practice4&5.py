import numpy as np
import json

#1.折线段（PolyLine）拐向的判断算法实现
def polyline_turn(p0, p1, p2):
    a = np.array([p2[0] - p0[0], p2[1] - p0[1]]) #a = p2 - p0
    b = np.array([p1[0] - p0[0], p1[1] - p0[1]]) #b = p1 - p0
    result = np.cross(a,b) #a、b进行叉乘
    if result < 0: #若叉乘结果小于0
        return '折线段拐向左侧'
    elif result == 0: #若叉乘结果等于0
        return '三点共线'
    else: #若叉乘结果大于0
        return '折线段拐向右侧'

#2.点在线上的算法实现
#思路：先判断线段p1q是否与线段p1p2共线。若共线，则存在三种情况：1.q位于线段的左侧射线；2.q位于线段的右侧射线；3.q位于线段上。若满足第三种情况，则可以判断点在线上
def point_on_line(q, p1, p2):
    direction = polyline_turn(p1, p2, q) #判断线段p1p2与线段p1q是否共线
    #若线段p1p2与线段p1q共线，且q的横坐标介于p1和p2的横坐标之间，且q的纵坐标介于p1和p2的纵坐标之间，则q点在线段p1pw2上
    if direction == '三点共线' and (min(p1[0],p2[0])) <= q[0] <= (max(p1[0],p2[0])) and (min(p1[1],p2[1])) <= q[1] <= (max(p1[1],p2[1])):
        return True
    else:
        return False

#3.直线段相交算法实现；
def intersection(p1, p2, q1, q2):
    #快速排斥试验
    if max(q1[0], q2[0]) < min(p1[0], p2[0]) or max(q1[1], q2[1]) < min(p1[1], p2[1]) or max(p1[0], p2[0]) < min(q1[0], q2[0]) or max(p1[1], p2[1]) < min(q1[1], q2[1]):
        return '直线段不相交'
    else:
        #矢量跨立试验
        p1p2 = np.array([p2[0] - p1[0],p2[1] - p1[1]]) #p1p2 = p2 - p1
        p1q1 = np.array([q1[0] - p1[0],q1[1] - p1[1]]) #p1q1 = q1 - p1
        p1q2 = np.array([q2[0] - p1[0],q2[1] - p1[1]]) #p1q2 = q2 - p1
        a = np.cross(p1p2, p1q1) #p1p2、p1q1进行叉乘
        b = np.cross(p1p2, p1q2) #p1p2、p1q2进行叉乘
        c = a * b #a与b相乘
        if c < 0:
            return '直线段相交'
        elif c > 0:
            return '直线段不相交'
        elif c == 0:
            return '直线段共线'  
        
#4.使用铅垂线法判断点在多边形内
def point_inside_polygon(polygon, point):
    inside = False #flag
    intersect = 0 #初始化交点个数为0
    ymin=[] #获得多边形所有顶点的纵坐标
    for i in range(len(polygon)): #遍历多边形的所有顶点
        x_, y_ = polygon[i]
        ymin.append(y_) #将当前顶点的纵坐标加入到列表中
    p_ =[point[0],min(ymin)-1] #p_为point铅垂线的另一个端点
    for j in range(len(polygon)):
        #获得多边形相邻两个顶点，从而获得多边形的一条边
        q1 = polygon[j]
        if j == len(polygon) - 1:
            q2 = polygon[0]
        else:
            q2 = polygon[j+1]
        result = intersection(q1, q2, point, p_)#判断铅垂线与边是否相交
        if result == '直线段相交':
            intersect += 1#若相交，交点数加1
    #若交点数为奇数，则点在多边形内
    if intersect % 2 == 1:
        inside = not inside
    return inside

#5.基于练习4：计算网线车轨迹经过了上海市的哪些行政区
#读取出租车轨迹数据
taxitrace_path = '/Users/jocelynli/Library/CloudStorage/OneDrive-stu.ecnu.edu.cn/ECNU/大三上/数据结构与算法/project/第4&5周/taxi_utm/2taxi_traces_utm.geojson'
with open(taxitrace_path, 'r',encoding="utf-8") as f2:
    taxitrace_data = json.loads(f2.read())

#读取上海区划数据
district_path = '/Users/jocelynli/Library/CloudStorage/OneDrive-stu.ecnu.edu.cn/ECNU/大三上/数据结构与算法/project/第4&5周/taxi_utm/sh_dist_utm.geojson'
with open(district_path, 'r',encoding="utf-8") as f1:
    district_data = json.loads(f1.read())
taxitrace_features = taxitrace_data['features']

#分别获取两辆车轨迹的坐标
for i in range(len(taxitrace_features)):
    taxi_feature = taxitrace_features[i]
    if taxi_feature['properties']['taxi_no'] == '000BA4D4FF6B202DEE08318485CE6E4C':
        C = taxi_feature['geometry']['coordinates']
    else:
        A = taxi_feature['geometry']['coordinates']

#获取各个区multipolygon的顶点
district_features = district_data['features'] #提取所有区的features
names = [] #用于存储区名称的空列表
coordinates = [] #用于存储区顶点坐标的空列表
for j in range(len(district_features)): #遍历每个区的feature
    district_feature = district_features[j]
    name = district_feature['properties']['NAME'] #提取当前区的名称
    names.append(name) #将名称加入到列表中
    coordinate = district_feature['geometry']['coordinates'] #获取区的顶点坐标
    L = [] #用于存储单个区的所有顶点的空列表
    for k in range(len(coordinate)):
        a = coordinate[k]
        for l in range(len(a)):
            b = a[l]
            for m in range(len(b)):
                c = b[m]
                L.append(c)
    coordinates.append(L)

#判断A车经过了哪些区
A_district = [] #用于存储A车经过的区的名称的空列表
for s in range(len(A)):  #遍历A车轨迹坐标列表
    A_point = A[s] #获取A车轨迹的单个坐标点
    for t in range(len(coordinates)): # 遍历所有区的顶点坐标信息列表
        district = coordinates[t] #获取单个区的顶点坐标信息
        judge = point_inside_polygon(district, A_point) #判断A点是否在该区内
        if judge:
            A_district.append(names[t]) #若A点在该区内，则将区名称添加到A_district列表中
A_district = list(set(A_district)) #将A_district列表去重

#判断C车经过了哪些区
C_district = []
for g in range(len(C)):
    C_point = C[g]
    for h in range(len(coordinates)):
        district = coordinates[h]
        judge = point_inside_polygon(district, C_point)
        if judge:
            C_district.append(names[h])
C_district = list(set(C_district))

print('A车经过的区有：','、'.join(A_district))
print('C车经过的区有：','、'.join(C_district))
#1.积分法
import json
import math
print('方法一：积分法')
#读取数据
with open(r'/Users/jocelynli/Library/CloudStorage/OneDrive-stu.ecnu.edu.cn/ECNU/大三上/数据结构与算法/project/第2周/sh_dist_utm.geojson', 'r',encoding="utf-8") as f:
    file = f.read()
data = json.loads(file) #将该文件转换为json格式

features = data['features'] #提取数据中的Features
coordinates = [] #初始化坐标列表
for feature in features: #遍历每个feature
    geometry = feature['geometry'] #提取每个feature中的geometry信息
    if geometry['type'] == 'MultiPolygon': #判断矢量类型是否为多个多边形
        coordinates.append(geometry['coordinates']) #若是，将该坐标信息添加到列表中

#遍历feature计算面积和周长
for i in range(len(features)): #遍历每个feature
    a=features[i] #提取当前feature
    name = a['properties']['区县名称'] #提取feature到名字
    s=0 #初始化面积为0
    l=0 #初始化周长为0
    b=coordinates[i] #提取当前feature的坐标
    for j in range(len(b)): #遍历当前坐标列表
        c=b[j] #提取当前坐标
        for k in range(len(c)): #遍历坐标
            d=c[k] #提取当前坐标
            for n in range(len(d)-1):
                coord1=d[n] #提取当前坐标点
                coord2=d[n+1] #提取下一个坐标点
                x1=coord1[0]
                y1=coord1[1]
                x2=coord2[0]
                y2=coord2[1]
                s=s+(y1+y2)*(x2-x1)/2 #计算面积，并加入到s中
                l=l+math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2)) #计算周长，并加入到s中
    print(f"{name}：面积{s/1000000}km^2，周长{l/1000}km") #输出结果

#2.使用shapely库
import geopandas as gpd
from shapely.geometry import shape
print('方法二：使用shapely库')
#读取数据
filepath='/Users/jocelynli/Library/CloudStorage/OneDrive-stu.ecnu.edu.cn/ECNU/大三上/数据结构与算法/project/第2周/sh_dist_utm.geojson'
gdf=gpd.read_file(filepath)
perimeters = [] #初始化周长列表
areas = [] #初始化面积列表
names=gdf['区县名称'] #获取行政区名称
for idx, row in gdf.iterrows():
    # 将GeoJSON几何对象转换为Shapely几何对象
    geom = shape(row['geometry']) #转换为Shapely几何对象
    perimeter = geom.length #计算周长
    area = geom.area #计算面积
    perimeters.append(perimeter/1000) #将周长加入到列表中
    areas.append(area/1000000) #将面积加入到列表周
for i in range(len(areas)):
    print(f'{names[i]}：面积{areas[i]}km^2，周长{perimeters[i]}km') #遍历输出结果

#与提供的数据对比验证
print('geojson文件中的面积和周长为：')
print(gdf[['区县名称', 'Shape_Area', 'Shape_Leng']])
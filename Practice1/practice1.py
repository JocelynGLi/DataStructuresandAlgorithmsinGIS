import pandas as pd
from scipy.spatial import distance
#读取数据
filepath = '/Users/jocelynli/Library/CloudStorage/OneDrive-stu.ecnu.edu.cn/ECNU/大三上/数据结构与算法/project/第1周/2辆车的轨迹数据/2辆车的轨迹数据.csv'
file = pd.read_csv(filepath, header = 0, encoding = 'utf-8')

#清洗经纬度不准确的数据(删除经纬度没有精确到小数点后6位的数据)
data = file[(file['经度'].apply(lambda x: len(str(x).split('.')[-1])) == 6) & (file['纬度'].apply(lambda x: len(str(x).split('.')[-1])) == 6)]

#计算两辆车瞬时速度的最值、平均值和变异系数
grouped = data.groupby('车牌号')
result = grouped['瞬时速度'].agg(['max', 'min', 'mean', 'std'])
print(result)

#计算两辆车轨迹中距离最近的两个点
plates = data['车牌号'].tolist() #获取所有的车牌号
plate = list(set(plates)) #删除列表中的重复值
data_a = data[data['车牌号'] == plate[1]] #筛选车牌号为A的数据
data_c = data[data['车牌号'] == plate[0]] #筛选车牌号为C的数据
min_dis = float('inf') #初始化设定最近距离为正无穷
min_points = [] #初始化放置最近两个点的空列表
for i in range(len(data_a)):
    a = data_a.iloc[i] #遍历A车的所有点
    for j in range(len(data_c)):
        c = data_c.iloc[j] #遍历C车点所有点
        dis = distance.euclidean((a['经度'], a['纬度']), (c['经度'], c['纬度'])) #计算两辆车任意两点之间的欧式距离
        if dis <= min_dis:
            min_dis = dis #若该距离小于先前的最近距离，则最近距离等于该距离
            min_points = [[a['经度'], a['纬度']], [c['经度'], c['纬度']]] #将这两个点放入列表中

#输出结果
print("两辆车轨迹中距离最近的两个点：")
print("A车点:", min_points[0])
print("C车点:", min_points[1])
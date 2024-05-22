#练习2:编写点四叉树索引程序，要求接受城市的名称和它们的地理位置(lon,lat)，然后插入到四叉树中
#练习3:计算到指定位置的距离为d的范围内的所有城市的名称
import math
#定义节点
class QdNode:
    def __init__(self, pt, ptName):
        self.point = pt
        self.name = ptName
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
#构建点四叉树
class QdTree:
    def __init__(self, x1, y1, x2, y2):
        self.root = None
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    #插入
    def insert(self, pt, ptName):
        node = QdNode(pt, ptName) #创建新节点
        if self.root is None: #如果树为空，则该节点为根节点
            self.root = node
        else:
            p = self.root
            x, y = pt
            x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
            while True: #判断节点位置是否在当前节点范围内
                if x1 <= x < x2 and y1 <= y < y2: #如果在当前节点范围内，判断四个子节点位置，并移动到相应子节点
                    if x < (x1 + x2) / 2: #判断节点是否在当前节点的左边
                        if y < (y1 + y2) / 2: #NW子节点
                            if p.nw is None: #如果当前节点的NW子节点为空，则将新节点设为NW子节点并中断循环
                                p.nw = node
                                break
                            p = p.nw #如果NW子节点不为空，则将当前节点移到NW子节点
                            x2 = (x1 + x2) / 2 #更新范围的x轴右边界
                            y1 = (y1 + y2) / 2 #更新范围的y轴下边界
                        else: #SW子节点
                            if p.sw is None:
                                p.sw = node
                                break
                            p = p.sw
                            x2 = (x1 + x2) / 2,
                            y1 = (y1 + y2) / 2
                    else: #节点在当前节点的右边
                        if y < (y1 + y2) / 2: #NE子节点
                            if p.ne is None:
                                p.ne = node
                                break
                            p = p.ne
                            x1 = (x1 + x2) / 2
                            y2 = (y1 + y2) / 2
                        else: #SE子节点
                            if p.se is None:
                                p.se = node
                                break
                            p = p.se
                            x1 = (x1 + x2) / 2
                            y1 = (y1 + y2) / 2
                else:
                    return
    #计算距离
    def distance(self, lon1, lat1, lon2, lat2):
        R = 6371 #地球半径
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2]) #将经度和纬度转换为弧度
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2 #计算球面距离
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c #计算距离
        return distance
    #相交
    def intersect(self, lon, lat, d, node):
        x1, y1, x2, y2 = node.point[0], node.point[1], node.point[0], node.point[1] #获取节点的边界坐标
        #调整边界坐标
        x1, y1, x2, y2 = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
        x1, y1, x2, y2 = max(x1, self.x1), max(y1, self.y1), min(x2, self.x2), min(y2, self.y2)
        x1, y1, x2, y2 = max(x1, self.x1), max(y1, self.y1), min(x2, self.x2), min(y2, self.y2)
        x1, y1, x2, y2 = max(x1, self.x1), max(y1, self.y1), min(x2, self.x2), min(y2, self.y2)
        x1, y1, x2, y2 = max(x1, self.x1), max(y1, self.y1), min(x2, self.x2), min(y2, self.y2)
        x1, y1, x2, y2 = max(x1, self.x1), max(y1, self.y1), min(x2, self.x2), min(y2, self.y2)
        #更新边界坐标范围
        x1 = max(x1, self.x1)
        y1 = max(y1, self.y1)
        x2 = min(x2, self.x2)
        y2 = min(y2, self.y2)
        #获取节点的最小和最大经纬度
        min_lon = min(node.point[0], self.x2)
        min_lat = min(node.point[1], self.y2)
        max_lon = max(node.point[0], self.x1)
        max_lat = max(node.point[1], self.y1)
        #调整边界坐标范围
        x1, y1, x2, y2 = max(x1, max_lon), max(y1, max_lat), min(x2, min_lon), min(y2, min_lat)
        x1, y1, x2, y2 = max(x1, max_lon), max(y1, max_lat), min(x2, min_lon), min(y2, min_lat)
        #判断给定点是否在范围内
        return self.distance(lon, lat, (x1 + x2) / 2, (y1 + y2) / 2) <= d
    #查找
    def search(self, lon, lat, d):
        result = [] #用于存储符合条件的节点名称
        stack = [self.root] #存放待检查节点的栈
        while stack:
            node = stack.pop() #弹出一个节点
            if node:
                x, y = node.point #获取节点的经纬度
                if self.distance(lon, lat, x, y) <= d: #判断节点是否在距离d内
                    result.append(node.name) #将满足条件的节点名称添加到结果中
                #判断当前节点的子节点是否在距离d内，将在范围内的子节点添加到堆栈中以进行后续检查
                if node.nw and self.intersect(lon, lat, d, node.nw):
                    stack.append(node.nw)
                if node.ne and self.intersect(lon, lat, d, node.ne):
                    stack.append(node.ne)
                if node.sw and self.intersect(lon, lat, d, node.sw):
                    stack.append(node.sw)
                if node.se and self.intersect(lon, lat, d, node.se):
                    stack.append(node.se)
        return result
    #先序遍历
    def preorder_traversal(self):
        result = [] #创建空列表用于存储遍历结果
        stack = [self.root] #创建栈stack并将根节点放入其中
        while stack:  #当栈不为空时
            node = stack.pop()  #弹出栈顶节点
            if node: #如果节点存在
                result.append((node.point, node.name)) #将节点的坐标和名称加入结果列表
                #依次将各个子节点加入栈
                stack.append(node.nw)
                stack.append(node.ne)
                stack.append(node.sw)
                stack.append(node.se)
        return result
    #最邻近搜索
    def ClosestPointSearch(self, lon, lat):
        result = {'name': None, 'distance': float('inf')} #初始化结果字典，包括名称和距离，默认距离设为无穷大
        stack = [self.root] #创建栈stack并将根节点放入其中
        while stack: #当栈不为空时执行以下操作
            node = stack.pop() #弹出栈顶节点
            if node: #如果节点存在
                x, y = node.point #获取节点的坐标
                dist = self.distance(lon, lat, x, y) #计算给定点与节点的距离
                if dist < result['distance']: #如果该距离小于结果中记录的最小距离
                    result['name'] = node.name #更新最近节点的名称
                    result['distance'] = dist #更新最近距离
                if node.nw: #如果节点有NW子节点
                    stack.append(node.nw) #将NW子节点加入栈
                if node.ne:
                    stack.append(node.ne)
                if node.sw:
                    stack.append(node.sw)
                if node.se:
                    stack.append(node.se)
        return result

#测试数据
quad_tree = QdTree(33, 73, 45, 87) #定义树的范围
#添加节点
quad_tree.insert((38, 85), "Louisville")
quad_tree.insert((41, 87), "Chicago")
quad_tree.insert((38, 77), "Washington")
quad_tree.insert((36, 87), "Nashville")
quad_tree.insert((34, 84), "Atlanta")
quad_tree.insert((40, 79), "Pittsburgh")
quad_tree.insert((40, 74), "New York")
quad_tree.insert((41, 81), "Cleveland")
quad_tree.insert((39, 84), "Dayton")
quad_tree.insert((45, 73), "Montreal")
preorder_result = quad_tree.preorder_traversal()
for node in preorder_result:
    print(f"Point: {node[0]}, Name: {node[1]}")
position = [38, 85]
dis = 200
result = quad_tree.search(position[0], position[1], dis)
print("到({},{})的距离为{}km的范围内的城市有:".format(position[0], position[1], dis))
for city in result:
    print(city)
closest_city = quad_tree.ClosestPointSearch(35, 80)
print(f"最近的城市是 {closest_city['name']}，距离为 {closest_city['distance']}km")
#练习1:设计k-d树数据结构，并实现对坐标点数据的插入、查找和删除算法
import math
#定义节点
class Node: 
    def __init__(self, x1, y1, level1 = -1):
        self.x = x1
        self.y = y1
        self.level = level1
        self.left = None
        self.right = None
#构造K-d树
class KdTree: 
    def __init__(self, k1 = 2):
        self.root = None
        self.k = k1
    #插入数据
    def insert(self, x1, y1):
        if self.root is None:
            self.root = Node(x1, y1, 0) #如果根节点为空，则将数据作为根节点
        else:
            p1 = self.root  #否则，从根节点开始查找插入位置
            level1 = 0 #记录当前节点的层
            while p1 is not None:
                r = p1.level % self.k #计算当前节点的分辨器
                level1 += 1 #层加一
                p2 = p1
                flag = 0 #标记插入左子树还是右子树
                if r == 0: #若当前维度为x轴
                    if p1.x > x1: #如果待插入节点的x小于当前节点的x，转向左子树
                        p1 = p1.left
                        flag = 1
                    else: #否则转向右子树
                        p1 = p1.right
                        flag = 2
                elif r == 1: #若当前维度为y轴
                    if p1.y > y1: #如果待插入节点的y小于当前节点的y，转向左子树
                        p1 = p1.left
                        flag = 1
                    else: #否则转向右子树
                        p1 = p1.right
                        flag = 2
                if p1 is None: #如果找到了插入位置
                    p1 = Node(x1, y1, level1) #创建新节点
                    if flag == 1: #如果应该插入左子树
                        p2.left = p1 #在双亲节点的左子树插入新节点
                        break
                    elif flag == 2: #如果应该插入右子树
                        p2.right = p1 #在双亲节点的右子树插入新节点
                        break
    #查找数据
    def search(self, x1, y1):
        L = [] #创建一个空栈
        p1 = self.root #将根节点赋值给p1
        while p1 or L: #循环直到p1为空且栈L为空
            if p1: #如果p1不为空
                if p1.x == x1 and p1.y == y1: #如果当前节点的x和y坐标与目标点的相同
                    return p1 #返回当前节点
                r = p1.level % self.k #计算当前节点的分辨器
                if r == 0: #如果维度为x轴
                    if x1 < p1.x: #若目标点的x小于当前节点的x
                        L.append(p1.right) #将右子节点加入栈
                        p1 = p1.left #向左子节点移动
                    else: #否则
                        L.append(p1.left) #将左子节点加入栈
                        p1 = p1.right #向右子节点移动
                elif r == 1: #如果维度为y轴
                    if y1 < p1.y: #若目标点的y小于当前节点的y
                        L.append(p1.right) #将右子节点加入栈
                        p1 = p1.left #向左子节点移动
                    else: #否则
                        L.append(p1.left) #将左子节点加入栈
                        p1 = p1.right #向右子节点移动
            else: #如果p1为空
                p1 = L.pop() #从栈中取出节点赋值给p1
        return None
    #删除数据
    def delete(self, x1, y1):
        p = None #初始化双亲节点
        p1 = self.root #将根节点赋值给当前节点p1
        while p1: #若当前节点存在时循环
            if p1.x == x1 and p1.y == y1: #如果当前节点的坐标与目标坐标相同
                break #结束循环
            p = p1 #将当前节点设为双亲节点
            r = p1.level % self.k #计算当前节点的分辨器
            if r == 0: #如果维度为x轴
                if p1.x > x1: #如果当前节点的x坐标大于目标点的x坐标
                    p1 = p1.left #向左子节点移动
                else:
                    p1 = p1.right #向右子节点移动
            elif r == 1: #如果维度为y轴
                if p1.y > y1: #如果当前节点的y坐标大于目标点的y坐标
                    p1 = p1.left #向左子节点移动
            else:
                p1 = p1.right #向右子节点移动
        if p1 is None: #如果当前节点为空
            return 
        if not p1.left: #如果当前节点的左子节点为空
            p2 = p1.right #将当前节点的右子节点赋值给p2
        elif not p1.right: #如果当前节点的右子节点为空
            p2 = p1.left #将当前节点的左子节点赋值给p2
        else: #当前节点左右子节点都不为空
            s_p = p1 #将当前节点赋值给s_p
            s = p1.right #将当前节点的右子节点赋值给s
            while s.left: #当s的左子节点存在时循环
                s_p = s
                s = s.left
            p1.x, s.x = s.x, p1.x #交换当前节点和s的x坐标
            p1.y, s.y = s.y, p1.y #交换当前节点和s的y坐标
            p = s_p
            p2 = s.right
        if not p: #如果p为空
            self.root = p2 #将p2设为根节点
        elif p.left == p1: #如果p的左子节点等于当前节点
            p.left = p2 #将p2设为p的左子节点
        else: #如果p的右子节点等于当前节点
            p.right = p2 #将p2设为p的右子节点

    #最邻近搜索
    def ClosestPointSearch(self, x1, y1):
        closest_dist = float('inf') #设置一个初始值为无穷大的变量表示最近距离
        closest_node = None #初始化最近的节点为None
        L = [self.root] #将根节点放入栈
        while L: #当栈非空时循环
            node = L.pop() #弹出栈的最后一个节点
            if node is None: #如果弹出的节点为空
                continue #继续循环
            dist = math.sqrt((node.x - x1)**2 + (node.y - y1)**2) #计算当前节点与目标点之间的距离
            if dist < closest_dist: #如果当前距离小于最近距离
                closest_dist = dist #更新最近距离
                closest_node = node #更新最近节点
            r = node.level % self.k #计算当前节点的分辨器
            if r == 0: #如果维度为x轴
                if x1 < node.x: #若目标点的x小于当前节点的x
                    L.extend([node.right, node.left]) #将右子节点和左子节点依次放入栈
                else:
                    L.extend([node.left, node.right]) #将左子节点和右子节点依次放入栈
            else: #如果维度为x轴
                if y1 < node.y: #若目标点的y小于当前节点的y
                    L.extend([node.right, node.left]) #将右子节点和左子节点依次放入栈
                else:
                    L.extend([node.left, node.right]) #将左子节点和右子节点依次放入栈
        return closest_node

#测试数据
kd_tree = KdTree() #创建一个K-d树
kd_tree.insert(40, 60) #插入点A(40,60)
kd_tree.insert(10, 75) #插入点B(10,75)
kd_tree.insert(70, 20) #插入点C(70,20)
kd_tree.insert(25, 15) #插入点D(25,15)
kd_tree.insert(80, 70) #插入点E(80,70)
kd_tree.insert(20, 45) #插入点F(20,45)
kd_tree.insert(35, 45) #插入点G(35,45)
kd_tree.insert(60, 50) #插入点H(60,50)
result = kd_tree.search(41, 60)
if result is not None:
    print(f"查找到: ({result.x}, {result.y})")
else:
    print("未查找到结果")
kd_tree.delete(35,45)
point = kd_tree.ClosestPointSearch(99, 90)
if point is not None:
    print(f"最邻近点: ({point.x}, {point.y})")
else:
    print("未找到最邻近点")
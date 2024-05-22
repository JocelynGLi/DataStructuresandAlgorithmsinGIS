#节点定义
class LNode():
    def  __init__(self, data_, next_=None):
        self.data = data_ #节点数据
        self.next = next_ #下一个节点
#链表定义
class LList():
    #表头定义
    def  __init__(self): 
        self.head = None #表头为空
        self.len = 0 #链表长度为0
    #判空与置空
    def isEmpty(self):
        return self.head is None #判断链表为空
    #新增节点
    def insert(self, data, index):
        if index < 0 or index > self.len: #判断索引是否越界
            print('Index超过范围')
            return False
        if index == 0: #如果在头部插入节点
            new_node = LNode(data, self.head) #创建新节点
            self.head = new_node #更新表头
            self.len += 1 #链表长度加1
        else: #如果在头部以外处插入节点
            prev_node = None #初始化前一个节点为None
            current_node = self.head #当前节点为链表头节点
            current_index = 0 #初始化当前索引为0
            while current_index < index: #循环直到找到要插入的节点的前一个节点
                prev_node = current_node #更新前一个节点为当前节点
                current_node = current_node.next #将当前节点更新为下一个节点
                current_index += 1 #索引加1
            new_node = LNode(data, current_node) #创建新节点
            prev_node.next = new_node #插入新节点
            self.len += 1 #链表长度加1
        return True
    #删除节点        
    def delete(self,index):
        if index < 0 or index >= self.len: #判断索引是否越界
            print('Index超过范围')
            return False
        if index == 0: #如果删除的是第一个节点
            self.head = self.head.next #将表头替换为下一个节点
        else: #如果删除的是头部以外处的节点
            prev_node = None #初始化前一个节点为None
            current_node = self.head #当前节点为链表头节点
            current_index = 0 #初始化当前索引为0
            while current_index < index: #循环直到找到要删除的节点的前一个节点
                prev_node = current_node #更新前一个节点为当前节点
                current_node = current_node.next #将当前节点更新为下一个节点
                current_index += 1 #索引加1
            prev_node.next = current_node.next #删除目标节点
        self.len -= 1 #链表长度减1
        return True
    #查找
    def indexOf(self, key):
        current_node = self.head #当前节点为链表头节点
        index = 0 #初始化当前索引为0
        while current_node is not None: #遍历链表中的节点
            if current_node.data == key: #若现节点是目标节点
                break
            else: #若现节点不是目标节点
                current_node = current_node.next #遍历下一个节点
                index += 1 #索引加1
        if current_node == None: #若未找到目标节点
            return -1
        else:
            return index #返回节点索引
    #遍历          
    def traverse(self):
        current_node = self.head #当前节点为链表头节点
        while current_node is not None: #遍历链表输出节点数据
            print(current_node.data, end=' -> ')
            current_node = current_node.next #将当前节点更新为下一个节点
        print('None')

#测试   
link_list = LList() #创建链表对象
#检查链表是否为空
if link_list.isEmpty():
    print("链表为空")
else:
    print("链表不为空")
#插入节点
link_list.insert(1,0)
link_list.insert(2,1)
link_list.insert(3,2)
link_list.traverse() #遍历输出链表
link_list.delete(1) #删除节点
link_list.traverse() #再次遍历输出链表
#查找节点
index = link_list.indexOf(3)
print(index)
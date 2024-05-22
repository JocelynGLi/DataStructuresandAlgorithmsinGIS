'''
1、创建链表class LinkList。

2、实现链表方法。如增加节点insertNode、删除节点deleteNode、查找indexOfNode等方法。

'''
class LinkNode:
    '''链表节点'''
    def __init__(self, data, next=None) -> None:
        self.data = data
        self.next = next

class LinkList:
    '''链表'''
    def __init__(self) -> None:
        self.head = None # 表头
        self.num = 0 # 节点个数



    def indexOfNode(self, index):
        '''查找节点'''
        
        '''
        index 查找节点的索引位置
        '''
        pn =self.head
        pn2 = pn
        j = 0
        if pn == None or index >= self.num: # 空链表或 超出查询范围
            pn, pn2 = None, None
            return  pn, pn2
        elif index == 0: # 查找表头
            return pn, pn2 
        else:
            while j < index and pn != None:
                pn2 = pn # 记录pn上一个节点的地址
                pn = pn.next
                j += 1
            return pn, pn2




    def insertNode(self, data, index=-1):
        '''增加节点'''
        '''
        data 节点数值
        index 插入节点位置
        '''
        pninsert = LinkNode(data)
        if self.head == None: # 空链表
            self.head = pninsert # 创建表头
            self.num = 1 # 节点数加一
            return True
        if index == -1 or index >= self.num: # defualt = -1 或者超出索引范围 默认从尾部添加节点 
            index = self.num - 1
            pn, pn2 = self.indexOfNode(index)
            pn.next = pninsert
            self.num += 1
            return True
        else: # 非空链表
            pn, pn2 = self.indexOfNode(index)
            if pn == pn2 or index == 0: # 在表头插入
                self.head = pninsert
                self.head.next = pn
                self.num += 1
                return True
            pn2.next = pninsert
            pninsert.next = pn
            self.num += 1
            return True


    def deleteNode(self, index = -1):
        '''删除节点'''
        '''
        index 删除节点的索引位置
        '''
        if index >= self.num:
            print("超出索引范围，删除失败")
            return False
        pn, pn2 = self.indexOfNode(index)
        if index ==  -1:
            index =   self.num - 1 # 默认从尾部删除节点
            pn = None
        elif index == 0: # 删除表头
            self.head = pn.next
            pn = None
        else:
            pn2.next = pn.next
            pn = None
        self.num -= 1
        return True




    def printallnodes(self):
        pn = self.head
        for i in range(self.num):
            print(pn.data, end='\x20')
            pn = pn.next
        

if __name__ == "__main__":
    newlinklist = LinkList() # 创建链表
    '''---------------------------------------------------------------------------添加节点---------------------------------------------------------------------------'''
    # 添加节点 按顺序添加 20 40 50 30 10 43 54
    print("\n-------------------按照顺序添加节点-------------------")
    data = [20, 40, 50, [30,30], 'string', 43, 54]
    for item in data:
        newlinklist.insertNode(item) # 插入节点
    newlinklist.printallnodes()
    # 在40 和 50 之间添加一个值为45的节点 index = 2
    print("\n-------------------在节点之间添加节点-------------------")
    newlinklist.insertNode(45, 2)
    newlinklist.printallnodes()

    # 在表头添加节点
    print("\n-------------------在表头添加节点-------------------")
    newlinklist.insertNode(80, 0)
    newlinklist.printallnodes()
    print('\nhead的值为：{0}'.format(newlinklist.head.data))
    '''---------------------------------------------------------------------------查找---------------------------------------------------------------------------'''
    pn, pn2 = newlinklist.indexOfNode(1)
    if pn is not None:
        print("查找成功，值为：{0}".format(pn.data))
    else:
        print('查询失败')
    pn, pn2 = newlinklist.indexOfNode(40)
    if pn is not None:
        print("查找成功，值为：{0}".format(pn.data))
    else:
        print('查询失败')
    '''---------------------------------------------------------------------------删除节点---------------------------------------------------------------------------'''
    # 删除表头 
    print("\n-------------------删除表头节点-------------------")
    newlinklist.deleteNode(0)
    newlinklist.printallnodes()
    # 默认删除表尾
    print("\n-------------------删除表尾节点-------------------")
    newlinklist.deleteNode()
    newlinklist.printallnodes()
    # 删除中间节点
    print("\n-------------------删除表尾节点-------------------")
    newlinklist.deleteNode(newlinklist.num - 1)
    newlinklist.printallnodes()
    print("\n-------------------删除中间节点-------------------")
    newlinklist.deleteNode(3)
    newlinklist.printallnodes()
    # 删除超出节点数的节点
    print("\n-------------------删除超出索引数的节点-------------------")
    newlinklist.deleteNode(newlinklist.num)
    newlinklist.printallnodes()

    

        
    





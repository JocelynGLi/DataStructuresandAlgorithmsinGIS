'''
根据给定序列，构造一棵二叉排序树

其关键码序列为：    63，90，70，55，67，42，98，83，10，45，58   

实现该二叉排序树的（先序）遍历、查找、插入和删除算法
'''

class BSNode:
    def __init__(self, data) -> None:
        self.data = data
        self.left = None
        self.right = None
        

class BSTree:
    def __init__(self) -> None:
        self.root = None
    def insertNode(self, data):
        newbsnode = BSNode(data)
        if self.root is None:
            self.root = newbsnode
        else:
            pn = self.root
            pn2 = pn
            flag = 0
            while pn is not None:
                pn2 = pn
                if(data <= pn.data):
                    pn = pn.left
                    flag = 1
                elif data > pn.data:
                    pn = pn.right
                    flag = 2
            if flag == 1:
                pn2.left = newbsnode
            elif flag == 2:
                pn2.right = newbsnode

    def indexOfNode(self, key):
        pn = self.root
        flag = 0
        while pn is not None:
            if key == pn.data:
                break
            pn2 = pn
            if key < pn.data:
                pn = pn.left
                flag = 1
            elif key > pn.data:
                pn = pn.right
                flag = 2
        if pn is None:
            return None
        else:
            return pn, pn2, flag # 返回当前pn pn的父节点pn2 和 左右节点flag=1为左 flag=2 为右
        




    def preordersearch(self, s, pn):
        '''深度优先遍历（先序）'''
        if pn is not None:
            s.append(pn.data)
            self.preordersearch(s, pn.left)
            self.preordersearch(s, pn.right)
        return s

        
    


    def deleteNode(self, data):
        pn = self.root
        if data == pn.data: # 删除根节点
            self.root = pn.left 
            tpnode1 = pn.left
            while tpnode1 is not None:
                tpnode2 = tpnode1
                tpnode1 = tpnode1.right
            tpnode2.right = pn.right

            pn = None

        else:
            if self.indexOfNode(data) is not None:
                pn, pn2, flag = self.indexOfNode(data)
                if flag == 1:
                    pn2.left = pn.left
                    tpnode1 = pn.left
                    while tpnode1 is not None:
                        tpnode2 = tpnode1
                        tpnode1 = tpnode1.right
                    tpnode2.right = pn.right
                    pn = None
                elif flag ==2:
                    pn2.right = pn.right
                    tpnode1= pn.right
                    while tpnode1 is not None:
                        tpnode2 = tpnode1
                        tpnode1 = tpnode1.left
                    tpnode2.left = pn.left
                    pn = None


                    
                



if __name__ == "__main__":
    # 构建二叉排序树
    data = [63, 90, 70, 55, 67, 42, 98, 83, 10, 45, 58]
    newbst = BSTree()
    for i in data:
        newbst.insertNode(i)
    # 先序遍历
    s = []
    s = newbst.preordersearch(s, newbst.root)
    print(s)
    # 删除根节点
    newbst2 = BSTree()
    for i in data:
        newbst2.insertNode(i)
    newbst2.deleteNode(63)
    s = []
    s = newbst2.preordersearch(s, newbst2.root)
    print(s)
    # 删除 节点
    newbst3 = BSTree()
    for i in data:
        newbst3.insertNode(i)
    newbst3.deleteNode(90)
    s = []
    s = newbst3.preordersearch(s, newbst3.root)
    print(s)

    
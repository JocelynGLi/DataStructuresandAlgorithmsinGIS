'''
基于Python并实现对二叉树的存储，创建并遍历二叉树（下图所示）：

（1）设计一个二叉链表，以完全二叉树规则存储这颗二叉树作为输入，先序创建这棵二叉树。

（2）使用队列作为辅助，实现该二叉树的宽度优先遍历（BFS）。
'''
class BTNode:
    '''二叉树节点'''
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

class BTree:
    '''二叉树'''
    def __init__(self):
        self.root = None
        self.nNode = 0

    def insertNode(self, data, key):
        '''添加节点'''
        '''
        data 表示节点的数据
        key 表示添加节点的位置

        '''
        newbtnode = BTNode(data)
        if self.root is None: # 空树
            self.root = newbtnode
            self.nNode = self.nNode + 1
            return True
        else: #非空树
            loc = []
            '''判断k在二叉树中的位置'''
            k = key
            while int(k/2) != 0:
                if k%2 == 1: # 奇数 右节点 notice 根节点的key为1 
                    loc.insert(0, 1) # 在数组的队列中
                elif k%2 == 0: # 偶数 左节点 
                    loc.insert(0, 0) 
                k = int(k/2)
            pn = self.root
            if len(loc) != 1:
                for i in range(len(loc) - 1):
                    if loc[i] == 1: # 右
                        pn = pn.right
                    elif loc[i] == 0:
                        pn = pn.left # 左

            if pn is None:
                print("没有找到父节点，插入失败")
                return False
            else:
                self.nNode += 1
                if loc[-1] == 1:
                    pn.right = newbtnode
                elif loc[-1] == 0:
                    pn.left = newbtnode
                return True
            
    def BFS(self):
        '''广度优先遍历'''
        '''利用队列进行广度优先遍历'''
        pn = self.root
        queue = [pn]
        bsf = []
        while len(queue) != 0:
             queue2 = []
             for i in queue:
                 bsf.append(i.data)
                 if i.left is not None:
                     queue2.append(i.left)
                 if i.right is not None:
                     queue2.append(i.right)
                 queue = queue2
        return bsf
                 
            
       
        


if __name__ == "__main__":
    '''创建二叉树'''
    key = [1, 2, 3, 4, 6, 7, 8, 9, 13, 15] # 先序 先根节点 再左节点 后右节点
    data = [31, 23, 12, 66, 5, 17, 70, 62, 88, 55]
    newbt = BTree()
    for i in range(len(data)):
        newbt.insertNode(data[i], key[i])
        
    '''宽度优先遍历'''

    bsf = newbt.BFS()
    print(bsf)



#二叉排序树节点描述
class BSNode:
    def __init__(self, k):
        self.key = k #节点值
        self.left = None #左子树
        self.right = None #右子树
#二叉排序树设计
class BSTree:
    #初始化定义
    def __init__(self):
        self.root = None #根节点为空
    #查找
    def search (self, k):
        if self.root == None:
            return None #若根节点为空，查找失败
        else:
            bn = self.root
            while bn != None: #查找非空，将给定值k与查找树的根结点关键码比较
                if k > bn.key:
                    bn = bn.right #当k大于根结点关键码，查找右子树
                elif k < bn.key:
                    bn = bn.left #当k小于根结点关键码，查找左子树
                else: #若找到，返回节点
                    return bn
            return None
    #插入
    def insert(self, k):
        if self.root == None: #如果根节点为空
            self.root = BSNode(k) #创建新的根节点
            return True
        else:
            bn1 = bn2 = self.root #bn1为子树，bn2为双亲节点
            flag = 0 #标志插入节点，0为根节点，1为右子树，2为左子树
            while bn1 != None: #循环查找插入位置
                bn2 = bn1 #更新双亲节点
                if k > bn1.key: #如果插入值大于当前节点值
                    bn1 = bn1.right #移向右子树
                    flag = 1 #更新插入方向为右子树
                elif k < bn1.key: #如果插入值小于当前节点值
                    bn1 = bn1.left #移向左子树
                    flag = 2 #更新插入方向为左子树
                else:
                    return False
            bn1 = BSNode(k) #创建新节点
            if flag == 1:
                bn2.right = bn1 #bn1是右子树
            else:
                bn2.left = bn1 #bn1是左子树
            return True
    #删除
    def delete(self, k):
        if self.root == None: #如果根节点为空
            return False  #返回删除失败
        p = None #双亲节点
        bn = self.root #将当前节点设为根节点
        flag = 0 #初始化标志为0
        while bn.key != k: #循环查找待删除节点
            p = bn #更新双亲节点
            if k > bn.key: #如果待删除值大于当前节点值
                bn = bn.right #移向右子树
                flag = 1 #更新删除方向为右子树
            elif k < bn.key: #如果待删除值小于当前节点值
                bn = bn.left # 移向左子树
                flag = 2 #更新删除方向为左子树
            else:
                break #找到待删除节点，退出循环
        if bn == None: #如果待删除节点为空，即未找到要删除的节点
            return False
        if flag == 1: #如果待删除节点在右子树
            if (bn.left == None) and (bn.right == None): #删除的是叶节点
                p.right= None #右子树置空
            elif bn.left == None: #只有右子树
                p.right = bn.right #右子树替换为待删除节点的右子树
            elif bn.right == None: #只有左子树
                p.right = bn.left #右子树替换为待删除节点的左子树
            else: #左右子树都有
                p2 = bn2 = bn.left
                while bn2 != None:
                    p2 = bn2
                    bn2 = bn2.right
                p2.right = bn.right
                p.right = bn.left
            return True  
        elif flag == 2: #如果待删除节点在左子树
            if (bn.left == None) and (bn.right == None): #删除的是叶节点
                p.left = None
            elif bn.left == None: #只有右子树
                p.left = bn.right
            elif bn.right == None: #只有左子树
                p.left = bn.left
            else:
                p2 = bn2 = bn.left
                while bn2 != None:
                    p2 = bn2
                    bn2 = bn2.right
                p2.right = bn.right
                p.left = bn.left
            return True
        else: #删除根节点
            if (self.root.left == None) and (self.root.right == None):  #删除的是叶节点
                self.root = None
            elif self.root.left == None: #只有右子树
                self.root = self.root.right
            elif self.root.right == None: #只有左子树
                self.root = self.root.left
            else:
                p2 = bn2 = self.root.left
                while bn2 != None:
                    p2 = bn2
                    bn2 = bn2.right
                p2.right = bn.right
                self.root = self.root.left
            return True
    #先序遍历
    def prevTraval(self,node, result = None):
        if result == None: #如果结果为空
            result = [] #初始化结果列表
        if  node != None: #如果当前节点不为空
            result.append(node.key) #将当前节点的值添加到结果列表中
            self.prevTraval(node.left, result) #递归遍历左子树
            self.prevTraval(node.right, result) #递归遍历右子树
        return result

#测试数据
bst = BSTree()
keys = [63, 90, 70, 55, 67, 42, 98, 83, 10, 45, 58]
for key in keys:
    bst.insert(key)
prevTraval_result = bst.prevTraval(bst.root)
print("先序遍历结果为:", prevTraval_result)
key_to_search = 67
result = bst.search(key_to_search)
if result:
    print(f"找到关键字 {key_to_search}。")
key_to_delete = 55
deleted = bst.delete(key_to_delete)
if deleted:
    print(f"删除关键字 {key_to_delete} 成功。")
else:
    print(f"未找到关键字 {key_to_delete}，删除失败。")
new_prevTraval_result = bst.prevTraval(bst.root)
print("新的先序遍历结果为:", new_prevTraval_result)
#定义节点
class BiNode:
    def __init__(self, _data = None):
        self.data = _data
        self.left = None
        self.right = None
#定义二叉树
class BiTree:
    #初始化二叉树
    def __init__(self, _data=None):
        self.root = BiNode(_data) #创建根节点
    #根据一个顺序存储的二叉树数组（列表），先序创建相应的二叉链表 
    def fromList(self,dataList): 
        def _preOrdCreate(node,idx): #先序创建二叉链表
            if idx<len(dataList) and (dataList[idx] is not None):
                if idx%2==0: #左子树
                    node.left=BiNode(dataList[idx])  #创建左子树节点
                    node=node.left #将当前节点移至左子树
                elif idx%2==1: #右子树
                    node.right=BiNode(dataList[idx]) #创建右子树节点
                    node=node.right #将当前节点移至右子树
                print(node.data) #输出节点值
                _preOrdCreate(node,2*idx) #创建左子树
                _preOrdCreate(node,2*idx+1) #创建右子树
        if dataList[1] is not None: #确保第二个节点非空，表示根节点
            self.root=BiNode(dataList[1]) #创建根节点
            print(self.root.data) #输出根节点值
            _preOrdCreate(self.root,2) #创建左子树
            _preOrdCreate(self.root,3) #创建右子树
    #先序遍历
    def preOrder(self,node):
        if  node is not None: #如果节点非空
            print(node.data) #输出节点值
            self.preOrder(node.left) #递归遍历左子树
            self.preOrder(node.right) #递归遍历右子树
    #中序遍历
    def midOrder(self,node):
        if  node is not None: #如果节点非空
            print(node.data) #输出节点值
            self.preOrder(node.left) #递归遍历左子树
            self.preOrder(node.right) #递归遍历右子树 
    #层次遍历       
    def BSF(self,node):
        if node is not None: #若节点为空
            queue = [] #创建一个空队列
            queue.append(node) #将根节点加入队列
            while queue: #循环直到队列为空
                current = queue.pop(0)  #出队首元素
                if current is not None: #如果当前节点不为空
                    print(current.data) #输出当前节点值
                    if current.left is not None: #如果左节点不为空
                        queue.append(current.left) #将左节点加入队列
                    if current.right is not None: #如果右节点不为空
                        queue.append(current.right) #将右节点加入队列

#测试数据  
treeData=[None,31,23,12,66,None,5,17,70,62,None,None,None,88,None,55]
bitree=BiTree()
print("创建二叉树:")
bitree.fromList(treeData)
print("先序遍历:")
bitree.preOrder(bitree.root)
print("中序遍历:")
bitree.midOrder(bitree.root)
print("层次遍历:")
bitree.BSF(bitree.root)

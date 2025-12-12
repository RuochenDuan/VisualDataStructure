# config.py
MARGIN = 20
NODE_ITEM_R = 40
TREE_NODE_R = 25
RECT_WIDTH = 80
RECT_HEIGHT = 50

COLORS = {
    "norm": "#d0d5dc",
    "highlight": "#73C0FF",
    "new": "#73C0FF",
    "path": "#9abedb",
    "delete": "#989CA6"
}

DSL_help = """
DSL语法
关键字：create, insert, delete, search, help, alist, nlist, stck, bt, bst, huff, l, r
字面量：整型，字符串均与python中的表达一致
分隔符：";"分隔命令，","分隔参数，"-"和"--"连接参数，一条命令内部不能忽略空格，命令之间可以忽略空格，不支持注释
具体解释：
create -alist 1,2,3 创建一个线性表[1,2,3]
insert -alist 4 在线性表的末尾插入4
insert -alist 1 4 在线性表遍历匹配的第一个1前面插入4
delete -alist 1 删除线性表中遍历匹配的第一个1
create -nlist 1,2,3 创建一个链表[1,2,3]
insert -nlist 4 头插法插入4
insert -nlist 1 4 在链表遍历匹配的第一个1后面插入4
delete -nlist 1 删除链表中遍历匹配的第一个1
create -stck 5 创建一个容量为5的栈
create -stck 5 1,2,3 创建一个栈[1,2,3,None,None]
insert -stck 4 向栈中压入4
delete -stck 弹出栈顶元素
create -bt 1,3,6,0 1,0,6,3 创建一个前、中序序列分别为1，3，6，0和1，0，6，3的二叉树
insert -bt 1 --l 4 在二叉树中由BFS遍历匹配的第一个1的左侧插入4
insert -bt 1 --r 4 在二叉树中由BFS遍历匹配的第一个1的右侧插入4
delete -bt 4 删除二叉树中由BFS遍历匹配的第一个4
create -bst 1,2,3 创建一个由1，2，3构造的二叉搜索树
insert -bst 4 向二叉搜索树中插入4
search -bst 1 在二叉搜索树中查找1
delete -bst 1 删除二叉搜索树中的1
create -huff aaaabbbccd 创建一个由aaaabbbccd构建的哈夫曼树
"""

ERR = {
    "INVALID_INPUT": {"message": "非法输入"},
    "NULL_POINTER": {"message": "操作对象为空"},
    "INDEX_OUT_OF_RANGE": {"message": "索引越界"},
    "CHILD_OVERFLOW": {"message": "子节点已满"},
    "FILE_WRITE_FAILED": {"message": "文件写入失败"},
    "FILE_READ_FAILED": {"message": "文件读出失败"},
    "INVALID_FILE": {"message": "文件格式错误"}
}

GSS = """
QWidget {
    font-family: "Consolas", "Segoe UI", "Microsoft YaHei";
    font-size: 22px;
    background-color: #ffffff;
    color: #2c2c2c;
}

QMainWindow {
    background-color: #f8f9fa;
}

QPushButton {
    background-color: #f3f4f5;
    color: #3d3d3d;
    border: 1px solid #f0f0f0;
    padding: 7px;
    border-radius: 20px;
    min-width: 70px;
    font-weight: 600;
    letter-spacing: 2px;
}

QPushButton:hover {
    background-color: #e4e5e6;
}

QPushButton:pressed {
    background-color: #c0c1c2;
}

QComboBox {
    padding: 7px;
    border: 1px solid #f0f0f0;
    border-radius: 20px;
    background-color: #ffffff;
    min-width: 100px;
    color: #3d3d3d;
    font-weight: 600;
    letter-spacing: 2px;
}

QComboBox:hover {
    background-color: #e4e5e6;
}

QComboBox::drop-down {
    border: 0px;
    outline: 0px;
}

QComboBox::down-arrow {
    image: none;
}

QGraphicsView {
    background-color: #fafafa;
    border: 1px solid #f0f0f0;
    border-radius: 20px;
    padding: 10px;
}

QScrollBar:vertical {
    background: #e3e3e3;
    width: 8px;
    margin: 2px;
    border-radius: 4px;
}

QScrollBar:horizontal {
    background: #e3e3e3;
    height: 8px;
    margin: 2px;
    border-radius: 4px;
}

QScrollBar::handle {
    background: #c0c0c0;
    min-width: 10px;
    border-radius: 4px;
}

QScrollBar::handle:hover {
    background: #b3b3b3;
}

QScrollBar::add-line,
QScrollBar::sub-line {
    width: 0px;
    background: none;
}

QScrollBar::add-page,
QScrollBar::sub-page {
    background: none;
}
"""

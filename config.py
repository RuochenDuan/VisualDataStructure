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
VisualDS语法规范  by RuochenDuan
关键字：create, insert, delete, search, help, alist, nlist, stck, bt, bst, huff, l, r
字面量：整型、字符串，语法与Python一致
分隔符：命令间用分号;分隔，可省略空白；参数用,分隔；选项用-引导；命令内部空格不可省略
命令定义：
create -alist v1,v2,...  创建线性表 [v1, v2, ...]
insert -alist x  在线性表末尾插入 x
insert -alist y x  在线性表中首个等于 y 的元素前插入 x
delete -alist x  删除线性表中首个等于 x 的元素
create -nlist v1,v2,...  创建链表 [v1, v2, ...]
insert -nlist x  在链表头部插入 x
insert -nlist y x  在链表中首个等于 y 的节点后插入 x
delete -nlist x  删除链表中首个等于 x 的节点
create -stck n  创建容量为 n 的空栈
create -stck n v1,v2,...  创建总长度为 n 的栈，初始元素从栈底到栈顶为 v1,v2,... ，其余位置为 None
insert -stck x  将 x 压入栈顶
delete -stck  弹出栈顶元素
create -bt pre in  根据前序遍历 pre 和中序遍历 in 序列构建二叉树
insert -bt x --l y  在二叉树中按 BFS 顺序找到首个值为 x 的节点，在其左子位置插入 y
insert -bt x --r y  在二叉树中按 BFS 顺序找到首个值为 x 的节点，在其右子位置插入 y
delete -bt x  在二叉树中按 BFS 顺序找到首个值为 x 的节点，删除该节点及其子树
create -bst v1,v2,...  按顺序插入 v1,v2,... 构造二叉搜索树
insert -bst x  在二叉搜索树中插入 x
search -bst x  在二叉搜索树中查找 x
delete -bst x  在二叉搜索树中删除值为 x 的节点
create -huff s  根据字符串 s 中各字符的出现频率构建哈夫曼树
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

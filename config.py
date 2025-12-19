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

MAPPING = {"顺序表": 1, "链表": 2, "栈": 3, "二叉树": 4, "二叉搜索树": 5, "哈夫曼树": 6}

URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/"

MODEL = "qwen-turbo"

S_PROMPT = {
        1: """
            你要模拟一个顺序表可视系统的后端，严格遵守以下要求。
            接收：用户用自然语言描述的顺序表。
            返回：单行，只有一个python列表格式表示的表结构，不要有多余内容。
                特别的，如果用户让你创建的不是顺序表，返回字符串：error
            返回示例：[1, 2, 3, 4]
        """,
        2: """
            你要模拟一个链表可视系统的后端，严格遵守以下要求。
            接收：用户用自然语言描述的链表。
            返回：单行，只有一个python列表格式表示的表结构，不要有多余内容。
                特别的，如果用户让你创建的不是链表，返回字符串：error
            返回示例：[1, 2, 3, 4]
        """,
        3: """
            你要模拟一个栈可视系统的后端，严格遵守以下要求。
            接收：用户用自然语言描述的栈。
            返回：单行，只有一个python字典格式表示的栈结构，不要有多余内容。
                第一个值描述总容量，第二个值描述压入的元素（栈底在左侧）。
                特别的，如果用户让你创建的不是栈，返回字符串：error
            返回示例：{"max_size": 5, "datas": [1, 2, 3, 4]}
        """,
        4: """
            你要模拟一个二叉树可视系统的后端，严格遵守以下要求。
            接收：用户用自然语言描述的二叉树。
            返回：单行，只有一个python字典格式表示的构建序列，不要有多余内容。
                第一个值是前序序列，第二个值是中序序列。
                特别的，如果用户让你创建的不是二叉树，返回字符串：error
            返回示例：{"preorder": [1, 2, 4, 5, 3, 6], "inorder": [4, 2, 5, 1, 6, 3]}
        """,
        5: """
            你要模拟一个二叉搜索树可视系统的后端，严格遵守以下要求。
            接收：用户用自然语言描述的二叉搜索树。
            返回：单行，只有一个python列表格式表示的构建序列，不要有多余内容。
                特别的，如果用户让你创建的不是二叉搜索树，返回字符串：error
            返回示例：[1, 2, 3, 4, 5]
        """,
        6: """
            你要模拟一个哈夫曼树可视系统的后端，严格遵守以下要求。
            接收：用户用自然语言描述的哈夫曼树。
            返回：单行，只有一个python字典格式表示的构建序列，包含构建这个树的原始字符串，不要有多余内容。
                特别的，如果用户让你创建的不是哈夫曼树，返回字符串：error
            返回示例：{"chars": "aaaabbbccd"}
        """
        }

DSL_help = """
VisualDS语法规范  by RuochenDuan
关键字：create, insert, delete, search, help, alist, nlist,
 stck, bt, bst, huff, l, r
字面量：整型、字符串，语法与Python一致
分隔符：命令间用分号;分隔，可省略空白；参数用,分隔，用-引导；
标志位用--引导；命令内部空格不可省略
格式：[cmd] -[type] [args] [optional args] --[flag];
create -alist v1,v2,...  创建线性表 [v1, v2, ...]
insert -alist x  在线性表末尾插入 x
insert -alist y x  在线性表中首个等于 y 的元素前插入 x
delete -alist x  删除线性表中首个等于 x 的元素
create -nlist v1,v2,...  创建链表 [v1, v2, ...]
insert -nlist x  在链表头部插入 x
insert -nlist y x  在链表中首个等于 y 的节点后插入 x
delete -nlist x  删除链表中首个等于 x 的节点
create -stck n  创建容量为 n 的空栈
create -stck n v1,v2,...  创建总长度为 n 的栈，初始元素从
栈底到栈顶为 v1,v2,... ，其余位置为 None
insert -stck x  将 x 压入栈顶
delete -stck  弹出栈顶元素
create -bt pre in  根据前序遍历 pre 和中序遍历 in 序列构建二叉树
insert -bt x --l y  在二叉树中按 BFS 顺序找到首个值为 x 的
节点，在其左子位置插入 y
insert -bt x --r y  在二叉树中按 BFS 顺序找到首个值为 x 的
节点，在其右子位置插入 y
delete -bt x  在二叉树中按 BFS 顺序找到首个值为 x 的节点，删除
该节点及其子树
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

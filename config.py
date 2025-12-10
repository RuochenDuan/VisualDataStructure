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

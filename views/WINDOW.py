# views/WINDOW.py
from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from . import HomeView
from . import ArrListView
from . import NodeListView
from . import StackView
from . import BTView
from . import BSTView
from . import HuffmanView


class Window(QMainWindow):
    """基本窗口容器"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据结构可视化")
        self.resize(1366, 768)
        self.window_centering()
        self.page = QStackedWidget()
        self.setCentralWidget(self.page)
        self.pages_setup()

    def pages_setup(self):
        self.home_view = HomeView()
        self.arrlist_view = ArrListView()
        self.nodelist_view = NodeListView()
        self.stack_view = StackView()
        self.bt_view = BTView()
        self.bst_view = BSTView()
        self.huffman_view = HuffmanView()
        self.page.addWidget(self.home_view)
        self.page.addWidget(self.arrlist_view)
        self.page.addWidget(self.nodelist_view)
        self.page.addWidget(self.stack_view)
        self.page.addWidget(self.bt_view)
        self.page.addWidget(self.bst_view)
        self.page.addWidget(self.huffman_view)

    def pages_switch(self, index):
        self.page.setCurrentIndex(index)

    def window_centering(self):
        """在屏幕中央显示窗口"""
        screen = self.screen().availableGeometry()
        ctr_point = screen.center()
        window_rect = self.frameGeometry()
        window_rect.moveCenter(ctr_point)
        self.move(window_rect.topLeft())

# views/home.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt


class HomeView(QWidget):
    req_get = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.page_init()

    def page_init(self):
        self.cbox = QComboBox()
        self.cbox.addItems(["顺序表", "链表", "栈", "二叉树", "二叉搜索树", "哈夫曼树"])
        self.btn_get = QPushButton("构造")
        self.btn_get.clicked.connect(lambda: self.req_get.emit(self.cbox.currentText()))

        self.v_layout = QVBoxLayout(self)
        self.v_layout.addStretch()
        self.h_layout = QHBoxLayout()
        self.h_layout.addStretch()
        self.h_layout.addWidget(self.cbox, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.h_layout.addWidget(self.btn_get, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.h_layout.addStretch()
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addStretch()

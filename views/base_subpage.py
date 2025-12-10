# views/base_subpage.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsView, QGraphicsScene
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor


class BaseSubPage(QWidget):
    """子页面组件的基类"""
    req_back = pyqtSignal()
    req_dscrb = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.page_init()

    def page_init(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        self.panel = QWidget()
        self.panel_layout = QVBoxLayout(self.panel)
        self.panel_layout.setContentsMargins(20, 20, 20, 20)
        self.panel_layout.setSpacing(10)

        self.btn_dscrb = QPushButton("描述")
        self.panel_layout.addWidget(self.btn_dscrb)
        self.btn_dscrb.clicked.connect(lambda: self.req_dscrb.emit())
        self.panel_layout.addStretch()
        self.btn_back = QPushButton("返回")
        self.panel_layout.addWidget(self.btn_back)
        self.btn_back.clicked.connect(lambda: self.req_back.emit())

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.view.setMinimumHeight(300)

        self.layout.addWidget(self.panel)
        self.layout.addWidget(self.view)

    def add_btn(self, text):
        """从下向上添加按钮"""
        btn = QPushButton(text)
        self.panel_layout.insertWidget(self.panel_layout.count()-2, btn)
        return btn

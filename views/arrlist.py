# views/arrlist.py
from PyQt6.QtWidgets import QGraphicsObject, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QBrush, QPen, QFont
import uuid
from config import RECT_WIDTH, RECT_HEIGHT, COLORS
from . import BaseSubPage


class ArrListView(BaseSubPage):
    def __init__(self):
        super().__init__()
        self.subpage_init()

    def subpage_init(self):
        self.btn_load = self.add_btn("导入")
        self.btn_create = self.add_btn("构建")
        self.btn_insert = self.add_btn("插入")
        self.btn_delete = self.add_btn("删除")
        self.btn_reset = self.add_btn("重置")
        self.btn_save = self.add_btn("导出")


class ArrListItem(QGraphicsObject):
    w = RECT_WIDTH
    h = RECT_HEIGHT
    highlight = QColor(COLORS["highlight"])
    norm = QColor(COLORS["norm"])
    clicked = pyqtSignal(str)

    def __init__(self, value, index: int = 0):
        super().__init__()
        self.uuid = str(uuid.uuid4())
        self.value = value
        self.index = index
        self.highlighted = False
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setZValue(1)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.w, self.h)

    def paint(self, painter: QPainter, option, widget=None):
        color = self.highlight if self.highlighted else self.norm
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(QColor(COLORS["norm"]), 2))
        painter.drawRoundedRect(0, 0, self.w, self.h, 7, 7)

        painter.setPen(Qt.GlobalColor.darkGray)
        painter.setFont(QFont("Consolas", 9, QFont.Weight.ExtraBold))
        painter.drawText(5, self.h-5, f"{self.index}")

        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(QFont("Consolas", 12, QFont.Weight.ExtraBold))
        text = str(self.value) if self.value is not None else " "
        painter.drawText(0, 0, self.w, self.h, Qt.AlignmentFlag.AlignCenter, text)

    def set_highlight(self, on: bool):
        self.highlighted = on
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.uuid)
        super().mousePressEvent(event)

# views/stack.py
from PyQt6.QtWidgets import QGraphicsObject
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QBrush, QFont, QPen
from config import COLORS, RECT_WIDTH, RECT_HEIGHT
from . import BaseSubPage


class StackView(BaseSubPage):
    def __init__(self):
        super().__init__()
        self.subpage_init()

    def subpage_init(self):
        self.btn_load = self.add_btn("导入")
        self.btn_create = self.add_btn("构建")
        self.btn_size = self.add_btn("容量")
        self.btn_push = self.add_btn("入栈")
        self.btn_pop = self.add_btn("出栈")
        self.btn_reset = self.add_btn("重置")
        self.btn_save = self.add_btn("导出")


class StackItem(QGraphicsObject):
    w = RECT_WIDTH
    h = RECT_HEIGHT
    norm = QColor(COLORS["norm"])
    highlight = QColor(COLORS["highlight"])

    def __init__(self, value, is_null=False):
        super().__init__()
        self.value = value
        self.is_null = is_null

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.w, self.h)

    def paint(self, painter: QPainter, option, widget=None):
        color = self.norm if self.is_null else self.highlight
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(QColor(COLORS["norm"]), 2))
        painter.drawRoundedRect(0, 0, self.w, self.h, 7, 7)

        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(QFont("Consolas", 12, QFont.Weight.ExtraBold))
        text = str(self.value)
        painter.drawText(0, 0, self.w, self.h, Qt.AlignmentFlag.AlignCenter, text)

# views/nodelist.py
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsPathItem
from PyQt6.QtCore import pyqtSignal, QPointF
from PyQt6.QtGui import QColor, QPen, QBrush, QFont, QPainterPath
from . import BaseSubPage
from config import NODE_ITEM_R, COLORS


class NodeListView(BaseSubPage):
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


class NodeItem(QGraphicsEllipseItem):
    """[str]node_id, [int]value, [bool]highlight"""
    clicked = pyqtSignal(str)

    def __init__(self, node_id, value, r=NODE_ITEM_R):
        super().__init__(-r, -r, 2*r, 2*r)  # (x_lt, y_lt, w, h)
        self.node_id = node_id
        self.value = value
        self.highlight = False

        self.setBrush(QBrush(QColor(COLORS["norm"])))
        self.setPen(QPen(QColor(COLORS["norm"]), 2))
        self.text = QGraphicsTextItem(str(value), self)
        self.text.setFont(QFont("Consolas", 12, QFont.Weight.ExtraBold))
        self.text.setPos(-10, -8)

    def set_highlight(self, on: bool):
        self.highlight = on
        color = QColor(COLORS["highlight"]) if on else QColor(COLORS["norm"])
        self.setBrush(QBrush(color))


class LinkItem(QGraphicsPathItem):
    """[str]from_id, [str]to_id"""
    def __init__(self, from_id, to_id):
        super().__init__()
        self.from_id = from_id
        self.to_id = to_id
        self.setPen(QPen(QColor(COLORS["norm"]), 4))
        self.setZValue(-1)
        self.pointer_r = 8
        self.pointer = QGraphicsEllipseItem(
            -self.pointer_r,
            -self.pointer_r,
            2*self.pointer_r,
            2*self.pointer_r,
            parent=self
        )
        self.pointer.setBrush(QBrush(QColor(COLORS["norm"])))
        self.pointer.setPen(QPen(QColor(COLORS["norm"]), 1))
        self.pointer.setZValue(0)

    def update_pos(self, from_pos, to_pos):
        path = QPainterPath()
        path.moveTo(from_pos)
        path.lineTo(to_pos)
        self.setPath(path)
        dx = to_pos.x() - from_pos.x()
        dy = to_pos.y() - from_pos.y()
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            ux = dx/length
            uy = dy/length
            pointer_x = to_pos.x() - ux*NODE_ITEM_R
            pointer_y = to_pos.y() - uy*NODE_ITEM_R
            self.pointer.setPos(QPointF(pointer_x, pointer_y))
        else:
            self.pointer.setPos(to_pos)

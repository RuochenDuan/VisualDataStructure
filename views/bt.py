# views/bt.py
from PyQt6.QtWidgets import QGraphicsObject
from PyQt6.QtCore import pyqtSignal, Qt, QRectF, QPointF
from PyQt6.QtGui import QColor, QPainter, QBrush, QPen, QFont, QPainterPath, QPainterPathStroker
from . import BaseSubPage
from config import COLORS, TREE_NODE_R


class BTView(BaseSubPage):
    def __init__(self):
        super().__init__()
        self.subpage_init()
        self.node_items = {}  # node_id -> NodeItem
        self.edge_items = {}  # (from_id, to_id) -> EdgeItem

    def subpage_init(self):
        self.btn_load = self.add_btn("导入")
        self.btn_create = self.add_btn("构建")
        self.btn_insert = self.add_btn("插入")
        self.btn_delete = self.add_btn("删除")
        self.btn_reset = self.add_btn("重置")
        self.btn_save = self.add_btn("导出")

    def clear_scene(self):
        self.scene.clear()
        self.node_items.clear()
        self.edge_items.clear()

    def add_node(self, node_id, value, pos):
        if node_id in self.node_items:
            return self.node_items[node_id]

        node_item = TreeNodeItem(node_id, value)
        self.scene.addItem(node_item)
        node_item.setPos(pos)
        self.node_items[node_id] = node_item
        return node_item

    def add_edge(self, from_id, to_id, direction):
        edge_key = (from_id, to_id)
        if edge_key in self.edge_items:
            return
        if from_id not in self.node_items or to_id not in self.node_items:
            return

        from_node = self.node_items[from_id]
        to_node = self.node_items[to_id]
        edge_item = EdgeItem(from_node, to_node, direction)
        self.scene.addItem(edge_item)
        self.edge_items[edge_key] = edge_item

    def remove_node(self, node_id):
        if node_id not in self.node_items:
            return

        edges_to_remove = []
        for (from_id, to_id), edge in self.edge_items.items():
            if from_id == node_id or to_id == node_id:
                edges_to_remove.append((from_id, to_id))
        for edge_key in edges_to_remove:
            self.remove_edge(edge_key)
        node_item = self.node_items[node_id]
        self.scene.removeItem(node_item)
        del self.node_items[node_id]

    def remove_edge(self, edge_key):
        if edge_key not in self.edge_items:
            return

        edge_item = self.edge_items[edge_key]
        self.scene.removeItem(edge_item)
        del self.edge_items[edge_key]

    def auto_layout(self, tree_data):
        if not tree_data or 'root' not in tree_data:
            return

        widths = {}
        self._calculate_widths(tree_data['root'], widths)
        positions = {}
        total_tree_width = widths.get(tree_data['root']['id'], 1)
        base_spacing = max(50, min(120, 800 / total_tree_width))
        root_x = self.view.width() // 2
        root_y = 80
        self._layout_tree(tree_data['root'], root_x, root_y, widths, positions, spacing_factor=base_spacing)
        for node_id, pos in positions.items():
            if node_id in self.node_items:
                self.node_items[node_id].setPos(pos['x'], pos['y'])
        for edge in self.edge_items.values():
            edge.update()

    def _layout_tree(self, node, x, y, widths, positions, spacing_factor=100):
        if not node:
            return

        node_id = node['id']
        positions[node_id] = {'x': x, 'y': y}
        vertical_spacing = 100
        left_child = node.get('left')
        right_child = node.get('right')

        if left_child:
            left_width = widths[left_child['id']]
            left_x = x - spacing_factor * (left_width + 1) / 2
            left_y = y + vertical_spacing
            self._layout_tree(left_child, left_x, left_y, widths, positions, spacing_factor)

        if right_child:
            right_width = widths[right_child['id']]
            right_x = x + spacing_factor * (right_width + 1) / 2
            right_y = y + vertical_spacing
            self._layout_tree(right_child, right_x, right_y, widths, positions, spacing_factor)

    def _calculate_widths(self, node, widths):
        """计算每个子树所占的宽度单位"""
        if not node:
            return 0

        left_width = self._calculate_widths(node.get('left'), widths)
        right_width = self._calculate_widths(node.get('right'), widths)
        total_width = left_width + right_width + 1
        widths[node['id']] = total_width
        return total_width

    def _position_nodes(self, node, x, y, widths, positions, depth=0):
        """递归定位所有节点的位置"""
        if not node:
            return

        node_id = node['id']
        positions[node_id] = {'x': x, 'y': y}
        vertical_spacing = 100
        current_width = widths[node_id]
        if node.get('left'):
            left_width = widths[node['left']['id']]
            left_x = x - (current_width - left_width) / 2 - 40
            left_y = y + vertical_spacing
            self._position_nodes(node['left'], left_x, left_y, widths, positions, depth + 1)
        if node.get('right'):
            right_width = widths[node['right']['id']]
            right_x = x + (current_width - right_width) / 2 + 40
            right_y = y + vertical_spacing
            self._position_nodes(node['right'], right_x, right_y, widths, positions, depth + 1)


class TreeNodeItem(QGraphicsObject):
    clicked = pyqtSignal(str)

    def __init__(self, node_id, value, parent=None):
        super().__init__(parent)
        self.node_id = node_id
        self.value = str(value)
        self.highlighted = False
        self.radius = TREE_NODE_R
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable)

    def boundingRect(self):
        return QRectF(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def paint(self, painter: QPainter, option, widget=None):
        color = QColor(COLORS["highlight"]) if self.highlighted else QColor(COLORS["norm"])
        pen = QPen(QColor(COLORS["norm"]), 2)
        brush = QBrush(color)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(QFont("Consolas", 12, QFont.Weight.ExtraBold))
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignCenter, self.value)

    def set_highlight(self, highlight: bool):
        self.highlighted = highlight
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.node_id)
        super().mousePressEvent(event)


class EdgeItem(QGraphicsObject):
    def __init__(self, from_node, to_node, direction, parent=None):
        super().__init__(parent)
        self.from_node = from_node
        self.to_node = to_node
        self.direction = direction
        self.setZValue(-1)

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        path = QPainterPath()
        try:
            if not self.from_node.scene() or not self.to_node.scene():
                return path
            start = self.from_node.scenePos()
            end = self.to_node.scenePos()
        except RuntimeError:
            return path
        ctrl_offset = 40
        if self.direction == "left":
            ctrl_point = start + QPointF(-ctrl_offset, ctrl_offset)
        else:
            ctrl_point = start + QPointF(ctrl_offset, ctrl_offset)

        path.moveTo(start)
        path.quadTo(ctrl_point, end)
        stroker = QPainterPathStroker()
        stroker.setWidth(5)
        return stroker.createStroke(path)

    def paint(self, painter, option, widget=None):
        try:
            if not self.from_node.scene() or not self.to_node.scene():
                return
            start = self.from_node.scenePos()
            end = self.to_node.scenePos()
        except RuntimeError:
            return
        pen = QPen(QColor(COLORS["norm"]), 5)
        painter.setPen(pen)
        ctrl_offset = 40
        if self.direction == "left":
            ctrl_point = start + QPointF(-ctrl_offset, ctrl_offset)
        else:
            ctrl_point = start + QPointF(ctrl_offset, ctrl_offset)
        path = QPainterPath(start)
        path.quadTo(ctrl_point, end)
        painter.drawPath(path)

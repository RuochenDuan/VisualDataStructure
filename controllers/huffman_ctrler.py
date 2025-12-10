# controllers/huffman_ctrler.py
from PyQt6.QtCore import QObject, QPointF
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QLineEdit
from models import HuffmanTree
from utils import Animator
import re
import json
import os


class HuffmanController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = HuffmanTree()
        self.animator = Animator(interval_ms=180)

        self.animator.req_step_played.connect(self.step_played)
        self.animator.req_finished.connect(self.animation_finished)
        self.view.btn_load.clicked.connect(self.load)
        self.view.btn_save.clicked.connect(self.save)
        self.view.btn_create.clicked.connect(self.create)
        self.view.btn_reset.clicked.connect(self.reset)
        self.reset()

    def step_played(self, step: dict, index: int, total: int):
        step_type = step["type"]

        if step_type == "create_node":
            node_id = step["node_id"]
            freq = step["value"]
            char = step["char"]
            is_leaf = step["is_leaf"]
            self.view.add_node(node_id, freq, char, is_leaf, QPointF(0, 0))
        elif step_type == "create_edge":
            from_id = step["from_id"]
            to_id = step["to_id"]
            direction = step["direction"]
            self.view.add_edge(from_id, to_id, direction)
        elif step_type == "warning":
            msg = step["value"]["message"]
            detail = step.get("text", "")
            QMessageBox.warning(self.view, "警告", f"{msg}!!{detail}")
        elif step_type == "notion":
            content = step["content"]
            QMessageBox.information(self.view, "提示", content)
        self.redraw()

    def save(self):
        if self.animator.is_running():
            return

        path, _ = QFileDialog.getSaveFileName(
            self.view,
            "导出文件",
            "./datas/default",
            "JSON Files (*.json)"
        )
        if not path:
            return
        path = "./" + re.sub(r'\\', '/', os.path.relpath(path, start=os.getcwd()))
        steps = self.model.export_to_file(path)
        self.animator.load_steps(steps)
        self.animator.start()

    def load(self):
        if self.animator.is_running():
            return

        path, _ = QFileDialog.getOpenFileName(
            self.view,
            "导入文件",
            "./datas/",
            "All Files (*);;JSON Files (*.json);;TXT Files (*.txt)"
        )
        if not path:
            return
        steps = self.model.import_from_file(path)
        self.animator.load_steps(steps)
        self.animator.start()

    def dscrb(self, res):
        if self.animator.is_running() or not res:
            return
        res = json.loads(res)
        steps = self.model.build(res.values())
        self.animator.load_steps(steps)
        self.animator.start()

    def create(self):
        if self.animator.is_running():
            return

        seq, ok = QInputDialog.getText(self.view, "构建", "请输入元素序列", QLineEdit.EchoMode.Normal)
        if not ok:
            return
        steps = self.model.build(seq)
        self.animator.load_steps(steps)
        self.animator.start()

    def animation_finished(self):
        pass

    def redraw(self):
        if not self.model.root:
            return
        tree_data = self._get_tree_data(self.model.root)
        self.view.auto_layout(tree_data)

    def _step_into(self, node):
        if not node:
            return None
        return {
            'id': node.id,
            'value': node.value,
            'left': self._step_into(node.left),
            'right': self._step_into(node.right)
        }

    def _get_tree_data(self, node):
        """递归获取树的结构，打包为嵌套字典"""
        if not node:
            return None
        return {"root": self._step_into(node)}

    def reset(self):
        self.animator.stop()
        self.model = HuffmanTree()
        self.view.clear_scene()


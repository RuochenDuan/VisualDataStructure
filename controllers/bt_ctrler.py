# controllers/bt_ctrler.py
from PyQt6.QtCore import QObject, QPointF
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QLineEdit
from models import BinaryTree
from utils import Animator
import json
import re
import os


class BTController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = BinaryTree()
        self.animator = Animator(interval_ms=180)
        self.selected_node_id = None

        self.animator.req_step_played.connect(self.step_played)
        self.animator.req_finished.connect(self.animation_finished)
        self.view.btn_load.clicked.connect(self.load)
        self.view.btn_save.clicked.connect(self.save)
        self.view.btn_create.clicked.connect(self.create)
        self.view.btn_insert.clicked.connect(self.insert)
        self.view.btn_delete.clicked.connect(self.delete)
        self.view.btn_reset.clicked.connect(self.reset)
        self.reset()

    def node_clicked(self, node_id):
        if self.animator.is_running():
            return

        if self.selected_node_id == node_id:
            self.selected_node_id = None
            self.view.node_items[node_id].set_highlight(False)
        else:
            if self.selected_node_id is not None and self.selected_node_id in self.view.node_items:
                self.view.node_items[self.selected_node_id].set_highlight(False)
            self.selected_node_id = node_id
            self.view.node_items[node_id].set_highlight(True)

    def step_played(self, step: dict, index: int, total: int):
        step_type = step["type"]

        if step_type == "create_node":
            node_id = step["node_id"]
            value = step["value"]
            node_item = self.view.add_node(node_id, value, QPointF(0, 0))
            node_item.clicked.connect(self.node_clicked)
        elif step_type == "create_edge":
            from_id = step["from_id"]
            to_id = step["to_id"]
            direction = step["direction"]
            self.view.add_edge(from_id, to_id, direction)
        elif step_type == "delete_node":
            node_id = step["node_id"]
            self.view.remove_node(node_id)
        elif step_type == "delete_edge":
            from_id = step["from_id"]
            to_id = step["to_id"]
            self.view.remove_edge((from_id, to_id))
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
        pre_seq, in_seq = res.values()
        post_seq = None
        steps = self.model.build(pre_seq, in_seq, post_seq)
        self.animator.load_steps(steps)
        self.animator.start()

    def create(self):
        if self.animator.is_running():
            return

        preorder, ok = QInputDialog.getText(self.view, "前序序列", "请输入用逗号分隔的元素序列", QLineEdit.EchoMode.Normal)
        if not ok:
            return
        inorder, ok = QInputDialog.getText(self.view, "中序序列", "请输入用逗号分隔的元素序列", QLineEdit.EchoMode.Normal)
        if not ok:
            return
        postorder, ok = QInputDialog.getText(self.view, "后序序列", "请输入用逗号分隔的元素序列", QLineEdit.EchoMode.Normal)
        if not ok:
            return
        if preorder:
            cleaned_pre = re.sub(r'[,，、;；\s]+', ',', str(preorder))
            seq_pre = json.loads(f"[{cleaned_pre}]")
        else:
            seq_pre = None
        if inorder:
            cleaned_in = re.sub(r'[,，、;；\s]+', ',', str(inorder))
            seq_in = json.loads(f"[{cleaned_in}]")
        else:
            seq_in = None
        if postorder:
            cleaned_post = re.sub(r'[,，、;；\s]+', ',', str(postorder))
            seq_post = json.loads(f"[{cleaned_post}]")
        else:
            seq_post = None
        steps = self.model.build(seq_pre, seq_in, seq_post)
        self.animator.load_steps(steps)
        self.animator.start()

    def insert(self):
        if self.animator.is_running():
            return
        if not self.selected_node_id:
            return

        value, ok = QInputDialog.getInt(self.view, "插入", "输入节点值")
        if not ok:
            return
        direction, ok = QInputDialog.getItem(
            self.view,
            "方向",
            "选择插入方向",
            ["左", "右"],
            0,
            False
        )
        if not ok:
            return
        direction = "left" if direction == "左" else "right"
        steps = self.model.insert_child(self.selected_node_id, value, direction)
        self.animator.load_steps(steps)
        self.animator.start()

    def delete(self):
        if self.animator.is_running() or not self.selected_node_id:
            return

        steps = self.model.delete_node(self.selected_node_id)
        if steps:
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
        self.model = BinaryTree()
        self.selected_node_id = None
        self.view.clear_scene()

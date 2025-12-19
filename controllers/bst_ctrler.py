# controllers/bst_ctrler.py
from PyQt6.QtCore import QObject, QPointF
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QLineEdit
from models import BinarySearchTree
from utils import Animator, DSLParser
from config import COLORS, DSL_help
import json
import re
import os


class BSTController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = BinarySearchTree()
        self.animator = Animator(interval_ms=150)
        self.dsl_parser = DSLParser()

        self.animator.req_step_played.connect(self.step_played)
        self.animator.req_finished.connect(self.animation_finished)
        self.view.btn_load.clicked.connect(self.load)
        self.view.btn_save.clicked.connect(self.save)
        self.view.btn_create.clicked.connect(self.create)
        self.view.btn_insert.clicked.connect(self.insert)
        self.view.btn_search.clicked.connect(self.search)
        self.view.btn_delete.clicked.connect(self.delete)
        self.view.btn_reset.clicked.connect(self.reset)
        self.view.req_dsl_cmd.connect(self.process_dsl_command)
        self.reset()

    def step_played(self, step: dict, index: int, total: int):
        step_type = step["type"]

        if step_type == "create_node":
            node_id = step["node_id"]
            value = step["value"]
            self.view.add_node(node_id, value, QPointF(0, 0))
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
        elif step_type == "highlight_node":
            node_id = step["node_id"]
            color = step["color"]
            self.highlight(node_id, color)
        elif step_type == "clear_highlight":
            self.clear_highlight()
        elif step_type == "warning":
            msg = step["value"]["message"]
            detail = step.get("text", "")
            QMessageBox.warning(self.view, "警告", f"{msg}!!{detail}")
        elif step_type == "notion":
            content = step["content"]
            QMessageBox.information(self.view, "提示", content)
        self.redraw()

    def highlight(self, node_id, color):
        if node_id not in self.view.node_items:
            return
        color = COLORS[color]
        self.view.node_items[node_id].set_color(color)

    def clear_highlight(self):
        for it in self.view.node_items.values():
            it.set_color(COLORS["norm"])

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
        if res == "error":
            QMessageBox.warning(self.view, "警告", f"你描述的不是二叉搜索树！")
            return
        steps = self.model.build(json.loads(res))
        self.animator.load_steps(steps)
        self.animator.start()

    def create(self):
        if self.animator.is_running():
            return

        seq, ok = QInputDialog.getText(self.view, "构建", "请输入用逗号分隔的元素序列", QLineEdit.EchoMode.Normal)
        if not ok:
            return
        cleaned = re.sub(r'[,，、;；\s]+', ',', str(seq))
        if not cleaned:
            return
        seq = json.loads(f"[{cleaned}]")
        steps = self.model.build(seq)
        self.animator.load_steps(steps)
        self.animator.start()

    def insert(self):
        if self.animator.is_running():
            return

        value, ok = QInputDialog.getInt(self.view, "插入", "输入节点值")
        if not ok:
            return
        steps = self.model.insert(value)
        self.animator.load_steps(steps)
        self.animator.start()

    def search(self):
        if self.animator.is_running():
            return

        value, ok = QInputDialog.getInt(self.view, "查找", "输入节点值")
        if not ok:
            return
        steps = self.model.search(value)
        self.animator.load_steps(steps)
        self.animator.start()

    def delete(self):
        if self.animator.is_running():
            return

        value, ok = QInputDialog.getInt(self.view, "删除", "输入节点值")
        if not ok:
            return
        steps = self.model.delete(value)
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
        self.model = BinarySearchTree()
        self.view.clear_scene()
        
    def process_dsl_command(self, dsl_text: str):
        if self.animator.is_running():
            return
            
        try:
            commands = self.dsl_parser.parse(dsl_text)
            all_steps = []
            for cmd in commands:
                steps = self.execute_dsl_command(cmd)
                if steps:
                    all_steps.extend(steps)
            if all_steps:
                self.animator.load_steps(all_steps)
                self.animator.start()
        except Exception as e:
            QMessageBox.warning(self.view, "警告", f"命令解析失败: {str(e)}")

    def execute_dsl_command(self, cmd: dict):
        command = cmd['command']
        args = cmd['args']
        options = cmd['options']
        flags = cmd['flags']

        if options.get('struct_type') not in ['bst', None]:
            QMessageBox.warning(self.view, "警告", "命令语法错误")
            return []

        if command == 'create':
            if len(args) > 0:
                steps = self.model.build(args)
                return steps
            else:
                QMessageBox.warning(self.view, "警告", "命令语法错误")
                return []
                
        elif command == 'insert':
            if len(args) > 0:
                value = args[0]
                steps = self.model.insert(value)
                return steps
            else:
                QMessageBox.warning(self.view, "警告", "命令语法错误")
                return []
                
        elif command == 'search':
            if len(args) > 0:
                value = args[0]
                steps = self.model.search(value)
                return steps
            else:
                QMessageBox.warning(self.view, "警告", "命令语法错误")
                return []
                
        elif command == 'delete':
            if len(args) > 0:
                value = args[0]
                steps = self.model.delete(value)
                return steps
            else:
                QMessageBox.warning(self.view, "警告", "命令语法错误")
                return []

        elif command == 'help':
            QMessageBox.information(self.view, "帮助", f"<pre>{DSL_help}</pre>")
            return []
        else:
            QMessageBox.warning(self.view, "警告", "命令语法错误")
            return []

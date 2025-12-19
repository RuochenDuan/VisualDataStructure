# controllers/nodelist_ctrler.py
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QInputDialog, QLineEdit, QFileDialog, QMessageBox
from views import NodeItem, LinkItem
from models import NodeList
from utils import Animator, DSLParser
from config import DSL_help
import json
import re
import os


class NodeListController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = NodeList()
        self.animator = Animator(interval_ms=200)
        self.selected_node_id = None
        self.node_items = {}  # {node_id : NodeItem}
        self.link_items = []  # [LinkItem]
        self.dsl_parser = DSLParser()

        self.animator.req_step_played.connect(self.step_played)
        self.animator.req_finished.connect(self.animation_finished)
        self.view.btn_load.clicked.connect(self.load)
        self.view.btn_save.clicked.connect(self.save)
        self.view.btn_create.clicked.connect(self.create)
        self.view.btn_insert.clicked.connect(self.insert)
        self.view.btn_delete.clicked.connect(self.delete)
        self.view.btn_reset.clicked.connect(self.reset)
        self.view.req_dsl_cmd.connect(self.process_dsl_command)
        self.reset()

    def node_clicked(self, node_id):
        """响应节点点击"""
        if self.animator.is_running():
            return

        if self.selected_node_id == node_id:
            self.selected_node_id = None
            self.node_items[node_id].set_highlight(False)
        else:
            if self.selected_node_id is not None and self.selected_node_id in self.node_items:
                self.node_items[self.selected_node_id].set_highlight(False)
            self.selected_node_id = node_id
            self.node_items[node_id].set_highlight(True)

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
            QMessageBox.warning(self.view, "警告", f"你描述的不是链表！")
            return
        steps = self.model.build_from_list(json.loads(res))
        self.animator.load_steps(steps)
        self.animator.start()

    def create(self):
        if self.animator.is_running():
            return

        input_seq, ok = QInputDialog.getText(self.view, "构建", "请输入用逗号分隔的元素序列", QLineEdit.EchoMode.Normal, "")
        if not ok:
            return
        cleaned = re.sub(r'[,，、;；\s]+', ',', str(input_seq))
        if not cleaned:
            return
        seq = json.loads(f"[{cleaned}]")
        steps = self.model.build_from_list(seq)
        self.animator.load_steps(steps)
        self.animator.start()

    def insert(self):
        """插入节点"""
        if self.animator.is_running():
            return

        value, ok = QInputDialog.getInt(self.view, "插入", "请输入节点值:", 0)
        if not ok:
            return
        if self.selected_node_id is None:
            steps = self.model.head_insert(value)
        else:
            steps = self.model.tail_insert(self.selected_node_id, value)
        self.animator.load_steps(steps)
        self.animator.start()

    def delete(self):
        """删除节点"""
        if self.animator.is_running() or self.selected_node_id is None:
            return

        steps = self.model.delete_node(self.selected_node_id)
        self.animator.load_steps(steps)
        self.animator.start()

    def step_played(self, step: dict, index: int, total: int):
        """执行每一个step的具体动画"""
        step_type = step["type"]

        if step_type == "create_node":
            node_id = step["node_id"]
            value = step["value"]
            node_item = NodeItem(node_id, value)
            self.view.scene.addItem(node_item)
            self.node_items[node_id] = node_item
            node_item.mousePressEvent = lambda e, nid=node_id: self.node_clicked(nid)
        elif step_type == "link":
            link_item = LinkItem(step["from"], step["to"])
            self.view.scene.addItem(link_item)
            self.link_items.append(link_item)
        elif step_type == "unlink":
            for link in self.link_items[:]:
                if link.from_id == step["from"] and link.to_id == step["to"]:
                    self.view.scene.removeItem(link)
                    self.link_items.remove(link)
                    break
        elif step_type == "delete_node":
            node_id = step["node_id"]
            if node_id in self.node_items:
                self.view.scene.removeItem(self.node_items[node_id])
                del self.node_items[node_id]
            if self.selected_node_id == node_id:
                self.selected_node_id = None
        elif step_type == "warning":
            msg = step["value"]["message"]
            detail = step.get("text", "")
            QMessageBox.warning(self.view, "警告", f"{msg}!!{detail}")
        elif step_type == "notion":
            content = step["content"]
            QMessageBox.information(self.view, "提示", content)
        self.redraw()

    def animation_finished(self):
        pass

    def redraw(self):
        nodes: list[NodeItem] = []
        cur = self.model.head
        while cur:
            if cur.id in self.node_items:
                nodes.append(self.node_items[cur.id])
            cur = cur.next

        x = 100
        y = 200
        spacing = 150
        for i, node_item in enumerate(nodes):
            node_item.setPos(x+i*spacing, y)
        for link_item in self.link_items:
            if link_item.from_id in self.node_items and link_item.to_id in self.node_items:
                from_pos = self.node_items[link_item.from_id].scenePos()
                to_pos = self.node_items[link_item.to_id].scenePos()
                link_item.update_pos(from_pos, to_pos)

    def reset(self):
        self.animator.stop()
        self.model = NodeList()
        self.selected_node_id = None
        self.node_items.clear()
        self.link_items.clear()
        self.view.scene.clear()
        
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

        if options.get('struct_type') not in ['nlist', None]:
            QMessageBox.warning(self.view, "警告", "命令语法错误")
            return []

        if command == 'create':
            if len(args) > 0:
                steps = self.model.build_from_list(args)
                return steps
            else:
                self.reset()
                return []
                
        elif command == 'insert':
            if len(args) == 0:
                QMessageBox.warning(self.view, "警告", "命令语法错误")
                return []
            value = args[0]
            if len(args) == 1:
                steps = self.model.head_insert(value)
                return steps
            elif len(args) >= 2:
                target_value = args[1]
                target_node_id = None
                for node_id, node_item in self.node_items.items():
                    if node_item.value == target_value:
                        target_node_id = node_id
                        break
                if target_node_id:
                    steps = self.model.tail_insert(target_node_id, value)
                    return steps
                return []
            return []

        elif command == 'delete':
            if len(args) == 0:
                QMessageBox.warning(self.view, "警告", "命令语法错误")
                return []
            target_value = args[0]
            target_node_id = None
            for node_id, node_item in self.node_items.items():
                if node_item.value == target_value:
                    target_node_id = node_id
                    break
            if target_node_id:
                steps = self.model.delete_node(target_node_id)
                return steps
            return []

        elif command == 'help':
            QMessageBox.information(self.view, "帮助", f"<pre>{DSL_help}</pre>")
            return []
        else:
            QMessageBox.warning(self.view, "警告", "命令语法错误")
            return []

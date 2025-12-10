# controllers/stack_ctrler.py
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QLineEdit
from views import StackItem
from models import Stack
from utils import Animator
from config import MARGIN
import json
import re
import os


class StackController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = Stack()
        self.animator = Animator(interval_ms=250)
        self.stack_items = []  # [bottom:top]
        self.null_items = []
        self.popped_item = None
        self.capacity = 0

        self.animator.req_step_played.connect(self.step_played)
        self.animator.req_finished.connect(self.animation_finished)
        self.view.btn_load.clicked.connect(self.load)
        self.view.btn_save.clicked.connect(self.save)
        self.view.btn_size.clicked.connect(self.create_empty)
        self.view.btn_create.clicked.connect(self.create)
        self.view.btn_push.clicked.connect(self.push)
        self.view.btn_pop.clicked.connect(self.pop)
        self.view.btn_reset.clicked.connect(self.reset)
        self.reset()

    def step_played(self, step: dict, index: int, total: int):
        step_type = step["type"]

        if step_type == "create_stack":
            self.handle_create(step)
        elif step_type == "push":
            self.handle_push(step)
        elif step_type == "pop":
            self.handle_pop(step)
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
        size, datas = res.values()
        steps = self.model.build_empty(size)
        for v in datas:
            steps.extend(self.model.push(v))
        self.animator.load_steps(steps)
        self.animator.start()

    def create_empty(self):
        if self.animator.is_running():
            return

        input_value, ok = QInputDialog.getInt(self.view, "容量", "输入容量大小", 5)
        if not ok:
            return
        steps = self.model.build_empty(input_value)
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

    def handle_create(self, step: dict):
        if self.popped_item:
            self.view.scene.removeItem(self.popped_item)
            self.popped_item = None
        self.capacity = step["capacity"]
        self.stack_items.clear()
        self.null_items.clear()
        for i in range(self.capacity):
            null_item = StackItem("")
            null_item.is_null = True
            self.null_items.append(null_item)
            self.view.scene.addItem(null_item)

    def handle_push(self, step: dict):
        value = step["value"]
        index = step["index"]
        new_item = StackItem(value)
        self.stack_items.insert(index, new_item)
        self.view.scene.addItem(new_item)
        if index < len(self.null_items):
            null_item = self.null_items.pop(index)
            self.view.scene.removeItem(null_item)
        while len(self.null_items) > self.capacity - len(self.stack_items):
            if self.null_items:
                item = self.null_items.pop()
                self.view.scene.removeItem(item)

    def animate_to_pos(self, item, x, y):
        item.setPos(x, y)

    def handle_pop(self, step: dict):
        index = step["index"]
        if not self.stack_items:
            return
        popped_item = self.stack_items.pop(index)
        popped_item.is_null = True
        self.popped_item = popped_item
        null_item = StackItem("")
        null_item.is_null = True
        self.null_items.insert(index, null_item)
        self.view.scene.addItem(null_item)

    def push(self):
        if self.animator.is_running():
            return

        value, ok = QInputDialog.getInt(self.view, "入栈", "请输入元素值:")
        if not ok:
            return
        steps = self.model.push(value)
        self.animator.load_steps(steps)
        self.animator.start()

    def pop(self):
        if self.animator.is_running():
            return
        steps = self.model.pop()
        self.animator.load_steps(steps)
        self.animator.start()

    def animation_finished(self):
        if self.popped_item:
            self.view.scene.removeItem(self.popped_item)
            self.popped_item = None

    def redraw(self):
        scene_width = self.view.scene.width()
        scene_height = self.view.scene.height()
        total_items = len(self.stack_items) + len(self.null_items)
        if total_items == 0:
            return

        item_height = StackItem.h
        item_width = StackItem.w
        spacing = 5
        total_height = total_items * item_height + (total_items - 1) * spacing

        start_y = (scene_height - total_height) / 2
        if start_y < MARGIN:
            start_y = MARGIN
        x_pos = (scene_width - item_width) / 2
        current_y = start_y
        for item in self.stack_items:
            item.setPos(x_pos, current_y)
            current_y += item_height + spacing
        for null_item in self.null_items:
            null_item.setPos(x_pos, current_y)
            current_y += item_height + spacing
        if self.popped_item:
            pop_x = scene_width - item_width
            pop_y = (item_height + spacing) * (self.capacity + 1)
            self.popped_item.setPos(pop_x, pop_y)

    def reset(self):
        self.animator.stop()
        self.model = Stack()
        self.stack_items.clear()
        self.null_items.clear()
        self.popped_item = None
        self.capacity = 0
        self.view.scene.clear()

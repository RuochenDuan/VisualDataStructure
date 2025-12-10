# controllers/arrlist_ctrler.py
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QLineEdit
from views import ArrListItem
from models import ArrList
from utils import Animator
import json
import re
import os


class ArrListController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = ArrList()
        self.animator = Animator(interval_ms=250)
        self.arr_items = {}  # uuid -> ArrListItem
        self.selected_uuid = None

        self.animator.req_step_played.connect(self.step_played)
        self.animator.req_finished.connect(self.animation_finished)
        self.view.btn_load.clicked.connect(self.load)
        self.view.btn_save.clicked.connect(self.save)
        self.view.btn_create.clicked.connect(self.create)
        self.view.btn_insert.clicked.connect(self.insert)
        self.view.btn_delete.clicked.connect(self.delete)
        self.view.btn_reset.clicked.connect(self.reset)
        self.reset()

    def node_clicked(self, uuid: str):
        if self.animator.is_running():
            return

        if self.selected_uuid == uuid:
            self.selected_uuid = None
            self.arr_items[uuid].set_highlight(False)
        else:
            if self.selected_uuid is not None and self.selected_uuid in self.arr_items:
                self.arr_items[self.selected_uuid].set_highlight(False)
            self.selected_uuid = uuid
            self.arr_items[uuid].set_highlight(True)

    def step_played(self, step: dict, index: int, total: int):
        step_type = step["type"]

        if step_type == "insert":
            self.handle_insert(step)
        elif step_type == "delete":
            self.handle_delete(step)
        elif step_type == "warning":
            msg = step["value"]["message"]
            detail = step.get("text", "")
            QMessageBox.warning(self.view, "警告", f"{msg}!!{detail}")
        elif step_type == "notion":
            content = step["content"]
            QMessageBox.information(self.view, "提示", content)
        self.redraw()

    def handle_insert(self, step: dict):
        value = step["value"]
        target_index = step["index"]
        new_item = ArrListItem(value, target_index)
        self.view.scene.addItem(new_item)
        for item in self.arr_items.values():
            if item.index >= target_index:
                item.index += 1
        new_item.index = target_index
        self.arr_items[new_item.uuid] = new_item
        new_item.clicked.connect(self.node_clicked)

    def handle_delete(self, step: dict):
        target_index = step["index"]
        target_item = None
        for item in self.arr_items.values():
            if item.index == target_index:
                target_item = item
                break
        if target_item:
            self.remove_item(target_item)

    def remove_item(self, item):
        if item.uuid in self.arr_items:
            self.view.scene.removeItem(item)
            self.selected_uuid = None
            del self.arr_items[item.uuid]
            for i, it in enumerate(sorted(self.arr_items.values(), key=lambda x: x.index)):
                it.index = i

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
        if self.animator.is_running():
            return

        value, ok = QInputDialog.getInt(self.view, "插入", "请输入元素值:")
        if not ok:
            return
        index = self.arr_items[self.selected_uuid].index if self.selected_uuid else None
        steps = self.model.insert(value, index)
        self.animator.load_steps(steps)
        self.animator.start()

    def delete(self):
        if self.animator.is_running() or self.selected_uuid is None:
            return

        index = self.arr_items[self.selected_uuid].index
        steps = self.model.delete(index)
        self.animator.load_steps(steps)
        self.animator.start()

    def animation_finished(self):
        pass

    def redraw(self):
        if not self.arr_items:
            return

        items_list = sorted(self.arr_items.values(), key=lambda x: x.index)
        total_width = len(items_list) * ArrListItem.w + (len(items_list) - 1) * 20
        start_x = (self.view.scene.width() - total_width) / 2
        y = self.view.scene.height() / 2 - ArrListItem.h / 2

        for i, item in enumerate(items_list):
            x = start_x + i * (ArrListItem.w + 20)
            item.setPos(x, y)

    def reset(self):
        self.animator.stop()
        self.model = ArrList()
        self.selected_uuid = None
        self.arr_items.clear()
        self.view.scene.clear()

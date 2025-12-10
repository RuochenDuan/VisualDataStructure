# models/stack_model.py
from config import ERR
import json
import datetime


class Stack:
    def __init__(self):
        self.max_size = 0
        self.elements = []
        self.top = -1

    def build_empty(self, size: int):
        if not isinstance(size, int) or size <= 0:
            return [{"type": "warning", "value": ERR["INVALID_INPUT"]}]

        self.max_size = size
        self.elements = [None] * size
        self.top = -1
        return [{"type": "create_stack", "capacity": size}]

    def build_from_list(self, seq: list):
        if not isinstance(seq, list):
            return [{"type": "warning", "value": ERR["INVALID_INPUT"]}]

        steps = self.build_empty(len(seq))
        for v in seq:
            steps.extend(self.push(v))
        return steps

    def push(self, value):
        if self.max_size == 0:
            return [{"type": "warning", "value": ERR["NULL_POINTER"]}]
        elif self.top + 1 >= self.max_size:
            return [{"type": "warning", "value": ERR["INDEX_OUT_OF_RANGE"]}]
        elif value is None:
            return []

        self.top += 1
        self.elements[self.top] = value
        return [{"type": "push", "index": self.top, "value": value}]

    def pop(self):
        if self.max_size == 0 or self.top == -1:
            return []
        if self.top == -1:
            return [{"type": "warning", "value": ERR["NULL_POINTER"]}]

        self.elements[self.top] = None
        self.top -= 1
        return [{"type": "pop", "index": self.top + 1}]

    def export_to_file(self, filepath: str):
        if filepath == "./datas/default.json":
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filepath = f"./datas/stack{timestamp}.json"

        export_data = {
            "max_size": self.max_size,
            "datas": [e for e in self.elements[:self.top+1]],
        }
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False)
            return [{"type": "notion", "content": f"文件已保存至{filepath}"}]
        except Exception as e:
            return [{"type": "warning", "value": ERR["FILE_WRITE_FAILED"], "text": str(e)}]

    def import_from_file(self, filepath: str):
        if not filepath:
            return []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            max_size, datas = import_data.values()
            steps = self.build_empty(max_size)
            for v in datas:
                steps.extend(self.push(v))
            return steps
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            return [{"type": "warning", "value": ERR["INVALID_FILE"], "text": str(e)}]
        except Exception as e:
            return [{"type": "warning", "value": ERR["FILE_READ_FAILED"], "text": str(e)}]

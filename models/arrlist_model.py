# models/arrlist_model.py
from config import ERR
import json
import datetime


class ArrList:
    def __init__(self):
        self.data = []
        self.size = 0

    def build_from_list(self, seq: list):
        if not isinstance(seq, list):
            return [{"type": "warning", "value": ERR["INVALID_INPUT"]}]

        steps = []
        for v in seq:
            steps.extend(self.insert(v))
        return steps

    def insert(self, value, index=None):
        """
        在指定位置插入值，index 默认表示添加到末尾；
        插入时自动扩展一位
        """
        if value is None:
            return []
        if index is None:
            index = self.size

        self.data.append(None)
        self.size += 1
        for i in range(self.size-1, index, -1):
            self.data[i] = self.data[i-1]
        self.data[index] = value
        return [{"type": "insert", "value": value, "index": index}]

    def delete(self, index: int):
        if not (0 <= index < self.size):
            return [{"type": "warning", "value": ERR["INDEX_OUT_OF_RANGE"]}]

        for i in range(index, self.size-1):
            self.data[i] = self.data[i+1]
        del self.data[-1]
        self.size -= 1
        return [{"type": "delete", "index": index}]

    def export_to_file(self, filepath: str):
        if filepath == "./datas/default.json":
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filepath = f"./datas/arrlist{timestamp}.json"

        export_data = self.data
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False)
            return [{"type": "notion", "content": f"文件已保存至 {filepath}"}]
        except Exception as e:
            return [{"type": "warning", "value": ERR["FILE_WRITE_FAILED"], "text": str(e)}]

    def import_from_file(self, filepath: str):
        if not filepath:
            return [{"type": "warning", "value": ERR["INVALID_INPUT"]}]

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            self.data = []
            self.size = 0
            steps = self.build_from_list(import_data)
            return steps
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            return [{"type": "warning", "value": ERR["INVALID_FILE"], "text": str(e)}]
        except Exception as e:
            return [{"type": "warning", "value": ERR["FILE_READ_FAILED"], "text": str(e)}]

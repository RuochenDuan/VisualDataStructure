# models/huffman_model.py
import uuid
import heapq
from collections import Counter
from config import ERR
import json
import datetime


class HuffmanNode:
    def __init__(self, value, char=None, node_id=None):
        self.value = value
        self.char = char
        self.id = node_id or str(uuid.uuid4())
        self.left = None
        self.right = None

    def __lt__(self, other):
        """按照频率排序，相同时按照id排序，返回小于否"""
        if self.value != other.value:
            return self.value < other.value
        return self.id < other.id


class HuffmanTree:
    def __init__(self):
        self.root = None
        self.nodes = {}
        self.char_list = {}

    def build(self, chars: str):
        freq_map = Counter(chars)  # char:str -> freq:int
        if not freq_map:
            return []
        steps = []

        heap = []
        self.char_list = {"chars": chars}
        for char, freq in freq_map.items():
            node_id = str(uuid.uuid4())
            node = HuffmanNode(freq, char, node_id)
            self.nodes[node_id] = node
            heapq.heappush(heap, node)
            steps.append({"type": "create_node", "node_id": node_id, "value": freq, "char": char, "is_leaf": True})
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            parent_freq = left.value + right.value
            parent_id = str(uuid.uuid4())
            parent = HuffmanNode(parent_freq, None, parent_id)
            self.nodes[parent_id] = parent
            parent.left = left
            parent.right = right
            steps.append({"type": "create_node", "node_id": parent_id, "value": parent_freq, "char": None, "is_leaf": False})
            steps.append({"type": "create_edge", "from_id": parent_id, "to_id": left.id, "direction": "left"})
            steps.append({"type": "create_edge", "from_id": parent_id, "to_id": right.id, "direction": "right"})
            heapq.heappush(heap, parent)
        self.root = heap[0] if heap else None
        return steps

    def export_to_file(self, filepath: str):
        if filepath == "./datas/default.json":
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filepath = f"./datas/huffman{timestamp}.json"

        export_data = self.char_list
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
            return self.build(import_data["chars"])
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            return [{"type": "warning", "value": ERR["INVALID_FILE"], "text": str(e)}]
        except Exception as e:
            return [{"type": "warning", "value": ERR["FILE_READ_FAILED"], "text": str(e)}]

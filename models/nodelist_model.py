# models/nodelist_model.py
import uuid
from config import ERR
import json
import datetime


class Node:
    def __init__(self, value, node_id=None):
        self.next = None
        self.id = node_id or str(uuid.uuid4())
        self.value = value


class NodeList:
    def __init__(self):
        self.head = None
        self.nodes = {}  # id -> Node

    def build_from_list(self, seq: list):
        if not seq:
            return []

        steps = []
        self.head = None
        self.nodes = {}
        pre_node = None
        pre_id = None
        for i, v in enumerate(seq, 0):
            node_id = str(uuid.uuid4())
            node = Node(v, node_id)
            self.nodes[node_id] = node
            if i == 0:
                self.head = node
                steps.append({"type": "create_node", "node_id": node_id, "value": v})
            else:
                pre_node.next = node
                steps.append({"type": "create_node", "node_id": node_id, "value": v})
                steps.append({"type": "link", "from": pre_id, "to": node_id})
            pre_node = node
            pre_id = node_id
        return steps

    def head_insert(self, value):
        new_id = str(uuid.uuid4())
        if self.head is None:
            steps = [{"type": "create_node", "node_id": new_id, "value": value}]
            self.head = Node(value, new_id)
            self.nodes[new_id] = self.head
        else:
            origin_id = self.head.id
            steps = [
                {"type": "create_node", "node_id": new_id, "value": value},
                {"type": "link", "from": new_id, "to": origin_id}
            ]
            new_node = Node(value, new_id)
            new_node.next = self.head
            self.head = new_node
            self.nodes[new_id] = self.head
        return steps

    def tail_insert(self, cur_id, value):
        new_id = str(uuid.uuid4())
        cur = self.nodes[cur_id]
        new_node = Node(value, new_id)
        if cur.next is not None:
            next_id = cur.next.id
            steps = [
                {"type": "create_node", "node_id": new_id, "value": value},
                {"type": "unlink", "from": cur_id, "to": next_id},
                {"type": "link", "from": new_id, "to": next_id},
                {"type": "link", "from": cur_id, "to": new_id},
            ]
            new_node.next = cur.next
            cur.next = new_node
        else:
            steps = [
                {"type": "create_node", "node_id": new_id, "value": value},
                {"type": "link", "from": cur_id, "to": new_id}
            ]
            cur.next = new_node
        self.nodes[new_id] = new_node
        return steps

    def delete_node(self, node_id):
        if self.head.id == node_id:
            if self.head.next is not None:
                next_id = self.head.next.id
                steps = [
                    {"type": "unlink", "from": node_id, "to": next_id},
                    {"type": "delete_node", "node_id": node_id}
                ]
            else:
                steps = [{"type": "delete_node", "node_id": node_id}]
            self.head = self.head.next
            del self.nodes[node_id]
            return steps

        pre = None
        cur = self.head
        while cur is not None and cur.id != node_id:
            pre = cur
            cur = cur.next
        pre.next = cur.next
        if pre.next is not None:
            fol_id = pre.next.id
            steps = [
                {"type": "unlink", "from": pre.id, "to": node_id},
                {"type": "unlink", "from": node_id, "to": fol_id},
                {"type": "link", "from": pre.id, "to": fol_id},
                {"type": "delete_node", "node_id": node_id}
            ]
        else:
            steps = [
                {"type": "unlink", "from": pre.id, "to": node_id},
                {"type": "delete_node", "node_id": node_id}
            ]
        del self.nodes[node_id]
        return steps

    def export_to_file(self, filepath: str):
        if filepath == "./datas/default.json":
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filepath = f"./datas/nodelist{timestamp}.json"

        export_data = []
        head = self.head
        cur = head
        while cur is not None:
            export_data.append(cur.value)
            cur = cur.next
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
            return self.build_from_list(import_data)
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            return [{"type": "warning", "value": ERR["INVALID_FILE"], "text": str(e)}]
        except Exception as e:
            return [{"type": "warning", "value": ERR["FILE_READ_FAILED"], "text": str(e)}]

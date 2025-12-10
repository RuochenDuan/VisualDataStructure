# models/bst_model.py
import uuid
from config import ERR
import json
import datetime


class BSTNode:
    def __init__(self, value, node_id=None):
        self.value = value
        self.id = node_id or str(uuid.uuid4())
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.nodes = {}
        self.value_list = []

    def build(self, seq: list):
        """从输入序列构建"""
        steps = []
        for v in seq:
            insert_steps = self.insert(v)
            steps.extend(insert_steps)
        return steps

    def insert(self, value):
        steps = []
        if not self.root:
            new_node_id = str(uuid.uuid4())
            new_node = BSTNode(value, new_node_id)
            self.root = new_node
            self.nodes[new_node_id] = new_node
            steps.append({"type": "create_node", "node_id": new_node_id, "value": value, "is_root": True})
            steps.append({"type": "highlight_node", "node_id": new_node_id, "color": "new"})
            self.value_list.append(value)
            return steps

        steps.append({"type": "clear_highlight"})
        current = self.root
        parent = None
        direction = None
        while current is not None:
            steps.append({"type": "highlight_node", "node_id": current.id, "color": "path"})
            if value < current.value:
                parent = current
                direction = "left"
                current = current.left
            elif value > current.value:
                parent = current
                direction = "right"
                current = current.right
            else:
                steps.append({"type": "clear_highlight"})
                steps.append({"type": "warning", "value": ERR["CHILD_OVERFLOW"]})
                return steps
        new_node_id = str(uuid.uuid4())
        new_node = BSTNode(value, new_node_id)
        self.nodes[new_node_id] = new_node
        if direction == "left":
            parent.left = new_node
        else:
            parent.right = new_node
        steps.append({"type": "create_node", "node_id": new_node_id, "value": value})
        steps.append({"type": "create_edge", "from_id": parent.id, "to_id": new_node_id, "direction": direction})
        steps.append({"type": "highlight_node", "node_id": new_node_id, "color": "new"})
        self.value_list.append(value)
        return steps

    def search(self, value):
        steps = []
        if self.root is None:
            return []

        steps.append({"type": "clear_highlight"})
        current = self.root
        while current is not None:
            steps.append({"type": "highlight_node", "node_id": current.id, "color": "path"})
            if value == current.value:
                steps.append({"type": "highlight_node", "node_id": current.id, "color": "highlight"})
                return steps
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        steps.append({"type": "warning", "value": ERR["NULL_POINTER"]})
        steps.append({"type": "clear_highlight"})
        return steps

    def delete(self, value):
        steps = []
        if self.root is None:
            return []

        steps.append({"type": "clear_highlight"})
        current = self.root
        parent = None
        direction = None
        while current is not None:
            steps.append({"type": "highlight_node", "node_id": current.id, "color": "path"})
            if value == current.value:
                break
            elif value < current.value:
                parent = current
                direction = "left"
                current = current.left
            else:
                parent = current
                direction = "right"
                current = current.right
        else:
            steps.append({"type": "clear_highlight"})
            steps.append({"type": "warning", "value": ERR["NULL_POINTER"]})
            return steps
        steps.append({"type": "highlight_node", "node_id": current.id, "color": "delete"})
        if current.left is None and current.right is None:
            steps.extend(self._leaf_delete(current, parent, direction))
        elif current.left is not None and current.right is None:
            child = current.left
            steps.extend(self._single_delete(current, parent, direction, child))
        elif current.left is None and current.right is not None:
            child = current.right
            steps.extend(self._single_delete(current, parent, direction, child))
        else:
            steps.extend(self._double_delete(current))
        steps.append({"type": "clear_highlight"})
        return steps

    def _leaf_delete(self, node, parent, direction):
        """删除叶子节点"""
        steps = []
        if parent:
            if direction == "left":
                parent.left = None
            else:
                parent.right = None
        else:
            self.root = None
        steps.append({"type": "delete_edge", "from_id": parent.id, "to_id": node.id, "direction": direction})
        steps.append({"type": "delete_node", "node_id": node.id})
        self.value_list.remove(node.value)
        del self.nodes[node.id]
        return steps

    def _single_delete(self, node, parent, direction, child):
        """删除单子节点"""
        steps = []
        if parent:
            if direction == "left":
                parent.left = child
            else:
                parent.right = child
        else:
            self.root = child
        steps.append({"type": "create_edge", "from_id": parent.id, "to_id": child.id, "direction": direction})
        steps.append({"type": "delete_edge", "from_id": parent.id, "to_id": node.id, "direction": direction})
        steps.append({"type": "delete_node", "node_id": node.id})
        self.value_list.remove(node.value)
        del self.nodes[node.id]
        return steps

    def _double_delete(self, node):
        """删除双子节点"""
        steps = []
        successor_parent = node
        successor = node.right
        while successor.left:
            steps.append({"type": "highlight_node", "node_id": successor.id, "color": "path"})
            successor_parent = successor
            successor = successor.left
        steps.append({"type": "highlight_node", "node_id": successor.id, "color": "delete"})

        node.value = successor.value
        if successor_parent == node:
            direction = "right"
        else:
            direction = "left"
        if successor.right:
            steps.append({"type": "create_edge", "from_id": successor_parent.id, "to_id": successor.right.id, "direction": direction})
            if direction == "left":
                successor_parent.left = successor.right
            else:
                successor_parent.right = successor.right
        steps.append({"type": "delete_edge", "from_id": successor_parent.id, "to_id": successor.id})
        steps.append({"type": "delete_node", "node_id": successor.id})
        self.value_list.remove(node.value)
        del self.nodes[successor.id]
        return steps

    def export_to_file(self, filepath: str):
        if filepath == "./datas/default.json":
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filepath = f"./datas/bst{timestamp}.json"

        export_data = self.value_list
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
            return self.build(import_data)
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            return [{"type": "warning", "value": ERR["INVALID_FILE"], "text": str(e)}]
        except Exception as e:
            return [{"type": "warning", "value": ERR["FILE_READ_FAILED"], "text": str(e)}]

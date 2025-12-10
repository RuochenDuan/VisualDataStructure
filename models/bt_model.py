# models/bt_model.py
import uuid
from config import ERR
import json
import datetime


class TreeNode:
    def __init__(self, value, node_id=None):
        self.value = value
        self.id = node_id or str(uuid.uuid4())
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None
        self.nodes = {}

    def build(self, preorder: list = None, inorder=None, postorder=None):
        """从遍历序列 preorder+inorder 或 inorder+postorder 构建二叉树"""
        if preorder is not None and inorder is not None and postorder is None:
            self.root, steps = self._build_from_pre(preorder, inorder)
        elif inorder is not None and postorder is not None and preorder is None:
            self.root, steps = self._build_from_post(inorder, postorder)
        elif preorder is not None and inorder is not None and postorder is not None:
            self.root, steps = self._build_from_pre(preorder, inorder)
        else:
            steps = []
        return steps

    def _build_from_pre(self, preorder, inorder):
        if not preorder or not inorder:
            return None, []
        root_val = preorder[0]
        root_id = str(uuid.uuid4())
        root = TreeNode(root_val, root_id)
        self.nodes[root_id] = root
        steps = [{"type": "create_node", "node_id": root_id, "value": root_val}]

        try:
            root_idx = inorder.index(root_val)
        except ValueError:
            steps.append({"type": "warning", "value": ERR["INVALID_INPUT"]})
            return None, steps
        left_in = inorder[:root_idx]
        right_in = inorder[root_idx+1:]
        left_pre = preorder[1:1+len(left_in)]
        right_pre = preorder[1+len(left_in):]
        left_child, left_steps = self._build_from_pre(left_pre, left_in)
        right_child, right_steps = self._build_from_pre(right_pre, right_in)
        steps.extend(left_steps)
        steps.extend(right_steps)
        if left_child:
            root.left = left_child
            steps.append({"type": "create_edge", "from_id": root_id, "to_id": left_child.id, "direction": "left"})
        if right_child:
            root.right = right_child
            steps.append({"type": "create_edge", "from_id": root_id, "to_id": right_child.id, "direction": "right"})
        return root, steps

    def _build_from_post(self, inorder, postorder):
        if not postorder or not inorder:
            return None, []
        root_val = postorder[-1]
        root_id = str(uuid.uuid4())
        root = TreeNode(root_val, root_id)
        self.nodes[root_id] = root
        steps = [{"type": "create_node", "node_id": root_id, "value": root_val}]

        try:
            root_idx = inorder.index(root_val)
        except ValueError:
            steps.append({"type": "warning", "value": ERR["INVALID_INPUT"]})
            return None, steps
        left_in = inorder[:root_idx]
        right_in = inorder[root_idx+1:]
        left_post = postorder[:len(left_in)]
        right_post = postorder[len(left_in):-1]
        left_child, left_steps = self._build_from_post(left_in, left_post)
        right_child, right_steps = self._build_from_post(right_in, right_post)
        steps.extend(left_steps)
        steps.extend(right_steps)
        if left_child:
            root.left = left_child
            steps.append({"type": "create_edge", "from_id": root_id, "to_id": left_child.id, "direction": "left"})
        if right_child:
            root.right = right_child
            steps.append({"type": "create_edge", "from_id": root_id, "to_id": right_child.id, "direction": "right"})
        return root, steps

    def insert_child(self, parent_id, value, direction: str):
        if parent_id not in self.nodes:
            return []

        parent = self.nodes[parent_id]
        if direction == "left" and parent.left is not None:
            return [{"type": "warning", "value": ERR["CHILD_OVERFLOW"]}]
        if direction == "right" and parent.right is not None:
            return [{"type": "warning", "value": ERR["CHILD_OVERFLOW"]}]

        child_id = str(uuid.uuid4())
        child = TreeNode(value, child_id)
        self.nodes[child_id] = child
        if direction == "left":
            parent.left = child
        else:
            parent.right = child
        return [
            {"type": "create_node", "node_id": child_id, "value": value},
            {"type": "create_edge", "from_id": parent_id, "to_id": child_id, "direction": direction}
        ]

    def delete_node(self, node_id):
        if node_id not in self.nodes:
            return []

        steps = []
        node = self.nodes[node_id]
        if node_id != self.root.id:
            parent, direction = self._find_parent(node_id)
            steps.append({"type": "delete_edge", "from_id": parent.id, "to_id": node_id, "direction": direction})
            if direction == "left":
                parent.left = None
            else:
                parent.right = None

        steps.extend(self._delete_subtree(node))
        if node_id == self.root.id:
            self.root = None
        return steps

    def _delete_subtree(self, node):
        """递归删除当前节点与子节点的联系和自身"""
        steps = []
        if node.left:
            steps.append({"type": "delete_edge", "from_id": node.id, "to_id": node.left.id, "direction": "left"})
            steps.extend(self._delete_subtree(node.left))
            node.left = None
        if node.right:
            steps.append({"type": "delete_edge", "from_id": node.id, "to_id": node.right.id, "direction": "right"})
            steps.extend(self._delete_subtree(node.right))
            node.right = None
        steps.append({"type": "delete_node", "node_id": node.id})
        if node.id in self.nodes:
            del self.nodes[node.id]
        return steps

    def _find_parent(self, node_id):
        """返回 (parent_node, direction)；若为根，返回 (None, None)"""
        if not self.root or self.root.id == node_id:
            return None, None

        stack = [(self.root, None, None)]  # (node, parent, direction from parent)
        while stack:
            current, parent, direction = stack.pop()
            if current.id == node_id:
                return parent, direction
            if current.right:
                stack.append((current.right, current, "right"))
            if current.left:
                stack.append((current.left, current, "left"))
        return None, None

    def _preorder_traversal(self, node, preorder: list):
        if node:
            preorder.append(node.value)
            self._preorder_traversal(node.left, preorder)
            self._preorder_traversal(node.right, preorder)

    def _inorder_traversal(self, node, inorder: list):
        if node:
            self._inorder_traversal(node.left, inorder)
            inorder.append(node.value)
            self._inorder_traversal(node.right, inorder)

    def export_to_file(self, filepath: str):
        if filepath == "./datas/default.json":
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filepath = f"./datas/bt{timestamp}.json"

        try:
            preorder = []
            inorder = []
            if self.root:
                self._preorder_traversal(self.root, preorder)
                self._inorder_traversal(self.root, inorder)
            export_data = {
                "preorder": preorder,
                "inorder": inorder
            }
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
            preorder, inorder = import_data.values()
            self.root = None
            self.nodes = {}
            return self.build(preorder=preorder, inorder=inorder)
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            return [{"type": "warning", "value": ERR["INVALID_FILE"], "text": str(e)}]
        except Exception as e:
            return [{"type": "warning", "value": ERR["FILE_READ_FAILED"], "text": str(e)}]

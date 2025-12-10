# controllers/Main_controller.py
from PyQt6.QtWidgets import QInputDialog, QLineEdit, QMessageBox
from controllers import NodeListController
from controllers import ArrListController
from controllers import StackController
from controllers import BTController
from controllers import BSTController
from controllers import HuffmanController
import os
from openai import OpenAI
import httpx


class MainController:
    def __init__(self, window):
        self.window = window
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.url = "https://dashscope.aliyuncs.com/compatible-mode/v1/"
        self.chat_model = "qwen-turbo"
        self.http_client = None
        self.client = None
        self.client_init()
        self.window.home_view.req_get.connect(self.get_page)

        self.arrlist_ctrler = ArrListController(self.window.arrlist_view)
        self.window.arrlist_view.req_back.connect(self.back_to_home)
        self.window.arrlist_view.req_dscrb.connect(self.create_by_dscrb)

        self.nodelist_ctrler = NodeListController(self.window.nodelist_view)
        self.window.nodelist_view.req_back.connect(self.back_to_home)
        self.window.nodelist_view.req_dscrb.connect(self.create_by_dscrb)

        self.stack_ctrler = StackController(self.window.stack_view)
        self.window.stack_view.req_back.connect(self.back_to_home)
        self.window.stack_view.req_dscrb.connect(self.create_by_dscrb)

        self.bt_ctrler = BTController(self.window.bt_view)
        self.window.bt_view.req_back.connect(self.back_to_home)
        self.window.bt_view.req_dscrb.connect(self.create_by_dscrb)

        self.bst_ctrler = BSTController(self.window.bst_view)
        self.window.bst_view.req_back.connect(self.back_to_home)
        self.window.bst_view.req_dscrb.connect(self.create_by_dscrb)

        self.huffman_ctrler = HuffmanController(self.window.huffman_view)
        self.window.huffman_view.req_back.connect(self.back_to_home)
        self.window.huffman_view.req_dscrb.connect(self.create_by_dscrb)

    def __del__(self):
        if self.http_client is not None:
            self.http_client.close()

    def client_init(self):
        self.http_client = httpx.Client(
            limits=httpx.Limits(
                max_keepalive_connections=1,
                max_connections=5,
                keepalive_expiry=360.0
            ),
            timeout=15.0
        )
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.url,
            http_client=self.http_client
        )

    def create_by_dscrb(self):
        index = str(self.window.page.currentIndex())
        prompt, ok = QInputDialog.getText(
            self.window.page.currentWidget(),
            "描述",
            "用自然语言描述数据结构",
            QLineEdit.EchoMode.Normal,
            ""
        )
        if not ok or not prompt:
            return
        mapping = {
            "1": """
                你要模拟一个顺序表可视系统的后端，严格遵守以下要求。
                接收：用户用自然语言描述的顺序表。
                返回：单行，只有一个python列表格式表示的表结构，不要有多余内容。
                返回示例：[1, 2, 3, 4]
                """,
            "2": """
                你要模拟一个链表可视系统的后端，严格遵守以下要求。
                接收：用户用自然语言描述的链表。
                返回：单行，只有一个python列表格式表示的表结构，不要有多余内容。
                返回示例：[1, 2, 3, 4]
                """,
            "3": """
                你要模拟一个栈可视系统的后端，严格遵守以下要求。
                接收：用户用自然语言描述的栈。
                返回：单行，只有一个python字典格式表示的栈结构，不要有多余内容。
                    第一个值描述总容量，第二个值描述压入的元素（栈底在左侧）。
                返回示例：{"max_size": 5, "datas": [1, 2, 3, 4]}
                """,
            "4": """
                你要模拟一个二叉树可视系统的后端，严格遵守以下要求。
                接收：用户用自然语言描述的二叉树。
                返回：单行，只有一个python字典格式表示的构建序列，不要有多余内容。
                    第一个值是前序序列，第二个值是中序序列。
                返回示例：{"preorder": [1, 2, 4, 5, 3, 6], "inorder": [4, 2, 5, 1, 6, 3]}
                """,
            "5": """
                你要模拟一个二叉搜索树可视系统的后端，严格遵守以下要求。
                接收：用户用自然语言描述的二叉搜索树。
                返回：单行，只有一个python列表格式表示的构建序列，不要有多余内容。
                返回示例：[1, 2, 3, 4, 5]
                """,
            "6": """
                你要模拟一个哈夫曼树可视系统的后端，严格遵守以下要求。
                接收：用户用自然语言描述的哈夫曼树。
                返回：单行，只有一个python字典格式表示的构建序列，包含构建这个树的原始字符串，不要有多余内容。
                返回示例：{"chars": "aaaabbbccd"}
                """
        }
        system_prompt = mapping.get(index, "")
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages
            )
            res = response.choices[0].message.content
        except Exception as e:
            res = ""
            QMessageBox.warning(
                self.window.page.currentWidget(),
                "请求失败",
                f"连接到{self.chat_model}时发生{str(e)}"
            )
        if index == '1':
            self.arrlist_ctrler.dscrb(res)
        elif index == '2':
            self.nodelist_ctrler.dscrb(res)
        elif index == '3':
            self.stack_ctrler.dscrb(res)
        elif index == '4':
            self.bt_ctrler.dscrb(res)
        elif index == '5':
            self.bst_ctrler.dscrb(res)
        elif index == '6':
            self.huffman_ctrler.dscrb(res)

    def get_page(self, page_name):
        mapping = {"顺序表": 1, "链表": 2, "栈": 3, "二叉树": 4, "二叉搜索树": 5, "哈夫曼树": 6}
        self.window.pages_switch(mapping.get(page_name, 0))

    def back_to_home(self):
        self.window.pages_switch(0)

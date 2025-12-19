# controllers/Main_controller.py
from PyQt6.QtWidgets import QInputDialog, QLineEdit, QMessageBox
from controllers import NodeListController
from controllers import ArrListController
from controllers import StackController
from controllers import BTController
from controllers import BSTController
from controllers import HuffmanController
import os
from config import URL, MODEL, S_PROMPT, MAPPING
from openai import OpenAI
import httpx


class MainController:
    def __init__(self, window):
        self.window = window
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.url = URL
        self.chat_model = MODEL
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

        system_prompt = S_PROMPT[int(index)]
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
        self.window.pages_switch(MAPPING.get(page_name, 0))

    def back_to_home(self):
        self.window.pages_switch(0)

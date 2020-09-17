# -*- coding:utf-8 -*-
import logging
from page.base_page import BasePage


class CommonPage(BasePage):
    def __getattr__(self, item):
        logging.warning(f"当前方法名为：{item}")
        self._method_name = item
        return self._po_method  # 这里返回了测试用例里面调用的方法名

    def _po_method(self, **kwargs):
        logging.warning(f"方法的传参为:{kwargs}")
        self.po_run(self._method_name, **kwargs)

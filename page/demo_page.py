# -*- coding:utf-8 -*-
from page.base_page import BasePage


class DemoPage(BasePage):
    """
    页面PO中的活动和活动中的步骤均可以存放在yaml中来获取
    """

    def search(self, keyword):
        self.po_run("search", keyword=keyword)
        return self

    def back(self):
        self.po_run("back")
        return self

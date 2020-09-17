# -*- coding:utf-8 -*-
import os
import pytest
from page.base_page import BasePage
from page.common_page import CommonPage
from page.demo_page import DemoPage
from page.utils import Utils

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class TestDemo:
    po_file = rootPath + '\\data\\page_demo.yaml'
    test_file = rootPath + '\\data\\test_search.yaml'
    data = Utils.from_file(test_file)

    def setup_class(self):
        self.app = BasePage()
        self.app.start()  # 调用start方法的时候就会赋值一个类属性_driver，后面就可以一直调用_driver了

    def teardown_class(self):
        self.app.stop()

    @pytest.mark.parametrize(data['key'], data['value'])
    def test_search(self, keyword):
        demo = DemoPage(self.po_file)
        demo.search(keyword=keyword)
        demo.back()

    def test_login(self):
        po_file1 = rootPath + '\\data\\page_login.yaml'
        login = CommonPage(po_file1)
        # 借助于__getattr__方法实现任意方法代理
        # login.xxxxx => login.__getattr__
        # 其实xxxxx用的就是CommonPage类的__getattr__方法中return的方法
        login.login_by_password(username="18900000000", password="888888")

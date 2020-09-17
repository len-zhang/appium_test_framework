# -*- coding:utf-8 -*-
import logging
import os
import yaml
from appium import webdriver
from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

"""
def exception_handle(fun):
    def magic(*args, **kwargs):
        _self: BasePage = args[0]
        try:
            result = fun(*args, **kwargs)
            # 清空错误次数
            _self._error_count = 0
            return result
        except Exception as e:
            # 如果次数太多，就退出异常逻辑，直接报错
            if _self._error_count > _self._error_max:
                raise e
            # 记录一直异常的次数
            _self._error_count += 1
            # 对黑名单里的弹框进行处理
            for element in _self._black_list:
                logging.info(element)
                elements = _self._driver.find_elements(*element)
                if len(elements) > 0:
                    elements[0].click()
                    # 继续寻找原来的正常控件
                    return magic(*args, **kwargs)
            # 如果黑名单也没有，就报错
            logging.warning("black list no one found")
            raise e
    return magic
"""


class BasePage:
    _driver: WebDriver = None
    _current_element: WebElement = None  # 初始一个当前元素的变量，用于后面find方法获取元素后赋值，然后可以再给click方法中使用
    _black_list = [
        (By.ID, 'tv_agree'),
        (By.XPATH, '//*[@text="确定"]'),
        (By.ID, 'image_cancel'),
        (By.XPATH, '//*[@text="下次再说"]')
    ]
    _error_max = 10
    _error_count = 0

    def __init__(self, po_file=None):
        if po_file is not None:
            self._po_file = po_file

    @classmethod
    def start(cls):
        caps = {
            'platformName': 'android',
            'deviceName': 'hogwarts',
            'appPackage': 'com.xueqiu.android',
            'appActivity': '.view.WelcomeActivityAlias',
            'noReset': True
        }
        cls._driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)
        cls._driver.implicitly_wait(10)
        return cls

    def stop(self):
        BasePage._driver.quit()

    # done: 当有广告、评价等各种弹框出现的时候，要进行异常流程处理
    # @exception_handle
    def find(self, locator, value=None):
        # 寻找控件
        if isinstance(locator, tuple):
            if locator[0] == 'text':
                locator_new = (By.XPATH, f'//*[contains(@text, "{locator[1]}")]')
            else:
                locator_new = locator
            self._current_element = BasePage._driver.find_element(*locator_new)
            return self
        else:
            self._current_element = BasePage._driver.find_element(locator, value)
            return self

    # done: 通用异常 通过装饰器让函数自动处理异常
    # @exception_handle
    # def get_text(self, locator, value=None):
    #     self.find(locator, value)
    #     return self._current_element.text

    def get_toast(self):
        toast_element = (By.XPATH, "//*[@class='android.widget.Toast']")
        self.find(toast_element)
        return self._current_element.text

    # def text(self, key):
    #     return (By.XPATH, "//*[@text='%s']" % key)

    # def find_by_text(self, key):
    #     return self.find(self.text(key))

    def click(self):
        self._current_element.click()
        return self

    def send_keys(self, text):
        self._current_element.send_keys(text)
        return self

    def po_run(self, po_method, **kwargs):
        with open(self._po_file, encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)
            for step in yaml_data[po_method]:  # 这一步中取出来的step是个字典，是PO动作里的每个步骤
                if isinstance(step, dict):  # 判断step是否为字典类型
                    for key in step.keys():  # dict.keys()字典的内置方法，以列表返回一个字典所有的键
                        if key in ["id", "aid", "text"]:
                            self.find((key, step[key]))  # step[key]为步骤中的value值
                        elif key == "click":
                            self.click()
                        elif key == "send_keys":
                            text = str(step[key])  # 这里text被赋值为${keyword}(即从page_demo.yaml中读出来的值)
                            for k, v in kwargs.items():
                                # 将text的值进行替换，旧值是${k}，新值是v，这里的k,v是通过**kwargs传进来的，必须要写成k=v的形式
                                text = text.replace('${' + k + '}', v)
                            self.send_keys(text)
                        else:
                            logging.error(f"unknown step{step}")

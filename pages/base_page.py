"""页面基类：统一封装显式等待与常用操作。"""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 8


class BasePage:
    """所有页面对象的父类：driver + 显式等待。"""

    def __init__(self, driver, base_url: str = "https://www.saucedemo.com"):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def open(self, path: str = "/"):
        self.driver.get(self.base_url + path)
        return self

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def type_into(self, locator, text: str):
        el = self.wait_visible(locator)
        el.clear()
        el.send_keys(text)
        return el

    def try_text(self, locator) -> str:
        """取元素文本；元素不出现则返回空串（用于错误提示是否弹出）。"""
        try:
            return self.wait_visible(locator).text
        except TimeoutException:
            return ""
